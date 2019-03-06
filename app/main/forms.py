from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required, Email, Length

class CompanyForm(FlaskForm):
    name = StringField('Name of the company', validators = [Required()])
    text = TextAreaField('Campany',validators = [Required()])
    services=TextAreaField('Services and Products',validators = [Required()])
    contacts=TextAreaField('Contacts',validators = [Required()])
    category = SelectField('Category', choices = [('accountancy', 'Accountancy'),('construction','Construction'), ('designer','Designer'),('food','Food Proccessing'), ('telecommunication','Telecommunication')], validators = [Required()])
    submit = SubmitField('Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you', validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    name = StringField('Add your name', validators = [Required()])
    text = TextAreaField('Leave a Feedback',validators = [Required()])
    submit = SubmitField('Add Feedback')

class SubscriberForm(FlaskForm):
    name  = StringField('Your name', validators = [Required()])
    email = StringField('Your email address', validators = [Required(), Email()])
    submit = SubmitField('Subscribe')

