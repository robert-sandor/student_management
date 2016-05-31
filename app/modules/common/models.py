# coding: utf-8
from sqlalchemy import Boolean, Column, Date, ForeignKey, ForeignKeyConstraint, Integer, SmallInteger, String, text
from sqlalchemy.orm import relationship
from app import db


class AdminStaff(db.Model):
    __tablename__ = 'admin_staff'

    id = Column(Integer, primary_key=True, unique=True)
    faculty_id = Column(ForeignKey('faculty.id'), nullable=False)
    admin_type = Column(String(50), nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)

    faculty = relationship('Faculty')
    user = relationship('User')


class Contract(db.Model):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('student.id'), nullable=False)

    student = relationship('Student')
    evaluation = relationship('Evaluation')


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
    study_group_id = Column(ForeignKey('study_group.id'), nullable=False)
    semigroup_number = Column(String(5))

    study_group = relationship('StudyGroup')


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
    contract = relationship('Contract')

    def __init__(self, semigroup_id, serial_number, user_id, first_name, last_name):
        self.semigroup_id = semigroup_id
        self.serial_number = serial_number
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name


class StudyGroup(db.Model):
    __tablename__ = 'study_group'

    id = Column(Integer, primary_key=True, unique=True)
    semester_id = Column(ForeignKey('semester.id'), nullable=False)
    group_number = Column(String(10))

    semester = relationship('Semester')
    semigroup = relationship('Semigroup')


class Vote(db.Model):
    __tablename__ = 'vote'

    optional_id = Column(ForeignKey('optional_course.id'), primary_key=True, nullable=False)
    contract_id = Column(ForeignKey('contract.id'), primary_key=True, nullable=False)
    package_id = Column(ForeignKey('package.id'), nullable=False)
    position = Column(Integer, nullable=False, server_default=text("0"))

    contract = relationship('Contract')
    optional = relationship('OptionalCourse')
    package = relationship('Package')


class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    _pass = Column('pass', Boolean, nullable=False, server_default=text("false"))
    contract_id = Column(ForeignKey('contract.id'), primary_key=True, nullable=False)
    course_id = Column(ForeignKey('course.id'), primary_key=True, nullable=False)

    contract = relationship('Contract')
    course = relationship('Course')
    grades = relationship('GradeEvaluation')


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
    course_language = Column(String(10))

    semester = relationship('Semester')

    professors_role = relationship('ProfessorRole')

    evaluation = relationship('Evaluation')


class Department(db.Model):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, unique=True)
    faculty_id = Column(ForeignKey('faculty.id'), nullable=False)
    dept_name = Column(String(50), nullable=False)
    id_cod = Column(ForeignKey('professor.id'), nullable=False)

    faculty = relationship('Faculty')
    professor = relationship('Professor', primaryjoin='Department.id_cod == Professor.id')


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
    package_id = Column(ForeignKey('package.id'), nullable=True)

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
    study_group = relationship('StudyGroup')


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
    semester = relationship('Semester')

    def __repr__(self):
        return str(self.study_year)


class Professor(db.Model):
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True, unique=True)
    rank = Column(String(50), nullable=False)
    id_department = Column(ForeignKey('department.id'), nullable=False)
    id_user = Column(ForeignKey('auth_user.id'), nullable=False)
    name = Column(String(20))

    department = relationship('Department', primaryjoin='Professor.id_department == Department.id')
    auth_user = relationship('User')

    professor_roles = relationship('ProfessorRole')

    def is_cod(self):
        if self.department.id_cod == self.id:
            return True
        return False

    def __repr__(self):
        return '<Professor %r>' % self.id


class ProfessorRole(db.Model):
    __tablename__ = 'professor_role'

    professor_id = Column(ForeignKey('professor.id'), primary_key=True, nullable=False)
    course_id = Column(ForeignKey('course.id'), primary_key=True, nullable=False)
    role_type_id = Column(ForeignKey('role_type.id'), primary_key=True, nullable=False)

    course = relationship('Course')
    professor = relationship('Professor')
    role_type = relationship('RoleType')

    def __repr__(self):
        return '<Professor role %r>' % self.role_type_id


class ProposedCourses(db.Model):
    __tablename__ = 'proposed_courses'

    id = Column(Integer, primary_key=True, unique=True)
    professor_id = Column(ForeignKey('professor.id'), nullable=False)
    speciality = Column(String(50), nullable=False)
    study_line = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    course_name = Column(String(50), nullable=False)

    professor = relationship('Professor')

    def __init__(self, professor_id, course_name, speciality, study_line, description):
        self.professor_id = professor_id
        self.course_name = course_name
        self.speciality = speciality
        self.study_line = study_line
        self.description = description


class AdminDates(db.Model):
    __tablename__ = 'admin_dates'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Integer, nullable=False)
    from_date = Column(Date, nullable=False)
    to = Column(Date, nullable=False)


