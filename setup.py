from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='pyicloud',
    version='0.9.6.1',
    url='https://github.com/picklepete/pyicloud',
    description=(
        'PyiCloud is a module which allows pythonistas to '
        'interact with iCloud webservices.'
    ),
    maintainer='The PyiCloud Authors',
    maintainer_email=' ',
    license='MIT',
    packages=find_packages(include=["pyicloud*"]),
    install_requires=required,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'icloud = pyicloud.cmdline:main'
        ]
    },
)
