from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """Format a successful response"""
    response_data = {"message": message}

    if data is not None:
        response_data["data"] = data
    response = jsonify(response_data)
    response.status_code = status_code
    return response

def error_response(message="An error occurred", status_code=400):
    """Format an error response."""
    response = jsonify({"error": message})
    response.status_code = status_code
    return response