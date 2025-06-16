"""
This file is only used for local development
and overrides some of the default values from the plugin.
"""

import getpass
import os
import sys

from tljh_plasma import tljh_custom_jupyterhub_config
from tljh_repo2docker import (
    TLJH_R2D_ADMIN_SCOPE,
    tljh_custom_jupyterhub_config as tljh_repo2docker_config_hook,
)

# Configure JupyterHub to bind to localhost to avoid hostname resolution issues
c.JupyterHub.ip = '127.0.0.1'
c.JupyterHub.port = 8000

c.JupyterHub.services = []

# tljh-plasma depends on tljh-repo2docker
tljh_repo2docker_config_hook(c)
tljh_custom_jupyterhub_config(c, "config.yaml")

user = getpass.getuser()

c.Authenticator.admin_users = {user}

# configure the volumes paths for local setup
c.PlasmaSpawner.base_volume_path = os.path.join(os.getcwd(), "volumes/user")
c.PlasmaSpawner.shared_data_path = os.path.join(os.getcwd(), "volumes/data")

c.JupyterHub.services.extend(
    [
        {
            "name": "tljh_repo2docker",
            "url": "http://127.0.0.1:6789",
            "command": [
                sys.executable,
                "-m",
                "tljh_repo2docker",
                "--ip",
                "127.0.0.1",
                "--port",
                "6789",
            ],
            "oauth_no_confirm": True,
            "oauth_client_allowed_scopes": [
                TLJH_R2D_ADMIN_SCOPE,
            ],
        }
    ]
)

c.JupyterHub.custom_scopes = {
    TLJH_R2D_ADMIN_SCOPE: {
        "description": "Admin access to tljh_repo2docker",
    },
}

c.JupyterHub.load_roles = [
    {
        "name": "tljh-repo2docker-service-admin",
        "users": [user],
        "scopes": [TLJH_R2D_ADMIN_SCOPE],
    },
]

