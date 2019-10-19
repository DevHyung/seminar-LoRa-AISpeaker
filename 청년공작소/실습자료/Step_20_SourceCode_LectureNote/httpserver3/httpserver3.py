# Name: httpserver3.py
# Client: http://localhost:9095

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        url = self.path
        form = parse_qs(urlparse(url).query)
        print("**", url, "**")
        if (form != {}):
            self.process_form(form)
        super().do_GET()
        print("do_get")

    def process_form(self,form):
        if 'food' in form:
            if form['food'][0] == 'Pizza':
                print(form['firstname'][0] + ", call Dominos tonight!")
            elif form['food'][0] == 'Tacos':
                print(form['firstname'][0] + ", go to TacoBell tonight!")
            elif form['food'][0] == 'Salad':
                print(form['firstname'][0] + ", have a Caesar Salad tonight!")

port = 9095 
httpd = HTTPServer(('', port), testHTTPServer_RequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()