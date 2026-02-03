from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "02213a39fba9c0d3cc7e63391dd30c9e"  # your OpenWeatherMap API key

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if data["cod"] == 200:
                    weather = {
                        "temp_c": round(data["main"]["temp"] - 273.15, 1),
                        "temp_f": round((data["main"]["temp"] * 9/5) - 459.67, 1),
                        "description": data["weather"][0]["description"].title(),
                        "emoji": get_weather_emoji(data["weather"][0]["id"])
                    }
                else:
                    error = data.get("message", "Could not fetch weather data.")

            except requests.exceptions.RequestException as e:
                error = f"Error: {e}"

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