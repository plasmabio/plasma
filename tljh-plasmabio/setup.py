from setuptools import setup, find_packages

setup(
    name="tljh-plasmabio",
    version="0.0.1",
    entry_points={"tljh": ["tljh_plasmabio = tljh_plasmabio"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dockerspawner"],
)
