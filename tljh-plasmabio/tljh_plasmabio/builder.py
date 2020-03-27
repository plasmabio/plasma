import asyncio
import subprocess

from concurrent.futures import ThreadPoolExecutor
from threading import Event

from jupyterhub.services.auth import HubAuthenticated
from tornado import web
from tornado.concurrent import run_on_executor
from tornado.log import app_log


def build_image():
    subprocess.run(["sleep", "10"])


def build_docker_image(name, repo, ref=None):
    ref = ref or "master"
    subprocess.run(
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
            f"{name}:latest",
            repo,
        ]
    )


class Builder:
    _kill_event = None
    _future = None

    executor = ThreadPoolExecutor(max_workers=5)
    building = False

    def __init__(self):
        pass

    async def get_status(self):
        if self.building:
            return {"status": "building", "message": ""}
        return {"status": status, "message": "\n".join(messages)}

    async def build(self):
        if not self.building:
            self._future = asyncio.Future()
            self.building = True
            self._kill_event = evt = Event()
            try:
                await self._run_build()
                self._future.set_result(True)
            except Exception as e:
                # TODO: handle failures
                print(e)
            finally:
                self.building = False
        try:
            await self._future
        except Exception as e:
            raise e

    @run_on_executor
    def _run_build(self):
        return build_image()


class BuildHandler(HubAuthenticated, web.RequestHandler):
    def initialize(self, builder):
        self.builder = builder
        self.log = app_log

    @web.authenticated
    async def get(self):
        data = await self.builder.get_status()
        self.finish(json.dumps(data))

    @web.authenticated
    async def post(self):
        self.log.debug("Build user images")
        try:
            await self.builder.build()
        except Exception as e:
            await web.HTTPError(500, str(e))

        self.log.debug("Build succeeded")
        self.set_status(200)
