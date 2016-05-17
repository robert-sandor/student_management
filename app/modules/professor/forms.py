from flask.ext.wtf import Form
from wtforms import StringField, validators, TextAreaField
from app.modules.common.models import Specialty, StudyLine
from wtforms.validators import ValidationError


def validate_course_name(form, field):
    #TODO make sure a course is not proposed multiple twice
    pass


def validate_speciality(form, field):
    specialities = Specialty.query.all()
    speciality_types = [s.specialty_type for s in specialities]
    if field.data not in speciality_types:
        raise ValidationError('Invalid speciality')


def validate_study_line(form, field):
    study_lines = [s.study_language for s in StudyLine.query.all()]
    if field.data not in study_lines:
        raise ValidationError('Invalid study line')


class ProposalForm(Form):
    course_name = StringField('Course name', [validators.Length(min=3,
                                                                message='The name needs to be more descriptive'),
                                              validators.DataRequired()])
    speciality = StringField('Speciality', [validate_speciality, validators.DataRequired()])
    study_line = StringField('Study line', [validate_study_line, validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=300, message='The description is too short'),
                                                validators.DataRequired()])
    # course_name = StringField('Course name',
    #                           [validators.Length(min=3, message='The name needs to be more descriptive')])
    # speciality = StringField('Speciality')
    # study_line = StringField('Study line')
    # description = TextAreaField('Description')
