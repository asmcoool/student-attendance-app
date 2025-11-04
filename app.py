
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))

def load_data(filename):
    path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)
    with open(path, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    path = os.path.join(DATA_FOLDER, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students')
def students():
    students = load_data('students.json')
    return render_template('students.html', students=students)

@app.route('/schedule')
def schedule():
    classes = load_data('classes.json')
    return render_template('schedule.html', classes=classes)

@app.route('/payments')
def payments():
    payments = load_data('payments.json')
    students = load_data('students.json')
    return render_template('payments.html', payments=payments, students=students)

@app.route('/reports')
def reports():
    students = load_data('students.json')
    classes = load_data('classes.json')
    payments = load_data('payments.json')
    return render_template('reports.html', students=students, classes=classes, payments=payments)

if __name__ == '__main__':
    app.run(debug=True)
