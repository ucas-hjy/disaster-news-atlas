# -*- coding: utf-8 -*-
"""
serve.py
Serve docs/ locally so the page can be tested before it is published.

Opening index.html straight from the file system does not work, because a
browser refuses fetch() on file:// addresses. Run this instead and open
http://localhost:8000.
"""
import http.server
import os
import socketserver
import webbrowser

PORT = 8000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        # Never cache during testing, so a rebuild shows up on reload.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        if '404' in (fmt % args):
            print('404', self.path)


if __name__ == '__main__':
    if not os.path.isdir(ROOT):
        raise SystemExit(f"{ROOT} does not exist. Run the two build scripts first.")
    print(f"Serving {ROOT} at http://localhost:{PORT}  (Ctrl+C to stop)")
    webbrowser.open(f'http://localhost:{PORT}')
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()