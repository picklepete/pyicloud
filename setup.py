from setuptools import setup, find_packages
from codecs import open

REPO_URL = "https://github.com/picklepete/pyicloud"
VERSION = "0.10.1"

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
    maintainer_email=" ",
    packages=find_packages(include=["pyicloud*"]),
    install_requires=required,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["icloud = pyicloud.cmdline:main"]},
    keywords=["icloud", "find-my-iphone"],
)
