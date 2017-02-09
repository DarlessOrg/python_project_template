import pytest
from context import python_project_template

def _raw_input(values):
  """Process the raw_input function call

  Store away the first item in the list.
  If there are more items then update the raw_input function to
  call this function with 1 less item.
  If there are no more items then have the raw_input return with an
  empty string.
  """
  cur = None
  items = values
  if type(items) is not list:
    if not values:
      items = []
    else:
      items = [values]
  if items:
    cur = items[0]
    del items[0]
  if items:
    python_project_template.project.raw_input = lambda _: _raw_input(items)
  else:
    python_project_template.project.raw_input = lambda _: ""
  if cur:
    return cur
  return ""

def _raw_input_set(values=None):
  """Change the raw_input function

  When raw_input is called it will override the function
  to instead return items from the values list.
  """
  python_project_template.project.raw_input = lambda _: _raw_input(values)

def test_project_init():
  """Test that a Project can be added"""
  proj = python_project_template.project.Project()
  print(proj)
  assert proj.package is None
  assert proj.authors_joined == ""

  # Set the package
  proj.package = "test"
  proj._process_settings()
  assert proj.description == "Fill in description"
  assert proj.title == proj.package

def test_project_ask_bool():
  """Test asking the user for a yes/no"""
  proj = python_project_template.project.Project()
  for val in ['y', 'yes']:
    _raw_input_set(val)
    assert proj.ask_bool("This is a test")

  for val in ['n', 'no']:
    _raw_input_set(val)
    assert not proj.ask_bool("This is a test")

  _raw_input_set()
  assert proj.ask_bool("This is a test", default=True)
  assert not proj.ask_bool("This is a test", default=False)

  # Test the loop
  _raw_input_set(["", "yes"])
  assert proj.ask_bool("This is a test")
  _raw_input_set(["", "no"])
  assert not proj.ask_bool("This is a test")

def test_project_ask_str():
  """Test asking for a string"""
  proj = python_project_template.project.Project()

  _raw_input_set(["test"])
  assert proj.ask_str("This is a test") == "test"

  _raw_input_set(["test"])
  assert proj.ask_str("This is a test", default="Jim") == "test"

  _raw_input_set()
  assert proj.ask_str("This is a test", default="Jim") == "Jim"

  _raw_input_set(["", "new"])
  assert proj.ask_str("This is a test") == "new"

def test_project_ask_more():
  """Test asking if there are more entries"""
  proj = python_project_template.project.Project()

  _raw_input_set(["yes", "y"])
  assert proj.ask_more()
  assert proj.ask_more()

  _raw_input_set(["no", "n"])
  assert not proj.ask_more()
  assert not proj.ask_more()

def test_project_prompt_str():
  """Test retrieving and setting of a string in the project"""
  proj = python_project_template.project.Project()

  _raw_input_set("answer")
  proj.prompt_str("Give me Jim", "jim")
  assert proj.jim == "answer"

  _raw_input_set()
  proj.prompt_str("Give me Jim", "jim", default="BOB")
  assert proj.jim == "BOB"

def test_project_prompt_multi():
  """Test multi prompts"""

  # With content with commas should not ask for additonal input
  _raw_input_set("one,two,three")
  proj = python_project_template.project.Project()
  proj.prompt_multi("Give me multi", "authors")
  assert proj.authors == ["one", "two", "three"]

  # Should ask for additional entries without a comma in the content
  _raw_input_set(["one", "y", "two", "n", "three"])
  proj = python_project_template.project.Project()
  proj.prompt_multi("Give me multi", "authors")
  assert proj.authors == ["one", "two"]

def test_project_copyright():
  """Test copyright of a project"""
  proj = python_project_template.project.Project()
  proj.authors = ["one", "two"]
  proj._generate_copyright()
  assert "one,two" in proj.copyright

def test_project_wizard():
  """Test project wizard support"""
  python_project_template.utils.setup_logging()
  proj = python_project_template.project.Project(test=True)
  _raw_input_set([
    # Title
    "My Title",
    # Package
    "my_title",
    # Authors
    "Author1",
    "yes",
    "Author2",
    "no",
    # Description
    "a description",
    "",
  ])
  proj.wizard()
  assert proj.title == "My Title"
  assert proj.package == "my_title"
  assert proj.authors_joined == "Author1,Author2"
  assert proj.description == "a description"
  proj.generate()

  # Attempt to write a template path which does not exist
  assert not proj.write_template("/does/not/exist", "/somewhere")
  assert not proj.write_template("Makefile", "somewhere")

  # Create an empty tmp file
  with open("/tmp/.python_template_empty.txt", "w"):
    pass
  assert not proj.write_template("/tmp/.python_template_empty.txt", "/dev/null")

  # Attempt to process a template directory
  proj.template_dir = "tests/test_templates"
  assert not proj.process_template_dir("test_dir")
