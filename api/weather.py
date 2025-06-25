import os
import json
import requests

def handler(request):
    city = request.query.get("city")
    if not city:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "City not provided"})
        }

    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "API key not set"})
        }

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(weather_info)
    }
