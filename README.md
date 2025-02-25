
# Hospital Data Simulator with Flask and MongoDB

This project simulates a hospital environment where patients, rooms, devices, and sensors generate data. The data is stored in MongoDB, and the Flask app provides APIs to interact with the data.

## Features

- **Patients**: Create and manage patients, assign them to rooms, and track their devices.
- **Rooms**: Create rooms and assign sensors to monitor environmental conditions.
- **Devices**: Manage devices (e.g., heart rate monitors, temperature sensors) and associate them with patients or rooms.
- **Measurements**: Generate and store measurements from devices and sensors.

- JWT Authentication
- MongoDB User Storage
- Role-Based Access Control (RBAC)
- Blueprint Modular Structure
- Marshmallow for Data Validation

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
