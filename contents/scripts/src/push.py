import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_git_user(cwd):
    email = subprocess.run(
        ['git', 'config', 'user.email'],
        cwd=cwd, capture_output=True, text=True
    ).stdout.strip()
    if not email:
        run(['git', 'config', 'user.email', '140817883+earthrover3000@users.noreply.github.com'], cwd)
        run(['git', 'config', 'user.name', 'earthrover3000'], cwd)


def check_not_behind(cwd):
    try:
        subprocess.run(
            ['git', 'fetch'],
            cwd=cwd, check=True, capture_output=True
        )
        local = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=cwd, capture_output=True, text=True, check=True
        ).stdout.strip()
        remote = subprocess.run(
            ['git', 'rev-parse', 'origin/main'],
            cwd=cwd, capture_output=True, text=True, check=True
        ).stdout.strip()
        behind = int(subprocess.run(
            ['git', 'rev-list', '--count', f'{local}..{remote}'],
            cwd=cwd, capture_output=True, text=True, check=True
        ).stdout.strip())
    except Exception:
        return

    if behind == 0:
        return

    print(f"WARNING: Repo is {behind} commit(s) behind origin/main.")
    print("MEGA may have synced changes from another machine that you haven't seen.")
    answer = input("Push anyway? [y/N] ").strip().lower()
    if answer != 'y':
        print("Aborted.")
        raise SystemExit(0)


def main():
    msg = ' '.join(sys.argv[1:]).strip() or 'update dashboard'

    print(f"Pushing from: {REPO_ROOT}")
    print(f"Commit message: {msg}")
    print()
    check_not_behind(REPO_ROOT)
    ensure_git_user(REPO_ROOT)

    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    if status:
        run(['git', 'add', '.'], REPO_ROOT)
        run(['git', 'commit', '-m', msg], REPO_ROOT)
    else:
        print("No working tree changes; pushing any unpushed commits.")

    run(['git', 'push', 'origin', 'main'], REPO_ROOT)
    print()
    print("Done! Live URL (1-2 min after push):")
    print("https://earthrover3000.github.io/personal-dashboard/")
    input("Press Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to continue...")
