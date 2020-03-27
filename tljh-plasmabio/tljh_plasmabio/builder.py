import asyncio
import subprocess

from threading import Event

from jupyterhub.services.auth import HubAuthenticated
from tornado import web
from tornado.log import app_log


def build_image(name, repo):
    ref = "master"
    image_name = f"{name}:latest"
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "repo2docker",
            "--ref",
            ref,
            "--user-name",
            "jovyan",
            "--user-id",
            "1100",
            "--no-run",
            "--image-name",
            image_name,
            "--appendix",
            f"LABEL repo2docker.name={image_name}",
            repo,
        ]
    )

def test_build():
    subprocess.Popen(["sleep", "60"])


class BuildHandler(HubAuthenticated, web.RequestHandler):
    def initialize(self):
        self.log = app_log

    @web.authenticated
    def post(self):
        self.log.debug("Build user images")

        # TODO: validate and parse input

        # TODO: cleanup defunct processes
        test_build()

        self.log.debug("Build succeeded")
        self.set_status(200)
