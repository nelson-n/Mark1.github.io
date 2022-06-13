
import time
import board
import adafruit_dht

# Initiate temperature sensor.
dht11 = adafruit_dht.DHT11(board.D4) # Temperature sensor is connected to GPIO pin 4.

# Initiate relay control.
import RPi.GPIO as GPIO
relay_pin = 17 # Relay is attached to GPIO pin 17.
GPIO.setmode(GPIO.BCM) # Specify GPIO numbers instead of board numbers.
GPIO.setup(relay_pin, GPIO.OUT) # GPIO assign mode.

# Heating loop.
while True:
    try:

        # Find current temperature.
        temperature_c = dht11.temperature
        temperature_f = temperature_c * (9/5) + 32
        humidity = dht11.humidity

        if temperature_f < 77.0:
            GPIO.output(relay_pin, GPIO.HIGH)

        if temperature_f >= 77.0:
            GPIO.output(relay_pin, GPIO.LOW)

        print("Temp: {:.1f} F, Humidity: {}%".format(temperature_f, temperature_c, humidity))

        time.sleep(60.0)

    # If a sensor error occurs, sleep and then continue loop.
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue

    # If fatal error occurs, exit loop and shut off heater.
    except Exception as error:
        dht11.exit()
        GPIO.output(relay_pin, GPIO.LOW)
        raise Exception("Heater Stopped")

    # If keyboard interrupt, shut off heater.
    except KeyboardInterrupt:
        dht11.exit()
        GPIO.output(relay_pin, GPIO.LOW)
        raise Exception("Heater Stopped")
        
