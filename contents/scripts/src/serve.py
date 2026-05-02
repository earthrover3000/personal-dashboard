import http.server
import os
import socketserver
import sys
import webbrowser
from urllib.parse import quote

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
SERVE_ROOT = os.path.abspath(os.path.join(REPO_ROOT, '..', '..'))
PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_ROOT, **kwargs)


def main():
    rel = os.path.relpath(REPO_ROOT, SERVE_ROOT).replace(os.sep, '/')
    base = f"http://localhost:{PORT}/{quote(rel)}/"
    dashboard_url = base
    spec_url = base + "contents/docs/dashboard.html"

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
