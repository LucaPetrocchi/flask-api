
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def create_app(config="settings"):
    app = Flask('Foro-Server')
    app.config.from_object(config)
    
    from extensions import (
        jwt,
        ma,
        migrate,
        db
    )

    jwt.init_app(app)
    ma.init_app(app)
    db.init_app(app)

    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    validate_database(db_uri)

    migrate.init_app(app, db)

    register_errorhandlers(app)
    # from views.views import blueprint

    # app.register_blueprint(blueprint)

    return app

def validate_database(db_uri):
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f'CREATED DB: {db_uri}')
    else:
        print(f'DB FOUND')

def register_errorhandlers(app):
    from error_handlers import (
        server_error,
        client_error,
        ClientError
    )

    app.register_error_handler(ClientError, client_error)
    app.register_error_handler(404, server_error)

if __name__ == '__main__':
    app = create_app()