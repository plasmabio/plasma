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