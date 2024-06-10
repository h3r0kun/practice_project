from flask import Blueprint, request, jsonify
from models import db, Projects
from routes.auth import basic_auth_required
from schemas import ProjectSchema
from pydantic import ValidationError

bp = Blueprint('projects', __name__, url_prefix='/projects')

# creating project
@bp.route('/', methods=['POST'])
@basic_auth_required
def create_project(worker):
    data = request.get_json()
    try:
        project_data = ProjectSchema(**data)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    project = Projects(
        name=project_data.name,
        description=project_data.description,
        manager=project_data.manager,
        start_date=project_data.start_date
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created successfully"}), 201

# list of projects
@bp.route('/', methods=['GET'])
@basic_auth_required
def get_projects(worker):
    projects = Projects.query.all()
    projects_data = [ProjectSchema.from_orm(project).dict() for project in projects]
    return jsonify(projects_data), 200

# updating project
@bp.route('/<int:project_id>', methods=['PUT'])
@basic_auth_required
def update_project(worker, project_id):
    data = request.get_json()
    project = Projects.query.get_or_404(project_id)
    try:
        project_data = ProjectSchema(**data, partial=True)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    project.description = project_data.description or project.description
    project.manager = project_data.manager or project.manager
    db.session.commit()
    return jsonify({"message": "Project updated successfully"}), 200
