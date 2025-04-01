from flask import Flask
from routes import app_routes
from models import db  # Import database instance
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Bind database to Flask app
migrate = Migrate(app, db)
app.register_blueprint(app_routes)  # Register routes

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
