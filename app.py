from flask import Flask
from routes import app_routes
from models import db  # Import database instance
from flask_migrate import Migrate
import os
import logging
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db' # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

bcrypt=Bcrypt()
bcrypt.init_app(app)
db.init_app(app)  # Bind database to Flask app
migrate = Migrate(app, db)
app.register_blueprint(app_routes)  # Register routes

logging.basicConfig(
    level=logging.DEBUG,  # Change to ERROR in production
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.logger.info("hi app started")
    app.run(debug=True)
