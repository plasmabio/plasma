import json
from inspect import isawaitable
from itertools import groupby

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tljh_repo2docker.base import BaseHandler, require_admin_role
from tljh_repo2docker.docker import list_images
from tornado import web

from . import Permissions


class PermissionsHandler(BaseHandler):
    """
    Expose a handler to handle permissions
    """

    @web.authenticated
    @require_admin_role
    async def get(self):
        include_groups = self.settings.get("include_groups")
        all_groups = list(include_groups)

        engine = create_engine(self.settings.get("db_url"))
        Session = sessionmaker(bind=engine)
        with Session() as session:
            permissions = list(session.query(Permissions))
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


class PermissionsAPIHandler(BaseHandler):
    """
    Handle edits to the mapping of environments and groups.
    """

    @web.authenticated
    @require_admin_role
    async def post(self):
        raw_args = self.request.body.decode("utf-8")
        args = json.loads(raw_args)
        engine = create_engine(self.settings.get("db_url"))
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.query(Permissions).delete()
            permissions = [
                Permissions(image=arg["name"], group=arg["value"]) for arg in args
            ]
            session.add_all(permissions)
            session.commit()

        self.finish(json.dumps({"status": "ok"}))
        self.set_status(200)
