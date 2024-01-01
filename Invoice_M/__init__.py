# Importing necessary flask libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Initialise the web app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwertyuiop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\admin\\Desktop\\Invoice Gen\\Invoice_M\\site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from Invoice_M import routes
