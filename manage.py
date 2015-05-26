import logging
import os
import sys

from flask import current_app, g
from flask.ext.script import Manager

from timesync import create_app
from timesync.models import create_db_session, init_db

def setup_app(config=None):
    return create_app(config) if config else create_app()


# Setup our manager
manager = Manager(setup_app)


@manager.command
def setup_db():
    """
    Either initialize the database if none yet exists, or migrate as needed
    """

    from alembic.config import Config
    from alembic import command

    with current_app.app_context():
        # Alembic config used by migration or stamping
        alembic_cfg = Config(
            os.path.join(current_app.config["PROJECT_PATH"], "alembic.ini")
        )

        # Database connections
        g.db_session = create_db_session()
        con = g.db_session.connection()

        # Query list of existing tables
        tables = con.execute("show tables").fetchall()
        alembic_table = ('alembic_version',)
        if alembic_table in tables:
            # Latest version has been stamped or we have been upgrading
            logging.info("Database: Migrating")
            command.upgrade(alembic_cfg, "head")
        else:
            # The database needs to be initialized
            logging.info("Database: Initializing")
            init_db()
            command.stamp(alembic_cfg, "head")


if __name__ == '__main__':
    manager.run()
