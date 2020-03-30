import os
import pwd
import shutil
import sys

from dockerspawner import DockerSpawner
from jupyterhub.auth import PAMAuthenticator
from jupyter_client.localinterfaces import public_ips
from tljh.hooks import hookimpl
from traitlets import default

from .images import list_images

# TODO: make this configurable
VOLUMES_PATH = "/volumes/users"


# See: https://github.com/jupyterhub/jupyterhub/tree/master/examples/bootstrap-script#example-1---create-a-user-directory
def create_pre_spawn_hook(base_path, uid=1100):
    def create_dir_hook(spawner):
        username = spawner.user.name
        volume_path = os.path.join(base_path, username)
        os.makedirs(volume_path, 0o755, exist_ok=True)
        # use jovyan id (used when building the image with repo2docker)
        shutil.chown(volume_path, user=uid)

    return create_dir_hook


class PlasmaSpawner(DockerSpawner):
    @default("options_form")
    def _default_options_form(self):
        """
        Override the default form to handle the case when there is only
        one image.
        """
        image_whitelist = self._get_image_whitelist()
        option_t = '<option value="{image}" {selected}>{image}</option>'
        options = [
            option_t.format(
                image=image, selected="selected" if image == self.image else ""
            )
            for image in image_whitelist
        ]
        return """
        <label for="image">Select an image:</label>
        <select class="form-control" name="image" required autofocus>
        {options}
        </select>
        """.format(
            options=options
        )

    def image_whitelist(self, spawner):
        """
        Retrieve the list of available images
        """
        images = list_images()
        return {image["image_name"]: image["image_name"] for image in images}


@hookimpl
def tljh_custom_jupyterhub_config(c):
    # hub
    c.JupyterHub.hub_ip = public_ips()[0]
    c.JupyterHub.cleanup_servers = False
    c.JupyterHub.authenticator_class = PAMAuthenticator
    c.JupyterHub.spawner_class = PlasmaSpawner
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.named_server_limit_per_user = 2

    # spawner
    # increase the timeout to be able to pull larger Docker images
    c.PlasmaSpawner.start_timeout = 120
    c.PlasmaSpawner.pull_policy = "Never"
    c.PlasmaSpawner.name_template = "{prefix}-{username}-{servername}"
    c.PlasmaSpawner.default_url = "/lab"
    c.PlasmaSpawner.cmd = ["jupyterhub-singleuser"]
    c.PlasmaSpawner.volumes = {
        os.path.join(VOLUMES_PATH, "{username}"): "/home/jovyan/work"
    }
    c.PlasmaSpawner.mem_limit = "2G"
    c.PlasmaSpawner.pre_spawn_hook = create_pre_spawn_hook(VOLUMES_PATH)
    c.PlasmaSpawner.remove = True

    # register the service to manage the user images
    c.JupyterHub.services = [
        {
            "name": "images",
            "admin": True,
            "url": "http://127.0.0.1:9988",
            "command": [sys.executable, "-m", "tljh_plasmabio.images"],
        }
    ]


@hookimpl
def tljh_extra_hub_pip_packages():
    return ["dockerspawner", "jupyter_client"]
