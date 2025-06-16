from setuptools import setup, find_packages

setup(
    name="tljh-plasma",
    version="0.1.0",
    entry_points={"tljh": ["tljh_plasma = tljh_plasma"]},
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dockerspawner>=14,<15", "tljh_repo2docker>=3.0.0a0,<4", "sqlalchemy>=2"],
)
