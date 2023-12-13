from flask import Flask
from flask_vite import Vite
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_smorest import Api

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/openhamshogelzoodb'

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
vite = Vite(app)
api = Api(app)

# Import models and views after initializing app to avoid circular imports
from .models import Zoo, Animal, User, ZooCustomization, Role, Event, EventType, Group, Membership, AnimalEvent, AnimalComment, UserEvent, AnimalAudit, AnimalHealthLog, AnimalActivityLog
from .views import animals_blueprint

# Register blueprints
app.register_blueprint(animals_blueprint, url_prefix='/animals')

@app.route('/')
def home():
    return "Welcome to OpenHAMSv8"
