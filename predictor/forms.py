from django import forms

class PredictionForm(forms.Form):
    # Fields for Option 1 (Random Forest)
    KhokanaRiver = forms.FloatField(required=False)
    SundarijalGHT = forms.FloatField(required=False)
    SundarijalRiver = forms.FloatField(required=False)
    Rain_Kumaltar = forms.FloatField(required=False)
    Rain_Kritipur = forms.FloatField(required=False)
    Rain_Sankhu = forms.FloatField(required=False)
    Rain_Chagu = forms.FloatField(required=False)
    Rain_DhapDam = forms.FloatField(required=False)
    Rain_Airport = forms.FloatField(required=False)

    # Field for Option 2 (LSTM input CSV)
    input_file = forms.FileField(required=False)
