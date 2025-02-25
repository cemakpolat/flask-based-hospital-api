# tests/test_services.py
import pytest
from app.services.data_transformation_service import generate_device_data

def test_generate_device_data():
    # Test heart rate monitor
    heart_rate = generate_device_data("Heart Rate Monitor")
    assert 50 <= heart_rate <= 120

    # Test blood pressure monitor
    blood_pressure = generate_device_data("Blood Pressure Monitor")
    systolic, diastolic = map(int, blood_pressure.split('/'))
    assert 90 <= systolic <= 140
    assert 60 <= diastolic <= 90