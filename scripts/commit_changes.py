import sys
import subprocess


def get_current_branch() -> str:
  result = subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    capture_output=True,
    text=True,
    check=True,
  )
  return result.stdout.strip()

def commit_and_push_changes(commit_message: str):
  try:
    current_branch = get_current_branch()
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push", "origin", current_branch], check=True)
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Error: Commit message required.")
    sys.exit(1)

  commit_message = sys.argv[1]
  commit_and_push_changes(commit_message)
