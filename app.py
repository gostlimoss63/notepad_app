import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "0845baae42966387e765176cd0e384abf337f7acd2aa48d74ae1b006de3c8259"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gabriel6@",
        database="notepad"
    )

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("notes"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("notes"))
        return "Invalid username or password"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
        except:
            return "Username already exists"
        db.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/notes")
def notes():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE user_id=%s AND completed=FALSE", (session["user_id"],))
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("notes.html", notes=notes)

@app.route("/completed_notes")
def completed_notes():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE user_id=%s AND completed=TRUE", (session["user_id"],))
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("completed_notes.html", notes=notes)

@app.route("/done/<int:note_id>", methods=["POST"])
def mark_done(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET completed=TRUE WHERE id=%s AND user_id=%s", (note_id, session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("notes"))


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s AND user_id=%s AND completed=TRUE", (note_id, session["user_id"]))
    conn.commit()
    cursor.close()
    return redirect(url_for("completed_notes"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/search_notes")
def search_notes():
    if "user_id" not in session:
        return "Unauthorized", 401

    db = get_db()
    cursor = db.cursor(dictionary=True)

    search = request.args.get("q", "")
    completed = request.args.get("completed", "false").lower() == "true"

    if search:
        cursor.execute(
            """
            SELECT * FROM notes
            WHERE user_id=%s AND (content LIKE %s OR title LIKE %s) AND completed=%s
            ORDER BY created_at DESC
            """,
            (session["user_id"], f"%{search}%", f"%{search}%", completed)
        )
    else:
        cursor.execute(
            """
            SELECT * FROM notes 
            WHERE user_id=%s AND completed=%s
            ORDER BY created_at DESC
            """,
            (session["user_id"], completed)
        )

    notes_list = cursor.fetchall()
    db.close()

    # Dynamically choose which partial to render
    template = "partials/notes_completed.html" if completed else "partials/notes_list.html"
    return render_template(template, notes=notes_list)


@app.route("/notes", methods=["POST"])
def add_note():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "Untitled")
    content = request.form["content"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, title, content, completed) VALUES (%s, %s, %s, FALSE)",
        (session["user_id"], title, content)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("notes"))

@app.route("/edit/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "Untitled")
    content = request.form["content"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET title=%s, content=%s WHERE id=%s AND user_id=%s AND completed=FALSE",
        (title, content, note_id, session["user_id"])
    )
    conn.commit()
    cursor.close()
    return redirect(url_for("notes"))

if __name__ == "__main__":
    app.run(debug=True)
