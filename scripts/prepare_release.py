import sys
import subprocess
import re
import toml
from packaging.version import Version, InvalidVersion


def to_version(name: str) -> Version:
  try:
    if name.startswith("v"):
      name = name[1:]
    return Version(name)
  except InvalidVersion:
    print(f"Error: Tagged version '{name}' does not conform to pep-0440.")
    sys.exit(1)


def get_latest_tag() -> str:
  try:
    return subprocess.check_output([
      "git", "describe", "--tags", "--abbrev=0"
    ]).strip().decode("utf-8").strip()
  except subprocess.CalledProcessError:
    print("Error: Could not get the latest Git tag.")
    sys.exit(1)


def update_package(version: str) -> None:
  init_file = "modlink/__init__.py"
  with open(init_file, "r") as file:
    content = file.read()

  new_content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', content)

  with open(init_file, "w") as file:
    file.write(new_content)
  print(f"Updated {init_file} __version__ = \"{version}\"")


def update_pyproject(version: str):
  with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

  config['tool']['poetry']['version'] = version

  with open('pyproject.toml', 'w') as f:
    toml.dump(config, f)
  print(f"Updated pyproject.toml version = \"{version_str}\"")


def print_version_output(version: Version):
  def set_output(name: str, value: str):
    print(f"::set-output name={name}::{value}")
  set_output("release", "true")
  set_output("version", str(version))
  if version.is_prerelease:
    set_output("prerelease", "true")
  else:
    set_output("prerelease", "false")


if __name__ == '__main__':
  # check if release is coming from argument
  if len(sys.argv) > 3:
    print(f"Error: Only one argument is allowed. {sys.argv[1:]}")
    sys.exit(1)

  if len(sys.argv) == 2:
    version = to_version(sys.argv[1])
  else:
    version = to_version(get_latest_tag())

  print(f"Latest release: {version}")
  version_str = str(version)
  update_package(version_str)
  update_pyproject(version_str)

  print_version_output(version)

  print("Prepared for release.")
