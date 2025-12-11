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

c.JupyterHub.log_level = 'DEBUG'

# tljh-plasma depends on tljh-repo2docker
tljh_repo2docker_config_hook(c)
tljh_custom_jupyterhub_config(c, 'config.yaml')

c.JupyterHub.allow_named_servers = True
#c.JupyterHub.ip =  "0.0.0.0"
c.JupyterHub.ip = "127.0.0.1"
c.JupyterHub.port = 8000

user = getpass.getuser()

c.Authenticator.admin_users = {user}
c.Authenticator.allow_all = True

# configure the volumes paths for local setup
c.PlasmaSpawner.base_volume_path = os.path.join(os.getcwd(), "volumes/user")
c.PlasmaSpawner.shared_data_path = os.path.join(os.getcwd(), "volumes/data")
c.DockerSpawner.remove = False
c.PlasmaSpawner.remove = False
c.SystemUserSpawner.remove = False

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
                "--machine_profiles",
                '[{"label": "Small", "cpu": 2, "memory": 2},'
                ' {"label": "Medium", "cpu": 4, "memory": 4},'
                ' {"label": "Large", "cpu": 8, "memory": 8}]',
                "--node_selector",
                '{"gpu": {"description": "GPU description", "values": ["yes", "no"]},'
                ' "ssd": {"description": "SSD description", "values": ["yes", "no"]}}',
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
        "description": "Role for tljh_repo2docker service",
        "name": "tljh-repo2docker-service",
        "scopes": ["read:users", "read:roles:users", "admin:servers"],
        "services": ["tljh_repo2docker"],
    },
    {
        "name": "tljh-repo2docker-service-admin",
        "users": [user],
          "scopes": [
              TLJH_R2D_ADMIN_SCOPE,
          ],
    },
    {
        "name": "user",
        "scopes": [
            "self",
            # access to the env page
            "access:services!service=tljh_repo2docker",
        ],
    },
]
