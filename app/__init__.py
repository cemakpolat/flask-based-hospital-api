from flask import Flask
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from config import Config
from .errors import register_error_handlers
from flask_cors import CORS


from app.extensions import  make_celery, marshmallow, jwt

application = Flask(__name__)
CORS(application)
application.config.from_object(Config)

jwt.init_app(application)
socketio = SocketIO(application, message_queue=application.config['SOCKETIO_MESSAGE_QUEUE'], cors_allowed_origins="*")
marshmallow.init_app(application)
celery = make_celery(application)

# Register error handlers
register_error_handlers(application)


# Register blueprints
from .blueprints.patients import patients_bp
from .blueprints.devices import devices_bp
from .blueprints.rooms import rooms_bp
from .blueprints.auth import auth_bp
from .blueprints.measurements import measurement_bp
from .blueprints.tasks import tasks_bp

application.register_blueprint(patients_bp, url_prefix='/api/patients')
application.register_blueprint(devices_bp, url_prefix='/api/devices')
application.register_blueprint(rooms_bp, url_prefix='/api/rooms')
application.register_blueprint(auth_bp, url_prefix='/api/auth')
application.register_blueprint(tasks_bp, url_prefix='/api/tasks')
application.register_blueprint(measurement_bp, url_prefix='/api/measurements')


# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")
#     emit('celery_data_received', {'status': 'success', 'data': 'Welcome!'})

# # Add this to your Flask app to listen for messages from Celery
# @socketio.on('data_from_celery')
# def handle_data_from_celery(data):
#     print(f"Received data from Celery: {data}")
#     socketio.emit('celery_data_received', data)