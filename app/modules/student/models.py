# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('auth_user_id_seq'::regclass)"))
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=False)


class Faculty(Base):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True, unique=True)
    faculty_name = Column(String(50))
    address = Column(String(200))
    contact = Column(String(200))


class Semester(Base):
    __tablename__ = 'semester'

    id = Column(Integer, primary_key=True, unique=True)
    year_id = Column(ForeignKey('year.id'), nullable=False)
    semester = Column(Integer, nullable=False)

    year = relationship('Year')


class Semigroup(Base):
    __tablename__ = 'semigroup'

    id = Column(Integer, primary_key=True, unique=True)
    semigroup_id = Column(ForeignKey('studygroup.id'), nullable=False)
    semigroup_number = Column(String(5))

    semigroup = relationship('Studygroup')


class Specialty(Base):
    __tablename__ = 'specialty'

    id = Column(Integer, primary_key=True, unique=True)
    specialty_type = Column(String(50), nullable=False)
    study_level_id = Column(ForeignKey('studylevel.id'), nullable=False)

    study_level = relationship('Studylevel')


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, unique=True)
    semigroup_id = Column(ForeignKey('semigroup.id'), nullable=False)
    serial_number = Column(Integer, nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)

    semigroup = relationship('Semigroup')
    user = relationship('AuthUser')


class Studygroup(Base):
    __tablename__ = 'studygroup'

    id = Column(Integer, primary_key=True, unique=True)
    semester_id = Column(ForeignKey('semester.id'), nullable=False)
    group_number = Column(String(10))

    semester = relationship('Semester')


class Studylevel(Base):
    __tablename__ = 'studylevel'

    id = Column(Integer, primary_key=True, unique=True)
    study_level = Column(String(50), nullable=False)
    faculty_id = Column(ForeignKey('faculty.id'), nullable=False)

    faculty = relationship('Faculty')


class Studyline(Base):
    __tablename__ = 'studyline'

    id = Column(Integer, primary_key=True, unique=True)
    study_language = Column(String(50), nullable=False)
    specialty_id = Column(ForeignKey('specialty.id'), nullable=False)

    specialty = relationship('Specialty')


class Studyplan(Base):
    __tablename__ = 'studyplan'

    id = Column(Integer, primary_key=True, unique=True)
    study_line_id = Column(ForeignKey('studyline.id'), nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    initial_capacity = Column(Integer, server_default=text("0"))

    study_line = relationship('Studyline')


class Year(Base):
    __tablename__ = 'year'

    id = Column(Integer, primary_key=True, unique=True)
    study_plan_id = Column(ForeignKey('studyplan.id'), nullable=False)
    study_year = Column(Integer, nullable=False)
    current_capacity = Column(Integer, nullable=False, server_default=text("0"))

    study_plan = relationship('Studyplan')
