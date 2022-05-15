#  See the NOTICE file distributed with this work for additional information
#  regarding copyright ownership.
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from flask import Flask
from src.havana.config import Config
from src.havana.extensions import (
    mysql1,
    mysql2
)


def create_app():
    """
    Creates app and registers all blueprints & extensions

    :return: Flask app object
    """

    app = Flask(__name__, template_folder='./template/')
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """
    Registers all the app extensions

    :param app: Flask app object
    :return: None
    """

    mysql1.init_app(app)
    mysql2.init_app(app)

    return None


def register_blueprints(app):
    """
    Registers all the app blueprints

    :param app: Flask app object
    :return: None
    """

    from src.havana.ni.routes import ni
    from src.havana.nsi.routes import nsi
    from src.havana.intron.routes import intron
    from src.havana.health.routes import health
    from src.havana.errors.handlers import errors

    app.register_blueprint(ni)
    app.register_blueprint(nsi)
    app.register_blueprint(intron)
    app.register_blueprint(health)
    app.register_blueprint(errors)

    return None
