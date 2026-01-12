(overview-overview)=

# Overview

Plasma is built with [The Littlest JupyterHub](https://the-littlest-jupyterhub.readthedocs.io/en/latest/) (TLJH) 1.0
and uses Docker containers to start the user servers.

The project provides:

- A TLJH plugin with a predefined JupyterHub configuration
- Ansible playbooks to automate the deployment on a new server
- Documentation for the plugin and the Ansible playbooks

Plasma can be seen as an **opinionated TLJH distribution**:

- It gives admin users the possibility to configure multiple user environments backed by Docker images
- It provides an interface to build the user environments, accessible from the JupyterHub panel, using
  [tljh-repo2docker](https://github.com/plasmabio/tljh-repo2docker)
- It uses PAM as the authenticator, and relies on system users for data persistence (home directories) and authentication

Here is an overview of all the different components and their interactions after Plasma has been deployed on a new server:

```{image} ../images/overview.png
:align: center
:alt: Overview Diagram
:width: 100%
```

## The JupyterHub Documentation

Since Plasma is built on top of JupyterHub and The Littlest JupyterHub distribution, it benefits from its community
and high quality documentation.

For more information on these projects:

- [JupyterHub Documentation](https://jupyterhub.readthedocs.io)
- [The Littlest JupyterHub Documentation](https://the-littlest-jupyterhub.readthedocs.io)
