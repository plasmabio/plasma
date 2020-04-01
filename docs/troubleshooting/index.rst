.. _troubleshooting/troubleshooting:

Troubleshooting
===============

.. contents:: Table of contents
    :local:
    :depth: 1

How to SSH to the machine
-------------------------

First make sure your SSH key has been deployed to the server. See :ref:`install/ssh-key` for more details.

Once the key is set up, connect to the machine over SSH using the following commands:

.. code-block:: bash

  ssh ubuntu@51.178.95.143

Looking at logs
---------------

See: `The Littlest JupyterHub documentation <https://the-littlest-jupyterhub.readthedocs.io/en/latest/troubleshooting/logs.html>`_.

Why is my environment not building?
-----------------------------------

If for some reasons an environment does not appear after :ref:`environments/add`, it is possible that
there are some issues building it and install the dependencies.

We recommend building the environment either locally with ``repo2docker`` or on Binder.

See :ref:`environments/prepare/binder` and the `repo2docker FAQ <https://repo2docker.readthedocs.io/en/latest/faq.html>`_
for more details.

The environment is very slow to build
-------------------------------------

Since the environments are built as Docker images, they can
`leverage the Docker cache <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache>`_
to make the builds faster.

In some cases Docker will not be able to leverage the cache, for example when building a Python or R environment for the first time.

Another reason for the build to be slow could be the amount of dependencies specified in files such as ``environment.yml`` or
``requirements.txt``.

Check out the previous section for more info on how to troubleshoot it.

Finding the source for an environment
-------------------------------------

(with the name of the repo and the commit hash)

Running the environments on my local machine
--------------------------------------------

with `repo2docker`

My extension and / or dependency does not seem to be installed
--------------------------------------------------------------

recommend trying locally or on Binder