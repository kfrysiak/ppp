from setuptools import setup, find_packages

setup(
    name="ppp-run",
    version="0.1",
    packages=find_packages(),
    install_requires=["toml", "rich"],
    entry_points={
        "console_scripts": [
            "ppp=ppp.cli:main",
        ],
    },
    author="Konrad Frysiak",
    description="A CLI tool to run scripts/aliases from pyproject.toml",
)
