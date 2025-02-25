# tests/test_device_model_integration.py
import pytest
from app.models.device import Device
from app.extensions import mongo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    mongo.init_app(app)
    return app

def test_device_save(app):
    with app.app_context():
        # Create a device and save it
        device = Device(device_id="device1", device_type="Temperature Sensor", name="Room Temperature Sensor")
        result = device.save()

        # Assertions
        assert result == True

        # Verify the device was saved in the database
        saved_device = mongo.db.devices.find_one({"device_id": "device1"})
        assert saved_device is not None
        assert saved_device["device_type"] == "Temperature Sensor"

        # Clean up
        mongo.db.devices.delete_one({"device_id": "device1"})