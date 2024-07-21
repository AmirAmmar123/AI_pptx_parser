from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, DateTime, func, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid

Base = None
if Base is None:
    Base = declarative_base()

class User(Base):
    """
    This class represents the 'users' table in the database.
    It contains information about users, including their unique ID, email, and associated uploads.

    Attributes:
    id (Column): The primary key of the user.
    email (Column): The unique email of the user.
    uploads (relationship): A relationship to the Upload class, representing the user's uploads.

    Methods:
    None
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    uploads = relationship('Upload', back_populates='user', cascade='all, delete-orphan')

class Upload(Base):
    """
    This class represents the 'uploads' table in the database.
    It contains information about uploaded files, including their unique ID, filename, upload and finish times, status,
    uploaded filename, JSON data, and the associated user.
    """
    __tablename__ = 'uploads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=func.now())
    finish_time = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    uploaded_filename = Column(String, nullable=False) 
    json_data = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='uploads')

engine, Session = None, None
if engine is None and Session is None:
    DATABASE_URL = "sqlite:////home/ameer/exteam/python-Home-Work/final-ex/final-exercise-AmirAmmar123/server/DB/gptDB.db"
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
