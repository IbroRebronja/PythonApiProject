import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path != '/api/weather':
            self.send_error(404, "Endpoint not found")
            return

        query_params = urllib.parse.parse_qs(parsed_path.query)
        city = query_params.get("city", [None])[0]

        if not city:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "City is required"}).encode())
            return

        api_key = "2ec8c559173d16db4b8bc1687ad46f96"
        if not api_key:
            self.send_error(500, "API key not set")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception("City not found")
            data = response.json()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run(server_class=HTTPServer, handler_class=WeatherHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Weather API server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
