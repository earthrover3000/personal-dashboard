import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# This app's root — the dashboard folder inside the 工坊 Workshop monorepo.
APP_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))


def get_remote_url():
    """Publish remote, read from site.json (the Launchpad manifest).

    The dashboard is no longer its own git repo — it's a subtree inside the
    工坊 Workshop monorepo — so the remote is taken from site.json rather than
    `git remote get-url origin`."""
    with open(os.path.join(APP_ROOT, 'site.json'), encoding='utf-8') as f:
        return json.load(f)['sync']['remote']


def monorepo_and_prefix():
    """Return (monorepo root, this app's path within it).

    We publish with `git subtree push` from the monorepo root, using this
    folder's relative path as the prefix."""
    top = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        cwd=APP_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    prefix = os.path.relpath(APP_ROOT, top).replace(os.sep, '/')
    return top, prefix


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    msg = ' '.join(sys.argv[1:]).strip() or 'update dashboard'
    top, prefix = monorepo_and_prefix()
    remote = get_remote_url()

    # 1) Commit THIS app's changes into the monorepo, scoped to its prefix so
    #    nothing from other projects is swept in. subtree push publishes the
    #    committed state, so an uncommitted edit would otherwise not go live.
    status = subprocess.run(
        ['git', 'status', '--porcelain', '--', prefix],
        cwd=top, capture_output=True, text=True, check=True
    ).stdout.strip()
    if status:
        print("Committing dashboard changes to the monorepo...")
        run(['git', 'add', '--', prefix], top)
        run(['git', 'commit', '-m', msg], top)
    else:
        print("No dashboard changes; publishing current committed state.")

    # 2) Publish just this subtree to its own GitHub repo (Pages serves it).
    print(f"subtree push  {prefix}  ->  {remote}")
    run(['git', 'subtree', 'push', '--prefix', prefix, remote, 'main'], top)

    print()
    print("Done! Live URL (1-2 min after push):")
    print("https://earthrover3000.github.io/personal-dashboard/")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
