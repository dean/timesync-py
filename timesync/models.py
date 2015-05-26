from flask import g, current_app
from sqlalchemy import (create_engine, Column, DateTime, ForeignKey,
                        Integer, String, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from datetime import date


Model = declarative_base()


def init_db():
    engine = g.db_session.get_bind()
    Model.metadata.create_all(bind=engine)


def create_db_session():
    _db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(_db_uri, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Model.query = session.query_property()
    return session


class User(Model):
    """
    Represents a user.
    """
    __tablename__ = 'users'

    username = Column(String(24), primary_key=True)
    entries = relationship('TimeEntry')

    def __repr__(self):
        return "<User('%s')>" % self.username


class Activity(Model):
    """
    Represents activies such as: development, documentation, support, etc.
    """
    __tablename__ = 'activies'

    activity = Column(String(100), primary_key=True)
    slug = Column(String(24), unique=True)
    entries = relationship('TimeEntry')

    def __repr__(self):
        return "<Activity('%s', '%s')>" % (self.activity, self.slug)


class Project(Model):
    """
    Represents a project such as: Ganeti Web Manager, ORVSD, Hosting, etc.
    """
    __tablename__ = 'projects'

    project = Column(String(100), primary_key=True)
    slug = Column(String(24), unique=True)
    entries = relationship('TimeEntry')

    def __repr__(self):
        return "<Project('%s', '%s')>" % (self.project, self.slug)


class TimeEntry(Model):
    """
    Represents a time entry.
    """
    __tablename__ = 'time_entries'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer)  # In Minutes
    notes = Column(String(500), default='')
    issue_uri = Column(String(500), default='')
    date = Column(DateTime, default=date.today())
    project = Column(String(24), ForeignKey('Project.slug',
                                      use_alter=True,
                                      name='fk_time_entries_projects'))
    activity = Column(String(24), ForeignKey('Activity.slug',
                                         use_alter=True,
                                         name='fk_time_entries_activities'))
    user = Column(String(24), ForeignKey('User.username',
                                      use_alter=True,
                                      name='fk_time_entries_users'))

    def __repr__(self):
        return ("<TimeEntry('%s', '%s', '%s', %s', '%s', %s', '%s', '%s')>" % (
                    self.id,
                    self.duration,
                    self.notes,
                    self.issue_uri,
                    self.date,
                    self.project,
                    self.activity,
                    self.user
                ))



