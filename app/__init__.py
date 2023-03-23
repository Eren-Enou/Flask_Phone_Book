from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#Instance of SQLAlchemy to connect our app to the database
db = SQLAlchemy(app)
#Instance of Migrate that will track our app and db
migrate = Migrate(app, db)
# import all of the routes/models from the routes file into the current package
from app import routes, models