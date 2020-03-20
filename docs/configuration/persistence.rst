Data Persistence
================

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
