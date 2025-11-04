
from flask import Flask, render_template, request, redirect
from datetime import datetime
import uuid

app = Flask(__name__)

students = []
classes = []
payments = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/students", methods=["GET", "POST"])
def students_page():
    if request.method == "POST":
        student = {
            "id": str(uuid.uuid4()),
            "name": request.form["name"],
            "address": request.form["address"],
            "parent": request.form["parent"],
            "mobile": request.form["mobile"],
            "fee": request.form["fee"]
        }
        students.append(student)
    return render_template("students.html", students=students)

@app.route("/classes", methods=["GET", "POST"])
def classes_page():
    if request.method == "POST":
        class_entry = {
            "id": str(uuid.uuid4()),
            "name": "Class-" + request.form["date"],
            "date": request.form["date"],
            "status": request.form["status"],
            "comments": request.form["comments"]
        }
        classes.append(class_entry)
    return render_template("classes.html", classes=classes)

@app.route("/payments", methods=["GET", "POST"])
def payments_page():
    if request.method == "POST":
        student_id = request.form["student"]
        student = next((s for s in students if s["id"] == student_id), None)
        if student:
            payment = {
                "id": str(uuid.uuid4()),
                "student": student["name"],
                "parent": student["parent"],
                "date": request.form["date"],
                "amount": request.form["amount"],
                "currency": request.form["currency"]
            }
            payments.append(payment)
    return render_template("payments.html", payments=payments, students=students)

@app.route("/reports")
def reports_page():
    return render_template("reports.html", students=students, classes=classes, payments=payments)

if __name__ == "__main__":
    app.run(debug=True)
