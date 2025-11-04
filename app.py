from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

students = []
classes = []
payments = []

def generate_time_slots():
    return [f"{str(h).zfill(2)}:00" for h in range(0, 24)]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students', methods=['GET', 'POST'])
def student_page():
    if request.method == 'POST':
        student_id = len(students) + 1
        student = {
            'id': student_id,
            'name': request.form['name'],
            'address': request.form['address'],
            'parent': request.form['parent'],
            'mobile': request.form['mobile'],
            'fee': request.form['fee']
        }
        students.append(student)
        return redirect(url_for('student_page'))
    return render_template('students.html', students=students)

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['address'] = request.form['address']
        student['parent'] = request.form['parent']
        student['mobile'] = request.form['mobile']
        student['fee'] = request.form['fee']
        return redirect(url_for('student_page'))
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('student_page'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_page():
    if request.method == 'POST':
        class_id = len(classes) + 1
        class_entry = {
            'id': class_id,
            'name': f"Class-{request.form['date']}",
            'date': request.form['date'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'status': request.form['status'],
            'comments': request.form['comments']
        }
        classes.append(class_entry)
        return redirect(url_for('schedule_page'))
    time_slots = generate_time_slots()
    return render_template('schedule.html', classes=classes, time_slots=time_slots)

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
        return redirect(url_for('payments_page'))
    return render_template('payments.html', students=students, payments=payments)

@app.route('/reports')
def reports_page():
    class_summary = {
        'total': len(classes),
        'held': sum(1 for c in classes if c['status'] == 'Conducted'),
        'cancelled': sum(1 for c in classes if c['status'] == 'Cancelled')
    }
    payment_summary = {
        'total': len(payments),
        'paid': sum(1 for p in payments if p['amount']),
        'pending': len(students) - sum(1 for p in payments if p['amount'])
    }
    return render_template('reports.html', students=students, class_summary=class_summary, payment_summary=payment_summary)

if __name__ == '__main__':
    app.run(debug=True)
