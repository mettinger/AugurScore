from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    kernelFunction = SelectField('Time Kernel Functions For Scores', 
                                 choices = [('gaussianKernel', 'Gaussian'),
                                            ('uniformKernel', 'Uniform'),
                                            ('triangularKernel','Triangular')])
    kernelWidth = StringField('Temporal Kernel Width in Days (float value)', 
                              validators=[DataRequired()])
    daysAhead = StringField('Days Ahead (float value)', validators=[DataRequired()])
    kernelFunctionCalibrated = SelectField('Probability Kernel Functions For Calibration', 
                                           choices = [('gaussianKernel', 'Gaussian'),
                                                      ('uniformKernel', 'Uniform'),
                                                      ('triangularKernel','Triangular')])
    kernelWidthCalibrated = StringField('Probability Kernel Width (float value)', 
                                        validators=[DataRequired()])
    submit = SubmitField('Submit')
    