import grp
import json

from itertools import groupby

from jupyterhub.apihandlers import APIHandler
from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Base, Column, Integer, Unicode
from jupyterhub.utils import admin_only
from tljh_repo2docker.docker import list_images
from tornado.web import authenticated


def list_groups(exclude_groups):
    """ Get the list of available groups """
    return [g.gr_name for g in grp.getgrall() if g.gr_name not in exclude_groups]


class Permissions(Base):

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(Unicode(255))
    image = Column(Unicode(255))


class PermissionsHandler(BaseHandler):
    """
    Renders the page to assign environments to user groups.
    """

    @authenticated
    @admin_only
    async def get(self):
        permissions = list(self.db.query(Permissions))
        mapping = {
            image: [p.group for p in groups]
            for image, groups in groupby(permissions, lambda p: p.image)
        }
        images = await list_images()
        exclude_groups = self.settings.get("exclude_groups")
        html = self.render_template(
            "permissions.html",
            static_url=self.static_url,
            images=images,
            groups=list_groups(exclude_groups),
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
        permissions = [
            Permissions(image=arg["name"], group=arg["value"]) for arg in args
        ]
        for permission in permissions:
            self.db.add(permission)
        self.db.commit()
        self.finish(json.dumps({"status": "ok"}))
        self.set_status(200)