from app.models.device import Device
from app.models.measurement import Measurement
from datetime import datetime, timedelta

def get_average_temperature_last_hour(device_id):
    """
    Calculates the average temperature for a given device over the last hour.
    """
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    measurements = Measurement.get_by_sensor_id(device_id)

    if not measurements:
        return None

    #Filter for values in the last hour.
    recent_measurements = []
    for measurement in measurements:
        if measurement.timestamp < now and measurement.timestamp > one_hour_ago:
            recent_measurements.append(measurement)
    
    #Extract the values for the relevant objects and do processing
    total_temp = 0
    num_measurements = 0
    for measurement in recent_measurements:
        try:
            total_temp += float(measurement.value) #If other types are present, this might be more complex
            num_measurements+=1
        except:
            pass
    
    if num_measurements == 0:
        return None

    return total_temp / num_measurements