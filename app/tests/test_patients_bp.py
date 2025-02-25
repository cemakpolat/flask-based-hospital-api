# tests/test_patients_bp.py
import pytest
from flask import Flask
from app.blueprints.patients import patients_bp
from app.models.patient import Patient, PatientSchema
from app.extensions import mongo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    mongo.init_app(app)
    app.register_blueprint(patients_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_patient(client, mocker):
    # Mock the Patient.save method
    mock_save = mocker.patch('app.models.patient.Patient.save')
    mock_save.return_value = True

    # Test data
    data = {
        "patient_id": "patient1",
        "name": "Alice Smith",
        "room_id": "room1",
        "devices": ["device1"]
    }

    # Send POST request
    response = client.post('/patients', json=data)

    # Assertions
    assert response.status_code == 201
    assert response.json["message"] == "Patient created successfully"

def test_get_patient(client, mocker):
    # Mock the Patient.get_by_id method
    mock_patient = mocker.patch('app.models.patient.Patient.get_by_id')
    mock_patient.return_value = Patient(patient_id="patient1", name="Alice Smith", room_id="room1")

    # Send GET request
    response = client.get('/patients/patient1')

    # Assertions
    assert response.status_code == 200
    assert response.json["patient_id"] == "patient1"