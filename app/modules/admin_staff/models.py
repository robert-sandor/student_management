from sqlalchemy import String, Column, ForeignKey, Integer
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
