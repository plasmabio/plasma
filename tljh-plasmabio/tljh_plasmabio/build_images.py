import logging
import sys
import subprocess

logging.basicConfig(level=logging.INFO)


# list of images to choose from when spawning a new server
# TODO: make this dynamic and easier to edit
IMAGES = {
    "python-template-test": "https://github.com/plasmabio/template-python",
    "python-requirements": "https://github.com/binder-examples/requirements",
}


def build_image(name, repo):
    ref = "master"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "repo2docker",
            "--ref",
            ref,
            "--user-name",
            "jovyan",
            "--user-id",
            "1100",
            "--no-run",
            "--image-name",
            f"{name}:latest",
            repo,
        ]
    )


def main():
    for name, repo in IMAGES.items():
        logging.info(f"Building image {name}")
        build_image(name, repo)


if __name__ == "__main__":
    main()
