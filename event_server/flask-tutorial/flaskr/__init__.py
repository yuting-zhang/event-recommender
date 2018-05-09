import os
import sys
sys.path.insert(0, '/recommender')

from flask import Flask, redirect, g

from .recommender import recommender

'''
Run on mac with these commands in the terminal:
export FLASK_APP=flaskr
export FLASK_ENV=development
python3 -m flask run

Update database with this command in the terminal:
python3 -m flask init-db
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # redirect page to register or log in page
    @app.route('/hello')
    def route():
        return redirect('/auth/register')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import model
    app.register_blueprint(model.bp)
    app.add_url_rule('/', endpoint='index')

    return app
