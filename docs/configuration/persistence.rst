Data Persistence
================

The user servers are started using JupyterHub's `SystemUserSpawner <https://github.com/jupyterhub/dockerspawner#systemuserspawner>`_.

This spawner is based on the `DockerSpawner <https://github.com/jupyterhub/dockerspawner#dockerspawner>`_, but makes it possible
to use the host users to start the notebook servers.

Concretely this means that the user inside the container will correspond to a real user that exists on the host.
Processes will be started by that user, instead of the default ``jovyan`` user that is usually found in the regular
Jupyter Docker images and on Binder.

For example when the user ``alice`` starts her server, the list of processes looks like the following:

.. code-block:: bash

  alice@e4286692bcf4:~$ ps aux
  USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  root         1  0.8  0.0   4524   864 ?        Ss   10:37   0:00 tini -g -- start-notebook.sh --ip=0.0.0.0 --port=8888 --NotebookApp.default_url=/lab
  root         6  0.0  0.0  51496  3788 ?        S    10:37   0:00 sudo -E -H -u alice PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin XDG_CACHE_HOME=/home/alice/.cache PYTHONPATH= jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --NotebookApp.default
  alice        31 4.6  1.8 465884 71480 ?        Sl   10:37   0:01 /opt/conda/bin/python /opt/conda/bin/jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --NotebookApp.default_url=/lab
  alice        66 1.7  0.0  20180  3804 pts/0    Ss   10:37   0:00 /bin/bash -l
  alice        76 1.7  1.2 534132 49296 ?        Ssl  10:37   0:00 /opt/conda/bin/python -m ipykernel_launcher -f /home/alice/.local/share/jupyter/runtime/kernel-d324b5e1-619c-4056-a1b0-dcebd92c3ba3.json
  alice        96 0.0  0.0  36076  3216 pts/0    R+   10:37   0:00 ps aux

By default ``SystemUserSpawner`` mounts the user's home directory into the user container. This means that each notebook or file
will persist in the home directory for that user on the host machine.

PlasmaBio uses the same default.