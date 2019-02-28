from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    title = StringField('Pitch title',validators=[Required()])
    review = TextAreaField('Text', validators=[Required()])
    category = SelectField('Type', choices= [('interview', 'Interview pitch'), ('product', 'Product pitch'), ('promotion', 'Promotion pitch')], validators= [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text= TextAreaField('Leave a comment',validators =[Required()])
    submit = SubmitField('Sign In')
 
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')