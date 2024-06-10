from flask import Flask
from config import Config
from models import db
from routes import auth, projects
from errors import handle_http_exception, handle_validation_error, handle_generic_error
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(projects.bp)

# Register error handlers
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(Exception, handle_generic_error)

# Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return {"message": "pong"}, 200

if __name__ == '__main__':
    app.run(debug=True)
