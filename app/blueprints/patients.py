from app.utils.responses import success_response, error_response
from flask import Blueprint, request, jsonify
from app.models.patient import Patient, PatientSchema
from app.extensions import mongo
from marshmallow import ValidationError  # Import ValidationError
from app.services.data_transformation_service import enrich_patient_data  # Import the service
from app.utils.auth_utils import roles_required

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

@patients_bp.route('', methods=['POST'])
@roles_required('admin', 'user')
def create_patient():
    """Creates a new patient."""
    try:
        data = request.get_json()
        validated_data = patient_schema.load(data)
        patient = Patient(**validated_data)
        patient.save()
        return success_response(patient_schema.dump(patient), "Patient created successfully", 201)
    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

@patients_bp.route('/<string:patient_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_patient(patient_id):
    """Retrieves a patient by ID."""
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return error_response("Patient not found", 404)
        return success_response(patient_schema.dump(patient))
    except Exception as e:
        return error_response(str(e), 500)

@patients_bp.route('', methods=['GET'])
@roles_required('admin', 'user')
def get_all_patients():
    """Lists all patients."""
    try:
        patients = Patient.get_all()
        return success_response(patients_schema.dump(patients))
    except Exception as e:
        return error_response(str(e), 500)

@patients_bp.route('/<string:patient_id>', methods=['PUT'])
@roles_required('admin', 'user')
def update_patient(patient_id):
    """Updates an existing patient."""
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return error_response("Patient not found", 404)

        data = request.get_json()
        validated_data = patient_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(patient, key, value)

        patient.save()
        return success_response(patient_schema.dump(patient), "Patient updated successfully")

    except ValidationError as e:
        return error_response(e.messages, 400)
    except Exception as e:
        return error_response(str(e), 500)

@patients_bp.route('/<string:patient_id>', methods=['DELETE'])
@roles_required('admin', 'user')
def delete_patient(patient_id):
    """Deletes a patient."""
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return error_response("Patient not found", 404)

        if patient.delete():
            return success_response(message="Patient deleted successfully", status_code=200)
        else:
            return error_response("Failed to delete patient", 500)
    except Exception as e:
        return error_response(str(e), 500)
    
@patients_bp.route('/<string:patient_id>/enriched', methods=['GET'])
@roles_required('admin', 'user')
def get_enriched_patient_data(patient_id):
    """Retrieves a patient's data and the corresponding enriched data"""
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return error_response("Patient not found", 404)
        
        enriched_data = enrich_patient_data(patient)
        if enriched_data:
            return success_response(enriched_data)
        else:
            return error_response("Room information not found for patient", 404)
        
    except Exception as e:
        return error_response(str(e), 500)

# TODO: Test this funcitonality
@patients_bp.route('/patients/<patient_id>', methods=['GET'])
@roles_required('admin', 'user')
def get_patient_details(patient_id):
    patient_details = Patient.get_patient_details(patient_id)
    if not patient_details:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient_details), 200