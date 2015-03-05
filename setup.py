#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="ig2lj",
      version="0.1.0",
      description="Instagram to LiveJournal translator",
      license="MIT",
      install_requires=["python-instagram","lj","Jinja2"],
      author="Eric Avdey",
      author_email="eiri@eiri.ca",
      url="http://github.com/eiri/ig2lj",
      packages = find_packages(),
      keywords= ["instagram","livejournal"],
      zip_safe = True)