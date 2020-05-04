import os
import pwd
import sys

from dockerspawner import SystemUserSpawner
from jupyterhub.auth import PAMAuthenticator
from tljh.hooks import hookimpl
from tljh.systemd import check_service_active
from tljh_repo2docker import SpawnerMixin
from traitlets import default, Unicode


class PlasmaBioSpawner(SpawnerMixin, SystemUserSpawner):

    base_volume_path = Unicode("/home", config=True, help="The base path for the user volumes")

    shared_data_path = Unicode(
        "/srv/data", config=True, help="The path to the shared data folder"
    )

    async def start(self, *args, **kwargs):
        # set the image limits
        await super().set_limits()

        # escape the display name of the environment
        username = self.user.name
        display_name = self.user_options.get("display_name")
        display_name_escaped = display_name.replace(":", "-").replace("/", "-")

        # create the user directory on the host if it does not exist
        volume_path = os.path.join(self.base_volume_path, username, display_name_escaped)
        os.makedirs(volume_path, exist_ok=True)

        # the escaped environment name is used to create a new folder in the user home directory
        self.host_homedir_format_string = f"{self.base_volume_path}/{username}"
        # pass the image name to the Docker container
        self.environment = {"USER_IMAGE": display_name_escaped}

        # mount volumes
        self.volumes = {
            os.path.join(
                os.path.dirname(__file__), "entrypoint", "entrypoint.sh"
            ): "/usr/local/bin/repo2docker-entrypoint",
            self.shared_data_path: {"bind": "/srv/data", "mode": "ro"},
        }

        return await super().start(*args, **kwargs)


@hookimpl(trylast=True)
def tljh_custom_jupyterhub_config(c):
    # hub
    c.JupyterHub.cleanup_servers = False
    c.JupyterHub.authenticator_class = PAMAuthenticator
    c.JupyterHub.spawner_class = PlasmaBioSpawner
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.named_server_limit_per_user = 2
    c.JupyterHub.template_paths.insert(
        0, os.path.join(os.path.dirname(__file__), "templates")
    )

    # spawner
    # update name template for named servers
    c.PlasmaBioSpawner.name_template = "{prefix}-{username}-{servername}"
    # increase the timeout to be able to pull larger Docker images
    c.PlasmaBioSpawner.start_timeout = 120
    c.PlasmaBioSpawner.pull_policy = "Never"
    c.PlasmaBioSpawner.remove = True
    c.PlasmaBioSpawner.default_url = "/lab"
    # TODO: change back to jupyterhub-singleuser
    c.PlasmaBioSpawner.cmd = ["/srv/conda/envs/notebook/bin/jupyterhub-singleuser"]
    # set the default cpu and memory limits
    c.PlasmaBioSpawner.args = ["--ResourceUseDisplay.track_cpu_percent=True"]

    # register Cockpit as a service if active
    if check_service_active("cockpit"):
        c.JupyterHub.services.append(
            {"name": "cockpit", "url": "http://0.0.0.0:9090",},
        )
