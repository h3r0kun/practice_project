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
