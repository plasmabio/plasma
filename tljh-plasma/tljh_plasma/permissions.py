import grp
import json

from concurrent.futures import ThreadPoolExecutor

from jupyterhub.apihandlers import APIHandler
from jupyterhub.handlers.base import BaseHandler
from jupyterhub.utils import admin_only, url_path_join
from tljh_repo2docker.images import list_images
from tornado.concurrent import run_on_executor
from tornado.web import authenticated


def list_groups():
    """ Get the list of available groups """
    # TODO: filter default groups
    return [g.gr_name for g in grp.getgrall()][:10]


class PermissionsHandler(BaseHandler):
    """
    Renders the page to assign environments to user groups.
    """

    executor = ThreadPoolExecutor(max_workers=5)

    @authenticated
    @admin_only
    @run_on_executor
    def get(self):
        html = self.render_template(
            "permissions.html",
            static_url=self.static_url,
            images=list_images(),
            groups=list_groups(),
        )
        self.write(html)


class PermissionsAPIHandler(APIHandler):
    """
    Handle edits to the mapping of environments and groups.
    """
    @admin_only
    @authenticated
    def post(self):
        print(self.request.body_arguments)
        self.finish(json.dumps({"status": "ok"}))
