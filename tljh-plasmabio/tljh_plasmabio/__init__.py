import os
import pwd
import shutil
import sys

from dockerspawner import DockerSpawner
from jupyterhub.auth import PAMAuthenticator
from jupyter_client.localinterfaces import public_ips
from tljh.hooks import hookimpl
from traitlets import default

from .builder import DEFAULT_CPU_LIMIT, DEFAULT_MEMORY_LIMIT
from .images import list_images, client

# TODO: make this configurable
VOLUMES_PATH = "/volumes/users"

# Default CPU period
# See: https://docs.docker.com/config/containers/resource_constraints/#limit-a-containers-access-to-memory#configure-the-default-cfs-scheduler
CPU_PERIOD = 100_000


# See: https://github.com/jupyterhub/jupyterhub/tree/master/examples/bootstrap-script#example-1---create-a-user-directory
def create_pre_spawn_hook(base_path, uid=1100):
    def pre_spawn_hook(spawner):

        # create user directory if it does not exist
        username = spawner.user.name
        volume_path = os.path.join(base_path, username)
        os.makedirs(volume_path, 0o755, exist_ok=True)
        # use jovyan id (used when building the image with repo2docker)
        shutil.chown(volume_path, user=uid)

        # set the image limits
        image = client.images.get(spawner.user_options.get("image"))
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
    c.JupyterHub.spawner_class = DockerSpawner
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.named_server_limit_per_user = 2

    # spawner
    # increase the timeout to be able to pull larger Docker images
    c.DockerSpawner.start_timeout = 120
    c.DockerSpawner.pull_policy = "Never"
    c.DockerSpawner.name_template = "{prefix}-{username}-{servername}"
    c.DockerSpawner.default_url = "/lab"
    c.DockerSpawner.cmd = ["jupyterhub-singleuser"]
    c.DockerSpawner.volumes = {
        os.path.join(VOLUMES_PATH, "{username}"): "/home/jovyan/work"
    }

    # set the default cpu and memory limits
    c.DockerSpawner.mem_limit = DEFAULT_MEMORY_LIMIT
    c.DockerSpawner.cpu_limit = float(DEFAULT_CPU_LIMIT)
    c.DockerSpawner.args = ["--ResourceUseDisplay.track_cpu_percent=True"]

    c.DockerSpawner.pre_spawn_hook = create_pre_spawn_hook(VOLUMES_PATH)
    c.DockerSpawner.remove = True
    c.DockerSpawner.image_whitelist = image_whitelist
    c.DockerSpawner.options_form = options_form

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
