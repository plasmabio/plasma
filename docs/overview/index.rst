.. _overview/overview:

========
Overview
========

PlasmaBio is built with `The Littlest JupyterHub <https://the-littlest-jupyterhub.readthedocs.io/en/latest/>`_ (TLJH)
and uses Docker containers to start the user servers.

The project provides:

- A TLJH plugin with a predefined JupyterHub configuration
- Ansible playbooks to automate the deployment on a new server
- Documentation for the plugin and the Ansible playbooks

Here is an overview of all the different components and their interactions after PlasmaBio has been deployed on a new server:

.. image:: ../images/overview.png
   :alt: Overview Diagram
   :width: 100%
   :align: center
