import logging
from flask import jsonify

logging.basicConfig(level=logging.ERROR, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')

class APIError(Exception):
    """Custom exception class for API errors"""
    
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
    def to_dict(self):
        return {"error":self.message}

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logging.error(f"API Error: {error.message}")
        response = jsonify(error.to_dict())
        response.status_code= error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found_error(error):
        logging.error("Not Found: 404")
        return jsonify({"error":"Not Found"}), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        logging.error("Internal Server Error: 500")
        return jsonify({"error":"Internal Server Error"}), 500