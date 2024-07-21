import sys
import subprocess

def commit_and_push_changes(commit_message: str):
  try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)
  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Error: Commit message required.")
    sys.exit(1)

  commit_message = sys.argv[1]
  commit_and_push_changes(commit_message)
