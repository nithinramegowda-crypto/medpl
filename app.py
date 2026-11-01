
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("medpuls.db")

def create_table():
    db = connect_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dosage TEXT,
            time TEXT
        )
    """)
    db.commit()
    db.close()

@app.route("/")
def home():
    db = connect_db()
    medicines = db.execute("SELECT * FROM medicines").fetchall()
    db.close()
    return render_template("index.html", medicines=medicines)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    dosage = request.form["dosage"]
    time = request.form["time"]

    db = connect_db()
    db.execute(
        "INSERT INTO medicines (name, dosage, time) VALUES (?, ?, ?)",
        (name, dosage, time)
    )
    db.commit()
    db.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    db = connect_db()
    db.execute("DELETE FROM medicines WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
