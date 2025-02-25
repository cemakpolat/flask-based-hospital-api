from app.extensions import mongo
from marshmallow import Schema, fields, post_load, pre_load
from datetime import datetime
from bson import ObjectId

class Patient:
    def __init__(self, name, room_id,patient_id, devices=None, _id=None, created_at=None, state=None):
        self.name = name
        self.room_id = room_id
        self.patient_id = patient_id
        self.state = state
        self.devices = devices
        self._id = _id
        self.created_at = created_at  # Add created_at

    def save(self):
        """Saves the patient to the database."""
        patient_data = PatientSchema().dump(self)
        if self._id:
            result = mongo.db.patients.update_one({'_id': ObjectId(self._id)}, {'$set': patient_data})
            if result.modified_count == 0:
                raise Exception("Patient not found or no changes applied") # General exception
            return True
        else:
            patient_data.pop('_id', None)  # Remove _id from the data
            result = mongo.db.patients.insert_one(patient_data)
            self._id = result.inserted_id
            return self


    def delete(self):
        """Deletes the patient from the database."""
        if self._id:
            result = mongo.db.patients.delete_one({'_id': ObjectId(self._id)})
            if result.deleted_count == 0:
               raise Exception("Patient not found") # General exception
            return True
        return False

    @staticmethod
    def get_by_id(patient_id):
        """Retrieves a patient by ID."""
        patient_data = mongo.db.patients.find_one({'_id': ObjectId(patient_id)})
        if patient_data:
            return PatientSchema().load(patient_data)
        return None

    @staticmethod
    def get_all():
        """Retrieves all patients from the database."""
        patients_data = list(mongo.db.patients.find())
        return PatientSchema(many=True).load(patients_data)

    def __repr__(self):
        return f"<Patient(name='{self.name}', room_id='{self.room_id}')>"

    # TODO: Test this funcitonality
    def get_patient_details(self, patient_id):
        # Fetch patient details
        patient = self.collection.find_one({'_id': patient_id})
        if not patient:
            return None

        # Fetch life data from patient-specific devices
        life_data = list(self.device_collection.find({
            'patient_id': patient_id,
            'is_shared': False
        }))

        # Fetch shared device data associated with the patient
        shared_data = list(self.device_collection.find({
            'patient_id': patient_id,
            'is_shared': True
        }))

        return {
            'patient': patient,
            'life_data': life_data,
            'shared_data': shared_data
        }
    
class PatientSchema(Schema):
    _id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    patient_id = fields.Str(required=True)
    room_id = fields.Str(required=True)
    devices = fields.List(fields.Str(), allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    state = fields.Str(required=True)

    @post_load
    def make_patient(self, data, **kwargs):
        return data

    @pre_load
    def remove_extra_fields(self, data, **kwargs):
        """Remove _id and created_at before loading"""
        data.pop('_id', None)
        data.pop('created_at', None)
        return data