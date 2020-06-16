import asyncio
import sys

import pytest

from jupyterhub.tests.conftest import (
    io_loop,
    event_loop,
    db,
    pytest_collection_modifyitems,
)
from jupyterhub.tests.mocking import MockHub, MockPAMAuthenticator
from tljh_repo2docker.tests.conftest import (
    DummyConfig,
    minimal_repo,
    image_name,
    generated_image_name,
    remove_all_test_images
)
from tljh_repo2docker.tests.utils import add_environment
from tljh_repo2docker import tljh_custom_jupyterhub_config as tljh_repo2docker_config
from tljh_plasma import tljh_custom_jupyterhub_config as tljh_plasma_config


@pytest.fixture(scope="module")
def app(request, io_loop):
    """
    Adapted from:
    https://github.com/jupyterhub/jupyterhub/blob/8a3790b01ff944c453ffcc0486149e2a58ffabea/jupyterhub/tests/conftest.py#L74
    """

    # create a JupyterHub mock instance
    mocked_app = MockHub.instance()
    c = DummyConfig()
    c.JupyterHub = mocked_app

    # apply the config from the plugins
    tljh_repo2docker_config(c)
    tljh_plasma_config(c)

    # switch back to the MockPAMAuthenticator for the tests
    c.JupyterHub.authenticator_class = MockPAMAuthenticator

    async def make_app():
        await mocked_app.initialize([])
        await mocked_app.start()

    def fin():
        # disconnect logging during cleanup because pytest closes captured FDs prematurely
        mocked_app.log.handlers = []
        MockHub.clear_instance()
        try:
            mocked_app.stop()
        except Exception as e:
            print("Error stopping Hub: %s" % e, file=sys.stderr)

    request.addfinalizer(fin)
    io_loop.run_sync(make_app)
    return mocked_app
