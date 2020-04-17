Monitoring
==========

.. warning::

  HTTPS must be enabled to be able to access Cockpit. Refer to :ref:`install/https` for more info.

Cockpit
-------

The ``site.yml`` playbook installs ``cockpit`` by default as a monitoring tool for the server.

Additionally the PlasmaBio TLJH plugin registers ``cockpit`` as a JupyterHub service. This means that
Cockpit is accessible to JupyterHub admin users via the JupyterHub interface:

.. image:: ../images/configuration/cockpit-navbar.png
   :alt: Accessing cockpit from the nav bar
   :width: 50%
   :align: center

Users will be asked to login with their system credentials. They can then access the Cockpit dashboard:

.. image:: ../images/configuration/cockpit.png
   :alt: Cockpit
   :width: 100%
   :align: center

Monitoring user servers with Cockpit
------------------------------------

Since user servers are started as Docker containers, they will be displayed in the Cockpit interface in the
``Docker Containers`` section:

.. image:: ../images/configuration/cockpit-docker.png
   :alt: Docker Containers from Cockpit
   :width: 100%
   :align: center

The Cockpit interface shows:

- The username as part of the name of the Docker container
- The resources they are currently using
- The environment currently in use

It is also possible to stop the user server by clicking on the "Stop" button.