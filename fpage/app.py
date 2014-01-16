# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from webassets.loaders import PythonLoader

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
    from fpage.modules import public, voting, submit

    app.register_blueprint(public.blueprint)
    app.register_blueprint(voting.blueprint)
    app.register_blueprint(submit.blueprint)
    return app