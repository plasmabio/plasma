"""
This file is only used for local development
and overrides some of the default values.
"""

import getpass
import os

from tljh_plasmabio import create_pre_spawn_hook, tljh_custom_jupyterhub_config

tljh_custom_jupyterhub_config(c)

user = getpass.getuser()

c.Authenticator.admin_users = { user }

volumes_path = os.path.join(os.getcwd(), "volumes/user")
c.DockerSpawner.volumes = {os.path.join(volumes_path, "{username}"): "/home/jovyan/work"}
c.DockerSpawner.pre_spawn_hook = create_pre_spawn_hook(volumes_path, user)
