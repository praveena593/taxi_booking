from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database and create the bookings table if it doesn't exist
def init_db():
    conn = sqlite3.connect('taxi_bookings.db')  # Connect to the database
    cursor = conn.cursor()
    # Create table with 'name' field along with other details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            car_type TEXT NOT NULL,
            pickup_address TEXT NOT NULL,
            destination_address TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route for the booking form page
@app.route('/')
def booking_form():
    return render_template('booking.html')

# Route to handle form submission and save data to the database
@app.route('/book', methods=['POST'])
def book_taxi():
    name = request.form.get('name')
    car_type = request.form.get('car_type')
    pickup_address = request.form.get('pickup_address')
    destination_address = request.form.get('destination_address')
    phone_number = request.form.get('phone_number')

    # Save the booking data to the database
    conn = sqlite3.connect('taxi_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, car_type, pickup_address, destination_address, phone_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, car_type, pickup_address, destination_address, phone_number))
    conn.commit()
    conn.close()

    return redirect(url_for('confirmation', name=name))

# Route for the confirmation page
@app.route('/confirmation')
def confirmation():
    name = request.args.get('name')  # Retrieve name from URL query parameters
    return render_template('confirmation.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
