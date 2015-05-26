from flask import Flask, current_app, g

from timesync.models import create_db_session


def create_app(config='timesync.config', config_changes=None):
    """
    Creates an instance of our application.

    We needed to create the app in this way so we could set different
    configurations within the same app. (hint: not using the same database
    when testing)
    """

    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        g.db_session = create_db_session()
        return app
