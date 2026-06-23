from typing import Any

from flask import Flask, flash, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key="hostel123"

# =========================
# 1. DATABASE CONNECTION
# =========================
def get_db():
    conn = sqlite3.connect("hostel.db")
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
# 4. INSERT (ADD VISITOR)
# =========================
@app.route("/add", methods=["GET", "POST"])
def add_visitor():

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
# 5. DELETE
# =========================
@app.route("/delete/<int:id>")
def delete_visitor(id):

    conn = get_db()

    conn.execute("""
        DELETE FROM visitors WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# 6. EDIT/UPDATE
# =========================
@app.route("/edit_visitor/<int:id>", methods=["GET", "POST"])
def edit_visitor(id):

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
# 7. VIEW VISITOR
# =========================
@app.route('/view/<int:id>')
def view_visitor(id):
    conn = get_db()
    visitor = conn.execute("SELECT * FROM visitors WHERE id=?", (id,)).fetchone()

    conn.execute("SELECT * FROM visitors WHERE id=?", (id,)).fetchone()

    conn.close()

    return render_template("view.html" , visitor=visitor)

# =========================
# 8. RECORDS PAGE (OPTIONAL BUT PROFESSIONAL)
# =========================
@app.route("/records")
def records():

    conn = get_db()

    visitors = conn.execute("""
        SELECT * FROM visitors
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return render_template("records.html", visitors=visitors)
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


@app.route("/about")
def about():
    return render_template("about.html ")
# =========================
# RUN
# =========================
if __name__ == "__main__":
   app.run(debug=True)