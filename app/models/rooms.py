from app.extensions import mongo
from marshmallow import Schema, fields, post_load, pre_load
from datetime import datetime
from bson import ObjectId

class Room:
    def __init__(self, name, room_id, _id=None, created_at=None):
        self.name = name
        self.room_id = room_id
        self._id = _id
        self.created_at = created_at

    def save(self):
        """Saves the room to the database."""
        room_data = RoomSchema().dump(self)
        if self._id:
            result = mongo.db.rooms.update_one({'_id': ObjectId(self._id)}, {'$set': room_data})
            return result.modified_count > 0
        else:
            room_data.pop('_id', None)  # Remove _id from the data
            result = mongo.db.rooms.insert_one(room_data)
            self._id = result.inserted_id
            return self

    def delete(self):
        """Deletes the room from the database."""
        if self._id:
            result = mongo.db.rooms.delete_one({'_id': ObjectId(self._id)})
            return result.deleted_count > 0
        return False

    @staticmethod
    def get_by_id(room_id):
        """Retrieves a room by ID."""
        room_data = mongo.db.rooms.find_one({'_id': ObjectId(room_id)})
        if room_data:
            return RoomSchema().load(room_data)
        return None

    @staticmethod
    def get_all():
        """Retrieves all rooms from the database."""
        rooms_data = list(mongo.db.rooms.find())
        return RoomSchema(many=True).load(rooms_data)

    def __repr__(self):
        return f"<Room(name='{self.name}')>"


class RoomSchema(Schema):
    _id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    room_id = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_room(self, data, **kwargs):
        return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id and created_at before loading"""
        data.pop('_id', None)
        data.pop('created_at', None)
        return data