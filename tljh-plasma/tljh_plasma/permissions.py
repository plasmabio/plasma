import json

from itertools import groupby

from inspect import isawaitable
from jupyterhub.apihandlers import APIHandler
from jupyterhub.handlers.base import BaseHandler
from jupyterhub.orm import Base, Column, Integer, Unicode
from jupyterhub.scopes import needs_scope
from tljh_repo2docker.docker import list_images
from tornado.web import authenticated


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
    @needs_scope("admin-ui")
    async def get(self):
        include_groups = self.settings.get("include_groups")
        all_groups = list(include_groups)
        permissions = list(self.db.query(Permissions))
        mapping = {
            image: [p.group for p in groups if p.group in all_groups]
            for image, groups in groupby(permissions, lambda p: p.image)
        }
        images = await list_images()
        html = self.render_template(
            "permissions.html",
            static_url=self.static_url,
            images=images,
            groups=all_groups,
            permissions=mapping,
        )
        if isawaitable(html):
            self.write(await html)
        else:
            self.write(html)


class PermissionsAPIHandler(APIHandler):
    """
    Handle edits to the mapping of environments and groups.
    """

    @authenticated
    @needs_scope("admin-ui")
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
