(install-https)=

# HTTPS

:::{warning}
HTTPS is **not** enabled by default.

**We do not recommend deploying JupyterHub without HTTPS for production use.**

However in some situations it can be handy to do so, for example when testing the setup.
:::

## Enable HTTPS

Support for HTTPS is handled automatically thanks to [Let's Encrypt](https://letsencrypt.org), which also
handles the automatic renewal of the certificates when they are about to expire.

In your `hosts` file, add the `name_server` and `letsencrypt_email` variables:

```text
[server]
51.178.95.237

[server:vars]
ansible_python_interpreter=/usr/bin/python3
name_server=dev.plasmabio.org
letsencrypt_email=contact@plasmabio.org
```

If you have multiple servers, the `hosts` file will look like the following:

```text
[server1]
51.178.95.237

[server2]
51.178.95.238

[server1:vars]
ansible_python_interpreter=/usr/bin/python3
name_server=dev1.plasmabio.org
letsencrypt_email=contact@plasmabio.org

[server2:vars]
ansible_python_interpreter=/usr/bin/python3
name_server=dev2.plasmabio.org
letsencrypt_email=contact@plasmabio.org
```

Modify these values to the ones you want to use.

Then, run the `https.yml` playbook:

```bash
ansible-playbook https.yml -i hosts -u ubuntu
```

This will reload the proxy to take the changes into account.

It might take a few minutes for the certificates to be setup and the changes to take effect.

## How to make the domain point to the IP of the server

The domain used in the playbook variables (for example `dev.plasmabio.org`), should also point to the IP of the
server running JupyterHub.

This is typically done by logging in to the registrar website and adding a new entry to the DNS records.

You can refer to the [documentation for The Littlest JupyterHub on how to enable HTTPS](http://tljh.jupyter.org/en/latest/howto/admin/https.html#enable-https)
for more details.

## Manual HTTPS

To use an existing SSL key and certificate, you can refer to the
[Manual HTTPS with existing key and certificate](http://tljh.jupyter.org/en/latest/howto/admin/https.html#manual-https-with-existing-key-and-certificate)
documentation for TLJH.

This can also be integrated in the `https.yml` playbook by replacing the `tljh-config` commands to the ones mentioned
in the documentation.
