import os
import pwd
import sys

from dockerspawner import SystemUserSpawner
from jupyterhub.auth import PAMAuthenticator
from jupyter_client.localinterfaces import public_ips
from tljh.hooks import hookimpl
from traitlets import default

from .builder import DEFAULT_CPU_LIMIT, DEFAULT_MEMORY_LIMIT
from .images import list_images, client

VOLUMES_PATH = "/home"
SHARED_DATA_PATH = "/srv/data"

# Default CPU period
# See: https://docs.docker.com/config/containers/resource_constraints/#limit-a-containers-access-to-memory#configure-the-default-cfs-scheduler
CPU_PERIOD = 100_000


# See: https://github.com/jupyterhub/jupyterhub/tree/master/examples/bootstrap-script#example-1---create-a-user-directory
def create_pre_spawn_hook(base_path):
    def pre_spawn_hook(spawner):

        # create user directory on the host if it does not exist
        username = spawner.user.name
        imagename = spawner.user_options.get("image")
        imagename_escaped = imagename.replace(":", "-").replace('/', "-")

        volume_path = os.path.join(base_path, username, imagename_escaped)
        os.makedirs(volume_path, exist_ok=True)

        # the escaped image name is used to create a new folder in the user home directory
        homedir = f"/home/{username}/{imagename_escaped}"
        spawner.host_homedir_format_string = homedir
        # keep the same home dir name in the container to reflect the host file structure
        spawner.image_homedir_format_string = homedir

        # set the image limits
        image = client.images.get(imagename)
        mem_limit = image.labels.get("plasmabio.mem_limit", None)
        cpu_limit = image.labels.get("plasmabio.cpu_limit", None)
        spawner.mem_limit = mem_limit or spawner.mem_limit
        spawner.cpu_limit = float(cpu_limit) if cpu_limit else spawner.cpu_limit
        spawner.extra_host_config = {
            "cpu_period": CPU_PERIOD,
            "cpu_quota": int(float(CPU_PERIOD) * spawner.cpu_limit),
        }

    return pre_spawn_hook


def options_form(spawner):
    """
    Override the default form to handle the case when there is only
    one image.
    """
    images = spawner.image_whitelist(spawner)
    option_t = '<option value="{image}" {selected}>{image}</option>'
    options = [
        option_t.format(
            image=image, selected="selected" if image == spawner.image else ""
        )
        for image in images
    ]
    return """
    <label for="image">Select an image:</label>
    <select class="form-control" name="image" required autofocus>
    {options}
    </select>
    """.format(
        options=options
    )


def image_whitelist(spawner):
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
    c.JupyterHub.spawner_class = SystemUserSpawner
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.named_server_limit_per_user = 2

    # spawner
    # increase the timeout to be able to pull larger Docker images
    c.SystemUserSpawner.start_timeout = 120
    c.SystemUserSpawner.pull_policy = "Never"
    c.SystemUserSpawner.name_template = "{prefix}-{username}-{servername}"
    c.SystemUserSpawner.default_url = "/lab"
    # TODO: change back to jupyterhub-singleuser
    c.SystemUserSpawner.cmd = ["/srv/conda/envs/notebook/bin/jupyterhub-singleuser"]
    c.SystemUserSpawner.volumes = {
        os.path.join(os.path.dirname(__file__), "entrypoint", "entrypoint.sh"): "/usr/local/bin/repo2docker-entrypoint",
        SHARED_DATA_PATH: {"bind": "/srv/data", "mode": "ro"},
    }
    c.SystemUserSpawner.host_homedir_format_string = os.path.join(
        VOLUMES_PATH, "{username}", "{imagename}"
    )

    # set the default cpu and memory limits
    c.SystemUserSpawner.mem_limit = DEFAULT_MEMORY_LIMIT
    c.SystemUserSpawner.cpu_limit = float(DEFAULT_CPU_LIMIT)
    c.SystemUserSpawner.args = ["--ResourceUseDisplay.track_cpu_percent=True"]

    c.SystemUserSpawner.pre_spawn_hook = create_pre_spawn_hook(VOLUMES_PATH)
    c.SystemUserSpawner.remove = True
    c.SystemUserSpawner.image_whitelist = image_whitelist
    c.SystemUserSpawner.options_form = options_form

    c.JupyterHub.template_paths = os.path.join(os.path.dirname(__file__), "templates"),

    # register the service to manage the user images
    c.JupyterHub.services += [
        {
            "name": "environments",
            "admin": True,
            "url": "http://127.0.0.1:9988",
            "command": [sys.executable, "-m", "tljh_plasmabio.images"],
        }
    ]


@hookimpl
def tljh_extra_hub_pip_packages():
    return ["dockerspawner", "jupyter_client"]
