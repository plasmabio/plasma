import asyncio
import os
import sys

import pytest

from tljh_repo2docker.tests.conftest import (
    minimal_repo,
    image_name,
    generated_image_name,
    remove_all_test_images
)
from tljh_repo2docker.tests.utils import add_environment
from tljh_repo2docker import tljh_custom_jupyterhub_config as tljh_repo2docker_config
from tljh_plasma import tljh_custom_jupyterhub_config as tljh_plasma_config
from traitlets.config import Config


@pytest.fixture
async def app(hub_app):
    config = Config()
    config.authenticator_class = 'jupyterhub.tests.mocking.MockPAMAuthenticator'

    tljh_repo2docker_config(config)
    tljh_plasma_config(config)

    app = await hub_app(config=config)
    return app