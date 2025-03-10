from flask_socketio import SocketIO
from pymongo import MongoClient
from config import Config
from flask_marshmallow import Marshmallow
from celery import Celery
from flask_jwt_extended import JWTManager

mongo = MongoClient(Config.MONGO_URI).hospital_db
marshmallow = Marshmallow() 
jwt = JWTManager()

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery