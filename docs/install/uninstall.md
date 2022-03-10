# Uninstalling

If you want to uninstall The Littlest JupyterHub from the machine, you can:

- Destroy the VM: this is the recommended way as it is easier to start fresh
- Run the `uninstall.yml` Ansible playbook if destroying the VM is not an option

To run the playbook:

```bash
ansible-playbook uninstall.yml -i hosts -u ubuntu
```

```{note}
The playbook will **only** uninstall TLJH from the server.

It will **not**:

- delete user data
- remove environments and Docker images
```
