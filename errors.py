from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "error": {
            "code": e.code,
            "name": e.name,
            "description": e.description
        }
    })
    response.content_type = "application/json"
    return response

def handle_validation_error(e):
    return jsonify({
        "error": {
            "code": 400,
            "name": "Validation Error",
            "description": e.errors()
        }
    }), 400

def handle_generic_error(e):
    return jsonify({
        "error": {
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unexpected error occurred."
        }
    }), 500
class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def handle_custom_error(e):
    return jsonify({
        "error": {
            "code": 400,
            "name": "Custom Error",
            "description": e.message
        }
    }), 400

# Add to error handler registration
app.register_error_handler(CustomError, handle_custom_error)
