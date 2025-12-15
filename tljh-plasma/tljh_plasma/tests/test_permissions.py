import grp
import json

from collections import namedtuple

import pytest

from jupyterhub.tests.utils import api_request, get_page
from tljh_repo2docker.tests.utils import add_environment, wait_for_image


# add the admin users to the admin groups
def mock_getgrall():
    group = namedtuple("struct_group", ["gr_name", "gr_mem", "gr_gid", "gr_passwd"])
    group.gr_name = "admin"
    group.gr_mem = ["admin"]
    group.gr_gid = 1000
    group.gr_passwd = "x"
    return [group]


@pytest.mark.asyncio
async def test_permissions_page(app):
    cookies = await app.login_user("admin")
    r = await get_page("permissions", app, cookies=cookies, allow_redirects=False)
    r.raise_for_status()
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_permissions_api_endpoint(app, minimal_repo, image_name):
    # create a new environment
    name, ref = image_name.split(":")
    r = await add_environment(app, repo=minimal_repo, name=name, ref=ref)
    assert r.status_code == 200
    await wait_for_image(image_name=image_name)

    # update the permissions
    r = await api_request(
        app,
        "permissions",
        method="post",
        data=json.dumps([{"name": image_name, "value": "test"}]),
    )
    r.raise_for_status()
    assert r.status_code == 200

    # check the permissions are displayed on the page
    cookies = await app.login_user("admin")
    r = await get_page("permissions", app, cookies=cookies, allow_redirects=False)
    r.raise_for_status()
    assert r.status_code == 200
    assert image_name in r.text


@pytest.mark.asyncio
async def test_spawn_page(app, minimal_repo, image_name, monkeypatch):
    # add a new environment
    name, ref = image_name.split(":")
    r = await add_environment(app, repo=minimal_repo, name=name, ref=ref)
    assert r.status_code == 200
    await wait_for_image(image_name=image_name)

    cookies = await app.login_user("admin")

    # add the user to the group
    monkeypatch.setattr(grp, "getgrall", mock_getgrall)

    # go to the spawn page
    r = await get_page("spawn", app, cookies=cookies, allow_redirects=False)
    r.raise_for_status()
    assert name not in r.text

    # update the permissions
    r = await api_request(
        app,
        "permissions",
        method="post",
        data=json.dumps([{"name": image_name, "value": "admin"}]),
    )
    r.raise_for_status()
    assert r.status_code == 200

    # the environment should now be on the page
    r = await get_page("spawn", app, cookies=cookies, allow_redirects=False)
    r.raise_for_status()
    assert r.status_code == 200
    print(r.text)
    assert name in r.text
