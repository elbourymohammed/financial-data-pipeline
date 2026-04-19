from setuptools import setup, find_packages

setup(
    name="data_project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
