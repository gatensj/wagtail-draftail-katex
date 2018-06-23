#!/usr/bin/env python
"""
Replace the values in setup to correspond to your own plugin information.
Information entered here will be used for your PyPi package page and the package build.
"""

from setuptools import setup, find_packages

with open("readme.md", "r") as fp:
    long_description = fp.read()

setup(name='wagtail-draftail-katex',
      version='0.1.3',
      description='Integrate KaTex render into the Wagtail CMS Draftail editor.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gatensj/wagtail-draftail-katex',
      author='Jeremy Gatens',
      author_email='jeremygatens@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'wagtail>=2.0',
      ],
      classifiers=(
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          "Operating System :: OS Independent",
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'Framework :: Django',
          'Framework :: Django :: 2.0',
          'Framework :: Wagtail',
          'Framework :: Wagtail :: 2',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ),
  )
