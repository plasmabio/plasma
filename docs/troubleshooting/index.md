(troubleshooting-troubleshooting)=

# Troubleshooting

```{contents} Table of contents
:depth: 1
:local: true
```

## How to SSH to the machine

First make sure your SSH key has been deployed to the server. See {ref}`install-ssh-key` for more details.

Once the key is set up, connect to the machine over SSH using the following command:

```bash
ssh ubuntu@51.178.95.143
```

## Looking at logs

See: [The Littlest JupyterHub documentation](https://the-littlest-jupyterhub.readthedocs.io/en/latest/troubleshooting/logs.html).

The main components to have a look at are:

- the JupyterHub instance
- Traefik (proxy)
- the user server

The logs for the hub and proxy can be inspected with:

```bash
sudo journalctl -u jupyterhub
sudo journalctl -u traefik
```

````{note}
To follow the logs of the services and print more content on the screen, you can combine the
`-f` (print the end and follow new logs) and `-n` (specify the number of lines to display) options:

```bash
sudo journalctl -u jupyterhub -f -n 1000
```
````

If you want a clean restart of these services, run:

```bash
sudo systemctl restart jupyterhub
sudo systemctl restart traefik
```

In Plasma, the user servers run in Docker containers. To access the logs of a particular server, first
identify the name of the user.

Then run:

```bash
# list all the containers
docker ps
# use -f to follow the logs
docker logs -f jupyter-username
```

The logs will look like the following:

```bash
$ docker logs -f jupyter-alice
[I 2022-03-09 08:42:40.322 SingleUserNotebookApp notebookapp:1593] Authentication of /metrics is OFF, since other authentication is disabled.
[I 2022-03-09 08:42:40.856 LabApp] JupyterLab extension loaded from /usr/local/lib/python3.9/site-packages/jupyterlab
[I 2022-03-09 08:42:40.856 LabApp] JupyterLab application directory is /usr/local/share/jupyter/lab
Patching auth into jupyter_server.base.handlers.JupyterHandler(jupyter_server.base.handlers.AuthenticatedHandler) -> JupyterHandler(jupyterhub.singleuser.mixins.HubAuthenticatedHandler, jupyter_server.base.handlers.AuthenticatedHandler)
[I 2022-03-09 08:42:40.864 SingleUserNotebookApp mixins:576] Starting jupyterhub-singleuser server version 1.5.0
[I 2022-03-09 08:42:40.867 SingleUserNotebookApp notebookapp:2329] Serving notebooks from local directory: /home/jovyan
[I 2022-03-09 08:42:40.867 SingleUserNotebookApp notebookapp:2329] Jupyter Notebook 6.4.8 is running at:
[I 2022-03-09 08:42:40.867 SingleUserNotebookApp notebookapp:2329] http://4aace966ddb0:8888/user/alice/
[I 2022-03-09 08:42:40.867 SingleUserNotebookApp notebookapp:2330] Use Control-C to stop this server and shut dow
```


## Why is my environment not building?

If for some reasons an environment does not appear after {ref}`environments-add`, it is possible that
there are some issues building it and installing the dependencies.

We recommend building the environment either locally with `repo2docker` (next section) or on Binder.

See {ref}`environments-prepare-binder` and the [repo2docker FAQ](https://repo2docker.readthedocs.io/en/latest/faq.html)
for more details.

### Accessing the `repo2docker` container

In Plasma, `repo2docker` runs in a Docker container, based on the Docker image available at
`quay.io/jupyterhub/repo2docker:main`.

If you are not able to run `repo2docker` manually to investigate a build failure (see section below), you can try to access the
logs of the Docker container.

On the machine running TLJH, run the `docker ps` command. The output should look like the following:

```bash
CONTAINER ID        IMAGE                                 COMMAND                  CREATED             STATUS              PORTS               NAMES
146b4d335215        quay.io/jupyterhub/repo2docker:main   "/usr/local/bin/entr…"   31 seconds ago      Up 30 seconds       52000/tcp           naughty_thompson
```

You can then access the logs of the container with:

```bash
docker logs 146b4d335215
# or with the generated name
docker logs naughty_thompson
```

If the `repo2docker` container has stopped, then you can use the `docker ps -a` to display all the containers.
The output will show `Exited` as part of the `STATUS`:

```bash
CONTAINER ID        IMAGE                                 COMMAND                  CREATED             STATUS                          PORTS               NAMES
146b4d335215        quay.io/jupyterhub/repo2docker:main   "/usr/local/bin/entr…"   4 minutes ago       Exited (0) About a m
```

## Running the environments on my local machine

To run the same environments on a local machine, you can use `jupyter-repo2docker` with the following parameters:

```bash
jupyter-repo2docker --ref a4edf334c6b4b16be3a184d0d6e8196137ee1b06 https://github.com/plasmabio/template-python
```

Update the parameters based on the image you would like to build.

This will create a Docker image and start it automatically once the build is complete.

Refer to the [repo2docker documentation](https://repo2docker.readthedocs.io/en/latest/usage.html) for more details.

## My extension and / or dependency does not seem to be installed

See the two previous sections to investigate why they are missing.

The logs might contain silent errors that did not cause the build to fail.

## The name of the environment is not displayed in the top bar

This functionality requires the `jupyter-topbar-text` extension to be installed in the environment.

This extension must be added to the `postBuild` file of the repository.
See this [commit](https://github.com/plasmabio/template-python/commit/b3dd6c4b525ed4584e79175d4ae340a8b2395682) as an example.

The name of the environment will then be displayed as follows:

```{image} ../images/troubleshooting/topbar-env-name.png
:align: center
:alt: The name of the environment in the top bar
:width: 75%
```

## The environment is very slow to build

Since the environments are built as Docker images, they can
[leverage the Docker cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache)
to make the builds faster.

In some cases Docker will not be able to leverage the cache, for example when building a Python or R environment for the first time.

Another reason for the build to be slow could be the amount of dependencies specified in files such as `environment.yml` or
`requirements.txt`.

Check out the previous section for more info on how to troubleshoot it.

## Finding the source for an environment

If you are managing the environments, you can click on the `Reference` link in the UI,
which will open a new tab to the repository pointing the commit hash:

```{image} ../images/troubleshooting/git-commit-hash.png
:align: center
:alt: The git commit hash on GitHub
:width: 50%
```

If you are using the environments, the name contains the information about the repository
and the reference used to build the environment.

On the repository page, enter the reference in the search input box:

```{image} ../images/troubleshooting/search-github-repo.png
:align: center
:alt: Searching for a commit hash on GitHub
:width: 100%
```

## Removing an environment returns an error

See {ref}`remove-error` for more info.
