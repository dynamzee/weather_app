import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("MY_WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    weather = {
                        "temp_f": round((data["main"]["temp"] * 9 / 5) - 459.67, 0),
                        "description": data["weather"][0]["description"].title(),
                        "emoji": get_weather_emoji(data["weather"][0]["id"])
                    }
                else:
                    match response.status_code:
                        case 400:
                            error = "Bad Request:<br>Please check your city name."
                        case 401:
                            error = "Unauthorized:<br>Invalid API key."
                        case 403:
                            error = "Forbidden:<br>Access is denied."
                        case 404:
                            error = "Not found:<br>City not found."
                        case 500:
                            error = "Internal Server:<br>Internal Server Error."
                        case 502:
                            error = "Bad Gateway:<br>Bad Gateway."
                        case 503:
                            error = "Service Unavailable:<br>Service Unavailable."
                        case 504:
                            error = "Gateway Timeout:<br>Gateway Timeout."
                        case _:
                            error = f"HTTP error occurred: {response.status_code}"

            except requests.exceptions.ConnectionError:
                error = "Connection error:<br>Please check your internet connection."
            except requests.exceptions.Timeout:
                error = "Timeout error:<br>Please try again, the request timed out."
            except requests.exceptions.TooManyRedirects:
                error = "Too many Redirects:<br>Check the url."
            except requests.exceptions.RequestException as req_error:
                error = f"Request Error:<br>{req_error}."

    return render_template("index.html", weather=weather, error=error)

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌨️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "☃️❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "☁️"
    else:
        return " "

if __name__ == "__main__":
    app.run(debug=True)









