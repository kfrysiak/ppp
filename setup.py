from setuptools import setup, find_packages

setup(
    name="ppp-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "toml",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "ppp=ppp.cli:main",
        ],
    },
    author="Your Name",
    description="A CLI tool to run scripts/aliases from pyproject.toml",
)
