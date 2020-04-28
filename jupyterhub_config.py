"""
This file is only used for local development
and overrides some of the default values from the plugin.
"""

import getpass
import os

from tljh_plasmabio import tljh_custom_jupyterhub_config

c.JupyterHub.services = []

tljh_custom_jupyterhub_config(c)

user = getpass.getuser()

c.Authenticator.admin_users = {user}

# configure the volumes paths for local setup
c.PlasmaBioSpawner.base_path = os.path.join(os.getcwd(), "volumes/user")
c.PlasmaBioSpawner.shared_data_path = os.path.join(os.getcwd(), "volumes/data")
