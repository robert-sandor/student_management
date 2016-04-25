from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from app import db


class Course(db.Model):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, unique=True)
    semester_id = Column(ForeignKey('semester.id'))
    course_name = Column(String(50), nullable=False)
    course_description = Column(String(200))
    code = Column(String(10), nullable=False)
    professor_name = Column(String(50))
    credits = Column(Integer)
    evaluation_type = Column(String(10), nullable=False)
    is_optional = Column(Boolean, nullable=False, server_default=text("true"))

    semester = relationship('Semester')


class Department(db.Model):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, unique=True)
    faculty_id = Column(ForeignKey('faculty.id'), nullable=False)
    dept_name = Column(String(50), nullable=False)
    id_cod = Column(ForeignKey('professor.id'), nullable=False)

    faculty = relationship('Faculty')
    professor = relationship('Professor', primaryjoin='Department.id_cod == Professor.id')


class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    _pass = Column('pass', Boolean, nullable=False, server_default=text("false"))
    contract_id = Column(ForeignKey('contract.id'), primary_key=True, nullable=False)
    course_id = Column(ForeignKey('course.id'), primary_key=True, nullable=False)

    contract = relationship('Contract')
    course = relationship('Course')


class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True, unique=True)
    faculty_name = Column(String(50))
    address = Column(String(200))
    contact = Column(String(200))


class OptionalCourse(db.Model):
    __tablename__ = 'optional_course'

    id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('course.id'), nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("false"))
    id_department = Column(ForeignKey('department.id'), nullable=False)
    course_language = Column(String(10))

    course = relationship('Course')
    department = relationship('Department')


class Package(db.Model):
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(10))


class Semester(db.Model):
    __tablename__ = 'semester'

    id = Column(Integer, primary_key=True, unique=True)
    year_id = Column(ForeignKey('year.id'), nullable=False)
    semester = Column(Integer, nullable=False)

    year = relationship('Year')


class Specialty(db.Model):
    __tablename__ = 'specialty'

    id = Column(Integer, primary_key=True, unique=True)
    specialty_type = Column(String(50), nullable=False)
    study_level_id = Column(ForeignKey('study_level.id'), nullable=False)

    study_level = relationship('StudyLevel')


class StudyLevel(db.Model):
    __tablename__ = 'study_level'

    id = Column(Integer, primary_key=True, unique=True)
    study_level = Column(String(50), nullable=False)
    faculty_id = Column(ForeignKey('faculty.id'), nullable=False)

    faculty = relationship('Faculty')


class StudyLine(db.Model):
    __tablename__ = 'study_line'

    id = Column(Integer, primary_key=True, unique=True)
    study_language = Column(String(50), nullable=False)
    specialty_id = Column(ForeignKey('specialty.id'), nullable=False)

    specialty = relationship('Specialty')


class StudyPlan(db.Model):
    __tablename__ = 'study_plan'

    id = Column(Integer, primary_key=True, unique=True)
    study_line_id = Column(ForeignKey('study_line.id'), nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    initial_capacity = Column(Integer, server_default=text("0"))

    study_line = relationship('StudyLine')


class Year(db.Model):
    __tablename__ = 'year'

    id = Column(Integer, primary_key=True, unique=True)
    study_plan_id = Column(ForeignKey('study_plan.id'), nullable=False)
    study_year = Column(Integer, nullable=False)
    current_capacity = Column(Integer, nullable=False, server_default=text("0"))

    study_plan = relationship('StudyPlan')


