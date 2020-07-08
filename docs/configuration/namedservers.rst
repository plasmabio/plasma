Named Servers
=============

By default, users can run only one server at once.

`Named servers functionality<https://jupyterhub.readthedocs.io/en/stable/reference/config-user-env.html#named-servers>`_ in JupyterHub
can be activated to let the user run several servers.

To allow up to 2 simultaneous named servers (in addition to the default one), create the file ``named_servers_config.py``
in the directory ``/opt/tljh/config/jupyterhub_config.d`` with the following content:

.. code-block:: text

   c.JupyterHub.allow_named_servers = True
   c.JupyterHub.named_server_limit_per_user = 2

Then, reload tljh:

.. code-block:: text

   sudo tljh-config reload

Have a look to `named servers documentation<https://jupyterhub.readthedocs.io/en/stable/reference/config-user-env.html#named-servers>`_
for more details.
