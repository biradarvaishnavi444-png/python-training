from flask import Flask

app = Flask(__name__)

# List of Dictionaries (Visitor Records)
visitors = [
    {"id": 1, "name": "Komal", "room": 101, "status": "IN"},
    {"id": 2, "name": "Priya", "room": 102, "status": "OUT"},
    {"id": 3, "name": "Pallavi", "room": 103, "status": "IN"},
    {"id": 4, "name": "Sneha", "room": 104, "status": "OUT"},
    {"id": 5, "name": "Pranjal", "room": 105, "status": "IN"}
]

# Route 1 - Hoomepage
@app.route("/")
def home():
    return """
    <h1>Hostel Visitor Log System</h1>
    <p>This project is used to manage and track hostel visitor records.</p>
    """

# Route 2 - Records Page
@app.route("/records")
def records():
    result = "<h2>Visitor Records</h2>"
    
    for visitor in visitors:
        result += f"""
        <p>
        ID: {visitor['id']} |
        Name: {visitor['name']} |
        Room: {visitor['room']} |
        Status: {visitor['status']}
        </p>
        """
    
    return result

# Route 3 - Extra Route
@app.route("/total")
def total():
    return f"<h2>Total Visitors : {len(visitors)}</h2>"

if __name__ == "__main__":
    app.run(debug=True)