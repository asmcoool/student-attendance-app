
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/students", methods=["GET", "POST"])
def students():
    students = load_data("students.json")
    if request.method == "POST":
        new_student = {
            "id": len(students) + 1,
            "name": request.form["name"],
            "address": request.form["address"],
            "parent": request.form["parent"],
            "mobile": request.form["mobile"],
            "fee": request.form["fee"]
        }
        students.append(new_student)
        save_data("students.json", students)
        return redirect(url_for("students"))
    return render_template("students.html", students=students)

@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    students = load_data("students.json")
    student = next((s for s in students if s["id"] == student_id), None)
    if request.method == "POST":
        student["name"] = request.form["name"]
        student["address"] = request.form["address"]
        student["parent"] = request.form["parent"]
        student["mobile"] = request.form["mobile"]
        student["fee"] = request.form["fee"]
        save_data("students.json", students)
        return redirect(url_for("students"))
    return render_template("edit_student.html", student=student)

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    students = load_data("students.json")
    students = [s for s in students if s["id"] != student_id]
    save_data("students.json", students)
    return redirect(url_for("students"))

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    classes = load_data("classes.json")
    if request.method == "POST":
        new_class = {
            "id": len(classes) + 1,
            "name": request.form["name"],
            "date": request.form["date"],
            "start": request.form["start"],
            "end": request.form["end"],
            "status": request.form["status"],
            "comments": request.form["comments"]
        }
        classes.append(new_class)
        save_data("classes.json", classes)
        return redirect(url_for("schedule"))
    return render_template("schedule.html", classes=classes)

@app.route("/edit_class/<int:class_id>", methods=["GET", "POST"])
def edit_class(class_id):
    classes = load_data("classes.json")
    class_item = next((c for c in classes if c["id"] == class_id), None)
    if request.method == "POST":
        class_item["name"] = request.form["name"]
        class_item["date"] = request.form["date"]
        class_item["start"] = request.form["start"]
        class_item["end"] = request.form["end"]
        class_item["status"] = request.form["status"]
        class_item["comments"] = request.form["comments"]
        save_data("classes.json", classes)
        return redirect(url_for("schedule"))
    return render_template("edit_class.html", class_item=class_item)

@app.route("/payments", methods=["GET", "POST"])
def payments():
    payments = load_data("payments.json")
    students = load_data("students.json")
    if request.method == "POST":
        student_id = int(request.form["student"])
        student = next((s for s in students if s["id"] == student_id), None)
        new_payment = {
            "id": len(payments) + 1,
            "student": student["name"],
            "parent": student["parent"],
            "date": request.form["date"],
            "amount": request.form["amount"],
            "currency": request.form["currency"],
            "status": request.form["status"]
        }
        payments.append(new_payment)
        save_data("payments.json", payments)
        return redirect(url_for("payments"))
    return render_template("payments.html", payments=payments, students=students)

@app.route("/reports", methods=["GET", "POST"])
def reports():
    students = load_data("students.json")
    classes = load_data("classes.json")
    payments = load_data("payments.json")
    report_type = request.form.get("report_type", "students")
    return render_template("reports.html", students=students, classes=classes, payments=payments, report_type=report_type)

if __name__ == "__main__":
    app.run(debug=True)
