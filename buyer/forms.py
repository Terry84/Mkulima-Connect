from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    category = SelectField('Category', choices=[
        ('all', 'All Categories'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('legumes', 'Legumes'),
        ('roots_tubers', 'Roots & Tubers'),
        ('others', 'Others')
    ], default='all')
    county = SelectField('County', choices=[
        ('all', 'All Counties'),
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
    ], default='all')
    submit = SubmitField('Search')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send Message')
