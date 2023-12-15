from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField


class Form(FlaskForm):
    # dropdowns
    choices = [(0, '< 6 Bulan'), (2, '> 6 Bulan'), (3, '> 1 Tahun')]
    pengalaman_kerja = SelectField('Select an option:', choices=choices)
    # checkboxes
    lokasi_kerja = BooleanField('Dalam Malang', default=False)
    pengalaman_organisasi = BooleanField('Memiliki Pengalaman Organisasi', default=False)
    umur = BooleanField('Lebih dari 25 Tahun', default=False)
    ipk = BooleanField('IPK 3.0 Keatas', default=False)