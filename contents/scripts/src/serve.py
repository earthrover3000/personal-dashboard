import http.server
import os
import socketserver
import sys
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
SERVE_ROOT = os.path.abspath(os.path.join(REPO_ROOT, '..', '..'))
PORT = 8000

# Clean public route the dashboard is published at, so the URL reads
# http://localhost:8000/personal-dashboard/ instead of the long CJK project
# path. Requests under this prefix are rewritten onto the dashboard repo; every
# other path still resolves against SERVE_ROOT unchanged, so shared assets and
# the original long path keep working — this only ADDS a tidy alias.
ROUTE = '/personal-dashboard'
# URL path from SERVE_ROOT down to REPO_ROOT, i.e. what ROUTE expands to.
_REPO_REL = '/' + os.path.relpath(REPO_ROOT, SERVE_ROOT).replace(os.sep, '/')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_ROOT, **kwargs)

    def translate_path(self, path):
        # Expand the /personal-dashboard alias onto the repo under SERVE_ROOT
        # before the base class decodes/normalizes; other paths pass through.
        if path == ROUTE or path.startswith(ROUTE + '/'):
            path = _REPO_REL + path[len(ROUTE):]
        return super().translate_path(path)


def serve_url():
    return f"http://localhost:{PORT}{ROUTE}/"


def main():
    if '--print-url' in sys.argv:
        # Report the canonical URL and exit — the launcher's [o] Open asks the
        # serve script where the dashboard lives rather than hard-coding it.
        print(serve_url())
        return

    dashboard_url = serve_url()
    spec_url = dashboard_url + "contents/docs/dashboard.html"

    print(f"Serving from: {SERVE_ROOT}")
    print()
    print(f"Published dashboard: {dashboard_url}")
    print(f"Spec viewer:         {spec_url}")
    print()
    print("Opening dashboard in your browser. Ctrl-C to stop the server.")
    print()

    webbrowser.open(dashboard_url)

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    except OSError as e:
        print(f"Could not start server on port {PORT}: {e}")
        print("Edit PORT at the top of serve.py if another service is using it.")
        input("Press Enter to continue...")
        sys.exit(1)


if __name__ == '__main__':
    main()
