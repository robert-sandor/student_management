# coding: utf-8
from sqlalchemy import Boolean, Column, Date, ForeignKey, ForeignKeyConstraint, Integer, SmallInteger, String, text
from sqlalchemy.orm import relationship
from app import db


class Contract(db.Model):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('student.id'), nullable=False)

    student = relationship('Student')


class GradeEvaluation(db.Model):
    __tablename__ = 'grade_evaluation'
    __table_args__ = (
        ForeignKeyConstraint(['course_id', 'contract_id'], ['evaluation.course_id', 'evaluation.contract_id']),
    )

    evaluation_date = Column(Date)
    grade = Column(Integer)
    present = Column(Boolean, nullable=False, server_default=text("false"))
    contract_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, unique=True)

    course = relationship('Evaluation')


class RoleType(db.Model):
    __tablename__ = 'role_type'

    id = Column(Integer, primary_key=True, unique=True)
    type_name = Column(String(50), nullable=False)


class Semigroup(db.Model):
    __tablename__ = 'semigroup'

    id = Column(Integer, primary_key=True, unique=True)
    semigroup_id = Column(ForeignKey('study_group.id'), nullable=False)
    semigroup_number = Column(String(5))

    semigroup = relationship('StudyGroup')


class Student(db.Model):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, unique=True)
    semigroup_id = Column(ForeignKey('semigroup.id'), nullable=False)
    serial_number = Column(Integer, nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)

    semigroup = relationship('Semigroup')
    user = relationship('User')


class StudyGroup(db.Model):
    __tablename__ = 'study_group'

    id = Column(Integer, primary_key=True, unique=True)
    semester_id = Column(ForeignKey('semester.id'), nullable=False)
    group_number = Column(String(10))

    semester = relationship('Semester')


class Vote(db.Model):
    __tablename__ = 'vote'

    optional_id = Column(ForeignKey('optional_course.id'), primary_key=True, nullable=False)
    contract_id = Column(ForeignKey('contract.id'), primary_key=True, nullable=False)
    package_id = Column(ForeignKey('package.id'), nullable=False)
    position = Column(Integer, nullable=False, server_default=text("0"))

    contract = relationship('Contract')
    optional = relationship('OptionalCourse')
    package = relationship('Package')


