from app.extensions import mongo
from marshmallow import Schema, fields, post_load, pre_load
from datetime import datetime
from bson import ObjectId

class Measurement:
    def __init__(self, device_id, timestamp=None, value=None, patient_id=None,unit=None,  _id=None):

        self.device_id = device_id
        self.patient_id = patient_id
        self.unit = unit
        self.timestamp = timestamp or datetime.utcnow()
        self.value = value
        self._id = _id

    def save(self):
        """Saves the measurement to the database."""
        measurement_data = MeasurementSchema().dump(self)
        if self._id:
            result = mongo.db.sensor_measurements.update_one({'_id': ObjectId(self._id)}, {'$set': measurement_data})
            return result.modified_count > 0
        else:
            measurement_data.pop('_id', None)  # Remove _id from the data
            result = mongo.db.sensor_measurements.insert_one(measurement_data)
            self._id = result.inserted_id
            return self

    def delete(self):
        """Deletes the measurement from the database."""
        if self._id:
            result = mongo.db.sensor_measurements.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        return False

    @staticmethod
    def get_by_id(self):
        """Retrieves a measurement by its ID."""
        measurement_data = mongo.db.sensor_measurements.find_one({'_id': ObjectId(self._id)})
        if measurement_data:
            return MeasurementSchema().load(measurement_data)
        return None

    @staticmethod
    def get_by_device_id(device_id):
        """Retrieves all measurements for a given sensor."""
        measurements_data = list(mongo.db.sensor_measurements.find({'device_id': device_id}))
        return MeasurementSchema(many=True).load(measurements_data)

    def __repr__(self):
        return f"<Measurement(device_id='{self._id}', timestamp='{self.timestamp}')>"

class MeasurementSchema(Schema):
    _id = fields.Str(dump_only=True)
    device_id = fields.Str(required=True)  # Reference to the sensor
    patient_id = fields.Str(allow_none=True)  # Reference to the sensor
    unit = fields.Str(required=False)
    timestamp = fields.DateTime(default=datetime.utcnow)  # Default to current time
    value = fields.Raw(required=True)  # Can be any type

    @post_load
    def make_measurement(self, data, **kwargs):
        return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id before loading"""
        data.pop('_id', None)
        return data