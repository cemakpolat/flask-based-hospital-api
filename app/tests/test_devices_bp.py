
# tests/test_devices_bp.py
import pytest
from flask import Flask
from app.blueprints.devices import devices_bp
from app.models.device import Device, DeviceSchema
from app.extensions import mongo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    mongo.init_app(app)
    app.register_blueprint(devices_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_device(client, mocker):
    # Mock the Device.save method
    mock_save = mocker.patch('app.models.device.Device.save')
    mock_save.return_value = True

    # Test data
    data = {
        "device_id": "device1",
        "device_type": "Temperature Sensor",
        "name": "Room Temperature Sensor",
        "room_id": "room1"
    }

    # Send POST request
    response = client.post('/devices', json=data)

    # Assertions
    assert response.status_code == 201
    assert response.json["message"] == "Device created successfully"

def test_get_device(client, mocker):
    # Mock the Device.get_by_id method
    mock_device = mocker.patch('app.models.device.Device.get_by_id')
    mock_device.return_value = Device(device_id="device1", device_type="Temperature Sensor", name="Room Temperature Sensor")

    # Send GET request
    response = client.get('/devices/device1')

    # Assertions
    assert response.status_code == 200
    assert response.json["device_id"] == "device1"


def test_device_save(mocker):
    # Mock the MongoDB insert_one method
    mock_insert = mocker.patch('pymongo.collection.Collection.insert_one')
    mock_insert.return_value.inserted_id = "12345"

    # Create a device and save it
    device = Device(device_id="device1", device_type="Temperature Sensor", name="Room Temperature Sensor")
    result = device.save()

    # Assertions
    assert result == True
    mock_insert.assert_called_once()