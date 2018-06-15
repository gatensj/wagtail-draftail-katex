#!/usr/bin/env python
"""
Replace the values in setup to correspond to your own plugin information.
Information entered here will be used for your PyPi package page and the package build.
"""

with open ("readme.md", "r") as fp:
      long_description = fp.read()

from setuptools import setup, find_packages

setup(name='wagtail-katek-plugin',
      version='1.0.0',
      description='This will be an integration of a KaTek into the Wagtail CMS Draftail editor.',
      long_description=long_description,
      long_description_content_type = "text/markdown",
      url='https://github.com/gatensj/wagtail-draftail-katex',
      author='Jeremy Gatens',
      author_email='jeremygatens@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'wagtail>=2.0',
      ],
      classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ),
)
