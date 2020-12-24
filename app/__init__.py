from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
import connexion

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    connexionApp = connexion.App(__name__, specification_dir='./')
    connexionApp.add_api('docs.json')
    app = connexionApp.app

    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    db.app = app

    from app.api.patient.routes import patient
    app.register_blueprint(patient, url_prefix="/patient")

    return app
