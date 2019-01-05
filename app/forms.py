from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    kernelFunction = SelectField('Kernel Functions', choices = [('gaussianKernel', 'Gaussian'), ('uniformKernel', 'Uniform')])
    kernelWidth = StringField('Kernel Width in Days (float value)', validators=[DataRequired()])
    daysAhead = StringField('Days Ahead (float value)', validators=[DataRequired()])
    #scoreFunction = SelectField('Score Function', choices = [('brierScore', 'Brier'), ('logScore', 'Log'),('sphericalScore','Spherical')])
    submit = SubmitField('Submit')
    
#class MarketSetForm: