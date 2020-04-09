"""
This file is only used for local development
and overrides some of the default values.
"""

import getpass
import os

from tljh_plasmabio import create_pre_spawn_hook, tljh_custom_jupyterhub_config

c.JupyterHub.services = []

tljh_custom_jupyterhub_config(c)

user = getpass.getuser()

c.Authenticator.admin_users = {user}

volumes_path = os.path.join(os.getcwd(), "volumes/user")
shared_data_path = os.path.join(os.getcwd(), "volumes/data")
c.DockerSpawner.volumes = {
    os.path.join(volumes_path, "{username}"): "/home/jovyan/work",
    shared_data_path: "/home/jovyan/data"
}
c.DockerSpawner.pre_spawn_hook = create_pre_spawn_hook(volumes_path, user)
