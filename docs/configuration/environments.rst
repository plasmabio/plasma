User Environments
=================

User environments are built as immutable Docker images. The Docker images bundle the dependencies, extensions,
and predefined notebooks that should be available to all users.

PlasmaBio uses `repo2docker <https://repo2docker.readthedocs.io>`_ to build the images on the server.

Environments can be managed by admin users by clicking on ``Services -> images``:

.. image:: ../images/configuration/services-navbar.png
   :alt: Manage the list of environments
   :width: 50%
   :align: center


Managing the user environments
------------------------------

The environments shows the list of environments currently available:

.. image:: ../images/configuration/environments.png
   :alt: List of built environments
   :width: 100%
   :align: center


Adding a new environment
........................

To add a new user environment, click on the ``Add New`` button and provide the following information:

- ``Repository URL``: the URL to the repository to build the environment from
- ``Ref``: the git commit hash to use


As an example:


.. image:: ../images/configuration/add-new.png
   :alt: Adding a new image
   :width: 100%
   :align: center


After clicking on the ``Add Image`` button, the page will automatically reload itself to show the list of built environments,
as well as the ones currently being built:


.. image:: ../images/configuration/building-environments.png
   :alt: Listing the environments being built
   :width: 100%
   :align: center


Building a new environment can take a few minutes. You can reload the page to refresh the status.

Removing an environment
.......................

TODO

Updating an environment
.......................

Since the environments are built as Docker images, they are immutable.

Instead of updating an environment, it is recommended to:

1. Add a new one with the new ``Ref``
2. Remove the previous one by clicking on the ``Remove`` button (see above)
