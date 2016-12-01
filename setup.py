#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re

from setuptools import find_packages, setup


def get_content(*fps):
    """Return content for specified file path parts.

    If the file doesn't exist, return ''.

    Arguments:
        fps (List(str)): One or more path parts to be joined with
            current directory

    Returns:
        str: Content of the specified file, otherwise ''.
    """
    fp = Path(__file__).parent.joinpath(*fps)
    content = ''
    if fp.exists():
        with fp.open() as f:
            content = f.read()
    return content


def get_requirements():
    """Return list of requirements from `requirements/app.in`.

    Returns:
        List(str)
    """
    reqs = get_content('requirements/app.in').splitlines()
    return reqs


def get_version(*file_paths):
    """Extract the version string from the file at the given path fragments.
    """
    version_file = get_content(*file_paths)
    version_match = re.search(
        r"""^__version__ = ['"]([^'"]*)['"]""", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


VERSION = get_version('interdiagram', '__init__.py')
README = get_content('README.md')
CHANGELOG = get_content('CHANGELOG.md')

setup(
    name='interdiagram',
    version=VERSION,
    description='Generate interaction diagrams',
    long_description=README + '\n\n' + CHANGELOG,
    url='https://github.com/gsong/interdiagram',
    author='George Song',
    author_email='george@damacy.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='interaction diagram sitemap',

    packages=find_packages(),
    install_requires=get_requirements(),

    entry_points={
        'console_scripts': [
            'interdiagram=interdiagram.bin.interdiagram:cli',
        ],
    },
)
