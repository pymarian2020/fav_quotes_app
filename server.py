from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import gunicorn
import os

app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URI', None)

#PASSWORD = "password"

#app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://postgres:{PASSWORD}@localhost/quotes"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Favquotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))


#db.create_all()


@app.route("/")
def index():
    result = Favquotes.query.all()
    return render_template("index.html", result=result)


@app.route("/quotes")
def quotes():
    return render_template("quotes.html")


@app.route("/process", methods=["POST"])
def process():
    author = request.form["author"]
    quote = request.form["quote"]
    quote_data = Favquotes(author=author, quote=quote)
    db.session.add(quote_data)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
