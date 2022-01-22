import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.base_url = "https://wallhaven.cc"
        path, args = urllib.parse.splitquery(self.path)
        self._response(self.path, args)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        args = self.rfile.read(int(self.headers['content-length'])).decode("utf-8")
        self._response(self.path, args)

    def _response(self, path, args):
        if args:
            args = urllib.parse.parse_qs(args).items()
            args = dict([(k, v[0]) for k, v in args])
        else:
            args = {}
        print(path, args)
        try:
            if path.startswith("/wallhaven"):
                url = f"{self.base_url}{path[len('/wallhaven'):]}"
                print(url)
                response = requests.get(url)
                self.send_response(response.status_code)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(response.text.encode())
            if path.startswith("/local/img"):
                file_path = args['path']
                content = open(file_path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(content.read())
                content.close()
        except Exception as e:
            print(e)
            if not isinstance(e, ConnectionAbortedError):
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(str(e).encode())



def start_http():
    httpd = HTTPServer(('127.0.0.1', 1746), HttpHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    server = Thread(target=start_http, args=[])
    server.start()
    print("xxx")
