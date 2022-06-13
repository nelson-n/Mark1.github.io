
import time
import board
import adafruit_dht

# Initiate relay control.
import RPi.GPIO as GPIO
relay_pin = 17 # Relay is attached to GPIO pin 17.
GPIO.setmode(GPIO.BCM) # Specify GPIO numbers instead of board numbers.
GPIO.setup(relay_pin, GPIO.OUT) # GPIO assign mode.

# Turn heater off.
GPIO.output(relay_pin, GPIO.HIGH)

