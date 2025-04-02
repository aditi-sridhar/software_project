from flask import Blueprint, render_template, request, redirect, url_for,flash, current_app
from models import User, Doctor, Appointment, Notification
from datetime import datetime
from models import db
from flask_bcrypt import Bcrypt
import logging
app_routes = Blueprint('app_routes', __name__)
bcrypt = Bcrypt()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)


@app_routes.route('/')
def home():
    return render_template('index.html')

@app_routes.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    current_app.logger.info("patient login accessed")
    current_app.logger.info(f"Request Method: {request.method}")
    if request.method == 'POST':
        current_app.logger.info("post")
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            current_app.logger.info("existing user")
            if bcrypt.check_password_hash(existing_user.password, password) and existing_user.name==username:
                return redirect(url_for('app_routes.health_monitoring', user_id=existing_user.id))
            else:
                flash('incorrect password or name')
                return render_template('patient_login_or_sign_up.html')

     
        else:
            current_app.logger.info('not existing')
            new_user = User(name=username, email=email, password=hashed_password)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                flash('did not save in db')
                return render_template('patient_login_or_sign_up.html')
                
            
        return redirect(url_for('app_routes.health_monitoring', user_id=new_user.id))
    
    return render_template('patient_login_or_sign_up.html')

@app_routes.route('/health_monitoring', methods=['GET', 'POST'])

def health_monitoring():
    user_id = request.args.get('user_id')  # Get user_id from URL
    user = User.query.get(user_id) if user_id else None

    if not user:
        current_app.logger.error("not logged in")
        return redirect(url_for('app_routes.home'))
    
    if request.method == 'POST':
        health_data = request.form.get('health_data')
        return redirect(url_for('app_routes.book_consultation', user_id=user_id))
    return render_template('health_monitoring.html')

@app_routes.route('/book_consultation', methods=['GET', 'POST'])

def book_consultation():
    user_id = request.args.get('user_id')  # Get user_id from URL
    user = User.query.get(user_id) if user_id else None

    if not user:
        current_app.logger.error("not logged in")
        return redirect(url_for('app_routes.home'))

    if request.method == 'POST':
        doctor_id = request.form['doctor']
        date_str = request.form['date']
        time_slot = request.form['time']
        
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Extract date
        appointment_time = datetime.strptime(str(time_slot), '%H').time()

        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime
        ).first()

        if existing_appointment:
            flash('The selected time slot is already booked. Please choose another one.', 'error')
            return redirect(url_for('app_routes.book_consultation', user_id=user_id))

        return redirect(url_for('app_routes.payment', doctor_id=doctor_id, appointment_datetime=appointment_datetime, user_id=user_id))
    doctors = Doctor.query.all()
    return render_template('book_consultation.html', doctors=doctors)

@app_routes.route('/payment', methods=['GET', 'POST'])
def payment():
    doctor_id = request.args.get('doctor_id')
    appointment_datetime = request.args.get('appointment_datetime')
    user_id = request.args.get('user_id')  # Get user_id from URL
    user = User.query.get(user_id) if user_id else None

    if not user:
        current_app.logger.error("not logged in")
        return redirect(url_for('app_routes.home'))


    appointment_datetime=datetime.strptime(appointment_datetime, "%Y-%m-%d %H:%M:%S")

    if request.method == 'POST':
        new_appointment = Appointment(
            user_id=user_id,  # Assuming you have a logged-in user with ID 1 (adjust as needed)
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime,
        )
        db.session.add(new_appointment)
        db.session.commit()

        return "Payment Completed Successfully!"
    return render_template('payment.html')

@app_routes.route('/doctor_login',  methods=['GET', 'POST'])
def doctor_login():
    current_app.logger.info("patient login accessed")
    current_app.logger.info(f"Request Method: {request.method}")
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        current_app.logger.info(name)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = Doctor.query.filter_by(name=name).first()
        if existing_user:
            current_app.logger.info("existing user")
            if bcrypt.check_password_hash(existing_user.password, password):
                return redirect(url_for('app_routes.doctor_landing', user_id=existing_user.id))
            else:
                flash('incorrect password')
                return render_template('doctor_login.html')

     
        else:
            flash("Doctor not found")
            return render_template('doctor_login.html')
    
    return render_template('doctor_login.html')

@app_routes.route('/doctor_landing')
def doctor_landing():
    # user_id = request.args.get('user_id')  # Get user_id from URL
    # user = Doctor.query.get(user_id) if user_id else None

    # if not user:
    #     current_app.logger.error("not logged in")
    #     return redirect(url_for('app_routes.home'))
    # appointments=Appointment.query.filter_by(doctor_id=user_id).all()
    return render_template('doctor_landing.html')

@app_routes.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@app_routes.route('/consult_request', methods=['GET', 'POST'])
def consult_request():
    return render_template('consult_request.html')

@app_routes.route('/notifications')
def notifications():
    user_id = request.args.get('user_id')  # Get user_id from URL
    user = User.query.get(user_id) if user_id else None

    if not user:
        current_app.logger.error("not logged in")
        return redirect(url_for('app_routes.home'))
        
    # Query to get notifications from the database
    notifications = Notification.query.filter_by(user_id=user_id).all()
    
    # Pass the notifications to the HTML template
    return render_template('notifications.html', notifications=notifications)
