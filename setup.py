#!/usr/bin/env python
"""pyiCloud setup."""

from setuptools import setup, find_packages

REPO_URL = "https://github.com/picklepete/pyicloud"
VERSION = "1.0.0"

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyicloud",
    version=VERSION,
    url=REPO_URL,
    download_url=REPO_URL + "/tarball/" + VERSION,
    description="PyiCloud is a module which allows pythonistas to interact with iCloud webservices.",
    long_description=long_description,
    maintainer="The PyiCloud Authors",
    packages=find_packages(include=["pyicloud*"]),
    install_requires=required,
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={"console_scripts": ["icloud = pyicloud.cmdline:main"]},
    keywords=["icloud", "find-my-iphone"],
)
