Upgrading
=========

Backup
------

Before performing an upgrade, you might want to back up some components of the stack.

Database
........

JupyterHub keeps the state in a sqlite database, with information such as the last login and whether a user is an admin or not.

TLJH keeps the database in the ``/opt/tljh/state`` directory on the server. The full path to the database is ``/opt/tljh/state/jupyterhub.sqlite``.

To know more about backing up the database please refer to:

- `The JupyterHub documentation <https://jupyterhub.readthedocs.io/en/stable/admin/upgrading.html#backup-database-config>`_
- `The TLJH documentation on the state files <http://tljh.jupyter.org/en/latest/topic/installer-actions.html#state-files>`_

For more info on where TLJH is installed: `What does the installer do? <http://tljh.jupyter.org/en/latest/topic/installer-actions.html>`_

Plasma TLJH Plugin
..................

This TLJH plugin is a regular Python package.

It is installed in ``/opt/tljh/hub/lib/python3.6/site-packages/tljh_plasma``, and doesn't need to be backed up
as it doesn't hold any state.

User Environments
.................

The user environments correspond to Docker images on the host. There is no need to back them up as they
will stay untouched if not removed manually.

User Data
.........

It is generally recommended to have a backup strategy for important data such as user data.

This can be achieved by setting up tools that for example sync the user home directories to another machine on a regular basis.

Check out the :ref:`persistence/user-data` section to know more about user data.


Running the playbook
--------------------

To perform an upgrade of the setup, you can re-run the playbooks as explained in :ref:`install/ansible`.

Re-running the playbooks will:

- Update the TLJH Plasma plugin
- Update TLJH
- Restart JupyterHub and the Proxy to take new changes into account

However, performing an upgrade does not:

- Stop user servers
- Remove user environments (Docker images)
- Delete user data

In most cases, it is enough to only run the ``tljh.yml`` playbook to perform the upgrade.

Refer to :ref:`install/individual-playbook` for more info.
