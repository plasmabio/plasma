"""
This file is only used for local development
and overrides some of the default values from the plugin.
"""

import getpass
import os

from tljh_plasma import tljh_custom_jupyterhub_config
from tljh_repo2docker import (
    tljh_custom_jupyterhub_config as tljh_repo2docker_config_hook,
)

c.JupyterHub.log_level = "DEBUG"

# tljh-plasma depends on tljh-repo2docker
tljh_repo2docker_config_hook(c)
tljh_custom_jupyterhub_config(c)

c.JupyterHub.ip = "127.0.0.1"
c.JupyterHub.port = 8000

user = getpass.getuser()
c.Authenticator.admin_users = {user}

# configure the volumes paths for local setup
c.PlasmaSpawner.base_volume_path = os.path.join(os.getcwd(), "volumes/user")
c.PlasmaSpawner.shared_data_path = os.path.join(os.getcwd(), "volumes/data")
