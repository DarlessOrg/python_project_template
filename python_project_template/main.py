#!/usr/bin/python

"""Create python projects"""

from __future__ import print_function
import os, sys, argparse, textwrap

import utils
import project
utils.setup_logging()

import logging
logger = logging.getLogger("app.main")

__author__ = "Nodar Nutsubidze"

if __name__ == "__main__":
  def add_sp(sub_p, action, func=None, help=None):
    """Add an action to the main parser

    :param sub_p: The sub parser
    :param action: The action name
    :param func: The function to perform for this action
    :param help: The help to show for this action
    :rtype: The parser that is generated
    """
    p = sub_p.add_parser(action, help=help)
    if func:
      p.set_defaults(func=func)
    p.add_argument('-v', '--verbose', action='store_true',
             help='Show verbose logging')
    return p

  def ap_wizard(args):
    """Create a project using the project wizard

    :param args: The command line arguments
    """
    proj = project.Project()
    proj.wizard()

  def ap_gen(args):
    """Create a project based on the command line arguments

    :param args: The command line arguments
    """
    proj = project.Project()
    proj.package = args.package
    proj.title = args.title
    proj.description = args.description
    proj.generate()

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description = 'Create python projects',
    epilog = textwrap.dedent('''\
      Examples:
      -----------------------
      {prg} wizard
      {prg} generate --name 'my_project' \
                     --author user1@company.com
    '''.format(prg=sys.argv[0])))
  sub_p = parser.add_subparsers(title='Actions',
    help='%(prog)s <action> -h for more info')
  p_wizard = add_sp(sub_p, "wizard", func=ap_wizard,
    help="Fill in the project details via a wizard")

  p_gen = add_sp(sub_p, "generate", func=ap_gen,
    help="Generate a project based on arguments")
  p_gen.add_argument("package",
    help="The name of the project package")
  p_gen.add_argument("--title",
    help="The title of the project")
  p_gen.add_argument("-d", "--description",
    help="Short description of the project")

  args = parser.parse_args()
  if args.verbose:
    utils.setup_logging('DEBUG')

  args.func(args)
