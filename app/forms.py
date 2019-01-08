from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    kernelFunction = SelectField('Time Kernel Functions For Scores', 
                                 choices = [('gaussianKernel', 'Gaussian'),
                                            ('uniformKernel', 'Uniform'),
                                            ('triangularKernel','Triangular')])
    kernelWidth = StringField('Temporal Kernel Width in Days (float value, e.g. 1)', 
                              validators=[DataRequired()])
    daysAhead = StringField('Days Ahead (float value, e.g. 7)', validators=[DataRequired()])
    kernelFunctionCalibrated = SelectField('Probability Kernel Functions For Calibration', 
                                           choices = [('gaussianKernel', 'Gaussian'),
                                                      ('uniformKernel', 'Uniform'),
                                                      ('triangularKernel','Triangular')])
    kernelWidthCalibrated = StringField('Probability Kernel Width (float value, e.g. .03)', 
                                        validators=[DataRequired()])
    submit = SubmitField('Submit')
    