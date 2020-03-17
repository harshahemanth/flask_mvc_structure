import os

cwd = os.getcwd()

parent_directory = "/opt/"
directory_to_create = 'mock_api'
try:
    path = os.path.join(parent_directory, directory_to_create)
    os.mkdir(path)

    os.chdir(path)

    service_file = open("service.py", "w")
    service_file.write("""from src.setup import app
from flask_swagger import swagger
from flask import jsonify

@app.route('/spec')
def swagger_spec():
    swag = swagger(app)
    swag['info']['title'] = 'Application Name'
    return jsonify(swag)


if __name__ == '__main__':
    app.run(host='localhost', port=9999, debug=True)""")
    service_file.close()

    config_file = open("config.py", "w")
    config_file.write("""import os
from configobj import ConfigObj

basedir = os.path.abspath(os.path.dirname(__file__))
config = ConfigObj(os.path.join(basedir, 'config.ini'))
postgresURI = config['db']['db_url']

SWAGGER_URL = config['swagger']['swagger_url']
API_URL = config['swagger']['api_url']""")
    config_file.close()

    config_file_ini = open("config.ini", "w")
    config_file_ini.write("""[db]
db_url ="postgresql://postgres:postgres@127.0.0.1/database_name"

[swagger]
swagger_url = '/swagger'
api_url = 'http://localhost:9999/spec'""")
    config_file_ini.close()

    requirements_file = open('requirements.txt', "w")
    requirements_file.write("""certifi
click
configobj
Flask
Flask-Cors
flask-swagger
flask-swagger-ui
itsdangerous
Jinja2
MarkupSafe
PyYAML
six
Werkzeug""")
    requirements_file.close()

    src_dir = 'src'
    src_path = os.path.join(path, src_dir)
    os.mkdir(src_path)
    os.chdir(src_path)

    models_file = open("models.py", "w")
    models_file.write("""#place db models here""")
    models_file.close()

    controller_dir = 'controllers'
    handler_dir = 'handlers'
    controller_path = os.path.join(src_path, controller_dir)
    os.mkdir(controller_path)
    handler_path = os.path.join(src_path, handler_dir)
    os.mkdir(handler_path)

    setup_file = open("setup.py", "w")
    setup_file.write("""from flask import Flask
from flask_cors import CORS

from flask_swagger_ui import get_swaggerui_blueprint
from config import SWAGGER_URL, API_URL

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# app.config['SQLALCHEMY_DATABASE_URI'] = config['db']['db_url']
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.create_all()

CORS(app)
""")
    setup_file.close()

    print("Directory structure created successfully!")
except OSError as error:
    print(error)
