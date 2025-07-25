from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BillForm(FlaskForm):
    bill_number = StringField('Bill Number', validators=[DataRequired()])
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_phone = StringField('Phone')
    submit = SubmitField('Create Bill')

class BillItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    rate = FloatField('Rate', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Add Item')
