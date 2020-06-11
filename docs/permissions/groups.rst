Managing UNIX groups
====================

The group include list
----------------------

By default Plasma users don't have access to any environments.

Users must be assigned to UNIX groups, and included groups be defined in the Plasma configuration.

To define the list of groups, create a file called ``ansible/include-groups-config.yml`` with the following content:

.. code-block:: yaml

    plasma:
        groups:
            - python-course
            - bash-intro

And execute the ``ansible/include-groups.yml`` playbook:

.. code-block:: bash

    cd ansible/
    ansible-playbook -i hosts include-groups.yml -u ubuntu

The playbook creates the groups on the host machine if they don't already exist, and defines the list
of included groups in the TLJH config.

Adding a user to a group via the command line
---------------------------------------------

New groups can be created using the following command:

.. code-block:: bash

    groupadd -g 1234 test

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
        groups: python-course,bash-intro
        password: PLAIN_TEXT_PASSWORD

      - name: bar
        groups: test,bash-intro
        password: PLAIN_TEXT_PASSWORD

This can also be a convenient way to create a default group and give every user access to all user
environments.

Listing the groups
------------------

Groups can be listed using the following command:

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
