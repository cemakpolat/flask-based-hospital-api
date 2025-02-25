from app import application, celery
from flask_socketio import SocketIO
from config import Config
import time
from celery.exceptions import Retry

@celery.task(name="long_task", autoretry_for=(Retry,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def long_task(sensor_id):
    """
    Simulates a long-running task (e.g., data processing) and then sends the result via WebSocket.
    """
    # Simulate a long-running task
    time.sleep(3)  
    result = f"Processed data for sensor {sensor_id} at {time.time()}"
    with application.app_context():
        send_message(result)
    return result



def send_message(message):
    socketio = SocketIO(application, message_queue=application.config['SOCKETIO_MESSAGE_QUEUE']) 
    socketio.emit('celery_data_received', {'status': 'success', 'data': message})
