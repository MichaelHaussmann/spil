#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SPIL Package configuration. """

import io
import sys

from setuptools import setup, find_packages

version = "0.0.2"

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()

setup(
    name='spil',
    version=version,
    description=(
        'The Simple Pipeline Lib. A simple library for CG Pipelines, built around the "Sid", or "Scene Identifier".'
    ),
    long_description=readme,
    # long_description_content_type='text/markdown',
    author='Michael Haussmann',
    author_email='spil@xeo.info',
    url='https://github.com/MichaelHaussmann/spil',
    # packages=['spil'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.4.*',
    license='LGPL',
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords=(
        'vfx', 'cg', 'vfx-pipeline', 'cg-pipeline', 'path templates'

    ),
    install_requires=[  # 'lucidity' for python 3 is shipped as vendor lib, not required.
        'six',
        'logzero',
    ],
    extras_require={
        ':python_version<"3.0"': ['pathlib2', 'lucidity']
    },
    tests_require=[
        'pytest',
    ],

)