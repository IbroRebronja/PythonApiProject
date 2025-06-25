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
            self._respond_json(400, {"error": "City is required"})
            return

        api_key = "2ec8c559173d16db4b8bc1687ad46f96"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception("City not found")
            self._respond_json(200, response.json())
        except Exception as e:
            self._respond_json(400, {"error": str(e)})

    def _respond_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run():
    server = HTTPServer(('', 8000), WeatherHandler)
    print("Weather API running at http://localhost:8000/api/weather")
    server.serve_forever()

if __name__ == "__main__":
    run()
