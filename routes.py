from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import User, Doctor, Appointment
from datetime import datetime
from models import db
app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/health_monitoring', methods=['GET', 'POST'])
def health_monitoring():
    if request.method == 'POST':
        health_data = request.form.get('health_data')
        return redirect(url_for('app_routes.book_consultation'))
    return render_template('health_monitoring.html')

@app_routes.route('/book_consultation', methods=['GET', 'POST'])
def book_consultation():
    if request.method == 'POST':
        doctor_id = request.form['doctor']
        date_str = request.form['date']
        time_slot = request.form['time']
        user_name = 'Aditi'
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Extract date
        appointment_time = datetime.strptime(str(time_slot), '%H').time()

        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime
        ).first()

        if existing_appointment:
            flash('The selected time slot is already booked. Please choose another one.', 'error')
            return redirect(url_for('app_routes.book_consultation'))

        return redirect(url_for('app_routes.payment', doctor_id=doctor_id, appointment_datetime=appointment_datetime))
    doctors = Doctor.query.all()
    return render_template('book_consultation.html', doctors=doctors)

@app_routes.route('/payment', methods=['GET', 'POST'])
def payment():
    doctor_id = request.args.get('doctor_id')
    appointment_datetime = request.args.get('appointment_datetime')

    if request.method == 'POST':
        new_appointment = Appointment(
            user_id=1,  # Assuming you have a logged-in user with ID 1 (adjust as needed)
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime,
        )
        db.session.add(new_appointment)
        db.session.commit()

        return "Payment Completed Successfully!"
    return render_template('payment.html')

@app_routes.route('/doctor_landing')
def doctor_landing():
    return render_template('doctor_landing.html')

@app_routes.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app_routes.route('/consult_request', methods=['GET', 'POST'])
def consult_request():
    return render_template('consult_request.html')
