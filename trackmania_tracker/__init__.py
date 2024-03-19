import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CONFIG_FILE=os.path.join(app.instance_path, '/opt/trackmania-tracker/data/config.yaml')
    )
    app.logger.setLevel(os.environ.get("LOGLEVEL","INFO"))
     # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    #Register filters
    from . import utils
    app.add_template_filter(utils.check_new_record)
    app.add_template_filter(utils.format_local_timestamp)
    app.add_template_filter(utils.format_season)
    app.add_template_filter(utils.parse_account)
    # Register blueprints

    from . import home
    app.register_blueprint(home.bp)


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app