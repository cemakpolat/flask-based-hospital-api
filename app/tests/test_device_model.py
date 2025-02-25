# tests/test_device_model.py
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
        device = Device(device_id="device1", device_type="Temperature Sensor", name="Room Temperature Sensor")
        assert device.save() == True

def test_device_get_by_id(app):
    with app.app_context():
        device = Device(device_id="device1", device_type="Temperature Sensor", name="Room Temperature Sensor")
        device.save()
        retrieved_device = Device.get_by_id("device1")
        assert retrieved_device.device_id == "device1"