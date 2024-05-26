from flask import Flask
from config import Config
from models import db
from routes import auth, projects

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Регистрация блюпринтов
app.register_blueprint(auth.bp)
app.register_blueprint(projects.bp)

@app.route('/ping', methods=['GET'])
def ping():
    return {"message": "pong"}, 200

if __name__ == '__main__':
    app.run(debug=True)
