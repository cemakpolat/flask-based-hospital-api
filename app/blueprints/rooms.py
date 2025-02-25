from flask import Blueprint, request
from app.extensions import mongo
from app.models.rooms import Room, RoomSchema
from app.celery_tasks import long_task
from app.models.device import Device, DeviceSchema
from app.models.measurement import Measurement, MeasurementSchema
from app.utils.responses import success_response, error_response
from marshmallow import ValidationError 
from app.utils.auth_utils import roles_required

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
device_schema = DeviceSchema()
sensors_schema = DeviceSchema(many=True)
measurement_schema = MeasurementSchema()


@rooms_bp.route('/sensors', methods=['POST'])
@roles_required('admin', 'user')
def create_sensor():
    """Creates a new sensor for a room."""
    try:
        data = request.get_json()
        validated_data = device_schema.load(data)
        sensor = Device(**validated_data)
        sensor.save()
        return success_response(device_schema.dump(sensor), "Sensor created successfully", 201)
    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('', methods=['POST'])
@roles_required('admin', 'user')
def create_room():
    """Creates a new room."""
    try:
        data = request.get_json()
        validated_data = room_schema.load(data)
        room = Room(**validated_data)
        room.save()
        return success_response(room_schema.dump(room), "Room created successfully", 201)
    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('/<string:room_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_room(room_id):
    """Retrieves a room by ID."""
    try:
        room = Room.get_by_id(room_id)
        if not room:
            return error_response("Room not found", 404)
        return success_response(room_schema.dump(room))
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('', methods=['GET'])
@roles_required('admin', 'user')
def get_all_rooms():
    """Lists all rooms."""
    try:
        rooms = Room.get_all()
        return success_response(rooms_schema.dump(rooms))
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('/<string:room_id>', methods=['PUT'])
@roles_required('admin', 'user')
def update_room(room_id):
    """Updates an existing room."""
    try:
        room = Room.get_by_id(room_id)
        if not room:
            return error_response("Room not found", 404)

        data = request.get_json()
        validated_data = room_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(room, key, value)

        room.save()
        return success_response(room_schema.dump(room), "Room updated successfully")

    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('/<string:room_id>', methods=['DELETE'])
@roles_required('admin', 'user')
def delete_room(room_id):
    """Deletes a room."""
    try:
        room = Room.get_by_id(room_id)
        if not room:
            return error_response("Room not found", 404)

        if room.delete():
            return success_response(message="Room deleted successfully", status_code=200)
        else:
            return error_response("Failed to delete room", 500)
    except Exception as e:
        return error_response(str(e), 500)

@rooms_bp.route('measurements/<string:device_id>', methods=['POST'])
@roles_required('admin', 'user')
def add_sensor_measurement(device_id):
    """Adds a new measurement to a specific sensor in a room."""
    try:
        # 1. Retrieve the Sensor
        sensor = Device.get_by_device_id(device_id)
        print(sensor)
        if not sensor:
            return error_response("Sensor not found", 404)

        # 2. Validate the new measurement data
        data = request.get_json()
        validated_data = measurement_schema.load(data)

        # 3. Create a new Measurement object and associate it with the sensor
        measurement = Measurement(**validated_data)
        measurement.save()

        # 4. Return success message
        return success_response(message="Measurement added successfully",status_code=201)

    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

