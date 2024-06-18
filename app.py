from flask import Flask, current_app
from config import Config
from models import db
from routes import auth, projects
from errors import handle_http_exception, handle_validation_error, handle_generic_error
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from logging_config import setup_logging
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(projects.bp)

# Setup logging
logger = setup_logging()

# Register error handlers
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(Exception, handle_generic_error)


@app.route('/')
def home():
    return {"message": "Welcome to the API"}

# Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    app.logger.info("Ping request received")
    return {"message": "pong"}, 200


if __name__ == '__main__':
    app.run(debug=True)
