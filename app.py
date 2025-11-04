from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# File paths for persistent storage
STUDENTS_FILE = 'students.json'
CLASSES_FILE = 'classes.json'
PAYMENTS_FILE = 'payments.json'

# Helper functions to load and save data
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    students = load_data(STUDENTS_FILE)
    if request.method == 'POST':
        new_student = {
            'name': request.form['name'],
            'address': request.form['address'],
            'parent': request.form['parent'],
            'mobile': request.form['mobile'],
            'monthly_fee': request.form['monthly_fee']
        }
        students.append(new_student)
        save_data(STUDENTS_FILE, students)
        return redirect(url_for('students'))
    return render_template('students.html', students=students)

@app.route('/edit_student/<int:index>', methods=['GET', 'POST'])
def edit_student(index):
    students = load_data(STUDENTS_FILE)
    if request.method == 'POST':
        students[index] = {
            'name': request.form['name'],
            'address': request.form['address'],
            'parent': request.form['parent'],
            'mobile': request.form['mobile'],
            'monthly_fee': request.form['monthly_fee']
        }
        save_data(STUDENTS_FILE, students)
        return redirect(url_for('students'))
    return render_template('edit_student.html', student=students[index], index=index)

@app.route('/delete_student/<int:index>')
def delete_student(index):
    students = load_data(STUDENTS_FILE)
    students.pop(index)
    save_data(STUDENTS_FILE, students)
    return redirect(url_for('students'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    classes = load_data(CLASSES_FILE)
    if request.method == 'POST':
        new_class = {
            'class_name': request.form['class_name'],
            'date': request.form['date'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'status': request.form['status'],
            'comments': request.form['comments']
        }
        classes.append(new_class)
        save_data(CLASSES_FILE, classes)
        return redirect(url_for('schedule'))
    return render_template('schedule.html', classes=classes)

@app.route('/edit_class/<int:index>', methods=['GET', 'POST'])
def edit_class(index):
    classes = load_data(CLASSES_FILE)
    if request.method == 'POST':
        classes[index] = {
            'class_name': request.form['class_name'],
            'date': request.form['date'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'status': request.form['status'],
            'comments': request.form['comments']
        }
        save_data(CLASSES_FILE, classes)
        return redirect(url_for('schedule'))
    return render_template('edit_class.html', class_info=classes[index], index=index)

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    payments = load_data(PAYMENTS_FILE)
    students = load_data(STUDENTS_FILE)
    if request.method == 'POST':
        selected_student = next((s for s in students if s['name'] == request.form['student']), {})
        new_payment = {
            'student': request.form['student'],
            'parent': selected_student.get('parent', ''),
            'date': request.form['date'],
            'amount': request.form['amount'],
            'currency': request.form['currency'],
            'status': request.form['status']
        }
        payments.append(new_payment)
        save_data(PAYMENTS_FILE, payments)
        return redirect(url_for('payments'))
    return render_template('payments.html', payments=payments, students=students)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    students = load_data(STUDENTS_FILE)
    classes = load_data(CLASSES_FILE)
    payments = load_data(PAYMENTS_FILE)
    report_type = request.form.get('report_type', 'students')
    return render_template('reports.html', students=students, classes=classes, payments=payments, report_type=report_type)

if __name__ == '__main__':
    app.run(debug=True)
