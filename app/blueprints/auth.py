from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.models.user import User, UserSchema
from app.utils.responses import success_response, error_response
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if User.get_by_username(username):
            return error_response("Username already exists", 400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, password=hashed_password, role=role)
        user.save()
        return success_response(message="User registered successfully", status_code=201)
    except Exception as e:
        return error_response(str(e), 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.get_by_username(username)
        if not user or not User.verify_password(user.password, password):
            return error_response("Invalid username or password", 401)

        access_token = create_access_token(
            identity=user.username,  # Identity must be a string or int
            additional_claims={"role": user.role}  # Store role separately
        )
        
        return success_response({'access_token': access_token}, "Login successful")
    except Exception as e:
        return error_response(str(e), 500)