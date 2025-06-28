import falcon
from falcon_cors import CORS
from config import *
import gpiozero
import threading
from queue import Queue
from time import sleep
from random import random
import json

# Create a queue to send messages from the Falcon thread to the GPIO thread
gpio_queue = Queue()

led = gpiozero.LED(TESTING_LED_PIN)
cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)

if SOILSENSORS_ACTIVE:
    sensor0 = gpiozero.MCP3008(channel=0)
    sensor1 = gpiozero.MCP3008(channel=1)
    sensor2 = gpiozero.MCP3008(channel=2)
    sensor3 = gpiozero.MCP3008(channel=3)


def correctSoilValue(value):
    
    maxValue = SOILSENSOR_DISCONNECTED_UPPER_TRESHOLD - SOILSENSOR_DISCONNECTED_LOWER_TRESHOLD
    resultValue = (value - SOILSENSOR_DISCONNECTED_LOWER_TRESHOLD) / maxValue
    # return 1-resultValue
    print(value, resultValue)
    
    if value > SOILSENSOR_DISCONNECTED_UPPER_TRESHOLD:
        return 0
    if value < SOILSENSOR_DISCONNECTED_LOWER_TRESHOLD:
        return 0
    return resultValue


def read_sensors():
    if DUMMY_ACTIVE:
        if SOILSENSORS_ACTIVE:
            soilSensorData = [0.4, 0.8, 0.2, 0.7]
        else:
            soilSensorData = None

        if WATERLEVELSENSOR_ACTIVE:
            waterLevelData = 3
        else:
            waterLevelData = None

        if TEMPERATURESENSOR_ACTIVE:
            temperatureData = 25
        else:
            temperatureData = None

        sleep(random() * 3)

    else:
        if SOILSENSORS_ACTIVE:
            print("Fetching soil sensor data")

            soilSensorData = [
                correctSoilValue(sensor0.value),
                correctSoilValue(sensor1.value),
                correctSoilValue(sensor2.value),
                correctSoilValue(sensor3.value),
            ]

        else:
            soilSensorData = None

        if WATERLEVELSENSOR_ACTIVE:
            waterLevelData = 3
        else:
            waterLevelData = None

        if TEMPERATURESENSOR_ACTIVE:
            temperatureData = 25
        else:
            temperatureData = None

    data = {
        "soilsensors": soilSensorData,
        "waterlevel": waterLevelData,
        "temperature": temperatureData,
    }

    return data


# GPIO logic
def gpio_thread():
    while True:
        # Get a message from the queue
        message = gpio_queue.get()
        # Process the message
        if message == "turn_on_led":
            led.on()
        if message == "turn_off_led":
            led.off()

        # Mark the message as processed
        gpio_queue.task_done()


# Falcon API
class GPIOControl:
    def on_post(self, req, resp):
        print("Post request received")
        data = req.media

        if data["command"]:
            command = data["command"]
            commandList = command.split("_")
            try:
                if commandList[0] == "led":
                    pinNumber = commandList[1]
                    ledState = commandList[2]
                    if ledState == "on":
                        gpio_queue.put("turn_on_led")
                    elif ledState == "off":
                        gpio_queue.put("turn_off_led")
                    resp.text = f'Command "turn led at GPIO pin {pinNumber} {ledState}" received'
            except Exception as e:
                print(e)
                resp.text = "Command not recognized"

        # resp.set_header("Access-Control-Allow-Origin", "*")
        # resp.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        # resp.set_header("Access-Control-Allow-Headers", "Content-Type")

    def on_get(self, req, resp):
        print("Get request received")
        # resp.set_header("Access-Control-Allow-Origin", "*")
        # resp.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        # resp.set_header("Access-Control-Allow-Headers", "Content-Type")

        data = read_sensors()
        resp.text = json.dumps(data)

    def on_options(self, req, resp):
        print("Options request received")
        # resp.set_header("Access-Control-Allow-Origin", "*")
        # resp.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        # resp.set_header("Access-Control-Allow-Headers", "Content-Type")
        resp.status = falcon.HTTP_OK


# Create a separate thread for GPIO logic
gpio_thread = threading.Thread(target=gpio_thread)
gpio_thread.daemon = True  # So that the thread dies when the main thread dies
gpio_thread.start()

# Create the Falcon app
app = falcon.App(middleware=[cors.middleware])
app.add_route("/API", GPIOControl(), methods=["POST", "OPTIONS", "GET"])

# Run the Falcon app
if __name__ == "__main__":
    from wsgiref import simple_server

    with simple_server.make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
