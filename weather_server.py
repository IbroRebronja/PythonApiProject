from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._serve_form()
        elif self.path.startswith("/weather?"):
            self._handle_weather_request()
        else:
            self.send_error(404, "Page not found")

    def _serve_form(self):
        with open("templates/form.html", "r", encoding="utf-8") as file:
            content = file.read()
        self._respond_html(200, content)

    def _handle_weather_request(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        city = params.get("city", [""])[0]

        if not city:
            self._respond_html(400, "<h2>City is required.</h2>")
            return

        api_key = "2ec8c559173d16db4b8bc1687ad46f96"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception("City not found")

            data = response.json()

            html = f"""
                <html><head><title>Weather Result</title></head><body>
                <h2>{data['name']}, {data['sys']['country']}</h2>
                <p>Temperature: {data['main']['temp']}°C</p>
                <p>Weather: {data['weather'][0]['description']}</p>
                <p>Humidity: {data['main']['humidity']}%</p>
                <p>Wind Speed: {data['wind']['speed']} m/s</p>
                <br><a href="/">Search another city</a>
                </body></html>
            """

            self._respond_html(200, html)
        except Exception as e:
            self._respond_html(400, f"<h2>Error: {str(e)}</h2><br><a href='/'>Try again</a>")

    def _respond_html(self, status_code, content):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

def run():
    server = HTTPServer(('', 8000), WeatherHandler)
    print("Server running at http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run()
