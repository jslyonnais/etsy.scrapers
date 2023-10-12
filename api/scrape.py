from http.server import BaseHTTPRequestHandler
import json
from script import main

class Args:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        url = data.get('url')
        
        try:
            args = Args(url)
            csv_data = main(args)
            response = {
                'csv': csv_data,
                'filename': 'output.csv'
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        return
