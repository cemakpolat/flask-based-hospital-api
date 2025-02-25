import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/hospital_db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')
    JWT_IDENTITY_CLAIM = os.getenv('JWT_IDENTITY_CLAIM', 'sub')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://redis:6379/0'
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE') or 'redis://redis:6379/0'
    CELERY_IMPORTS = ('app.celery_tasks',)