from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField


class Form(FlaskForm):
    # dropdowns
    choices = [(1, '< 6 Bulan'), (3, '> 6 Bulan'), (6, '> 1 Tahun')]
    pengalaman_kerja = SelectField('Select an option:', choices=choices)
    