from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address1 = StringField('Address1', validators=[DataRequired()])
    address2 = StringField('Address2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    website = StringField('Website', validators=[Length(min=0, max=140)])
    facebook = StringField('Facebook', validators=[Length(min=0, max=140)])
    twitter = StringField('Twitter', validators=[Length(min=0, max=140)])
    instagram = StringField('Instagram', validators=[Length(min=0, max=140)])
    company = StringField('Company', validators=[Length(min=0, max=140)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')