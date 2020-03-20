HTTPS
=====

HTTPS is **enabled by default** when using the Ansible playbooks, see :ref:`install/ansible`.

Support for HTTPS is handled automatically thanks to `Let's Encrypt <https://letsencrypt.org>`_, which also
handles the renewal of the certificates when they are about to expire.

In the Ansible playbook, the Let's Encrypt configuration is defined in ``ansible/vars/default.yml`` with the following values:

.. code-block:: text

    letsencrypt_email: contact@plasmabio.org
    letsencrypt_domain: dev.plasmabio.org

If you decide to change the domain and email later, modify ``ansible/vars/default.yml`` and rerun the playbook.

How to make the domain point to the IP of the server
----------------------------------------------------

The domain used in the playbook variables (for example ``dev.plasmabio.org``), should also point to the IP of the
server running JupyterHub.

This is typically done by logging in to the registrar website and adding a new entry to the DNS records.

You can refer to the `documentation for The Littlest JupyterHub on how to enable HTTPS <http://tljh.jupyter.org/en/latest/howto/admin/https.html#enable-https>`_
for more details.