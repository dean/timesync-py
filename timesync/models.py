from sqlalchemy import (create_engine, Column, DateTime, ForeignKey,
                        Integer, String, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from datetime import date
import config


engine = create_engine(config.DB_URI)
session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Model = declarative_base(name='Model')
Model.query = session.query_property()


def init_db():
    """
    Sets up db and returns a db object to interact with.
    """
    Model.metadata.create_all(bind=engine)


class TimeEntry(Model):
    """
    Represents a time entry.
    """
    __tablename__ = 'time_entries'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer)  # In Minutes
    notes = Column(String, default='')
    issue_uri = Column(String, default='')
    date = Column(DateTime, default=date.today())
    project = Column(String, ForeignKey('Project.slug',
                                      use_alter=True,
                                      name='fk_time_entries_projects')
    activity = Column(String, ForeignKey('Activity.slug',
                                         use_alter=True,
                                         name='fk_time_entries_activities')
    user = Column(Integer, ForeignKey('User.username',
                                      use_alter=True,
                                      name='fk_time_entries_users')

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
                )


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

    activity = Column(String, primary_key=True)
    slug = Column(String, unique=True)
    entries = relationship('TimeEntry')

    def __repr__(self):
        return "<Activity('%s', '%s')>" % (self.activity, self.slug)


class Project(Model):
    """
    Represents a project such as: Ganeti Web Manager, ORVSD, Hosting, etc.
    """
    __tablename__ = 'projects'

    project = Column(String, primary_key=True)
    slug = Column(String, unique=True)
    entries = relationship('TimeEntry')

    def __repr__(self):
        return "<Project('%s', '%s')>" % (self.project, self.slug)
