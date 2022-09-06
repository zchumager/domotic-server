import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema

base_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(base_dir, 'app.db')
engine = create_engine(f"sqlite:///{db_file}")

session = scoped_session(sessionmaker(bind=engine))
Orm = declarative_base()


class Device(Orm):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    partial_mac = Column(String, unique=True, nullable=False)

    email = Column(String)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    role = Column(String, nullable=False)
    desired_temperature = Column(Integer, nullable=False)
    is_sick = Column(Boolean, nullable=False)
    medical_condition_level = Column(String)


class DeviceSchema(SQLAlchemySchema):
    class Meta:
        model = Device


# schema instances
device_schema = DeviceSchema()

Orm.metadata.create_all(engine)
