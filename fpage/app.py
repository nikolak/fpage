# -*- coding: utf-8 -*-
from flask import Flask
from webassets.loaders import PythonLoader

from flask.ext.assets import Environment
from fpage import assets
from fpage.models import db


assets_env = Environment()


def create_app(config_object):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    # Initialize SQLAlchemy
    db.init_app(app)
    # Register asset bundles
    assets_env.init_app(app)
    assets_loader = PythonLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)
        # Register blueprints
    from fpage.modules import page, voting, submit, public, comments, user

    app.register_blueprint(page.blueprint)
    app.register_blueprint(voting.blueprint)
    app.register_blueprint(submit.blueprint)
    app.register_blueprint(public.blueprint)
    app.register_blueprint(comments.blueprint)
    app.register_blueprint(user.blueprint)

    return app