from setuptools import setup, find_packages

setup(
    name="tljh-plasma",
    version="0.1.0",
    entry_points={"tljh": ["tljh_plasma = tljh_plasma"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dockerspawner~=12.1", "tljh_repo2docker", "jupyterhub~=1.4.2", "sqlalchemy<2"],
)
