import os
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "0845baae42966387e765176cd0e384abf337f7acd2aa48d74ae1b006de3c8259"

# --- Database Connection ---
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gabriel6@",
        database="notepad"
    )

# --- Routes ---
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

@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Add new note
    if request.method == "POST" and "content" in request.form:
        content = request.form["content"]
        cursor.execute("INSERT INTO notes (user_id, content) VALUES (%s, %s)", (session["user_id"], content))
        db.commit()

    # Search functionality
    search = request.args.get("search", "")
    if search:
        cursor.execute(
            "SELECT * FROM notes WHERE user_id=%s AND content LIKE %s ORDER BY created_at DESC",
            (session["user_id"], f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY created_at DESC", (session["user_id"],))

    notes_list = cursor.fetchall()
    db.close()
    return render_template("notes.html", notes=notes_list, search=search)

@app.route("/edit/<int:note_id>", methods=["POST"])
def edit(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    new_content = request.form["content"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE notes SET content=%s WHERE id=%s AND user_id=%s", (new_content, note_id, session["user_id"]))
    db.commit()
    db.close()
    return redirect(url_for("notes"))

@app.route("/delete/<int:note_id>")
def delete(note_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s AND user_id=%s", (note_id, session["user_id"]))
    db.commit()
    db.close()
    return redirect(url_for("notes"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/search_notes")
def search_notes():
    if "user_id" not in session:
        return "Unauthorized", 401

    search = request.args.get("q", "")
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if search:
        cursor.execute(
            "SELECT * FROM notes WHERE user_id=%s AND content LIKE %s ORDER BY created_at DESC",
            (session["user_id"], f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY created_at DESC", (session["user_id"],))

    notes_list = cursor.fetchall()
    db.close()

    # Render just the notes part
    return render_template("partials/notes_list.html", notes=notes_list)

if __name__ == "__main__":
    app.run(debug=True)
