from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Zoo, Animal, User, ZooCustomization, Role, Event, EventType, Group, Membership, AnimalEvent, AnimalComment, UserEvent, AnimalAudit, AnimalHealthLog, AnimalActivityLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:thezoo801@localhost/openhamshogelzoodb'
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def home():
    return "Welcome to OpenHAMSv8"

if __name__ == '__main__':
    app.run(debug=True)