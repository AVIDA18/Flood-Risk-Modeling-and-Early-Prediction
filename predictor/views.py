import math
import joblib
import pandas as pd
from django.shortcuts import render
from .forms import PredictionForm

# Load model once globally (adjust path if needed)
model = joblib.load('predictor/model.joblib')

def predict_view(request):
    predicted_value = None
    flood_status = None

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            KhokanaRiver = form.cleaned_data.get('KhokanaRiver', 0)
            SundarijalRiver = form.cleaned_data.get('SundarijalRiver', 0)

            try:
                product = KhokanaRiver * SundarijalRiver
                sqrt_product = math.sqrt(product)
                Lag = 14.64 / (sqrt_product ** 0.4)
            except ZeroDivisionError:
                Lag = 0

            input_dict = {
            'KhokanaRiver': KhokanaRiver,
            'SundarijalGHT': form.cleaned_data.get('SundarijalGHT', 0),
            'SundarijalRiver': SundarijalRiver,
            'Rain_Kumaltar': form.cleaned_data.get('Rain_Kumaltar', 0),
            'Rain_Kritipur': form.cleaned_data.get('Rain_Kritipur', 0),
            'Rain_Sankhu': form.cleaned_data.get('Rain_Sankhu', 0),
            'Rain_Chagu': form.cleaned_data.get('Rain_Chagu', 0),
            'Rain_DhapDam': form.cleaned_data.get('Rain_DhapDam', 0),
            'Rain_Airport': form.cleaned_data.get('Rain_Airport', 0),
            'Lag': Lag
            }

            input_data = pd.DataFrame([input_dict])
            predicted_value = model.predict(input_data)[0]
            
            if predicted_value is not None:
                if predicted_value >= 4:
                    flood_status = 'Danger'
                elif predicted_value <= 3.5:
                    flood_status = 'No Flood'
                else:
                    flood_status = 'Warning'
    else:
        form = PredictionForm()

    return render(request, 'predictor/predict.html', {
        'form': form,
        'predicted_value': round(predicted_value, 3) if predicted_value is not None else None,
        'flood_status': flood_status,
    })
