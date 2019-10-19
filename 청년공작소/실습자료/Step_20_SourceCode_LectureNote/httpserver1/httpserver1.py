from http.server import SimpleHTTPRequestHandler, HTTPServer

port = 8090
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()
