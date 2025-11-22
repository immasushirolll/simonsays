from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

with app.test_request_context():
    print(url_for("static", filename="styles.css"))

@app.route("/simonsays/")
def simonsays():
    return render_template("simonsays.html")

with app.test_request_context():
    print(url_for("static", filename="simonsays.css"))
