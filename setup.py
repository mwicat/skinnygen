#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="skinnygen",
    version="0.5.0",
    author="Marek Wiewiorski",
    author_email="mwicat@gmail.com",
    description=("Skinny protocol traffic generator"),
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        'sccp',
        'argh==0.24.1'
    ],
    entry_points={
        'console_scripts': [
            'skinnygen=skinnygen.main:main',
            ]
    }
)
