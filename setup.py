from setuptools import setup, find_packages

setup(
    name="ppp-run",
    version="0.2",
    packages=find_packages(),
    install_requires=["toml", "rich"],
    entry_points={
        "console_scripts": [
            "ppp=ppp.cli:main",
        ],
    },
    author="Konrad Frysiak",
    description="A CLI tool to run scripts/aliases from pyproject.toml",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
)
