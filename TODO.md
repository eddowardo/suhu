# TODO: Integrate DHT22 + NodeMCU Sensor to Django Web App

## Backend Django Updates
- [x] Add POST endpoint in views.py to receive sensor data (temperature, humidity) and save to TemperatureReading model
- [x] Update serializers.py to handle input data from sensor (add humidity field if needed)
- [x] Update urls.py to add new API path for sensor data submission
- [x] Update settings.py to allow CORS for sensor requests (install django-cors-headers if needed)

## NodeMCU Configuration
- [x] Create Arduino code for NodeMCU to read DHT22 data and send via HTTP POST to Django API
- [ ] Test WiFi connection and POST request in NodeMCU code

## Frontend Dashboard Updates
- [x] Update views.py index view to fetch real data from database instead of dummy data
- [ ] Update index.html JavaScript to load real sensor data and update charts dynamically

## Testing and Deployment
- [x] Run Django server and test API endpoint with Postman/curl
- [ ] Upload NodeMCU code and verify data transmission
- [x] Verify data appears in dashboard and database
- [ ] Debug any connection or data issues
