import grp

from concurrent.futures import ThreadPoolExecutor

from jupyterhub.handlers.base import BaseHandler
from tljh_repo2docker.images import list_images
from tornado.concurrent import run_on_executor
from tornado.web import authenticated


def list_groups():
    """ Get the list of available groups """
    # TODO: filter default groups
    return [g.gr_name for g in grp.getgrall()]


class PermissionsHandler(BaseHandler):

    executor = ThreadPoolExecutor(max_workers=5)

    @authenticated
    @run_on_executor
    def get(self):
        html = self.render_template(
            "permissions.html",
            images=list_images(),
            groups=list_groups()
        )
        self.write(html)

    @authenticated
    def post(self):
        pass