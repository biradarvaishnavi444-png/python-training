from flask import Flask, render_template

app = Flask(__name__)

visitors = [
    {"id": 1, "name": "Komal", "room": "101","entry": "10:00 AM","status": "Inside"},
    {"id": 2, "name": "Priya", "room": "102",  "entry": "11:00 AM","status": "Exited"},
    {"id": 3, "name": "Sneha", "room": "104","entry": "01:00 PM","status": "Exited"},
    {"id": 4, "name": "Vamika", "room": "105", "entry": "02:00 PM","status": "Inside"}
]
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", visitors=visitors)

@app.route("/about")
def about():
    return render_template("about.html")
 
if __name__ == "__main__":
    app.run(debug=True)

    