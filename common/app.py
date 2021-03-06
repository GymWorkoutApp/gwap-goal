import logging

from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api
from gwa_framework.app import GWAApp
from gwa_framework.auth import GWAAuth

from common.database import db
from common.resources import resources_v1
from common.settings import PORT, DEBUG, GWAAppConfig


def create_app():
    new_app = GWAApp(__name__, static_folder=None)
    GWAAppConfig(new_app)
    GWAAuth(new_app)
    CORS(new_app)
    db.init_app(new_app)
    return new_app


app = create_app()

# version 1
bp_v1 = Blueprint('v1', __name__, url_prefix='/v1')
api_v1 = Api(bp_v1)
app.register_blueprint(bp_v1)

for resource_v1 in resources_v1:
    api_v1.add_resource(resource_v1['resource'], *resource_v1['urls'], endpoint=resource_v1['endpoint'],
                        methods=resource_v1['methods'])

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.run(debug=DEBUG, port=PORT)
