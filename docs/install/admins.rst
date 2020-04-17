.. _install/admins:

Admin Users
===========

By default the ``site.yml`` playbook does not add admin users to JupyterHub.

New admin users can be added by running the ``admins.yml`` playbook:

.. code-block:: bash

    ansible-playbook admins.yml -i hosts -u ubuntu --extra-vars '{"admins": ["foo", "bar"]}'

This playbook processes the list of users specified via the ``--extra-vars`` command and add them as admin one at a time.

Alternatively it is also possible to use the ``tljh-config`` command on the server directly.
Please refer to `the Littlest JupyterHub documentation <http://tljh.jupyter.org/en/latest/howto/admin/admin-users.html#adding-admin-users-from-the-command-line>`_
for more info.