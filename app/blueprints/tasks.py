from flask import Blueprint, jsonify
from app.celery_tasks import long_task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/start_task/<string:sensor_id>', methods=['POST'])
def start_task(sensor_id):
    # Trigger the Celery task
    task = long_task.delay(sensor_id)
    print("Task started")
    return jsonify({"task_id": task.id, "status": "Task started"}), 202