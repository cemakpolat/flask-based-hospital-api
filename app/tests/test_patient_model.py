# tests/test_patient_model.py
import pytest
from app.models.patient import Patient
from app.extensions import mongo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    mongo.init_app(app)
    return app

def test_patient_save(app):
    with app.app_context():
        patient = Patient(patient_id="patient1", name="Alice Smith", room_id="room1")
        assert patient.save() == True

def test_patient_get_by_id(app):
    with app.app_context():
        patient = Patient(patient_id="patient1", name="Alice Smith", room_id="room1")
        patient.save()
        retrieved_patient = Patient.get_by_id("patient1")
        assert retrieved_patient.patient_id == "patient1"