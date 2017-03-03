from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
from sqlConnector import sqlconnector
from trainer import init


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        msg = query_components["msg"]
        name = sqlconnector(msg)
        self.wfile.write("received message : " + msg + " : " + name + "\n")


    def do_HEAD(self):
        self._set_headers()


def run():
    # server_address = ('', 8080)
    # httpd = HTTPServer(server_address, S)
    # print 'Starting http...'
    # httpd.serve_forever()
    init()


if __name__ == "__main__":
    run()