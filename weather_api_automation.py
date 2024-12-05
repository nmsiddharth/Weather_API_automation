import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText


# Step 1: Function to fetch weather data from OpenWeatherMap API
def get_weather_api(city,api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                                                        # api_key = "6923d774071fae92bb5164e8e8215501"
    # Make a request to OpenWeatherMap API
    response = requests.get(url)

    # Check if the response is successful ( Status code 200 )
    if response.status_code==200:
        data = response.json()  # To extract the JSON content from the API response

        # Return selected weather details
        return {
            "city": data["name"],  # City name
            "temperature": data["main"]["temp"],  # Temperature in Celsius
            "humidity": data["main"]["humidity"],  # Humidity percentage
            "weather": data["weather"][0]["description"]  # Weather condition
        }
    else:
        # If the API request failed, print the error message and return None
        print(f"Error: {response.status_code}, {response.json().get('message','No details available')}")
        return None


# Step 2: Function to display weather data in console
def display_weather(weather):
    print(f"Weather update for {weather['city']}: ")
    print(f"  - Temperature: {weather['temperature']}°C")
    print(f"  - Humidity: {weather['humidity']}%")
    print(f"  - Condition: {weather['weather']}")


# Step 3: Function to send Weather updates via email
def send_email(weather_data,recipient_email,sender_email,sender_password):
    subject = "Weather Updates"   # Email Subject

    # Create the email body with weather details for multiple cities
    body = "Weather Updates for the cities:\n\n"

    # Loop through the weather data of each city and add to the email body
    for weather in weather_data:
        body+=f"Weather update for {weather['city']}\n"
        body+=f"    - Temperature: {weather['temperature']}°C\n"
        body+=f"    - Humidity: {weather['humidity']}%\n"
        body+=f"    - Condition: {weather['weather']}\n\n"

    # Create the MIMEText message (plain text email)
    message = MIMEText(body)
    message["Subject"] = subject                           # When you create a MIMEText object using the MIMEText(body) constructor,
    message["From"] = sender_email                         # it initially only contains the body of the email (the main content).
    message["To"] = recipient_email                        # However, the MIMEText class supports the addition of email headers as metadata, such as Subject, From, and To.
                                                           # These headers are separate from the body of the email but are part of the message object.

# Sending Email using SMTP
    try:
        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()   # Secure the connection using tls
            server.login(sender_email,sender_password)
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Step 4: Job function to fetch weather data and send email. It combines all functions and handle the main workflow.
def job():
    API_KEY = "6923d774071fae92bb5164e8e8215501"
    cities = ['Bengaluru','Kolkata']
    recipient = "nmsiddharth5069@gmail.com"
    sender = "nmsiddharth5069@gmail.com"
    password = "cuhf ryqs oicu jiph"

    # List to store weather data for all cities
    weather_data = []

    # Loop through cities and fetch weather data for each one
    for city in cities:
        weather = get_weather_api(city,API_KEY)
        if weather:      # If weather data is successfully fetched
            display_weather(weather)
            weather_data.append(weather)   # Add weather data to the list
        else:         # Handle the case where the API request fails
            print(f"Failed to fetch weather data for {city}.")

    # If weather data is fetched atleast for one city, send mail
    if weather_data:
        send_email(weather_data,recipient,sender,password)

# Call the job function once to send the email
#job()


# Step 5: Schedule the job to run for every 1 minute
schedule.every(1).minutes.do(job)

# Run the scheduled tasks
print("Starting weather automation script. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()     # It checks if any scheduled task (in this case, job) is due to run.
    time.sleep(1)
