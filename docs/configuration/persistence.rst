Data Persistence
================

.. _persistence/user-data:

User Data
---------

The user servers are started using JupyterHub's `DockerSpawner <https://github.com/jupyterhub/dockerspawner>`_.

Inside the container, the processes are started using the default ``jovyan`` user that is usually found in the regular
Jupyter Docker images, on Binder and in the images built with ``repo2docker``.

By default PlasmaBio mounts the ``/home/{username}/work`` directory on the host into the user container under ``/home/jovyan/work``. This means that each notebook or file
will persist in the home directory for that user on the host machine.

The ``/home/jovyan/work`` will be located next to the other folders already in the user environment and packaged with ``repo2docker``.

.. image:: ../images/configuration/persistence.png
   :alt: Mounting user's home directories
   :width: 100%
   :align: center

Shared Data
-----------

In addition to the user data, the plugin also mounts a shared data volume for all users.

The shared data is available under ``/home/jovyan/data`` inside the user server.

On the host machine, the shared data should be placed under ``/srv/data`` as recommended in the
`TLJH documentation <https://github.com/plasmabio/plasmabio/blob/684515bfc5837705d89fc6a7863a69a561e8d15d/ansible/vars/default.yml#L4>`_.

The shared data is **read-only**.
