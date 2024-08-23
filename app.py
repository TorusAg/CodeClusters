from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Sample specialists data (replace with database integration)
specialists = [
    {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "location": {"lat": 34.0522, "lng": -118.2437}},
    {"id": 2, "name": "Dr. Brown", "specialization": "Neurologist", "location": {"lat": 40.7128, "lng": -74.0060}},
    {"id": 3, "name": "Dr. Taylor", "specialization": "Dermatologist", "location": {"lat": 37.7749, "lng": -122.4194}},
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/video+consultancy')
def startVideoCall():
    return render_template('index2.html')

@app.route('/find_specialists', methods=['POST'])
def find_specialists():
    user_location = request.json.get('location')
    nearby_specialists = specialists  # Replace with actual filtering logic
    return jsonify(specialists=nearby_specialists)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    send(f"{data['username']} has joined the room.", to=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} has left the room.", to=room)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('signal')
def handle_signal(data):
    room = data['room']
    signal_data = data['signalData']
    emit('signal', {'signalData': signal_data}, room=room, broadcast=True)

@socketio.on('message')
def handle_message(data):
    send(data['msg'], to=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
