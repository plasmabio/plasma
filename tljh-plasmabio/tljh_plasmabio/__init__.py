from dockerspawner import SystemUserSpawner
from jupyterhub.auth import PAMAuthenticator
from jupyter_client.localinterfaces import public_ips
from tljh.hooks import hookimpl


from .build_images import IMAGES


@hookimpl
def tljh_custom_jupyterhub_config(c):
    # hub
    c.JupyterHub.hub_ip = public_ips()[0]
    c.JupyterHub.allow_named_servers = True
    c.JupyterHub.authenticator_class = PAMAuthenticator
    c.JupyterHub.spawner_class = SystemUserSpawner

    # spawner
    # increase the timeout to be able to pull larger Docker images
    c.SystemUserSpawner.start_timeout = 120
    # TODO: make the image_whitelist a callable so it can pick up new images dynamically
    c.SystemUserSpawner.image_whitelist = {k: k for k in IMAGES.keys()}
    c.SystemUserSpawner.pull_policy = "Never"
    c.SystemUserSpawner.name_template = "{prefix}-{username}-{imagename}-{servername}"
    c.SystemUserSpawner.default_url = "/lab"
    c.SystemUserSpawner.cmd = ["jupyterhub-singleuser"]
    c.SystemUserSpawner.remove = True


@hookimpl
def tljh_extra_hub_pip_packages():
    return ["dockerspawner", "jupyter_client", "jupyter-repo2doocker"]
