import random
import logging
import uuid
from datetime import datetime
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL of the Flask app
BASE_URL = "http://flask-app:5000/api"

# User credentials for authentication
USERNAME = "admin"
PASSWORD = "admin123"



# Configuration
NUM_ROOMS = 2
NUM_PATIENTS = 2
NUM_DEVICES_PER_PATIENT = 3
NUM_SHARED_DEVICES = 2

DEVICE_TYPES_PERSONAL = [
    "Heart Rate Monitor",
    "Blood Pressure Cuff",
    "Pulse Oximeter",
    "Continuous Glucose Monitor (CGM)",
    "Activity Tracker",
    "Smart Inhaler",
]

DEVICE_TYPES_SHARED = [
    "Defibrillator",
    "Ventilator",
    "Infusion Pump",
    "ECG Machine",
    "Ultrasound Machine",
    "MRI Scanner",
    "CT Scanner",
    "X-Ray Machine",
    "EEG Machine",
    "Dialysis Machine",
    "Anesthesia Machine",
    "Electrosurgical Unit",
    "Patient Warming System",
    "Blood Gas Analyzer",
    "Automated Medication Dispensing System",
]

SENSOR_TYPES = ["Temperature", "Humidity", "CO2 Level"]

REALISTIC_RANGES = {
    "Heart Rate Monitor": (50, 120),
    "Blood Pressure Cuff": ((90, 140), (60, 90)),
    "Pulse Oximeter": (90, 100),
    "Continuous Glucose Monitor (CGM)": (70, 200),
    "Activity Tracker": (0, 15000),
    "Smart Inhaler": (0, 5),
    "Defibrillator": (200, 360),
    "Ventilator": (12, 20),
    "Infusion Pump": (1, 50),
    "ECG Machine": "Normal Sinus Rhythm",
    "Ultrasound Machine": "Image Acquired",
    "MRI Scanner": "Scan Complete",
    "CT Scanner": "Scan Complete",
    "X-Ray Machine": "Image Captured",
    "EEG Machine": "Reading Stable",
    "Dialysis Machine": "Cycle Complete",
    "Anesthesia Machine": "Stable Anesthesia Levels",
    "Electrosurgical Unit": "Ready",
    "Patient Warming System": (36, 38),
    "Blood Gas Analyzer": "Analysis Complete",
    "Automated Medication Dispensing System": "Medication Dispensed",
    "Temperature": (18, 25),
    "Humidity": (30, 70),
    "CO2 Level": (400, 1000),
}


def generate_id(prefix=""):
    """
    Generates a short, unique ID using a shortened UUID.
    Args:
        prefix (str): A prefix to add to the ID (e.g., "device_" or "patient_").
    Returns:
        str: A unique ID.
    """
    # Generate a UUID and take the first 8 characters
    short_id = str(uuid.uuid4())[:8]
    
    return f"{prefix}{short_id}"
def assign_patients_to_rooms(patients, rooms):
    """
    Assigns patients to rooms randomly
    """
    for patient in patients:
        patient["room_id"] = random.choice(rooms)["room_id"]
    return patients
    

def assign_devices_to_patients(patients, devices):
    """
    Assigns devices to patients randomly
    """
    for device in devices:
        patient = random.choice(patients)
        patient["devices"].append(device["device_id"]) 
    logging.info(f"Assigned devices to patients: {patients}")
    return patients

def assign_sensors_to_rooms(sensors, rooms):
    """
    Assigns room sensors to all rooms
    """
    
    for room in rooms:
        for sensor in sensors:
            sensor["room_id"] = room["room_id"]
    return sensors


def generate_rooms():
    """
    Generates rooms
    """
    rooms = []
    for i in range(NUM_ROOMS):
        rooms.append({
            "room_id": f"room_{i}",
            "name": f"Room {i}"
        })
    return rooms

def generate_patients(rooms):
    """
    Generates patients
    """
    patients = []
    for i in range(NUM_PATIENTS):
        patients.append({
            "patient_id": f"patient_{generate_id()}",
            "name": f"Patient {i}", 
            "room_id": random.choice(rooms)["room_id"],
            "state": "Processing",
            "devices": []
        })
        
    return patients


def generate_personal_devices():
    personal_devices = []
    for i in range(len(DEVICE_TYPES_PERSONAL)):
        personal_devices.append({
            "device_id": f"device_personal_{generate_id()}",
            "name": f"Personal Device {i}", 
            "device_type": random.choice(DEVICE_TYPES_PERSONAL),        
            "device_category": "personal",
            "room_id": None
        })
    return personal_devices 

def generate_shared_devices():
    shared_devices = []
    for i in range(NUM_SHARED_DEVICES):
        shared_devices.append({
            "device_id": f"device_shared_{generate_id()}",
            "name": f"Shared Device {i}",
            "device_type": random.choice(DEVICE_TYPES_SHARED),
            "device_category": "shared",
            "room_id": None
        })
    return shared_devices


def generate_sensors(rooms):
    sensors = []
    for i in range(len(SENSOR_TYPES)):
        sensors.append({
            "device_id": f"sensor_{generate_id()}",
            "name": f"Sensor {i}",
            "device_type": SENSOR_TYPES[i],
            "device_category": "sensor",
            "room_id": random.choice(rooms)["room_id"]
        })
    return sensors






async def generate_device_data(device_type):
    if device_type in REALISTIC_RANGES:
        range_value = REALISTIC_RANGES[device_type]
        if isinstance(range_value, tuple):
            if isinstance(range_value[0], tuple):  # For Blood Pressure Cuff
                systolic = random.randint(range_value[0][0], range_value[0][1])
                diastolic = random.randint(range_value[1][0], range_value[1][1])
                return {"systolic": systolic, "diastolic": diastolic}
            else:  # For numeric ranges
                return random.randint(range_value[0], range_value[1])
        else:  # For status-based devices
            return range_value
    return 0 # TODO find a better way to handle this

async def generate_sensor_data(sensor_type):
    if sensor_type in REALISTIC_RANGES:
        range_value = REALISTIC_RANGES[sensor_type]
        if isinstance(range_value, tuple):
            return random.randint(range_value[0], range_value[1])
        else:  # For status-based sensors
            return range_value
    return 0 # TODO find a better way to handle this


async def get_shared_devices(session, headers):
    """Fetches all shared devices."""
    async with session.get(f"{BASE_URL}/devices/shared", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch shared devices: {await response.text()}")
            return {"data": []}

async def get_device_by_id(session, device_id, headers):
    """Fetches a device by its ID."""
    async with session.get(f"{BASE_URL}/devices/{device_id}", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch device {device_id}: {await response.text()}")
            return None
        
async def get_room_sensors(session, headers):
    async with session.get(f"{BASE_URL}/devices/room/notnulls", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch room sensors: {await response.text()}")
            return []
        
async def get_all_patients(session, headers):
    """Fetches all patients from the database."""
    async with session.get(f"{BASE_URL}/patients", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch patients: {await response.text()}")
            return {"data": []}
        
async def generate_device_data(device_type):
    if device_type == "Heart Rate Monitor":
        return random.randint(60, 100)  # Simulate heart rate in bpm
    elif device_type == "Blood Pressure Monitor":
        return f"{random.randint(90, 120)}/{random.randint(60, 80)}"  # Simulate blood pressure in mmHg
    else:
        return 0  # Default value for unknown device types

async def get_device_by_id(session, device_id, headers):
    """Fetches a device by its ID."""
    async with session.get(f"{BASE_URL}/devices/{device_id}", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch device {device_id}: {await response.text()}")
            return None
        
async def get_devices(session, headers):
    async with session.get(f"{BASE_URL}/devices", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logging.error(f"Failed to fetch shared devices: {await response.text()}")
            return []
        

async def register_user(session):
    """Register a user if not already registered."""
    try:
        user_data = {
            "username": USERNAME,
            "password": PASSWORD,
            "role": "admin"
        }
        async with session.post(f"{BASE_URL}/auth/register", json=user_data) as response:
            if response.status == 201:
                logging.info("User registered successfully.")
            elif response.status == 400 and "Username already exists" in await response.text():
                logging.info("User already exists.")
            else:
                logging.error(f"Failed to register user: {response.status} - {await response.text()}")
    except Exception as e:
        logging.error(f"Error registering user: {e}")


async def login_user(session):
    """Log in the user and obtain an access token."""
    
    try:
        login_data = {
            "username": USERNAME,
            "password": PASSWORD
        }
        async with session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
            if response.status == 200:
                data = await response.json()
                
                access_token = data["data"]["access_token"]
                logging.info("User logged in successfully.")
                return access_token
            else:
                logging.error(f"Failed to log in user: {response.status} - {await response.text()}")
    except Exception as e:
        logging.error(f"Error logging in user: {e}")


def get_header_with_token(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }