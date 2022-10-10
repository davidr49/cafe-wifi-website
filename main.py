from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    map_url = db.Column(db.String, nullable=False, unique=True)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    all_locations = sorted(db.session.query(Cafe.location).distinct())
    locations_list = []
    for location in all_locations:
        if location not in locations_list:
            locations_list.append(str(location))
    locations_formatted = []
    for loc in locations_list:
        locations_formatted.append(loc[2:-3])
    return render_template('index.html', cafes=all_cafes, locations=locations_formatted)


@app.route("/location/<location_id>", methods=['GET', 'POST'])
def show_cafes(location_id):
    requested_location = Cafe.query.filter_by(location=location_id).all()
    all_locations = sorted(db.session.query(Cafe.location).distinct())
    location_title = str(location_id)
    locations_list = []
    for location in all_locations:
        if location not in locations_list:
            locations_list.append(str(location))
    locations_formatted = []
    for loc in locations_list:
        locations_formatted.append(loc[2:-3])
    return render_template('location.html', cafes=requested_location, locations=locations_formatted, title=location_title)


if __name__ == "__main__":
    app.run(debug=True)
