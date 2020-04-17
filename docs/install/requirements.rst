.. _install/requirements:

Requirements
============

Before installing PlasmaBio, you will need:

* A server running at least **Ubuntu 18.04**
* The public IP of the server
* SSH access to the machine
* A `priviledged user` on the remote machine that can issue commands using ``sudo``


.. _install/ssh-key:

Adding the public SSH key to the server
---------------------------------------

To deploy PlasmaBio, you need to be able to access the server via SSH.

This is typically done by copying the key to the remote server using the ``ssh-copy-id`` command, or
by providing the key during the creation of the server (see section below).

To copy the SSH key to the server:

.. code-block:: bash

    ssh-copy-id ubuntu@51.178.95.143

Alternatively, the SSH key can be copied from ``~/.ssh/id_rsa.pub``, and looks like the following:

.. code-block:: bash

    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCeeTSTvuZ4KzWBwUj2yIKNhX9Jw+LLdNfjOaVONfnYrlVYywRLexRcKJVcUOL8ofK/RXW2xuRQzUu4Kpa0eKMM+iUPEKFF+RtLQGxn3aCVctvXprzrugm69unWot+rc2aBosX99j64U74KkEaLquuBZDd/hmqxxbCr9DRYqb/aFIjfhBS8V0QdKVln1jPoy/nPCY6HMnovicExjB/E5s5lTj/2qUoNXWF5r4zHQlXuc6CY0NN11F2/5n0KfSD3eunBd26zrhzpOJbcyftUV9YOICjJXWOLLOPFn2mqXsPa0k/xRCjCiLv/aiU8xF5mJvYDEJ2jigqGihzfgPz4UEwH0bqQRsq9LrFYVcFLQprCknxxt9F2WgO6nv/V5kgRSi3WOzRt12NcWjg1um/C2TTK9bSqFTEMXlPlsLxDa7Js/kUMZh6N3rIzTsQpXuhKjQLxZ5TReUUdsGyAtU0eQv5rrJBr6ML02C9EMZ5NvduPs1w44+39WONCmoQoKBkiFIYfN0EV7Ps6kM6okzT7Cu8n4DOlsrdLT1b4gSK891461EjIHsfQsD+m53tKZx3Q2FTPJkPofUISzUXzRnXoPflWPbvwLl42qEjWJ4eZv0LHDtJhyr1RvRCXi7P24DdbLbjTjWy3kpNWTdO3b0Zto90ekHNElriHlM1BeqFo+6ABnw== your_email@example.com

It can then be manually added to ``~/.ssh/authorized_keys`` on the server.

For more information, checkout `this tutorial on DigitalOcean to set up SSH Keys on Ubuntu 18.04 <https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1804>`_.

.. _requirements/server:

Creating a new server (optional)
--------------------------------

If you don't already have a server (or want to test the setup from scratch) you can create a new one using a cloud provider.

`The Littlest JupyterHub documentation <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/index.html>`_
provides detailed guides for different cloud providers.

You can pick one of them, and stop at the point where the TLJH script (starting with ``#!/bin/bash``) should be provided
(this part is covered in the next section).

During the installation steps, you will be able to specify the SSH key to use to connect to the server.

The key must first be added to the list of available keys by using the cloud provider interface:

.. image:: ../images/install/add-ssh-key.png
   :alt: Add a new SSH key
   :width: 75%
   :align: center

When asked to choose an SSH key, select the one you just added:

.. image:: ../images/install/select-ssh-key.png
   :alt: Select the SSH key
   :width: 75%
   :align: center

Testing the connection
----------------------

For a server with an ``ubuntu`` user, validate that you have access to it with:

.. code-block:: bash

    ssh -t ubuntu@51.178.95.143 echo "test"

Which should output the following:

.. code-block:: bash

    test
    Connection to 51.178.95.143 closed.

Updating the local SSH config (optional)
----------------------------------------

Depending on the server used for the deployment, see :ref:`requirements/server`, you might want to add the
following to your local SSH config located in ``~/.ssh/config``:

.. code-block:: bash

    Host *
        ServerAliveInterval 60
        ServerAliveCountMax 10

These settings help keep the connection to server alive while the deployment is happening,
or if you have an open SSH connection to the server.
