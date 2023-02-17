import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('weather.html')
    else:
        # city = request.form["city"]
        cities = ('London', 'Shimla', 'Delhi', 'Karachi');
        weather_data = []
        for city in cities:

            api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings['api']}"

            res = requests.get(api).json()
            
            weather = {
                "city" : city,
                "temperature" : res["main"]["temp"],
                "description": res["weather"][0]["description"],
                "icon" : res["weather"][0]["icon"]

            }
            weather_data.append(weather)
        return render_template("weather.html", weather_data=weather_data)
    

with app.app_context():
    db.create_all()

