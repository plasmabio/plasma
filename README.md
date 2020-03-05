# plasmabio

Configuration files to setup and deploy Plasma Bio on a single machine.

## Requirements

- Ubuntu 18.04
- Docker CE
- `docker-compose`

## Run locally

```bash
docker-compose build
docker-compose up
```

Open http://localhost:8000 in a web browser and use the host users to authenticate.

To tear down:

```bash
docker-compose down
```

## Deploy

First make sure [Ansible](https://docs.ansible.com/ansible/latest/index.html) is installed:

```bash
python -m pip install ansible
```

Then run:

```bash
ansible-playbook -i <ip>, ansible/docker.yaml -u <user>
```

As an example:

```bash
ansible-playbook -i 51.178.95.237, ansible/docker.yml -u ubuntu
```