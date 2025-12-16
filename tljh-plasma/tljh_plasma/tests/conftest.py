import sys

import pytest
from jupyterhub.tests.mocking import MockPAMAuthenticator
from tljh_plasma import PlasmaSpawner
from tljh_plasma import tljh_custom_jupyterhub_config as tljh_plasma_config
from tljh_repo2docker import \
    tljh_custom_jupyterhub_config as tljh_repo2docker_config
from tljh_repo2docker.tests.conftest import minimal_repo
from tljh_repo2docker.tests.local_build.conftest import image_name
from traitlets.config import Config


class MockPlasmaSpawner(PlasmaSpawner):
    def _user_id_default(self):
        return 1000

    def _group_id_default(self):
        return 1000


@pytest.fixture
async def app(hub_app):
    config = Config()

    tljh_repo2docker_config(config)
    tljh_plasma_config(config)

    config.JupyterHub.authenticator_class = MockPAMAuthenticator
    config.Authenticator.admin_users = {"admin"}

    config.JupyterHub.spawner_class = MockPlasmaSpawner

    app = await hub_app(config=config)
    return app
