import sys
import subprocess
import re
import toml

def get_latest_release() -> str:
  try:
    latest_tag = subprocess.check_output([
      "git", "describe", "--tags", "--abbrev=0"
    ]).strip().decode("utf-8")
    return latest_tag
  except subprocess.CalledProcessError:
    print("Error: Could not get the latest Git tag.")
    return None

def update_version_in_init(version):
  init_file = "modlink/__init__.py"
  with open(init_file, "r") as file:
    content = file.read()

  new_content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', content)
  
  with open(init_file, "w") as file:
    file.write(new_content)

def update_pyproject(version: str):
  with open('pyproject.toml', 'r') as f:
    config = toml.load(f)

  config['tool']['poetry']['version'] = version
  
  with open('pyproject.toml', 'w') as f:
    toml.dump(config, f)

if __name__ == '__main__':
  latest_release = get_latest_release()
  if latest_release is None:
    sys.exit(1)

  version = latest_release.split('-')[0]
  update_pyproject(version)
  print(f"Updated pyproject.toml to version {version}")


