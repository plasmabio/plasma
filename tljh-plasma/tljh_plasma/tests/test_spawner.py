from types import SimpleNamespace

import pytest
from tljh_plasma import PlasmaSpawner
from tornado import web


def fake_spawner(image, allowed_images):
    async def list_images():
        return [
            {"image_name": name, "display_name": name} for name in allowed_images
        ]

    return SimpleNamespace(
        user=SimpleNamespace(name="alice"),
        user_options={"image": image},
        list_images=list_images,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "image",
    [
        # built environment the user's groups have no permission for
        "forbidden-env:HEAD",
        # any other local Docker image
        "ubuntu:latest",
        None,
    ],
)
async def test_start_refuses_image_without_permission(image):
    spawner = fake_spawner(image, allowed_images=["allowed-env:HEAD"])
    with pytest.raises(web.HTTPError) as e:
        await PlasmaSpawner.start(spawner)
    assert e.value.status_code == 403
