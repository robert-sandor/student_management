from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Professor(db.Model):
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True, unique=True)
    rank = Column(String(50), nullable=False)
    id_department = Column(ForeignKey('department.id'), nullable=False)
    id_user = Column(ForeignKey('auth_user.id'), nullable=False)

    department = relationship('Department', primaryjoin='Professor.id_department == Department.id')
    auth_user = relationship('User')


class ProfessorRole(db.Model):
    __tablename__ = 'professor_role'

    professor_id = Column(ForeignKey('professor.id'), primary_key=True, nullable=False)
    course_id = Column(ForeignKey('course.id'), primary_key=True, nullable=False)
    role_type_id = Column(ForeignKey('role_type.id'), primary_key=True, nullable=False)

    course = relationship('Course')
    professor = relationship('Professor')
    role_type = relationship('RoleType')

