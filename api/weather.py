import requests

def handler(request):
    city = request.query.get("city")
    if not city:
        return {"statusCode": 400, "body": "City not provided"}

    api_key = "2ec8c559173d16db4b8bc1687ad46f96"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    res = requests.get(url)
    if res.status_code != 200:
        return {"statusCode": res.status_code, "body": res.text}

    data = res.json()
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }

    return {"statusCode": 200, "body": weather_info}
