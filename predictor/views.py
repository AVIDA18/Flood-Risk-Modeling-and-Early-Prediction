import pandas as pd
import numpy as np
import math
import joblib
from django.shortcuts import render
from keras.models import load_model
from .forms import PredictionForm

# Load models and scalers
model_option1 = joblib.load('predictor/rf_model.joblib')
lstm_model = load_model('predictor/lstm_model.h5', compile=False)
scaler = joblib.load('predictor/scaler.pkl')

def predict_view(request):
    predicted_value = None
    flood_status = None

    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES)
        model_option = request.POST.get('model_option')

        if form.is_valid():
            if model_option == 'option1':
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
                predicted_value = model_option1.predict(input_data)[0]

            elif model_option == 'option2':
                uploaded_file = request.FILES.get('input_file')
                if uploaded_file:
                    try:
                        input_df = pd.read_csv(uploaded_file)

                        SEQ_LEN = input_df.shape[0]

                        scaled_input = scaler.transform(input_df)
                        scaled_input_df = pd.DataFrame(scaled_input, columns=input_df.columns)

                        input_sequence = scaled_input_df.values.reshape(1, SEQ_LEN, -1)

                        pred_scaled = lstm_model.predict(input_sequence)

                        padded = np.concatenate([np.zeros((1, scaled_input_df.shape[1] - 1)), pred_scaled], axis=1)

                        pred_inverse = scaler.inverse_transform(padded)[0, -1]

                        predicted_value = pred_inverse

                    except Exception as e:
                        print(f"LSTM processing error: {e}")
                        predicted_value = None
            
            if predicted_value is not None:
                if predicted_value >= 1.5:
                    flood_status = 'Danger'
                elif predicted_value <= 1:
                    flood_status = 'No Flood'
                else:
                    flood_status = 'Warning'

    else:
        form = PredictionForm()

    selected_model = request.POST.get('model_option') if request.method == 'POST' else None

    return render(request, 'predictor/predict.html', {
        'form': form,
        'predicted_value': round(predicted_value, 3) if predicted_value is not None else None,
        'flood_status': flood_status,
        'selected_model': selected_model
    })
