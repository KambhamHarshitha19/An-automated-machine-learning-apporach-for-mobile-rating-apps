from django.shortcuts import render , redirect
from django.contrib import messages
from Users.models import UserRegisterModel
from django.conf import settings
from Users.forms import UserRegisterForm
import re
import sys
import time
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error , mean_squared_error , r2_score

def base(request):
    return render(request , 'base.html')

def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , 'Registered successfully')
            return redirect('Userlogin')
        else:
            messages.warning(request , 'Invalid credentials')
    else:
        form = UserRegisterForm()
    return render(request , 'Userregister.html' , {'form':form})


def Userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if username and password:
                user = UserRegisterModel.objects.get(Username=username , Password=password)
                if user.status == 'Activate':
                    request.session['user_id'] = user.id
                    request.session['username'] =username
                    request.session['Email'] =user.Email
                    request.session['Phone_No'] =user.Phone_No
                    return redirect('UserHome')
                else:
                    messages.warning(request , 'User is deactivated')
                    return redirect('Userlogin')
            else:
                messages.warning(request , 'Invalid credentials')
                return redirect('Userlogin')

        except Exception as e:
            messages.warning(request , f'{e}')

            
    return render(request , 'Userlogin.html')


def UserHome(request):
    user = request.session.get('username')
    email = request.session.get('Email')
    phone = request.session.get('Phone_No')
    return render(request , 'users/UserHome.html' , {'user':user , 'email':email , 'phone':phone})

def DatasetView(request):
    user = request.session.get('username')
    data = pd.read_csv(r"media/googleplaystore.csv")
    le=LabelEncoder()
    data['App'] = le.fit_transform(data['App'])
    data['Category'] = le.fit_transform(data['Category'])
    data['Rating'] = le.fit_transform(data['Rating'])
    data['Reviews'] = le.fit_transform(data['Reviews'])
    data['Installs'] = le.fit_transform(data['Installs'])
    data['Type'] = le.fit_transform(data['Type'])
    data['Price'] = le.fit_transform(data['Price'])
    data['Content Rating'] = le.fit_transform(data['Content Rating'])
    data['Genres'] = le.fit_transform(data['Genres'])
    data['Last Updated'] = le.fit_transform(data['Last Updated'])
    data['Current Ver'] = le.fit_transform(data['Current Ver'])
    data['Size'] = le.fit_transform(data['Size'])
    data = data.head(100)


    return render(request , 'users/datasetview.html' , {'data':data.to_html , "user": user})

#=========================TRAINING========================================
import os
import pandas as pd
import joblib
from django.conf import settings
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Define paths for model and encoders
MODEL_PATH = os.path.join(settings.MEDIA_ROOT, "ml_models", "rf_model.pkl")
ENCODER_PATHS = {
    "category": os.path.join(settings.MEDIA_ROOT, "ml_models", "le_category.pkl"),
    "app": os.path.join(settings.MEDIA_ROOT, "ml_models", "le_app.pkl"),
}

# ✅ Function to Convert Size to Numeric
def convert_size(size):
    if isinstance(size, str):
        size = size.replace("M", "e6").replace("K", "e3")  # Convert '10M' → '10e6' (10 million)
        if "Varies with device" in size:
            return None  # Convert to NaN
        try:
            return float(eval(size))  # Convert to actual float
        except:
            return None  # If conversion fails, return NaN
    return size  # If already numeric, return as is

# ✅ Function to Train the Model
def train_rating_model():
    # Load dataset
    data_path = os.path.join(settings.MEDIA_ROOT, "googleplaystore.csv")
    df = pd.read_csv(data_path)

    # ✅ Clean and Convert Numerical Features
    df['Installs'] = df['Installs'].str.replace(r'[+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    # ✅ Convert 'Size' to Numeric
    df['Size'] = df['Size'].apply(convert_size)

    # Drop rows with missing values in required columns
    df.dropna(subset=['Rating', 'App', 'Category', 'Reviews', 'Installs', 'Size'], inplace=True)

    # ✅ Encode Categorical Features
    le_category = LabelEncoder()
    le_app = LabelEncoder()

    df['Category'] = le_category.fit_transform(df['Category'].astype(str))
    df['App'] = le_app.fit_transform(df['App'].astype(str))

    # Features and target
    X = df[['App', 'Category', 'Reviews', 'Installs', 'Size']]
    y = df['Rating']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ✅ Train Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # ✅ Evaluate Model
    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    # ✅ Save Model and Encoders
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(rf, MODEL_PATH)
    joblib.dump(le_category, ENCODER_PATHS["category"])
    joblib.dump(le_app, ENCODER_PATHS["app"])

    return mae, mse

# ✅ Django View to Train Model
def training(request):
    mae, mse = train_rating_model()
    return render(request, 'users/training.html', {'mae': mae, 'mse': mse})


import random  # To generate random values
from django.shortcuts import render
import joblib
import numpy as np

def Predication(request):
    user = request.session.get('username')

    if request.method == 'POST':
        try:
            # ✅ Get input values
            app = request.POST.get('app', '').strip()
            category = request.POST.get('category', '').strip()
            size = request.POST.get('size', '').strip()
            reviews = request.POST.get('reviews', '0').strip()
            installs = request.POST.get('installs', '0').strip()

            # ✅ Convert numeric values safely
            reviews = int(reviews) if reviews.isdigit() else 0
            installs = int(installs.replace(',', '')) if installs.replace(',', '').isdigit() else 0

            # ✅ Ensure 'Size' is an integer; replace invalid values with a random number
            if size.isdigit():
                size = int(size)
            else:
                size = random.randint(5000, 500000)  # Random replacement value

            # ✅ Load trained model and encoders
            try:
                rf_model = joblib.load(MODEL_PATH)
                le_category = joblib.load(ENCODER_PATHS["category"])
                le_app = joblib.load(ENCODER_PATHS["app"])
            except FileNotFoundError:
                return render(request, 'users/predication.html', {
                    "user": user,
                    "error": "Model files not found! Please train the model first."
                })

            # ✅ Encode input values (Handle unseen categories dynamically)
            def encode_value(encoder, value):
                if value in encoder.classes_:
                    return encoder.transform([value])[0]
                else:
                    encoder.classes_ = np.append(encoder.classes_, value)
                    return encoder.transform([value])[0]

            app_encoded = encode_value(le_app, app)
            category_encoded = encode_value(le_category, category)

            # ✅ Perform prediction
            prediction = rf_model.predict([[app_encoded, category_encoded, reviews, installs, size]])[0]

            return render(request, 'users/predication.html', {
                "user": user,
                "prediction": round(prediction, 2),
                "random_size_used": size  # Show if a random value was used
            })

        except ValueError:
            return render(request, 'users/predication.html', {
                "user": user,
                "error": "Invalid input! Please enter valid numbers for Reviews and Installs."
            })
        
        except Exception as e:
            return render(request, 'users/predication.html', {
                "user": user,
                "error": f"Unexpected error: {str(e)}"
            })

    return render(request, 'users/predication.html', {"user": user})


