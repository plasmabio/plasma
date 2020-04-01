.. _troubleshooting/troubleshooting:

Troubleshooting
===============

How to SSH to the machine
-------------------------

First make sure your SSH key has been deployed to the server. See :ref:`install/ssh-key` for more details.

Once the key is set up, connect to the machine over SSH using the following commands:

.. code-block:: bash

  ssh ubuntu@51.178.95.143


Why is my environment not building?
-----------------------------------

The environment is very slow to build
-------------------------------------

(mention the Docker cache)

Finding the source for an environment
-------------------------------------

(with the name of the repo and the commit hash)

Running the environments on my local machine
--------------------------------------------

with `repo2docker`

My extension and / or dependency does not seem to be installed
--------------------------------------------------------------

recommend trying locally or on Binder