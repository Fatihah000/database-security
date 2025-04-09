from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialisation de l'application Flask et des extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/gestion_cours'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données et du gestionnaire de connexion
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Fonction pour charger l'utilisateur depuis la base de données
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Importer après la création de l'app pour éviter les problèmes de dépendances
    return User.query.get(int(user_id))

# Importer les modèles et les routes après l'initialisation
from app.models import User
from app import routes
