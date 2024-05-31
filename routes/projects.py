from flask import Blueprint, request, jsonify
from models import db, Projects
from routes.auth import basic_auth_required


bp = Blueprint('projects', __name__, url_prefix='/projects')

# creating project
@bp.route('/', methods=['POST'])
@basic_auth_required # checks authorization
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

# list of projects
@bp.route('/', methods=['GET'])
@basic_auth_required # and here
def get_projects():
    projects = Projects.query.all()
    return jsonify([project.to_dict() for project in projects]), 200

# updating project (duh)
@bp.route('/<int:project_id>', methods=['PUT'])
@basic_auth_required # and here too
def update_project(project_id):
    data = request.get_json()
    project = Projects.query.get_or_404(project_id)
    project.description = data.get('description', project.description)
    project.manager = data.get('manager', project.manager)
    db.session.commit()
    return jsonify({"message": "Project updated successfully"}), 200
