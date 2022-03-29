import grp
import os
import pwd
import shutil

from dockerspawner import SystemUserSpawner
from jupyterhub.auth import PAMAuthenticator
from jupyterhub.handlers.static import CacheControlStaticFilesHandler
from tljh.configurer import load_config, CONFIG_FILE
from tljh.hooks import hookimpl
from tljh.systemd import check_service_active
from tljh_repo2docker import SpawnerMixin
from traitlets import Unicode

from .permissions import Permissions, PermissionsHandler, PermissionsAPIHandler


class PlasmaSpawner(SpawnerMixin, SystemUserSpawner):
    """
    A custom Spawner to start user servers using Docker images
    built locally with repo2docker.
    """

    base_volume_path = Unicode(
        "/home", config=True, help="The base path for the user volumes"
    )

    shared_data_path = Unicode(
        "/srv/data", config=True, help="The path to the shared data folder"
    )

    async def list_images(self):
        all_images = await super().list_images()
        groups = [
            group.gr_name for group in grp.getgrall() if self.user.name in group.gr_mem
        ]
        permissions = self.db.query(Permissions).filter(Permissions.group.in_(groups))
        whitelist = set(p.image for p in permissions)
        images = [image for image in all_images if image["image_name"] in whitelist]
        return images

    async def start(self, *args, **kwargs):
        # set the image limits
        await super().set_limits()

        # escape the display name of the environment
        username = self.user.name
        image_name = self.user_options.get("image")

        images = await super().list_images()
        image = next(img for img in images if img["image_name"] == image_name)
        display_name = image["display_name"].replace(":", "-").replace("/", "-")

        # get the user home directory
        if self.base_volume_path is not None and self.base_volume_path != "":
            user_home = os.path.join(self.base_volume_path, username)
        else:
            user_home = pwd.getpwnam(username).pw_dir

        # create the user directory on the host if it does not exist
        volume_path = os.path.join(user_home, display_name)
        os.makedirs(volume_path, exist_ok=True)
        shutil.chown(volume_path, username, username)

        # the escaped environment name is used to create a new folder in the user home directory
        home = os.path.abspath(os.path.join(user_home, os.path.pardir))
        self.host_homedir_format_string = f"{home}/{username}"
        self.image_homedir_format_string = f"{home}/{username}"
        # pass the image name to the Docker container
        self.environment = {"USER_IMAGE": display_name}

        # mount volumes
        self.volumes = {
            os.path.join(
                os.path.dirname(__file__), "entrypoint", "entrypoint.sh"
            ): "/usr/local/bin/repo2docker-entrypoint",
            self.shared_data_path: {"bind": "/srv/data", "mode": "ro"},
        }

        return await super().start(*args, **kwargs)


@hookimpl(trylast=True)
def tljh_custom_jupyterhub_config(c, tljh_config_file=CONFIG_FILE):
    # hub
    c.JupyterHub.cleanup_servers = False
    c.JupyterHub.authenticator_class = PAMAuthenticator
    c.JupyterHub.spawner_class = PlasmaSpawner
    c.JupyterHub.template_paths.insert(
        0, os.path.join(os.path.dirname(__file__), "templates")
    )

    # let the spawner infer the user home directory
    c.PlasmaSpawner.base_volume_path = ""

    # fetch the list of allowed UNIX groups from the TLJH config
    tljh_config = load_config(tljh_config_file)
    include_list = tljh_config.get("plasma", {}).get("groups", [])
    include_groups = set(include_list)

    c.JupyterHub.tornado_settings.update({"include_groups": include_groups})

    # add an extra handler to handle user group permissions
    c.JupyterHub.extra_handlers.extend(
        [
            (r"permissions", PermissionsHandler),
            (r"api/permissions", PermissionsAPIHandler),
            (
                r"permissions-static/(.*)",
                CacheControlStaticFilesHandler,
                {"path": os.path.join(os.path.dirname(__file__), "static")},
            ),
        ]
    )

    # spawner
    # update name template for named servers
    c.PlasmaSpawner.name_template = "{prefix}-{username}-{servername}"
    # increase the timeout to be able to pull larger Docker images
    c.PlasmaSpawner.start_timeout = 120
    c.PlasmaSpawner.pull_policy = "Never"
    c.PlasmaSpawner.remove = True
    c.PlasmaSpawner.default_url = "/lab"
    # TODO: change back to jupyterhub-singleuser
    c.PlasmaSpawner.cmd = ["/srv/conda/envs/notebook/bin/jupyterhub-singleuser"]
    # set the default cpu and memory limits
    c.PlasmaSpawner.args = ["--ResourceUseDisplay.track_cpu_percent=True"]

    # prevent PID 1 running in the Docker container to stop when child processes are killed
    # see https://github.com/plasmabio/plasma/issues/191 for more info
    c.PlasmaSpawner.extra_host_config = {'init': True}

    # register Cockpit as a service if active
    if check_service_active("cockpit"):
        c.JupyterHub.services.append(
            {"name": "cockpit", "url": "http://0.0.0.0:9090",},
        )
