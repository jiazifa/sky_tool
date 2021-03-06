from app.utils.ext import Flask, db, scheduler, \
    current_app, socket_app, flask_app, fileStorage, configure_uploads
from config import config, Config, root_dir
from dynaconf import FlaskDynaconf, settings
import os

__all__ = ['create_app']

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
                and routes != 'templates' \
                and not routes.startswith('__'):
            __import__('app.' + routes)

    print(route_list)
    for blueprints in route_list:
        if blueprints[1] is not None:
            app.register_blueprint(blueprints[0], url_prefix=blueprints[1])
        else:
            app.register_blueprint(blueprints[0])


def create_table(config_name, app):
    from app.models import __all__
    with app.app_context():
        db.create_all()

def create_app(env: str) -> Flask:
    assert(type(env) is str)
    config_obj = config[env]
    app = Flask(__name__)
    FlaskDynaconf(app=app, dynaconf_instance=settings)
    app.config.from_object(config_obj)
    # 注册插件
    db.init_app(app)
    socket_app.init_app(app)
    configure_uploads(app, fileStorage)
    config_obj.init_app(app)
    register_blueprint(app)
    create_table(env, app)
    flask_app = app
    return app
