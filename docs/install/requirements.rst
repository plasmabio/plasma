Requirements
------------

Before installing PlasmaBio, you will need:

* A server running at least **Ubuntu 18.04**
* The public IP of the server
* SSH access to the machine
* A `priviledged user` on the remote machine that can issue commands using ``sudo``

If you already have a server available with the ``ubuntu`` user, validate that you have access to it with:

.. code-block:: bash

    ssh -t ubuntu@51.178.95.143 echo "test"

Which should output the following:

.. code-block:: bash

    test
    Connection to 51.178.95.143 closed.

Creating a new server (optional)
--------------------------------

If you don't already have a server (or want to test the setup from scratch) you can create a new one using a cloud provider.

`The Littlest JupyterHub documentation <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/index.html>`_
provides detailed guides for different cloud providers.

You can pick one of them, and stop at the point where the TLJH script (starting with ``#!/bin/bash``) should be provided
(this part is covered in the next section).
