## Patient details API

{
  "patient": {
    "_id": "65f4c8e1b4f4a3e4f4a3e4f4",
    "name": "Patient 1",
    "room_id": 1,
    "device_ids": ["device_1_1", "device_1_2"],
    "created_at": "2025-02-16T12:34:56.789Z"
  },
  "life_data": [
    {
      "_id": "65f4c8e1b4f4a3e4f4a3e4f5",
      "name": "Heart Rate Monitor for Patient 1",
      "type": "Heart Rate Monitor",
      "is_shared": false,
      "data": 72,
      "patient_id": 1,
      "room_id": null,
      "created_at": "2025-02-16T12:35:00.123Z"
    },
    {
      "_id": "65f4c8e1b4f4a3e4f4a3e4f6",
      "name": "Blood Pressure Cuff for Patient 1",
      "type": "Blood Pressure Cuff",
      "is_shared": false,
      "data": "120/80 mmHg",
      "patient_id": 1,
      "room_id": null,
      "created_at": "2025-02-16T12:35:05.456Z"
    }
  ],
  "shared_data": [
    {
      "_id": "65f4c8e1b4f4a3e4f4a3e4f7",
      "name": "Defibrillator (Shared) for Patient 1",
      "type": "Defibrillator",
      "is_shared": true,
      "data": 300,
      "patient_id": 1,
      "room_id": null,
      "created_at": "2025-02-16T12:35:10.789Z"
    }
  ]
}


# Hospital Data Simulator with Flask and MongoDB

This project simulates a hospital environment where patients, rooms, devices, and sensors generate data. The data is stored in MongoDB, and the Flask app provides APIs to interact with the data.

## Features

- **Patients**: Create and manage patients, assign them to rooms, and track their devices.
- **Rooms**: Create rooms and assign sensors to monitor environmental conditions.
- **Devices**: Manage devices (e.g., heart rate monitors, temperature sensors) and associate them with patients or rooms.
- **Measurements**: Generate and store measurements from devices and sensors.

 JWT Authentication
✅ MongoDB User Storage
✅ Role-Based Access Control (RBAC)
✅ Blueprint Modular Structure
✅ Marshmallow for Data Validation

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
    ```
2. Run MongoDB:
Ensure MongoDB is running locally or update the 
`MONGO_URI` in `app/extensions.py`.

3. Run the Flask App:

```bash
flask run
```
4. Run the Simulator:

```bash
python simulator.py
```

## API Endpoints

Patients: `/api/patients`

Rooms: `/api/rooms`

Devices: `/api/devices`

Measurements: `/api/measurements`

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Test Run Locally
```bash
docker run -d -p 27017:27017 --name test-mongo mongo:latest
docker run -d -p 27017:27017 --name test-mongo mongo:latest
docker stop test-mongo
docker rm test-mongo

```
## Login to get the access token

```bash
curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{
    "username": "test",
    "password": "test"
}'
## Get the access token  and use it to create a device

```bash
curl -X POST http://localhost:5000/api/devices -H "Content-Type: application/json" \
-H "Authorization: Bearer <access_token>" \
-d '{
    "name": "Device 1",
    "device_id": "12345",
    "device_type": "Sensor",
    "room_id": "Room101",
    "device_category": "personal"
}'
```


## License

This project is licensed under the MIT License.