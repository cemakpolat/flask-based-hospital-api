from flask import Blueprint, request
from app.models.device import Device, DeviceSchema
from app.extensions import mongo
from app.utils.responses import success_response, error_response
from marshmallow import ValidationError  # Import ValidationError
from app.utils.auth_utils import roles_required

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)


@devices_bp.route('', methods=['POST'])
@roles_required('admin', 'user')
def create_device():
    """Creates a new device."""
    
    try:
        data = request.get_json()
        validated_data = device_schema.load(data)

        device = Device(**validated_data)
        device.save()
        return success_response(device_schema.dump(device), "Device created successfully", 201)
    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)


@devices_bp.route('/room/nulls', methods=['GET'])
@roles_required('admin', 'user')
def get_devices_with_null_room():
    """Retrieves devices where room_id is null."""
    try:
        devices = Device.get_devices_with_null_room_id()
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)

@devices_bp.route('/room/notnulls', methods=['GET'])
@roles_required('admin', 'user')
def get_devices_with_not_null_room():
    """Retrieves devices where room_id is not null."""
    try:
        devices = Device.get_devices_with_not_null_room_id()
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)
    
@devices_bp.route('/room/<string:room_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_devices_by_room(room_id):
    """Retrieves devices assigned to a specific room."""
    try:
        devices = Device.get_by_room_id(room_id)
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)
    
@devices_bp.route('/patient', methods=['GET'])
@roles_required('admin', 'user')
def get_patient_devices():
    """Retrieves devices assigned to patients."""
    try:
        devices = Device.get_patient_devices()
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)

@devices_bp.route('/<string:device_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_device(device_id):
    """Retrieves a device by ID."""
    try:
        device = Device.get_by_device_id(device_id)
        if not device:
            return error_response("Device not found", 404)
        return success_response(device_schema.dump(device))
    except Exception as e:
        return error_response(str(e), 500)

@devices_bp.route('', methods=['GET'])
@roles_required('admin', 'user')
def get_all_devices():
    """Lists all devices."""
    try:
        devices = Device.get_all()
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)

@devices_bp.route('/shared', methods=['GET'])
@roles_required('admin', 'user')
def get_shared_devices():
    """Retrieves all shared devices."""
    try:
        devices = Device.get_shared_devices()
        return success_response(devices_schema.dump(devices))
    except Exception as e:
        return error_response(str(e), 500)  

@devices_bp.route('/<string:device_id>', methods=['PUT'])
@roles_required('admin', 'user')
def update_device(device_id):
    """Updates an existing device."""
    try:
        device = Device.get_by_id(device_id)
        if not device:
            return error_response("Device not found", 404)

        data = request.get_json()
        validated_data = device_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(device, key, value)

        device.save()
        return success_response(device_schema.dump(device), "Device updated successfully")

    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)


@devices_bp.route('/<string:device_id>', methods=['DELETE'])
@roles_required('admin', 'user')
def delete_device(device_id):
    """Deletes a device."""
    try:
        device = Device.get_by_id(device_id)
        if not device:
            return error_response("Device not found", 404)

        if device.delete():
            return success_response(message="Device deleted successfully", status_code=200)
        else:
            return error_response("Failed to delete device", 500)
    except Exception as e:
        return error_response(str(e), 500)