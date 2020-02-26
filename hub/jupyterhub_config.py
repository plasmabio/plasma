import os

from dockerspawner import DockerSpawner
from jupyterhub.auth import PAMAuthenticator

IMAGES = {
    'python': 'jupyter/scipy-notebook',
    'r': 'jupyter/r-notebook',
}

c.JupyterHub.hub_ip = 'hub'
c.JupyterHub.allow_named_servers = True
c.JupyterHub.authenticator_class = PAMAuthenticator
c.JupyterHub.spawner_class = DockerSpawner

# Increase the timeout to be able to pull larger Docker images
c.DockerSpawner.start_timeout=120
c.DockerSpawner.image_whitelist = IMAGES
c.DockerSpawner.network_name = os.getenv('DOCKER_NETWORK_NAME')
c.DockerSpawner.name_template = "{prefix}-{username}-{imagename}-{servername}"
c.DockerSpawner.default_url = '/lab'
c.DockerSpawner.remove = True
