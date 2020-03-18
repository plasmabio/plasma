# This file is only used for local development

import os

from tljh_plasmabio import tljh_custom_jupyterhub_config

tljh_custom_jupyterhub_config(c)

# configure the volumes
user_dir = os.path.join(os.getcwd(), "volumes/user/{username}")


def create_user_volume(spawner):
    """
    A pre-spawn hook to create the user home directory with
    the correct permissions when testing locally
    """
    username = spawner.user.name  # get the username
    os.makedirs(user_dir.format(username=username), exist_ok=True)


c.SystemUserSpawner.pre_spawn_hook = create_user_volume
c.SystemUserSpawner.host_homedir_format_string = user_dir
