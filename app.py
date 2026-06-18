from routes.auth_routes import auth_bp
from flask import Flask
from dotenv import load_dotenv
import os
from database import *
from flask_jwt_extended import JWTManager

from routes.message_route import message_bp
from routes.user_routes import user_bp

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jwt_secret_key')

JWTManager(app)

# routes
app.register_blueprint(auth_bp)
app.register_blueprint(message_bp)
app.register_blueprint(user_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/message')
def message():
    return "Message"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
