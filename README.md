# plasmabio

Configuration files to setup and deploy Plasma Bio on a single machine.

## Requirements

- Ubuntu 18.04+
- Docker CE

## Run Locally

TODO

## Deploy

First make sure [Ansible](https://docs.ansible.com/ansible/latest/index.html) is installed:

```bash
python -m pip install ansible
```

Go to the `ansible` directory:

```bash
cd ansible/
```

Then run:

```bash
ansible-playbook all.yaml -u <user>
```

As an example with the `ubuntu` user on the remote machine:

```bash
ansible-playbook all.yml -u ubuntu
```
