# -*- coding: utf-8 -*-
"""
Shared resources for Directory Tests
"""
from setuptools import setup, find_packages


setup(
    name="directory_tests_shared",
    version="1.0",
    url="https://github.com/uktrade/directory-tests",
    license="MIT",
    author="Department for International Trade",
    description="Shared resources for Directory Tests",
    packages=find_packages(exclude=["tests.*", "tests"]),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "envparse>=0.2.0",
    ],
    extras_require={},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
