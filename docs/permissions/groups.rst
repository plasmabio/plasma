Managing UNIX groups
====================

Most Ubuntu installations include a default list of groups. These groups can be listed with the
following command:

.. code-block:: bash

    $ cat /etc/group
    root:x:0:
    daemon:x:1:
    bin:x:2:
    sys:x:3:
    adm:x:4:syslog,ubuntu
    tty:x:5:
    disk:x:6:
    lp:x:7:
    mail:x:8:
    ...

By default this list can be relatively long:

.. code-block:: bash

    $ cat /etc/group | wc -l
    64

The group exclude list
----------------------

To prevent the default groups from being displayed in the JupyterHub interface, Plasma
defines a list of groups to ``exclude`` via an Ansible variable.

The list is defined in ``ansible/exclude-groups-config.yml``.

The ``ansible/exclude-groups.yml`` playbook automatically adds the list of excluded groups to
the TLJH config when it is executed.

If you would like to modify the list of groups to exclude, edit ``ansible/exclude-groups-config.yml``
and run the following command:

.. code-block:: bash

    cd ansible/
    ansible-playbook -i hosts exclude-groups.yml -u ubuntu


Adding a user to a group via the command line
---------------------------------------------

New groups can be created using the following command:

To add a user ``alice`` to the ``test`` group:

.. code-block:: bash

    usermod -G test alice

There are also plenty of good resources online to learn more about UNIX user and groups management.

Adding a user to groups with Ansible
------------------------------------

Alternatively, groups can be defined in the users playbook, as mentioned in :ref:`install/users-playbook`.

To add users to specific groups, edit ``users-config.yml`` to add the ``groups`` field:

.. code-block:: yaml

    users:
      - name: foo
        groups: python,bash
        password: PLAIN_TEXT_PASSWORD

      - name: bar
        groups: test,bash
        password: PLAIN_TEXT_PASSWORD

This can also be a convenient way to create a default group and give every user access to all user
environments.
