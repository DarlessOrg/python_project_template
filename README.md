[![Build Status](https://travis-ci.org/Darless/python_project_template.svg?branch=master)](https://travis-ci.org/Darless/python_project_template)
[![Coverage Status](https://coveralls.io/repos/github/Darless/python_project_template/badge.svg)](https://coveralls.io/github/Darless/python_project_template)
[![Docker Automated build](https://img.shields.io/docker/automated/madrussian/python_project_template.svg)](https://hub.docker.com/r/madrussian/python_project_template/)

TL;DR
=====

1. Clone
2. make
3. ./python_project_template.py wizard
4. Copy build/<name> to your project workspace
5. Happy Coding

Overview
========

Create python projects based on the [Python Structure Guide](http://docs.python-guide.org/en/latest/writing/structure/).
The associated [GitHub](https://github.com/kennethreitz/samplemod) with a simple module is located here.
In the basic sense this generates a module for you based on your requirements.

The project can be generated via 2 different methods, one is via a wizard and the other via command line arguments.
For either one the following components will be setup:

* [Sphinx](http://www.sphinx-doc.org/en/1.5.1/) with a configuration file setup for you based on the project settings
* [pytest](http://doc.pytest.org/en/latest/) in the tests directory with a couple of files to get you started.
