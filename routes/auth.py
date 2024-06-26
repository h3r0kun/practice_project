from flask import Blueprint, request, jsonify
from models import db, Workers
from functools import wraps
from schemas import WorkerSchema
from pydantic import ValidationError
import traceback
from werkzeug.security import check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

# registration
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)
    try:
        worker_data = WorkerSchema(**data)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    worker = Workers(
        name=worker_data.name,
        title=worker_data.title,
        login=worker_data.login,
        email=worker_data.email
    )
    worker.set_password(worker_data.password)
    db.session.add(worker)
    db.session.commit()
    return jsonify({"message": "Worker registered successfully"}), 201


# change password
@bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    login = data.get('login')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    worker = Workers.query.filter_by(login=login).first()

    if worker and worker.check_password(old_password):
        worker.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 400


# basic authorization
def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"message": "Invalid credentials"}), 401

        worker = Workers.query.filter_by(login=auth.username).first()
        if worker and check_password_hash(worker.password, auth.password):
            return f(worker, *args, **kwargs)
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    return decorated
