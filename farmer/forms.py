from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProduceForm(FlaskForm):
    crop_name = StringField('Crop Name', validators=[DataRequired(), Length(min=2, max=100)])
    quantity = IntegerField('Quantity (kg)', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('Price (Ksh)', validators=[DataRequired(), NumberRange(min=0.01)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', choices=[
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('legumes', 'Legumes'),
        ('roots_tubers', 'Roots & Tubers'),
        ('others', 'Others')
    ], validators=[DataRequired()])
    county = SelectField('County', choices=[
        ('Nairobi', 'Nairobi'),
        ('Kiambu', 'Kiambu'),
        ('Kakamega', 'Kakamega'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Nakuru', 'Nakuru'),
        ('Uasin Gishu', 'Uasin Gishu'),
        ('Meru', 'Meru'),
        ('Machakos', 'Machakos'),
        ('Nyeri', 'Nyeri'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Produce')
