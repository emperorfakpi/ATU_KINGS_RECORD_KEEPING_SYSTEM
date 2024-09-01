import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from devices import db, Device  # Import db and Device from devices.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SQLAlchemy with the app
db.init_app(app)

# Define the Reservation model in app.py

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unique_code = db.Column(db.String(100), nullable=False)
    booking_details = db.Column(db.Text)
    time_of_collection = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    time_of_return = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Not Collected')

# Routes and other code remain the same

@app.route('/')
def index():
    reservations = Reservation.query.all()
    return render_template('index.html', reservations=reservations)

@app.route('/add', methods=['POST'])
def add_reservation():
    name = request.form['name']
    unique_code = request.form['unique_code']
    booking_details = request.form['booking_details']
    
    time_of_collection_str = request.form['time_of_collection']
    time_of_collection = datetime.strptime(time_of_collection_str, '%Y-%m-%dT%H:%M')
    duration = int(request.form['duration'])
    time_of_return = None

    reservation = Reservation(
        name=name,
        unique_code=unique_code,
        booking_details=booking_details,
        time_of_collection=time_of_collection,
        duration=duration,
        time_of_return=time_of_return
    )
    db.session.add(reservation)
    db.session.commit()
    flash('Reservation added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    reservation.status = request.form['status']
    
    time_of_return_str = request.form.get('time_of_return')
    if time_of_return_str:
        reservation.time_of_return = datetime.strptime(time_of_return_str, '%Y-%m-%dT%H:%M')

    db.session.commit()
    flash('Reservation updated successfully', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_reservations():
    query = request.args.get('query', '')
    reservations = Reservation.query.filter(
        (Reservation.name.like(f'%{query}%')) |
        (Reservation.unique_code.like(f'%{query}%'))
    ).all()
    return render_template('index.html', reservations=reservations)

@app.route('/booked_devices')
def booked_devices():
    booked_reservations = Reservation.query.filter_by(status='Collected').all()
    return render_template('booked_devices.html', reservations=booked_reservations)

@app.route('/telegram_messages')
def telegram_messages():
    # Your code here
    return render_template('telegram_messages.html')

@app.route('/waiting_list')
def waiting_list():
    waiting_reservations = Reservation.query.filter_by(status='Not Collected').all()
    return render_template('waiting_list.html', reservations=waiting_reservations)

@app.route('/available_devices')
def available_devices():
    available_devices = Device.query.all()
    return render_template('available_devices.html', devices=available_devices)

@app.route('/update_device/<int:id>', methods=['POST'])
def update_device(id):
    device = Device.query.get_or_404(id)
    action = request.form['action']

    if action == 'book':
        if device.available_quantity > 0:
            device.available_quantity -= 1
    elif action == 'return':
        if device.available_quantity < device.total_quantity:
            device.available_quantity += 1

    db.session.commit()
    flash('Device quantity updated successfully', 'success')
    return redirect(url_for('available_devices'))

# Database initialization code
def init_db():
    # Delete the existing database (only do this during development)
    if os.path.exists('reservations.db'):
        os.remove('reservations.db')
        print("Existing database deleted.")

    # Create a new database
    with app.app_context():
        db.create_all()  # Ensure database tables are created
        print("New database created.")

        # Check if the Device table is empty and seed it
        if not Device.query.first():
            devices = [
                Device(name='LED pointers ', total_quantity=15, available_quantity=10),
                Device(name='Projector', total_quantity=20, available_quantity=5),
                Device(name='Speakers and microphones', total_quantity=20, available_quantity=8)
            ]
            db.session.add_all(devices)
            db.session.commit()
            print("Sample devices added to the database.")

if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Start the Flask app
    app.run(debug=True)
