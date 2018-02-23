from flask_wtf import FlaskForm
from wtforms import StringField, \
    DateField, TextAreaField, IntegerField, validators


class EntryForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=30)])
    date = DateField('Date')
    time_spent = IntegerField('Time Spent')
    learned = TextAreaField('What-I-Learned')
    resources = TextAreaField('Resources')
