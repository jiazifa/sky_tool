from app.utils.ext import Flask, request, db, fileStorage
from config import config, Config, root_dir
import os
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads


__all__ = ['db', 'create_app']

route_list = []


def fetch_route(blueprint, prefix=None):
    t = (blueprint, prefix)
    route_list.append(t)

def register_blueprint(app):
    app_dir = os.path.join(root_dir, 'app')
    for routes in os.listdir(app_dir):
        rou_path = os.path.join(app_dir, routes)
        if (not os.path.isfile(rou_path)) \
                and routes != 'static' \
                and routes != 'templates':
            try:
                __import__('app.' + routes)
            except:
                pass

    print(route_list)
    for blueprints in route_list:
        if blueprints[1] is not None:
            app.register_blueprint(blueprints[0], url_prefix=blueprints[1])
        else:
            app.register_blueprint(blueprints[0])


def createTable(config_name, app):
    if config_name is not 'production':
        from app.models import __all__
        with app.test_request_context():
            db.create_all()

def create_app(env: str) -> Flask:
    configObj = config[env]
    app = Flask(__name__)
    app.config.from_object(configObj)
    db.init_app(app)
    configObj.init_app(app)
    # 注册插件
    register_blueprint(app)
    configure_uploads(app, fileStorage)
    createTable(env, app)
    return app
