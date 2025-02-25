from app.extensions import mongo
from marshmallow import Schema, fields, post_load, pre_load
from datetime import datetime
from bson import ObjectId

class Sensor:
    def __init__(self, name, type, room_id, _id=None,created_at=None):
        self.name = name
        self.type = type
        self.room_id = room_id
        self._id = _id
        self.created_at = created_at

    def save(self):
        """Saves the sensor to the database."""
        sensor_data = SensorSchema().dump(self)
        if self._id:
            result = mongo.db.sensors.update_one({'_id': ObjectId(self._id)}, {'$set': sensor_data})
            return result.modified_count > 0
        else:
            sensor_data.pop('_id', None)  # Remove _id from the data
            result = mongo.db.sensors.insert_one(sensor_data)
            self._id = result.inserted_id
            return self

    def delete(self):
        """Deletes the sensor from the database."""
        if self._id:
            result = mongo.db.sensors.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        return False

    @staticmethod
    def get_by_id(sensor_id):
        """Retrieves a sensor by ID."""
        sensor_data = mongo.db.sensors.find_one({'_id': ObjectId(sensor_id)})
        if sensor_data:
            return SensorSchema().load(sensor_data)
        return None

    @staticmethod
    def get_all():
        """Retrieves all sensors from the database."""
        sensors_data = list(mongo.db.sensors.find())
        return SensorSchema(many=True).load(sensors_data)

    def __repr__(self):
        return f"<Sensor(name='{self.name}', type='{self.type}')>"


class SensorSchema(Schema):
    _id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    room_id = fields.Str(required=True)  # Use Str instead of Int if room_id is a string (ObjectId)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_sensor(self, data, **kwargs):
        return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id and created_at before loading"""
        data.pop('_id', None)
        data.pop('created_at', None)
        return data