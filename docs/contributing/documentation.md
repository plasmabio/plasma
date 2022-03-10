# Writing Documentation

The documentation is available at [docs.plasmabio.org](https://docs.plasmabio.org) and is written
with [Sphinx](https://sphinx-doc.org/).

The Littlest JupyterHub has a good [overview page](https://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/docs.html)
on writing documentation, with externals links to the tools used to generate it.

First, create a new environment:

```bash
conda create -n plasma-docs -c conda-forge python
conda activate plasma-docs
```

In the `docs` folder, run:

```bash
python -m pip install -r requirements.txt
make html
```

Open `docs/_build/index.html` in a browser to start browsing the documentation.

Rerun `make html` after making any changes to the source.
