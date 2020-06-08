import grp
import json

from concurrent.futures import ThreadPoolExecutor
from itertools import groupby

from jupyterhub.apihandlers import APIHandler
from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Base, Column, Integer, Unicode
from jupyterhub.utils import admin_only, url_path_join
from tljh_repo2docker.images import list_images
from tornado.concurrent import run_on_executor
from tornado.web import authenticated


def list_groups():
    """ Get the list of available groups """
    # TODO: filter default groups
    return [g.gr_name for g in grp.getgrall()][:10]


class Permissions(Base):

    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(Unicode(255))
    image = Column(Unicode(255))

class PermissionsHandler(BaseHandler):
    """
    Renders the page to assign environments to user groups.
    """

    executor = ThreadPoolExecutor(max_workers=5)

    @authenticated
    @admin_only
    @run_on_executor
    def get(self):
        permissions = list(self.db.query(Permissions))
        mapping = {
            group: [p.image for p in images]
            for group, images in groupby(permissions, lambda p: p.group)
        }
        html = self.render_template(
            "permissions.html",
            static_url=self.static_url,
            images=list_images(),
            groups=list_groups(),
            permissions=mapping,
        )
        self.write(html)


class PermissionsAPIHandler(APIHandler):
    """
    Handle edits to the mapping of environments and groups.
    """

    @admin_only
    @authenticated
    async def post(self):
        raw_args = self.request.body.decode("utf-8")
        args = json.loads(raw_args)
        self.db.query(Permissions).delete()
        permissions = [Permissions(group=arg['name'], image=arg['value']) for arg in args]
        for permission in permissions:
            self.db.add(permission)
        self.db.commit()
        self.finish(json.dumps({"status": "ok"}))
        self.set_status(200)
