import mysql.connector
from django.shortcuts import render, redirect
from django.contrib import messages
import requests # type: ignore
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
# Create your views here.
def home(request):
    return render(request,'index.html',{})
def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ClimateSmartAgriculture",
         charset="utf8"  
    )

# Function to Execute Queries
def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    conn = db_connect()
    cursor = conn.cursor()
    
    cursor.execute(query, params)

    result = None
    if fetch_one:
        result = cursor.fetchone()
    elif fetch_all:
        result = cursor.fetchall()
    else:
        conn.commit()  # Commit only for INSERT, UPDATE, DELETE

    cursor.close()
    conn.close()
    return result

# Function to Insert User Data
def register_user(name, email, password, phone, location):
    conn = db_connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO farmers (name, email, password, phone, location) VALUES (%s, %s, %s, %s, %s)",
            (name, email, password, phone, location),
        )
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()

# Register Page
def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        location = request.POST["location"]

        result = register_user(name, email, password, phone, location)

        if result is True:
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Error: " + result)

    return render(request, "register.html")
# Login Page
# User Login Function
def login_user(email, password):
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM farmers WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        return user  # Returns user details if found, else None
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()

# Login View
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = login_user(email, password)

        if user:
            request.session["user_id"] = user["id"]
            request.session["user_name"] = user["name"]
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Redirect to dashboard
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")

# Logout View
def logout(request):
    request.session.flush()  # Clear session data
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Dashboard Page
def dashboard(request):
    if "user_id" in request.session:
        return render(request, "dashboard.html")
    return redirect("login")

# Logout
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect("index")
def weather_details(request):
    weather_data = {}  # Default empty dictionary

    if request.method == "POST":
        city = request.POST.get("city")
        API_KEY = "47646a079e76400abe7181644251903"  # 🔑 API Key Enter பண்ணுங்க
        BASE_URL = "http://api.weatherapi.com/v1/current.json"

        response = requests.get(f"{BASE_URL}?key={API_KEY}&q={city}")

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "temperature": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "condition": data["current"]["condition"]["text"],
                "wind_speed": data["current"]["wind_kph"],
                "location": data["location"]["name"]
            }
        else:
            weather_data = {"error": "Invalid City Name or API Issue!"}

    return render(request, "weather_details.html", {"weather": weather_data})

def get_soil_data(city):
    API_KEY = "96b0f62b338c5f4a3b7f5d1e38650e90"  # OpenWeather API Key மாற்றவும்
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            # மண்ணின் ஈரப்பதம் கணிப்பதற்கான logic (Assumed)
            if humidity < 40:
                soil_moisture = "குறைந்த ஈரப்பதம் (Dry)"
            elif 40 <= humidity < 70:
                soil_moisture = "மிதமான ஈரப்பதம் (Moderate)"
            else:
                soil_moisture = "அதிக ஈரப்பதம் (Wet)"

            return {
                "city": city,
                "temperature": temperature,
                "soil_moisture": soil_moisture,
                "condition": condition.capitalize()
            }
        else:
            return None
    except Exception as e:
        return None

def soil_analysis(request):
    analysis = None

    if request.method == "POST":
        city = request.POST.get("city")
        analysis = get_soil_data(city)

    return render(request, "soil_analysis.html", {"analysis": analysis})
# பயிர் தரவுகள் (மண்ணின் ஈரப்பதம் மற்றும் வெப்பநிலைக்கு ஏற்ப)
CROP_DATA = {
    "dry": ["மக்காச்சோளம்", "கோதுமை", "பார்லி"],
    "moderate": ["நெல்", "மணல் பயிர்கள்", "தக்காளி"],
    "wet": ["பாசி பயிர்கள்", "தண்ணீர் நேசிக்கும் பயிர்கள்", "கொய்யா"]
}

def get_weather(city):
    API_KEY = "96b0f62b338c5f4a3b7f5d1e38650e90"  # உங்கள் API கீயை இங்கே இடவும்
    url = f"https://api.open-meteo.com/v1/forecast?latitude=10.8&longitude=79.1&daily=soil_moisture_0_to_7cm,temperature_2m_max&timezone=Asia/Kolkata"
    
    try:
        response = requests.get(url)
        data = response.json()

        # வெப்பநிலை மற்றும் மண்ணின் ஈரப்பதம் பெறுதல்
        temperature = data["daily"]["temperature_2m_max"][0]
        moisture = data["daily"]["soil_moisture_0_to_7cm"][0]

        return temperature, moisture
    except Exception as e:
        return None, None

# பயிர் பரிந்துரைக்கும் function
def recommend_crop(soil_type, ph_value, rainfall):
    crops = {
        "சல்லி மண்": {
            "low_ph": "மாம்பழம்",
            "medium_ph": "பயறு",
            "high_ph": "பன்னீர் திராட்சை"
        },
        "கரிசல் மண்": {
            "low_ph": "வேர்க்கடலை",
            "medium_ph": "தக்காளி",
            "high_ph": "அரசந்தி"
        },
        "நுண் மணல் மண்": {
            "low_ph": "எள்",
            "medium_ph": "பாசிப் பருப்பு",
            "high_ph": "நெல்லு"
        }
    }

    ph_category = "low_ph" if ph_value < 5.5 else "medium_ph" if ph_value < 7.5 else "high_ph"

    return crops.get(soil_type, {}).get(ph_category, "பயிர் தகவல் கிடைக்கவில்லை")

# Crop Recommendation View
def crop_recommendation(request):
    crop = None

    if request.method == "POST":
        soil_type = request.POST.get("soil_type")
        ph_value = float(request.POST.get("ph_value"))
        rainfall = int(request.POST.get("rainfall"))

        crop = recommend_crop(soil_type, ph_value, rainfall)

    return render(request, "crop_recommendation.html", {"crop": crop})

def analytics_reports(request):
    # Use a fixed city or make it dynamic as needed
    city = "Thanjavur"
    weather_api_key ="96b0f62b338c5f4a3b7f5d1e38650e90"  # Replace with your key

    # --- Weather Data from OpenWeatherMap ---
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_json = weather_response.json()
        weather_data = {
            'city': city,
            'temperature': weather_json['main']['temp'],
            'humidity': weather_json['main']['humidity'],
            'pressure': weather_json['main']['pressure'],
            'weather_description': weather_json['weather'][0]['description'],
            'wind_speed': weather_json['wind']['speed'],
        }
    except Exception as e:
        return render(request, "analytics_reports.html", {"error": f"Error fetching weather data: {e}"})

    # --- Dummy Crop Data (Replace with actual logic if available) ---
    crop_data = {
        'recommended_crop': 'Rice',
        'sowing_season': 'June to July',
        'harvest_time': 'November to December',
        'yield': 4.5,
    }

    # --- Dummy Soil Data (Replace with actual soil API/logic if available) ---
    soil_data = {
        'ph_level': 6.5,
        'nitrogen_content': 30,
        'phosphorus_content': 20,
        'potassium_content': 25,
        'organic_matter': 3.5,
    }

    # Combine all data into a context dictionary
    context = {
        'city': weather_data['city'],
        'temperature': weather_data['temperature'],
        'humidity': weather_data['humidity'],
        'pressure': weather_data['pressure'],
        'weather_description': weather_data['weather_description'],
        'wind_speed': weather_data['wind_speed'],
        'crop_data': crop_data,
        'soil_data': soil_data,
    }

    return render(request, "analytics_reports.html", context)
def agri_support(request):
    return render(request, 'agri_support.html')



def download_excel(request):
    # For demonstration, we create a DataFrame using the same dummy data
    data = {
        "Category": ["Weather", "Crop", "Soil"],
        "Parameter": [
            f"Temperature:  {request.GET.get('temperature', '25')} °C, Humidity: {request.GET.get('humidity', '70')}%, Description: {request.GET.get('weather_description', 'clear sky')}",
            f"Recommended Crop: Rice, Sowing Season: June-July, Harvest: Nov-Dec, Yield: 4.5 tons/ha",
            f"pH: 6.5, Nitrogen: 30 mg/kg, Phosphorus: 20 mg/kg, Potassium: 25 mg/kg, Organic Matter: 3.5%"
        ]
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='AnalyticsReport')
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Analytics_Report.xlsx"'
    return response