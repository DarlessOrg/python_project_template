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
