(environments-add)=

# Adding a new environment

Now that the repository is ready, we can add it to the JupyterHub via the user interface.

To add the new user environment, click on the `Add New` button and provide the following information:

- `Repository URL`: the URL to the repository to build the environment from
- `Reference (git commit)`: the git commit hash to use
- `Name of the environment`: the display name of the environment. If left empty, it will be automatically generated from the repository URL.
- `Memory Limit (GB)`: the memory limit to apply to the user server.
  Float values are allowed (for example a value of `3.5` corresponds to a limit of 3.5GB)
- `CPU Limit`: the number of cpus the user server is allowed to used.
  See the [JupyterHub documentation](https://jupyterhub.readthedocs.io/en/stable/api/spawner.html#jupyterhub.spawner.Spawner.cpu_limit) for more info.

As an example:

```{image} ../images/environments/add-new.png
:align: center
:alt: Adding a new image
:width: 100%
```

After clicking on the `Add Image` button, the page will automatically reload and show the list of built environments,
as well as the ones currently being built:

```{image} ../images/environments/environments.png
:align: center
:alt: Listing the environments being built
:width: 100%
```

Building a new environment can take a few minutes. You can reload the page to refresh the status.
