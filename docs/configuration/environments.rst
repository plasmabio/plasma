User Environments
=================

User environments are built as immutable Docker images. The Docker images bundle the dependencies, extensions,
and predefined notebooks that should be available to all users.

PlasmaBio uses `repo2docker <https://repo2docker.readthedocs.io>`_ to build the images on the server.

For now the user environments are static and built when running the ``images.yml`` Ansible playbook. This
will be replaced by a UI within the JupyterHub interface and the steps to manage the environments will be
described in the section below.

Managing the user environments
------------------------------

Adding a new environment
........................

TODO

Updating an environment
.......................

TODO

Removing an environment
.......................

TODO