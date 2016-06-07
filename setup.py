# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''


setup(
    name='ivona_speak',
    url='https://github.com/Pythonity/ivona-speak',
    download_url='https://github.com/Pythonity/ivona-speak/releases/latest',
    bugtrack_url='https://github.com/Pythonity/ivona-speak/issues',
    version='0.1.0',
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
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[
        'ivona_api>=0.1.1',
        'click>=6.6',
        'click-default-group>=1.2',
        'PyYAML>=3.11',
    ],
    extras_require={
        'testing': ['pytest', 'flaky'],
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
)
