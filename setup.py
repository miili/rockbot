#!/usr/bin/env python3
from setuptools import setup

setup(
    name='rockbot',
    version='0.0.1',
    description='Pyrocko\'s devote Mattermost Bot',
    author='Marius Isken',
    author_email='info@pyrocko.org',
    url='https://github.com/pyrocko/rockbot',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=['mattermostdriver'],
    package_dir={
        'rockbot': 'src'
    },
    packages=[
        'rockbot',
        'rockbot.handlers'
    ],
    entry_points={
        'console_scripts': [
            'rockbot = rockbot.main:main',
    ]},
)
