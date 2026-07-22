from http import client
from click import prompt
from flask import Flask, abort, redirect, render_template, request, flash, session , url_for
from flask.cli import load_dotenv
from database import get_db, init_db
from groq import Groq
import os
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key='Linkiwi2026'  # Necessary for flash messages

# =========================
# 1. DATABASE CONNECTION
# =========================
def get_db():
    conn = sqlite3.connect("Database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 2. INIT DATABASE
# =========================
def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS visitors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room_no TEXT NOT NULL,
        purpose TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()


# =========================
# 3. SELECT (HOME PAGE)
# =========================
@app.route("/")
def home():
    conn = get_db()

    visitors = conn.execute("""
        SELECT * FROM visitors
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return render_template("home.html", visitors=visitors)

# =========================
# 4. DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM visitors")
    total_visitors = cursor.fetchone()[0]


    conn.close()

    return render_template(
        "dashboard.html",
        total_visitors=total_visitors,
        today_visitors=0,
        last_visitors=0
    )

# ========================
# 5. INSERT (ADD VISITOR)
# =========================
@app.route("/add", methods=["GET", "POST"])
def add_visitor():
    print(session)
    
    if session.get('role') !='admin':
        flash( "Admins only! You do not have permission","danger")
        return redirect('/')


    if request.method == "POST":

        visitor_name = request.form["visitor_name"]
        student_name = request.form["student_name"]
        room_no = request.form["room_no"]
        purpose = request.form["purpose"]

        conn = get_db()

        conn.execute("""
        INSERT INTO visitors (visitor_name, student_name, room_no, purpose)
        VALUES (?, ?, ?, ?)
        """, (visitor_name, student_name, room_no, purpose))

        conn.commit()
        conn.close()
        flash("Visitor Added Successfully!")

        return redirect("/records")

    return render_template("add_visitor.html")


# =========================
# 6. DELETE
# =========================
@app.route("/delete/<int:id>")
def delete_visitor(id):
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect('/')

    conn = get_db()

    conn.execute("""
        DELETE FROM visitors WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# 7. EDIT/UPDATE
# =========================
@app.route("/edit_visitor/<int:id>", methods=["GET", "POST"])
def edit_visitor(id):
    if session.get('role') !='admin':
        flash("Admins only! You do not have permission","danger")
        return redirect('/')


    conn = get_db()

    if request.method == "POST":

        visitor_name = request.form["visitor_name"]
        student_name = request.form["student_name"]
        room_no = request.form["room_no"]
        purpose = request.form["purpose"]

        conn.execute("""
            UPDATE visitors
            SET visitor_name=?, student_name=?, room_no=?, purpose=?
            WHERE id=?
        """, (visitor_name, student_name, room_no, purpose, id))

        conn.commit()
        conn.close()

        return redirect("/records")

    visitor = conn.execute("""
        SELECT * FROM visitors WHERE id=?
    """, (id,)).fetchone()

    conn.close()

    return render_template("edit_visitor.html", visitor=visitor)

# =========================
# 8. VIEW VISITOR
# =========================

@app.route('/view/<int:id>')
def view_visitor(id):
    conn = get_db()
    visitor = conn.execute("SELECT * FROM visitors WHERE id=?", (id,)).fetchone()
    conn.close()

    if visitor is None:
        abort(404)

    tip = get_ai_tip(id)  # Get AI tip for the visitor

    return render_template("view.html", visitor=visitor )

@app.route(('/view/<int:id>/tip'))
def get_ai_tip(id):
    conn = get_db()
    visitor = conn.execute(
        "SELECT * FROM visitors WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if visitor is None:
        abort(404)

    prompt = f"""
    Visitor Name: {visitor['visitor_name']}
    Student Name: {visitor['student_name']}
    Room Number: {visitor['room_no']}
    Purpose: {visitor['purpose']}

    Give one short and professional hostel security recommendation.
    Keep the response within 2 lines.
    """

    client = Groq(api_key=os.getenv("GROQ_API_KEY",""))

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    tip= response.choices[0].message.content  # Return the AI tip

    return render_template("view.html", visitor=visitor, tip=tip)

# =============================================
# 9. RECORDS PAGE (OPTIONAL BUT PROFESSIONAL)
# =============================================
@app.route("/records")
def records():

    conn = get_db()

    visitors = conn.execute("""
        SELECT * FROM visitors
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return render_template("records.html", visitors=visitors )

# ==========================
# SEARCH  
#  =========================

@app.route("/search")
def search():
    #step 1 - get query from URL
    q = request.args.get('q','')
    # request.args - GET parameters
    # 'q' - Form  - name = 'q'
    conn = get_db()
    
    if q:
        visitors = conn.execute('''SELECT * FROM visitors
                                WHERE visitor_name LIKE ? 
                                OR student_name LIKE ?
                                OR room_no LIKE ?''',
                                (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
        
    else:
        visitors = conn.execute('SELECT * FROM visitors ORDER BY id DESC').fetchall()
    conn.close()
    return render_template("search.html", visitors=visitors, query=q)

# =======================
# 11. FILTER
# =======================

@app.route('/filter')
def filter_students():

    purpose = request.args.get('purpose', '')

    conn = get_db()

    # Dropdown unique purposes
    purposes = conn.execute("""
        SELECT DISTINCT purpose
        FROM visitors
        ORDER BY purpose
    """).fetchall()

    # Filter query
    if purpose:
        visitors = conn.execute("""
            SELECT *
            FROM visitors
            WHERE purpose = ?
            ORDER BY id ASC
        """, (purpose,)).fetchall()
    else:
        visitors = conn.execute("""
            SELECT *
            FROM visitors
            ORDER BY id ASC
        """).fetchall()

    conn.close()

    return render_template(
        'filter.html',
        visitors=visitors,
        purposes=purposes,
        selected_purpose=purpose
    )
# =====================
# 12. ABOUT 
# =====================

@app.route("/about")
def about():
    return render_template("about.html")

# =============================
# 13.REGISTER , LOGIN, LOGOUT
# =============================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        # Check if username already exists
        existing = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Username already exists!', 'danger')
            conn.close()          
            return render_template('register.html')
        
        hashed = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed, 'student'))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(('/login'))
    
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']
            flash(f'Welcome {username}!', 'success')
            return redirect(('/'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    
    
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(('/'))

def page_not_found(e):
    return render_template("404.html"), 404
 
       
init_db()  # Initialize the database

if __name__ == "__main__":
   app.run(debug=True)
