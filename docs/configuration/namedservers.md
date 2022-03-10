# Named Servers

By default, users can run only one server at once.

[Named servers functionality](https://jupyterhub.readthedocs.io/en/stable/reference/config-user-env.html#named-servers) in JupyterHub
can be activated to let the user run several servers.

To allow up to 2 simultaneous named servers (in addition to the default one), create the file `named_servers_config.py`
in the directory `/opt/tljh/config/jupyterhub_config.d` with the following content:

```text
c.JupyterHub.allow_named_servers = True
c.JupyterHub.named_server_limit_per_user = 2
```

Then, reload tljh:

```text
sudo tljh-config reload
```

Have a look at the [named servers documentation](https://jupyterhub.readthedocs.io/en/stable/reference/config-user-env.html#named-servers)
for more details.
