# predictor/forms.py
from django import forms

class PredictionForm(forms.Form):
    KhokanaRiver = forms.FloatField(required=True)
    SundarijalGHT = forms.FloatField(required=True)
    SundarijalRiver = forms.FloatField(required=True)
    Rain_Kumaltar = forms.FloatField(required=True)
    Rain_Kritipur = forms.FloatField(required=True)
    Rain_Sankhu = forms.FloatField(required=True)
    Rain_Chagu = forms.FloatField(required=True)
    Rain_DhapDam = forms.FloatField(required=True)
    Rain_Airport = forms.FloatField(required=True)
