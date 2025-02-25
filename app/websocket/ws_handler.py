from flask_socketio import emit
from app.extensions import socketio, mongo
from app.models.device import Device, DeviceSchema  # Import the Device model and schema
from marshmallow import ValidationError
import logging
logging.basicConfig(level=logging.INFO)

device_schema = DeviceSchema() # Instantiate the schema

@socketio.on('connect')
def handle_connect():
    try:
        logging.info('Client connected')
    except Exception as e:
        logging.error(f"Error during WebSocket connection: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    try:
        logging.info('Client disconnected')
    except Exception as e:
        logging.error(f"Error during WebSocket disconnection: {e}")

@socketio.on('send_data')
def handle_send_data(data):
    """Handles incoming sensor data via WebSocket, validates it, and stores it in MongoDB."""
    try:
        # Validate the incoming data against the DeviceSchema
        validated_data = device_schema.load(data)

        device_id = validated_data.get('device_id')
        patient_id = validated_data.get('patient_id')
        data_payload = validated_data.get('data')

        # Store data in MongoDB (using PyMongo)
        mongo.db.sensor_data.insert_one({
            'device_id': device_id,
            'patient_id': patient_id,
            'data': data_payload
        })
        emit('data_received', {'status': 'success', 'data': data_payload}, broadcast=True)

    except ValidationError as err:
        # Handle validation errors
        print(f"Validation Error: {err.messages}")
        emit('data_received', {'status': 'error', 'message': err.messages}, broadcast=True)  # Send error back to client
    except Exception as e:
        # Handle other errors
        print(f"Error saving to MongoDB: {e}")
        emit('data_received', {'status': 'error', 'message': str(e)}, broadcast=True)