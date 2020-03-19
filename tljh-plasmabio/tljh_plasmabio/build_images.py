import logging
import sys
import subprocess

import docker

logging.basicConfig(level=logging.INFO)


# list of images to choose from when spawning a new server
# TODO: make this dynamic and easier to edit
IMAGES = {
    "materials-example": "https://github.com/plasmabio/materials-example",
    "python": "https://github.com/binder-examples/requirements",
    "jupyter/scipy-notebook": "https://github.com/binder-examples/requirements",
}


def build_image(name, repo):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "repo2docker",
            "--ref",
            "master",
            "--user-name",
            "jovyan",
            "--user-id",
            "1000",
            "--no-run",
            "--image-name",
            name,
            repo,
        ]
    )


def main():
    # prune stopped containers and dangling images
    client = docker.from_env()
    client.containers.prune()
    client.images.prune()

    for name, repo in IMAGES.items():
        logging.info(f"Building image {name}")
        build_image(name, repo)


if __name__ == "__main__":
    main()
