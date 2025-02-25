from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required

def roles_required(*roles):
    """Decorator for enforcing multiple role-based access control."""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in roles:
                return jsonify({"msg": "Unauthorized"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator