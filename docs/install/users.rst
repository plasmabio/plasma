.. _install/users:

Creating Users on the host
==========================

.. note::
  By default the ``site.yml`` playbook does not create any users on the host machine.

  This step is optional because in some scenarios users might already exist on the host machine
  and don't need to be created.

.. _install/users-playbook:

Using the users playbook
------------------------

The ``ansible/`` directory contains a ``users.yml`` playbook that makes it easier to create new users on the host in batches.

First you need to create a new ``users-config.yml`` with the following content:

.. code-block:: yaml

    users:
      - name: foo
        password: PLAIN_TEXT_PASSWORD

      - name: bar
        password: PLAIN_TEXT_PASSWORD

Replace the ``name`` and ``password`` entries by the real values.

``password`` should correspond to the plain text value of the user password.

For more info about password hashing, please refer to the
`Ansible Documentation <http://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module>`_
to learn how to generate the encrypted passwords.

When the user file is ready, execute the ``users.yml`` playbook with the following command:

.. code-block:: bash

    ansible-playbook users.yml -i host -u ubuntu -e @users-config.yml

Handling secrets
----------------

.. warning::

  Passwords are sensitive data. The ``users.yml`` playbook mentioned in the previous section
  automatically encrypts the password from a plain text file.

  For production use, you should consider protecting the passwords using the
  `Ansible Vault <https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#playbooks-vault>`_.

This ``users.yml`` playbook is mostly provided as a convenience script to quickly bootstrap the host machine with
a predefined set of users.

You are free to choose a different approach for managing users that suits your needs.

Set Disk Quotas
---------------

Users can save their files on the host machine in their home directrory. More details in :ref:`persistence/user-data`.

If you would like to enable quotas for users to limit how much disk space they can use, you can use the ``quotas.yml`` Ansible playbook.

The playbook is heavily inspired by the excellent `DigitalOcean tutorial on user quotas <https://www.digitalocean.com/community/tutorials/how-to-set-filesystem-quotas-on-ubuntu-18-04>`_.
Check it out for more info on user and group quotas.

.. warning::

  It is recommended to do the initial quota setup **before** letting users to connect to the hub.

Finding the source device
.........................

`As mentioned in the tutorial <https://www.digitalocean.com/community/tutorials/how-to-set-filesystem-quotas-on-ubuntu-18-04>`_, the first step is to find the device to apply quotas to.

To do so, SSH into the machine (:ref:`install/requirements`) and execute the following command:

.. code-block:: bash

  cat /etc/fstab

The output will be similar to:

.. code-block:: text

  LABEL=cloudimg-rootfs   /        ext4   defaults        0 0
  LABEL=UEFI      /boot/efi       vfat    defaults        0 0

The source device for ``/`` might be different than ``LABEL=cloudimg-rootfs``. If this is the case, copy the value somewhere so it can be used in the next step with the playbook.

Using the quotas playbook
.........................

To enable quotas on the machine, execute the ``quotas.yml`` playbook with the source device found in the previous section (if different):

.. code-block:: bash

  # if the device is also named LABEL=cloudimg-rootfs
  ansible-playbook quotas.yml -i hosts -u ubuntu

  # if the source device is different (replace with the real value)
  ansible-playbook quotas.yml -i hosts -u ubuntu -e "device=UUID=aaef63c7-8c31-4329-8b7f-b90085ecccd4"

Setting the user quotas
.......................

The ``users.yml`` playbook can also be used to set the user quotas. In ``users-config.yml`` you can defined quotas as follows:

.. code-block:: yaml

  # default quotas for all users
  quota:
    soft: 10G
    hard: 12G

  users:
    - name: foo
      password: foo
      # override quota for a specific user
      quota:
        soft: 20G
        hard: 25G

    - name: bar
      password: bar

Then re-run the ``users.yml`` playbook as mentioned in :ref:`install/users-playbook`.
