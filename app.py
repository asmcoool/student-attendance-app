from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

students = []
classes = []
attendance = {}
payments = {}

@app.route("/")
def index():
    return render_template("index.html", students=students)

@app.route("/add_student", methods=["POST"])
def add_student():
    student = {
        "name": request.form["name"],
        "address": request.form["address"],
        "parent": request.form["parent"],
        "mobile": request.form["mobile"],
        "fee": request.form["fee"]
    }
    students.append(student)
    return redirect("/")

@app.route("/schedule_class", methods=["POST"])
def schedule_class():
    class_date = request.form["class_date"]
    class_students = request.form.getlist("class_students")
    class_entry = {
        "date": class_date,
        "students": class_students
    }
    classes.append(class_entry)
    for student in class_students:
        attendance[(class_date, student)] = request.form.get(f"attendance_{student}", "Absent")
    return redirect("/")

@app.route("/record_payment", methods=["POST"])
def record_payment():
    student_name = request.form["student_name"]
    month = request.form["month"]
    payments[(student_name, month)] = "Paid"
    return redirect("/")

@app.route("/summary")
def summary():
    return render_template("summary.html", students=students, classes=classes, attendance=attendance, payments=payments)

if __name__ == "__main__":
    app.run(debug=True)
