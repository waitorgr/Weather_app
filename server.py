from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city=request.args.get('city')

    #check for empty strings or only spc string
    if not bool(city.strip()):
        city = "Legnica"

    weateger_data = get_current_weather(city)

    #City is not found by APY
    if not weateger_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weateger_data["name"],
        status=weateger_data["weather"][0]["description"].capitalize(),
        temp=f"{weateger_data['main']['temp']:.2f}",
        feels_like=f"{weateger_data['main']['feels_like']:.2f}"
    )

if __name__ == '__main__':
    serve(app,host="0.0.0.0", port=8000)