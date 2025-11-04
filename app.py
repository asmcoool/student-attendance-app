
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []
classes = []
payments = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students', methods=['GET', 'POST'])
def students_page():
    if request.method == 'POST':
        student = {
            'name': request.form['name'],
            'address': request.form['address'],
            'parent': request.form['parent'],
            'mobile': request.form['mobile'],
            'fee': request.form['fee']
        }
        students.append(student)
    return render_template('students.html', students=students)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_page():
    if request.method == 'POST':
        class_entry = {
            'name': f"Class-{request.form['date']}",
            'date': request.form['date'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'status': request.form['status'],
            'comments': request.form['comments']
        }
        classes.append(class_entry)
    return render_template('schedule.html', classes=classes)

@app.route('/payments', methods=['GET', 'POST'])
def payments_page():
    if request.method == 'POST':
        payment = {
            'student': request.form['student'],
            'parent': request.form['parent'],
            'date': request.form['date'],
            'amount': request.form['amount'],
            'currency': request.form['currency']
        }
        payments.append(payment)
    return render_template('payments.html', payments=payments, students=students)

if __name__ == '__main__':
    app.run(debug=True)
