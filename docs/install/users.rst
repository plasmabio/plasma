.. _install/users:

Creating Users on the host
==========================

.. note::
  By default the ``site.yml`` playbook does not create any users on the host machine.

  This step is optional because in some scenarios users might already exist on the host machine
  and don't need to be created.

The ``ansible/`` directory contains a ``users.yml`` playbook that makes it easier to create new users on the host in batches.

First you need to create a new ``users-config.yml`` with the following content:

.. code-block:: yaml

    users:
      - name: foo
        password: HASHED_PASSWORD

      - name: bar
        password: HASHED_PASSWORD

Replace the ``name`` and ``password`` entries by the real values.

``password`` should correspond to the encrypted value of the user password. Please refer to the
`Ansible Documentation <http://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module>`_
to learn how to generate the encrypted passwords.

When the user file is ready, execute the ``users.yml`` playbook with the following command:

.. code-block:: bash

    ansible-playbook users.yml -i host -u ubuntu -e @users-config.yml
