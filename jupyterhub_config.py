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

# configure volumes for local setup
volumes_path = os.path.join(os.getcwd(), "volumes/user")
shared_data_path = os.path.join(os.getcwd(), "volumes/data")

c.SystemUserSpawner.volumes = {
    os.path.join(
        os.path.dirname(__file__),
        "tljh-plasmabio",
        "tljh_plasmabio",
        "entrypoint",
        "entrypoint.sh",
    ): "/usr/local/bin/repo2docker-entrypoint",
    shared_data_path: {"bind": "/srv/data", "mode": "ro"},
}
c.SystemUserSpawner.host_homedir_format_string = os.path.join(
    volumes_path, "{username}", "{imagename}"
)
c.SystemUserSpawner.pre_spawn_hook = create_pre_spawn_hook(volumes_path)
