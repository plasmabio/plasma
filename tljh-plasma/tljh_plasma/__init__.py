import grp
import os
import pwd
import sys

from urllib.parse import urlparse, parse_qs

from dockerspawner import SystemUserSpawner
from jupyterhub.auth import PAMAuthenticator
from sqlalchemy import Column, Integer
from sqlalchemy import Unicode as SAUnicode
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tljh.hooks import hookimpl
from tljh.systemd import check_service_active
from tljh_repo2docker import TLJH_R2D_ADMIN_SCOPE, SpawnerMixin
from traitlets import Unicode

TLJH_PLASMA_DB_URL = os.environ.get("TLJH_PLASMA_DB_URL", "sqlite:///tljh_plasma.sqlite")
Base = declarative_base()


class Permissions(Base):

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(SAUnicode(255))
    image = Column(SAUnicode(255))


engine = create_engine(TLJH_PLASMA_DB_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class PlasmaSpawner(SpawnerMixin, SystemUserSpawner):
    """
    A custom Spawner to start user servers using Docker images
    built locally with repo2docker.
    """

    base_volume_path = Unicode(
        "/home", config=True, help="The base path for the user volumes"
    )

    shared_data_path = Unicode(
        "/srv/data", config=True, help="The path to the shared data folder"
    )

    async def list_images(self):
        # filter images based on the group permissions
        all_images = await super().list_images()
        groups = [
            group.gr_name for group in grp.getgrall() if self.user.name in group.gr_mem
        ]
        with Session() as session:
            permissions = session.query(Permissions).filter(
                Permissions.group.in_(groups)
            )
        whitelist = set(p.image for p in permissions)
        images = [image for image in all_images if image["image_name"] in whitelist]

        # filter images based on the url query parameter
        next_url = self.handler.get_argument("next", default="")
        query = urlparse(next_url).query
        parsed = parse_qs(query)
        if "environment-name" in parsed:
            display_name = parsed["environment-name"][0]
            images = [
                image for image in images if image["display_name"] == display_name
            ]

        return images

    async def start(self, *args, **kwargs):
        # set the image limits
        await super().set_limits()

        # escape the display name of the environment
        username = self.user.name
        image_name = self.user_options.get("image")

        images = await super().list_images()
        image = next(img for img in images if img["image_name"] == image_name)
        display_name = image["display_name"].replace(":", "-").replace("/", "-")

        # get the user home directory
        if self.base_volume_path is not None and self.base_volume_path != "":
            user_home = os.path.join(self.base_volume_path, username)
        else:
            user_home = pwd.getpwnam(username).pw_dir

        # create the user directory on the host if it does not exist
        volume_path = os.path.join(user_home, display_name)
        os.makedirs(volume_path, exist_ok=True)

        # the escaped environment name is used to create a new folder in the user home directory
        home = os.path.abspath(os.path.join(user_home, os.path.pardir))
        self.host_homedir_format_string = f"{home}/{username}"
        self.image_homedir_format_string = f"{home}/{username}"
        # pass the image name to the Docker container
        self.environment = {"USER_IMAGE": display_name}

        # mount volumes
        self.volumes = {
            os.path.join(
                os.path.dirname(__file__), "entrypoint", "entrypoint.sh"
            ): "/usr/local/bin/repo2docker-entrypoint",
            self.shared_data_path: {"bind": "/srv/data", "mode": "ro"},
        }

        return await super().start(*args, **kwargs)


if hookimpl:

    @hookimpl(trylast=True)
    def tljh_custom_jupyterhub_config(c):
        # hub
        c.JupyterHub.cleanup_servers = False
        c.JupyterHub.authenticator_class = PAMAuthenticator
        c.Authenticator.allow_all = True
        c.JupyterHub.template_paths.insert(
            0, os.path.join(os.path.dirname(__file__), "templates")
        )
        c.JupyterHub.allow_named_servers = True

        # spawner
        c.JupyterHub.spawner_class = PlasmaSpawner
        # let the spawner infer the user home directory
        c.PlasmaSpawner.base_volume_path = ""
        # update name template for named servers
        c.PlasmaSpawner.name_template = "{prefix}-{username}-{servername}"
        # increase the timeout to be able to pull larger Docker images
        c.PlasmaSpawner.start_timeout = 120
        c.PlasmaSpawner.pull_policy = "Never"
        c.PlasmaSpawner.remove = True
        c.PlasmaSpawner.default_url = "/lab"
        # TODO: change back to jupyterhub-singleuser
        c.PlasmaSpawner.cmd = ["/srv/conda/envs/notebook/bin/jupyterhub-singleuser"]
        # set the default cpu and memory limits
        c.PlasmaSpawner.args = ["--ResourceUseDisplay.track_cpu_percent=True"]
        # explicitely opt-in to enable the custom entrypoint logic
        c.PlasmaSpawner.run_as_root = True

        # Since dockerspawner 13
        c.PlasmaSpawner.allowed_images = "*"

        # prevent PID 1 running in the Docker container to stop when child processes are killed
        # see https://github.com/plasmabio/plasma/issues/191 for more info
        c.PlasmaSpawner.extra_host_config = {"init": True}

        # services
        c.JupyterHub.services.extend(
            [
                {
                    "name": "tljh_plasma",
                    "url": "http://127.0.0.1:6788",
                    "display": False,
                    "command": [
                        sys.executable,
                        "-m",
                        "tljh_plasma",
                        "--ip",
                        "127.0.0.1",
                        "--port",
                        "6788",
                    ],
                    "environment": {
                        "TLJH_PLASMA_DB_URL": TLJH_PLASMA_DB_URL,
                    },
                    "oauth_no_confirm": True,
                    "oauth_client_allowed_scopes": [
                        TLJH_R2D_ADMIN_SCOPE,
                    ],
                },
                {
                    "name": "tljh_repo2docker",
                    "url": "http://127.0.0.1:6789",
                    "display": False,
                    "command": [
                        sys.executable,
                        "-m",
                        "tljh_repo2docker",
                        "--ip",
                        "127.0.0.1",
                        "--port",
                        "6789",
                        "--machine_profiles",
                        '[{"label": "Small", "cpu": 2, "memory": 2},'
                        ' {"label": "Medium", "cpu": 4, "memory": 4},'
                        ' {"label": "Large", "cpu": 8, "memory": 8}]',
                        "--node_selector",
                        '{"gpu": {"description": "GPU description", "values": ["yes", "no"]},'
                        ' "ssd": {"description": "SSD description", "values": ["yes", "no"]}}',
                        "--custom_links",
                        '{"Permissions": "../tljh_plasma/permissions"}',
                    ],
                    "oauth_no_confirm": True,
                    "oauth_client_allowed_scopes": [
                        TLJH_R2D_ADMIN_SCOPE,
                    ],
                },
            ]
        )

        c.JupyterHub.custom_scopes = {
            TLJH_R2D_ADMIN_SCOPE: {
                "description": "Admin access to tljh_repo2docker",
            },
        }

        c.JupyterHub.load_roles = [
            {
                "description": "Role for tljh_repo2docker and tljh_plasma services",
                "name": "tljh-services",
                "scopes": ["read:users", "read:roles:users", "admin:servers"],
                "services": ["tljh_repo2docker", "tljh_plasma"],
            },
            {
                "name": "user",
                "scopes": [
                    "self",
                    # access to the environments and servers pages
                    "access:services!service=tljh_repo2docker",
                ],
            },
        ]
