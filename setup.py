from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='pyicloud',
    version='0.2',
    url='https://github.com/picklepete/pyicloud',
    description=(
        'PyiCloud is a module which allows pythonistas to '
        'interact with iCloud webservices.'
    ),
    author='Peter Evans',
    author_email='evans.peter@gmail.com',
    packages=find_packages(),
    install_requires=required
)
