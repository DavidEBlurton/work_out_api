from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Blessedone1!',
    'database': 'fitness_center_db'
}

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

@app.route('/')
def home():
    return 'Welcome to the Fitness Center API!'

# CRUD operations for Members
@app.route('/members', methods=['POST'])
def add_member():
    data = request.jsonify
    name = data['name']
    email = data['email']
    phone = data.get('phone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Member added successfully!'}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Members WHERE id = %s', (id,))
    member = cursor.fetchone()

    cursor.close()
    conn.close()

    if member is None:
        return jsonify({'message': 'Member not found'}), 404
    return jsonify(member)

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s', (name, email, phone, id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Member updated successfully!'})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Members WHERE id = %s', (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Member deleted successfully!'})

# CRUD operations for Workout Sessions

@app.route('/workout-sessions', methods=['POST'])
def add_workout_session():
    data = request.json
    member_id = data['member_id']
    session_date = data['session_date']
    duration = data['duration']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO WorkoutSessions (member_id, session_date, duration) VALUES (%s, %s, %s)', (member_id, session_date, duration))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Workout session added successfully!'}), 201

@app.route('/workout-sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    data = request.json
    member_id = data.get('member_id')
    session_date = data.get('session_date')
    duration = data.get('duration')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE WorkoutSessions SET member_id = %s, session_date = %s, duration = %s WHERE id = %s', (member_id, session_date, duration, id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Workout session updated successfully!'})

@app.route('/workout-sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM WorkoutSessions WHERE id = %s', (id,))
    session = cursor.fetchone()

    cursor.close()
    conn.close()

    if session is None:
        return jsonify({'message': 'Workout session not found'}), 404
    return jsonify(session)

@app.route('/members/<int:member_id>/workout-sessions', methods=['GET'])
def get_workout_sessions_for_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM WorkoutSessions WHERE member_id = %s', (member_id,))
    sessions = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(sessions)

if __name__ == '__main__':
    app.run(debug=True)

