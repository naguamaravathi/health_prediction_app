from flask import Flask, render_template, request, redirect, flash
import sqlite3, os, re
from datetime import date, datetime
import joblib

model = joblib.load("risk_model.pkl")

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_FILE = "database.db"

def connect_db():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError("Database file not found. Please check database.db")
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection failed: {e}")

def validate_input(full_name, dob, email, glucose, haemoglobin, cholesterol):

    # Check Email first
    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        raise ValueError(
            "Invalid Email Address. Please enter a valid email like: rahul@gmail.com"
        )

    # Check DOB only if email is valid
    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

    if dob_date > date.today():
        raise ValueError(
            "Future Date of Birth is not allowed."
        )

    # Numeric validation
    glucose = float(glucose)
    haemoglobin = float(haemoglobin)
    cholesterol = float(cholesterol)

    return glucose, haemoglobin, cholesterol

def predict_health(glucose, haemoglobin, cholesterol):

    prediction = model.predict(
        [[glucose, haemoglobin, cholesterol]]
    )[0]

    if prediction == 1:
        return "Health Risk Detected"
    else:
        return "Healthy"

@app.route('/')
def index():
    try:
        conn = connect_db()
        patients = conn.execute('SELECT * FROM patients').fetchall()
        conn.close()
        return render_template('index.html', patients=patients)
    except Exception as e:
        flash(str(e))
        return render_template('add.html')

@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        try:
            full_name = request.form['full_name']
            dob = request.form['dob']
            email = request.form['email']

            glucose, haemoglobin, cholesterol = validate_input(
                full_name,
                dob,
                email,
                request.form['glucose'],
                request.form['haemoglobin'],
                request.form['cholesterol']
            )

            # Health Prediction Logic
            remarks = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            conn = connect_db()

            conn.execute(
                '''
                INSERT INTO patients
                (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    full_name,
                    dob,
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                )
            )

            conn.commit()
            conn.close()

            return redirect('/')

        except Exception as e:
            flash(str(e))
            return render_template('add.html')

    return render_template('add.html')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = connect_db()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (id,)).fetchone()

    if not patient:
        flash("Patient not found!", "danger")
        return redirect('/')

    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            dob = request.form['dob']
            email = request.form['email']

            glucose, haemoglobin, cholesterol = validate_input(
                full_name, dob, email,
                request.form['glucose'],
                request.form['haemoglobin'],
                request.form['cholesterol']
            )

            conn.execute('''
                UPDATE patients
                SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?
                WHERE id=?
            ''', (full_name, dob, email, glucose, haemoglobin, cholesterol, id))
            conn.commit()
            conn.close()

            flash("Patient updated successfully!", "success")
            return redirect('/')
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(f'/edit/{id}')

    conn.close()
    return render_template('edit.html', patient=patient)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = connect_db()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (id,)).fetchone()

    if not patient:
        flash("Patient not found!", "danger")
        return redirect('/')

    conn.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash("Patient deleted successfully!", "success")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
