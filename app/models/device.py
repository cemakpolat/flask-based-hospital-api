from app.extensions import mongo
from marshmallow import Schema, fields, post_load, pre_load
from bson import ObjectId

class Device:
    def __init__(self, name,device_id, device_type=None,room_id=None,device_category="personal", _id=None):
        self.name = name
        self.device_id = device_id
        self.device_type = device_type
        self.room_id = room_id
        self.device_category = device_category  # "personal" or "shared"


        self._id = _id

    def save(self):
        """Saves the device to the database."""
        device_data = DeviceSchema().dump(self)  # Serialize the object
        if self._id:
            # Update existing device
            result = mongo.db.devices.update_one({'_id': ObjectId(self._id)}, {'$set': device_data})
            if result.modified_count == 0:
                raise Exception("Device not found or no changes applied") # General exception
            return True
        else:
            # Insert new device
            device_data.pop('_id', None)  # Remove _id from the data
            result = mongo.db.devices.insert_one(device_data)
            self._id = result.inserted_id
            return self


    def delete(self):
        """Deletes the device from the database."""
        if self._id:
            result = mongo.db.devices.delete_one({'_id': ObjectId(self._id)})
            if result.deleted_count == 0:
               raise Exception("Device not found") # General exception
            return True
        return False  # Nothing to delete


    @staticmethod
    def get_by_id(id):
        """Retrieves a device by its ID."""
        device_data = mongo.db.devices.find_one({'_id': ObjectId(id)})
        if device_data:
            return DeviceSchema().load(device_data)  # Deserialize the data
        return None
    
    @staticmethod
    def get_shared_devices():
        """Retrieves all shared devices."""
        devices_data = list(mongo.db.devices.find({'device_category': 'shared'}))
        return DeviceSchema(many=True).load(devices_data)

    @staticmethod
    def get_personal_devices():
        """Retrieves all personal devices."""
        devices_data = list(mongo.db.devices.find({'device_category': 'personal'}))
        return DeviceSchema(many=True).load(devices_data)


    @staticmethod
    def get_by_device_id(device_id):
        """Retrieves a device by its ID."""
        device_data = mongo.db.devices.find_one({'device_id': device_id})
        if device_data:
            return DeviceSchema().load(device_data)  # Deserialize the data
        return None

    @staticmethod
    def get_by_room_id(room_id):
        """Retrieves devices assigned to a specific room."""
        devices_data = list(mongo.db.devices.find({'room_id': room_id}))
        return DeviceSchema(many=True).load(devices_data)
    
    @staticmethod
    def get_devices_with_null_room_id():
        """Retrieves devices where room_id is null."""
        devices_data = list(mongo.db.devices.find({'room_id': None}))
        return DeviceSchema(many=True).load(devices_data)

    @staticmethod
    def get_devices_with_not_null_room_id():
        """Retrieves devices where room_id is null."""
        devices_data = list(mongo.db.devices.find({'room_id': {'$ne': None}}))
        return DeviceSchema(many=True).load(devices_data)


    @staticmethod
    def get_all():
        """Retrieves all devices from the database."""
        devices_data = list(mongo.db.devices.find())
        return DeviceSchema(many=True).load(devices_data)


    @staticmethod
    def get_patient_devices():
        """Retrieves devices assigned to patients."""
        devices_data = list(mongo.db.devices.find({'patient_id': {'$ne': None}}))
        return DeviceSchema(many=True).load(devices_data)
    def __repr__(self):
        return f"<Device(name='{self.name}', type='{self.type}')>"


class DeviceSchema(Schema):
    _id = fields.Str(dump_only=True)  # MongoDB _id as a string, only for output
    name = fields.Str(required=True)
    device_id  = fields.Str(required=True)
    device_type = fields.Str(required=True)
    room_id = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True) #ADDED THIS
    device_category = fields.Str(required=True, default="personal")  # "personal" or "shared"


    @post_load
    def make_device(self, data, **kwargs):
         return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id and created_at before loading"""
        data.pop('_id', None)
        data.pop('created_at', None)
        return data