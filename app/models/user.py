
from app.extensions import mongo
import bcrypt
from marshmallow import Schema, fields, post_load, pre_load
from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, password, role='user', _id=None):
        self.username = username
        self.password = password
        self.role = role
        self._id = _id

    def save(self):
        """Saves the user to the database."""
        user_data = UserSchema().dump(self)
        if self._id:
            result = mongo.db.users.update_one({'_id': ObjectId(self._id)}, {'$set': user_data})
            if result.modified_count == 0:
                raise Exception("User not found or no changes applied")
            return True
        else:
            user_data.pop('_id', None)
            result = mongo.db.users.insert_one(user_data)
            self._id = result.inserted_id
            return self

    @staticmethod
    def get_by_username(username):
        """Retrieves a user by username."""
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return UserSchema().load(user_data)
        return None

    @staticmethod
    def verify_password(hashed_password, password):
        """Verifies the password."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserSchema(Schema):
    _id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True, default='user')

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
    

    # @post_load
    # def make_sensor(self, data, **kwargs):
    #     return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id and created_at before loading"""
        data.pop('_id', None)
        return data