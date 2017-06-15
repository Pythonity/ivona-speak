# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import io
import os
import re

from setuptools import setup, find_packages


# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst', 'markdown')
except (OSError, ImportError):
    description = ''


# Get package version number
# Source: https://packaging.python.org/single_source_version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='ivona_speak',
    url='https://github.com/Pythonity/ivona-speak',
    download_url='https://github.com/Pythonity/ivona-speak/releases/latest',
    bugtrack_url='https://github.com/Pythonity/ivona-speak/issues',
    version=find_version('ivona_speak', '__init__.py'),
    license='MIT License',
    author='Pythonity',
    author_email='pythonity@pythonity.com',
    maintainer='Paweł Adamczak',
    maintainer_email='pawel.adamczak@sidnet.info',
    description="Python script that lets you easily convert text to "
                "synthesized audio files, with help of Amazon's IVONA.",
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=6.7',
        'click-default-group>=1.2',
        'ivona_api>=0.3.0',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    scripts=['bin/ivona-speak'],
    keywords='amazon ivona text to speech synthesize',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
