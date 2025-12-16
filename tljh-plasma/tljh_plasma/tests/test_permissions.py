import grp
import json
from collections import namedtuple

import pytest
from jupyterhub.tests.utils import (async_requests, auth_header,
                                    check_db_locks, get_page, public_host,
                                    public_url)
from jupyterhub.utils import url_path_join as ujoin
from tljh_repo2docker.tests.utils import add_environment, wait_for_image


# add the admin users to the admin groups
def mock_getgrall():
    group = namedtuple("struct_group", ["gr_name", "gr_mem", "gr_gid", "gr_passwd"])
    group.gr_name = "admin"
    group.gr_mem = ["admin"]
    group.gr_gid = 1000
    group.gr_passwd = "x"
    return [group]


def get_service_page(path, app, **kw):
    prefix = app.base_url
    service_prefix = "services/tljh_plasma"
    url = ujoin(public_host(app), prefix, service_prefix, path)
    return async_requests.get(url, **kw)


@check_db_locks
async def api_request(app, *api_path, method="get", noauth=False, **kwargs):
    """Make an API request"""

    base_url = public_url(app, path="services/tljh_plasma")

    headers = kwargs.setdefault("headers", {})
    if "Authorization" not in headers and not noauth and "cookies" not in kwargs:
        # make a copy to avoid modifying arg in-place
        kwargs["headers"] = h = {}
        h.update(headers)
        h.update(auth_header(app.db, kwargs.pop("name", "admin")))

    url = ujoin(base_url, "api", *api_path)
    f = getattr(async_requests, method)
    if app.internal_ssl:
        kwargs["cert"] = (app.internal_ssl_cert, app.internal_ssl_key)
        kwargs["verify"] = app.internal_ssl_ca
    resp = await f(url, **kwargs)

    return resp


@pytest.mark.asyncio
async def test_permissions_page(app):
    cookies = await app.login_user("admin")
    r = await get_service_page(
        "permissions", app, cookies=cookies, allow_redirects=True
    )
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
    r = await get_service_page(
        "permissions", app, cookies=cookies, allow_redirects=True
    )
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
    assert name in r.text
