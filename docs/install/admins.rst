.. _install/admins:

Adding Admin Users to JupyterHub
================================

By default the ``site.yml`` playbook does not add admin users to JupyterHub.

New admin users can be added by adding ``admin: true`` to the ``users-config.yml`` file
from the previous section:

.. code-block:: yaml

    users:
      - name: foo
        password: PLAIN_TEXT_PASSWORD
        groups:
          - group_1
          - group_2
        admin: true

And re-running the ``users.yml`` playbook:

.. code-block:: bash

    ansible-playbook users.yml -i hosts -u ubuntu -e @users-config.yml

.. warning::

    The list of existing admin users is first reset before adding the new admin users.

Alternatively it is also possible to use the ``tljh-config`` command on the server directly.
Please refer to `the Littlest JupyterHub documentation <http://tljh.jupyter.org/en/latest/howto/admin/admin-users.html#adding-admin-users-from-the-command-line>`_
for more info.
