from flask import Blueprint, request, jsonify
from models import db, Workers

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'login' not in data or 'password' not in data or 'email' not in data:
        return jsonify({"message": "Missing fields"}), 400

    worker = Workers(
        name=data.get('name'),
        title=data.get('title'),
        login=data['login'],
        email=data['email']
    )
    worker.set_password(data['password'])
    db.session.add(worker)
    db.session.commit()
    return jsonify({"message": "Worker registered successfully"}), 201


@bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    worker = Workers.query.filter_by(login=data['login']).first()
    if worker and worker.check_password(data['old_password']):
        worker.set_password(data['new_password'])
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 400
