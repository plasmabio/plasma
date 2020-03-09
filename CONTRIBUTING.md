# Setting up a dev environment

Create a virtual environment to install the dependencies.

Using `conda`:

```bash
conda create -n plasmasbio -c conda-forge python nodejs
conda activate plasmabio
```

Alternatively, with Python's built in `venv` module, you can make a virtual environment with:

```bash
python3 -m venv .
source bin/activate
```

Install the development requirements:

```bash
pip install -r dev-requirements.txt

# dev install of the plasmabio package
pip install -e tljh-plasmabio

# Install [configurable-http-proxy](https://github.com/jupyterhub/configurable-http-proxy):
npm -g install configurable-http-proxy
```

Finally, start `jupyterhub` with the config:

```bash
python3 -m jupyterhub -f jupyterhub_config.py
```

Open `https://localhost:8000` to start servers.


# Contributing to the documentation

Create a new environment:

```bash
conda create -n plasmabio-docs -c conda-forge python
conda activate plasmabio-docs
```

In the `docs` folder:

```bash
python -m pip install -r requirements.txt
make html
```

Open `docs/_build/index.html` in a browser to start browsing the documentation.

Rerun `make html` after making any changes to the source.
