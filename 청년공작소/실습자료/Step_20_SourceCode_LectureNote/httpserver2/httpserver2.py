# Name: httpserver2.py
# Client: http://localhost:8096

from http.server import HTTPServer, SimpleHTTPRequestHandler

class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()
        print("do_get")
        
port = 8096
httpd = HTTPServer(('', port), testHTTPServer_RequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()