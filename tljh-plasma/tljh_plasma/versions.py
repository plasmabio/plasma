import json
from importlib import metadata

PACKAGES = [
    ("Plasma", "tljh-plasma"),
    ("tljh-repo2docker", "tljh-repo2docker"),
    ("JupyterHub", "jupyterhub"),
]


def _package_version(name):
    try:
        dist = metadata.distribution(name)
    except metadata.PackageNotFoundError:
        return "not installed"
    version = dist.version
    # pip records the commit of a package installed from git (PEP 610),
    # which is how Plasma is deployed from master
    direct_url = dist.read_text("direct_url.json")
    if direct_url:
        commit = json.loads(direct_url).get("vcs_info", {}).get("commit_id")
        if commit:
            version = f"{version} ({commit[:7]})"
    return version


def get_versions():
    """Return the (label, version) pairs shown to admins in the header"""
    return [(label, _package_version(name)) for label, name in PACKAGES]
