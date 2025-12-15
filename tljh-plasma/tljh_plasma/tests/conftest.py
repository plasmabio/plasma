import pytest
import sys

from jupyterhub.tests.mocking import MockPAMAuthenticator
from tljh_repo2docker.tests.local_build.conftest import (
    image_name,
    generated_image_name,
)
from tljh_repo2docker.tests.conftest import (
    minimal_repo,
    remove_all_test_images,
)
from tljh_repo2docker import tljh_custom_jupyterhub_config as tljh_repo2docker_config
from tljh_plasma import tljh_custom_jupyterhub_config as tljh_plasma_config
from traitlets.config import Config


@pytest.fixture
async def app(hub_app):
    config = Config()

    tljh_repo2docker_config(config)
    tljh_plasma_config(config)

    config.JupyterHub.authenticator_class = MockPAMAuthenticator

    config.JupyterHub.services.extend(
        [
            {
                "name": "tljh_repo2docker",
                "url": "http://127.0.0.1:6789",
                "command": [
                    sys.executable,
                    "-m",
                    "tljh_repo2docker",
                    "--ip",
                    "127.0.0.1",
                    "--port",
                    "6789",
                ],
                "oauth_no_confirm": True,
            }
        ]
    )

    config.JupyterHub.load_roles = [
        {
            "description": "Role for tljh_repo2docker service",
            "name": "tljh-repo2docker-service",
            "scopes": ["read:users", "read:roles:users", "admin:servers"],
            "services": ["tljh_repo2docker"],
        },
    ]

    app = await hub_app(config=config)
    return app
