# -*- coding: utf-8 -*-
"""
Shared resources for Directory Tests
"""
from setuptools import find_packages, setup

setup(
    name="directory_tests_shared",
    version="1.1",
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
        "directory-api-client>=20.0.0",
        "directory-cms-client>=11.0.0",
        "directory-sso-api-client>=6.2.0",
        "notifications-python-client>=5.4.0",
        "parse>=1.12.1",
        "pdfminer2>=20151206",
        "retrying>=1.3.3",
        "scrapy>=1.8.0",
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
    ],
)
