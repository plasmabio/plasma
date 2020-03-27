import json
import os

import docker

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader
from jupyterhub._data import DATA_FILES_PATH
from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import auth_decorator, url_path_join
from tornado import ioloop, web

from .builder import Builder, BuildHandler

loader = ChoiceLoader(
    [
        PackageLoader("tljh_plasmabio", "templates"),
        FileSystemLoader(os.path.join(DATA_FILES_PATH, "templates")),
    ]
)
templates = Environment(loader=loader)
client = docker.from_env()


def list_images():
    """
    Retrieve local images built and being built by repo2docker
    """
    r2d_images = [
        image
        for image in client.images.list(
            filters={"dangling": False, "label": ["repo2docker.ref"]}
        )
    ]
    images = [
        {
            "repo": image.labels["repo2docker.repo"],
            "ref": image.labels["repo2docker.ref"],
            "status": "built",
        }
        for image in r2d_images
        if image.labels["repo2docker.repo"] != "local"
    ]

    r2d_containers = [
        container
        for container in client.containers.list()
        if "repo2docker.name" not in container.labels
    ]
    containers = [
        {
            "repo": container.labels["repo2docker.repo"],
            "ref": container.labels["repo2docker.ref"],
            "status": "building",
        }
        for container in r2d_containers
        if container.labels["repo2docker.repo"] != "local"
    ]
    return images + containers


@auth_decorator
def admin_only(self):
    """Decorator for restricting access to admin users"""
    user = self.get_current_user()
    if user is None or not user["admin"]:
        raise web.HTTPError(403)


class ImagesHandler(HubAuthenticated, web.RequestHandler):
    @admin_only
    def get(self):
        template = templates.get_template("images.html")
        user = self.get_current_user()
        prefix = self.hub_auth.hub_prefix
        logout_url = url_path_join(prefix, "logout")
        self.write(
            template.render(
                user=user,
                images=list_images(),
                static_url=self.static_url,
                login_url=self.hub_auth.login_url,
                logout_url=logout_url,
                base_url=prefix,
                no_spawner_check=True,
            )
        )


class MultiStaticFileHandler(web.StaticFileHandler):
    """
    A static file handler that 'merges' a list of directories

    If initialized like this::
        application = web.Application([
            (r"/content/(.*)", web.MultiStaticFileHandler, {"paths": ["/var/1", "/var/2"]}),
        ])
    A file will be looked up in /var/1 first, then in /var/2.

    From: https://github.com/voila-dashboards/voila/blob/112163d88a2d1a5c7706327e68825ddc02819d3a/voila/static_file_handler.py#L16
    """

    def initialize(self, paths, default_filename=None):
        # find the first absolute path that exists
        self.roots = paths
        super(MultiStaticFileHandler, self).initialize(
            path=paths[0], default_filename=default_filename
        )

    def get_absolute_path(self, root, path):
        self.root = self.roots[0]
        for root in self.roots:
            abspath = os.path.abspath(os.path.join(root, path))
            if os.path.exists(abspath):
                self.root = root  # make sure all the other methods in the base class know how to find the file
                break
        return abspath


def make_app():
    service_prefix = os.environ["JUPYTERHUB_SERVICE_PREFIX"]
    static_paths = [
        # JupyterHub static files
        os.path.join(DATA_FILES_PATH, "static"),
        # The PlasmaBio static files
        os.path.join(os.path.dirname(__file__), "static"),
    ]
    app_settings = {
        "static_path": "/",
        "static_url_prefix": f"{service_prefix}/static/",
    }
    builder = Builder()
    return web.Application(
        [
            (rf"{service_prefix}?", ImagesHandler),
            (rf"{service_prefix}api/build", BuildHandler, {"builder": builder}),
            (
                rf"{service_prefix}static/(.*)",
                MultiStaticFileHandler,
                {"paths": static_paths},
            ),
        ],
        **app_settings,
    )


if __name__ == "__main__":
    if not os.environ["JUPYTERHUB_API_URL"].endswith("/"):
        os.environ["JUPYTERHUB_API_URL"] = os.environ["JUPYTERHUB_API_URL"] + "/"
    app = make_app()
    app.listen(9988)
    ioloop.IOLoop.current().start()
