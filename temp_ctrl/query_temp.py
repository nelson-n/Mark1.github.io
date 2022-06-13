
import time
import board
import adafruit_dht

# Initiate temperature sensor.
dht11 = adafruit_dht.DHT11(board.D4) # Temperature sensor is connected to GPIO pin 4.


# Find current temperature.
temperature_c = dht11.temperature
temperature_f = temperature_c * (9/5) + 32
humidity = dht11.humidity

print("Temp: {:.1f} F, Humidity: {}%".format(temperature_f, temperature_c, humidity))

