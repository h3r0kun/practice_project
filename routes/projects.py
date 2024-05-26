from flask import Blueprint, request, jsonify
from models import db, Projects

bp = Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Projects(
        name=data['name'],
        description=data['description'],
        manager=data['manager'],
        start_date=data['start_date']
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created successfully"}), 201

@bp.route('/', methods=['GET'])
def get_projects():
    projects = Projects.query.all()
    return jsonify([project.to_dict() for project in projects]), 200

@bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    project = Projects.query.get_or_404(project_id)
    project.description = data.get('description', project.description)
    project.manager = data.get('manager', project.manager)
    db.session.commit()
    return jsonify({"message": "Project updated successfully"}), 200
