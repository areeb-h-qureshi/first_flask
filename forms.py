from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField)
from wtforms.validators import InputRequired, Length


class CourseForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    description = TextAreaField('Course Description',
                                validators=[InputRequired(),
                                            Length(max=200)])
    price = IntegerField('Price', validators=[InputRequired()])
    level = RadioField('Level',
                       choices=['Beginner', 'Intermediate', 'Advanced'],
                       validators=[InputRequired()])
    available = BooleanField('Available', default='checked')
    submit_button = SubmitField('Submit', render_kw={'class': 'btn btn-primary'})

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    content = TextAreaField('Course Description',
                                validators=[InputRequired(),
                                            Length(max=200)])
    submit_button = SubmitField('Submit', render_kw={'class': 'btn btn-primary'})