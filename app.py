from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "2ec8c559173d16db4b8bc1687ad46f96"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = {}
    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        
        if res.get("cod") == 200:
            weather = {
                "city": res["name"],
                "temperature": res["main"]["temp"],
                "description": res["weather"][0]["description"],
            }
        else:
            weather = {"error": "City not found or invalid request."}
    
    return render_template("index.html", weather=weather)
