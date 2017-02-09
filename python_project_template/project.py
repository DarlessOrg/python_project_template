from __future__ import print_function
import os
import datetime

import logging
logger = logging.getLogger("app.project")

class Project(object):
  def __init__(self, test=False):
    self.package = None
    self.title = None
    self.description = None
    self.authors = []
    self.copyright = None
    self.version = "1.0"
    self.build_dir = "build"
    if test:
      self.build_dir = ".test_build"

    # Private
    self.path = None
    self.script_path = os.path.dirname(os.path.abspath(__file__))
    self.template_dir = os.path.join(self.script_path, "templates")

  def __repr__(self):
    return ("package={} title={} authors={}".format(
      self.package,
      self.title,
      self.authors))

  @property
  def authors_joined(self):
    """Retrieve the authors as a comma separated list

    :return: Authors separated by commas
    """
    return ",".join(self.authors)

  def ask_bool(self, prompt, default=None):
    """Ask the user a yes/no question

    This asks the users to type in 'y' or 'n' but to help those
    users that are used to typing yes or no this function will work
    for them too.

    :param prompt: What to ask the user
    :param default: What the default should be if the user just presses enter
    :return: If the default is True or the user says yes/y will return True.
             Otherwise False will be returned.
    """
    full_prompt = "{}? [y/n] ".format(prompt)
    if default:
      full_prompt = ("{}? [y/n] [Default: {}]: ".format(
        prompt, default))
    while True:
      val = raw_input(full_prompt).lower()
      if val in ['y', 'yes']:
        return True
      elif val in ['n', 'no']:
        return False
      elif val == '' and default is not None:
        return default
      else:
        print("Please type either 'y' or 'n' and hit Enter")

  def ask_str(self, prompt, default=None):
    """This will ask the user to provide a value

    :param prompt: The prompt to print to the user
    :param default: What the default should be if the user just presses enter
                    without any content.
    :return: The value that is returned
    """
    full_prompt = "{}: ".format(prompt)
    if default:
      full_prompt = ("{}: [Default: {}]: ".format(
        prompt, default))
    while True:
      val = raw_input(full_prompt)
      if val:
        return val
      elif default:
        return default
      else:
        print("Invalid. Must be at least 1 character")

  def ask_more(self):
    """Ask the user if there are more entries to fill in

    :return: True if there are more to fill in, False otherwise
    """
    return self.ask_bool("More entries")

  def prompt_str(self, prompt, attr, default=None):
    """Prompt a user for a value

    :param prompt: The prompt to print
    :param attr: Where to put the result
    :param default: What the default should be if the user just presses enter.
    """
    setattr(self, attr, self.ask_str(prompt, default=default))

  def prompt_multi(self, prompt, attr):
    """Prompt the user for values

    This will ask the user if there are more entries to enter

    :param prompt: The prompt to show to the user
    :param attr: Where to put the result
    """
    obj = getattr(self, attr)
    while True:
      data = self.ask_str(prompt)
      # If there is a comma in the data then do not ask for
      # more data
      if ',' in data:
        obj.extend(data.split(','))
        break
      obj.append(data)
      if not self.ask_more():
        break

  def _generate_copyright(self):
    """Generate the copyright value"""
    year = datetime.datetime.now().strftime("%Y")
    self.copyright = "{}, {}".format(
      year, self.authors_joined)

  def _process_settings(self):
    """Process any settings that are not set"""
    if not self.copyright:
      self._generate_copyright
    if not self.description:
      self.description = "Fill in description"
    if not self.title:
      self.title = self.package

  def wizard(self):
    """This will ask the user what the values should be for the project

    :return: True on success, False otherwise
    """
    self.prompt_str("Project Title", "title")
    self.prompt_str("Project package name", "package")
    self.prompt_multi("Authors", "authors")
    self.prompt_str("Brief Description", "description")
    self._generate_copyright()
    self.prompt_str("Copyright", "copyright", default=self.copyright)
    return self.generate()

  def _setup_dir(self):
    """Create the directory for the project"""
    if not os.path.exists(self.build_dir):
      os.mkdir(self.build_dir)

    self.path = "{}/{}".format(self.build_dir, self.package)
    if os.path.exists(self.path):
      logger.error("{} already exists. Please remove it first".format(
        self.path))
      return False
    os.mkdir(self.path)
    logger.info("Directory: {}".format(self.path))
    return True

  def template_data(self):
    """Return the template dictionary

    :return: The dictionary with settings used for the template files
    """
    settings = {
      'package': self.package,
      'title': self.title,
      'author': self.authors_joined,
      'description': self.description,
      'copyright': self.copyright,
      'version': self.version,
    }
    return settings

  def write_template(self, template_path, dest_path):
    """Write the template to the destination

    :param template_path: Location of the template file
    :param dest_path: Where to write the output of the template
    :return: True on success, False otherwise
    """
    if not os.path.exists(template_path):
      logger.error("Failed to process template {}. Does not exist".format(
        template_path))
      return False
    dest_dir = os.path.dirname(dest_path)
    if not dest_dir:
      logger.error("Failed to get base directory of {}".format(dest_path))
      return False
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir)

    content = None
    with open(template_path, 'r') as fp:
      content = fp.read()
    if not content:
      logger.error("Template {} has no content".format(template_path))
      return False
    with open(dest_path, 'w') as fp:
      fp.write(content.format(**self.template_data()))
    return True

  def process_template(self, f_name):
    """Process a template file

    :param f_name: The name of the template file
    :return: True on success, False otherwise
    """
    template_path = os.path.join(self.template_dir, f_name)
    dest_path = os.path.join(self.path, f_name)
    return self.write_template(template_path, dest_path)

  def process_template_dir(self, d_name, dest=None):
    """Process a template directory

    :param d_name: The directory in the main template directory
    :param dest: If passed in this will write to a directory named dest
    :return: True on success, False otherwise
    """
    template_start = os.path.join(self.template_dir, d_name)
    dest_start = os.path.join(self.path, d_name)
    success = True
    if dest:
      dest_start = os.path.join(self.path, dest)
    for root, dirs, files in os.walk(template_start):
      for name in files:
        unique = os.path.join(root[len(template_start) + 1:], name)
        tmp_path = os.path.join(template_start, unique)
        dst_path = os.path.join(dest_start, unique)
        if not self.write_template(tmp_path, dst_path):
          success = False
    return success

  def generate(self):
    """Based on the project settings generate the project"""
    self._process_settings()
    if not self._setup_dir():
      return False

    # Create package directory
    os.mkdir(os.path.join(self.path, self.package))
    self.process_template("requirements.txt")
    self.process_template("setup.py")
    self.process_template("Makefile")
    self.process_template(".gitignore")

    # Documentation - Sphinx
    self.process_template_dir("sphinx", dest="docs")

    # Tests
    self.process_template_dir("tests")
