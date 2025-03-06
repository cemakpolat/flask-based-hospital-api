import asyncio
import random
import logging
from aiohttp import ClientSession
from datetime import datetime

from helper import *

rooms = []
sensors = []
patients = []
shared_devices = []
patients_devices = []
patients = []

async def simulate_rooms_and_sensors(session):
    global rooms
    rooms = generate_rooms()

    for room in rooms:
        print(room)
        async with session.post(f"{BASE_URL}/rooms", json=room, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Room created: {room}")
            else:
                logging.error(f"Failed to create room: {await response.text()}")

    global sensors 
    sensors = generate_sensors(rooms)
    sensors = assign_sensors_to_rooms(sensors, rooms)


    for sensor_data in sensors:
        async with session.post(f"{BASE_URL}/devices", json=sensor_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Room sensor created: {sensor_data}")
            else:
                logging.error(f"Failed to create room sensor: {await response.text()}")


async def simulate_shared_devices(session):
 
    global shared_devices
    shared_devices = generate_shared_devices()

    for  device_data in shared_devices:
        async with session.post(f"{BASE_URL}/devices", json=device_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Shared device created: {device_data}")
            else:
                logging.error(f"Failed to create shared device: {await response.text()}")


async def simulate_patients_and_devices(session):

    global patients, patients_devices
    patients = generate_patients(rooms)

    patients_devices = generate_personal_devices()
    patients = assign_devices_to_patients(patients, patients_devices)

    for  device_data in patients_devices:
        async with session.post(f"{BASE_URL}/devices", json=device_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Patient device created: {device_data}")
            else:
                logging.error(f"Failed to create patient device: {await response.text()}")

    
    for  patient_data in patients:
        async with session.post(f"{BASE_URL}/patients", json=patient_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Patient created: {patient_data}")
            else:
                logging.error(f"Failed to create patient: {await response.text()}")


   

async def simulate_measurements(session):
    # Simulate measurements for room sensors
    room_sensors = await get_room_sensors(session, headers=get_header_with_token(access_token=ACCESS_TOKEN))
    for sensor in room_sensors["data"]:
        measurement_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "value": await generate_sensor_data(sensor["device_type"]),
            "unit": "°C" if sensor["device_type"] == "Temperature Sensor" else "%" if sensor["device_type"] == "Humidity Sensor" else "ppm",
            "device_id": sensor["device_id"],
            "patient_id": None
        }
        async with session.post(f"{BASE_URL}/measurements/{sensor['device_id']}", json=measurement_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Measurement created for room sensor: {measurement_data}")
            else:
                logging.error(f"Failed to create measurement for room sensor: {await response.text()}")

    
# Fetch all patients
    patients = await get_all_patients(session, headers=get_header_with_token(access_token=ACCESS_TOKEN))
    if not patients:
        logging.error("No patients found.")
        return

    for patient in patients["data"]:
        patient_id = patient["patient_id"]
        device_ids = patient.get("devices", [])  # Get the list of device IDs assigned to the patient

        for device_id in device_ids:
            # Fetch the device object
            device = await get_device_by_id(session, device_id, headers=get_header_with_token(access_token=ACCESS_TOKEN))
            if not device:
                logging.error(f"Device {device_id} not found for patient {patient_id}.")
                continue
            device = device["data"]
            
            # Generate measurement data
            measurement_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "value": await generate_device_data(device["device_type"]),
                "unit": "bpm" if device["device_type"] == "Heart Rate Monitor" else "mmHg",
                "device_id": device["device_id"],
                "patient_id": patient_id
            }
            # Send the measurement to the Flask API
            async with session.post(f"{BASE_URL}/measurements/{device['device_id']}", json=measurement_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
                if response.status == 201:
                    logging.info(f"Measurement created for patient device: {measurement_data}")
                else:
                    logging.error(f"Failed to create measurement for patient device: {await response.text()}")

    # Simulate measurements for shared devices
    shared_devices = await get_shared_devices(session, headers=get_header_with_token(access_token=ACCESS_TOKEN))
    if not shared_devices:
        logging.error("No shared devices found.")
        return

    for device in shared_devices["data"]:
        # Randomly assign a patient to the shared device measurement
        patients = await get_all_patients(session, headers=get_header_with_token(access_token=ACCESS_TOKEN))
        patient_id = random.choice(patients["data"])["patient_id"] if patients["data"] else None

        measurement_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "value": await generate_device_data(device["device_type"]),
            "unit": "lbs" if device["device_type"] == "Weight Scale" else "",
            "device_id": device["device_id"],
            "patient_id": patient_id
        }

        # Send the measurement to the Flask API
        async with session.post(f"{BASE_URL}/measurements/{device['device_id']}", json=measurement_data, headers=get_header_with_token(access_token=ACCESS_TOKEN)) as response:
            if response.status == 201:
                logging.info(f"Measurement created for shared device: {measurement_data}")
            else:
                logging.error(f"Failed to create measurement for shared device: {await response.text()}")

# Global variable to store the access token
ACCESS_TOKEN = None

async def main():
    global ACCESS_TOKEN
    async with ClientSession() as session:
        await register_user(session)
        ACCESS_TOKEN = await login_user(session)
        if ACCESS_TOKEN:
            await simulate_rooms_and_sensors(session)
            await simulate_shared_devices(session)
            await simulate_patients_and_devices(session)
            while True:
                try:
                # Generate measurements every 20 seconds
                    await simulate_measurements(session)
                 # Wait for 40 seconds before the next iteration
                    logging.info("Waiting for 40 seconds before the next iteration...")
                    await asyncio.sleep(40)
                except Exception as e:
                    logging.error(f"Error in simulation loop: {e}")
                    break
        else:
            logging.error("No access token available. Cannot start device simulation.")

if __name__ == '__main__':
    asyncio.run(main())