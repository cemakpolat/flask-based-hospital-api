from flask import Blueprint, request
from app.extensions import mongo
from app.models.rooms import Room, RoomSchema
from app.celery_tasks import long_task
from app.models.device import Device, DeviceSchema
from app.models.measurement import Measurement, MeasurementSchema
from app.utils.responses import success_response, error_response
from marshmallow import ValidationError 
from app.utils.auth_utils import roles_required

measurement_bp = Blueprint('measurements', __name__, url_prefix='/measurements')
device_schema = DeviceSchema()
measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)


@measurement_bp.route('/<string:device_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_device_measurement(device_id):
    """Adds a new measurement to a specific sensor in a room."""
    try:
        # 1. Retrieve the Sensor
        device = Device.get_by_device_id(device_id)
        if not device:
            return error_response("Device not found", 404)
        measurements = Measurement.get_by_device_id(device_id)
        if not measurements:
            return error_response("Measurements not found", 404)
        return success_response(measurements_schema.dump(measurements))
    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)


@measurement_bp.route('/<string:device_id>', methods=['POST'])
@roles_required('admin', 'user')
def add_sensor_measurement(device_id):
    """Adds a new measurement to a specific sensor in a room."""
    try:
        # 1. Retrieve the Sensor
        device = Device.get_by_device_id(device_id)
        print(device)
        if not device:
            return error_response("Device not found", 404)

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

