import falcon
#import RPi.GPIO as GPIO
import gpiozero
import threading
from queue import Queue

# Create a queue to send messages from the Falcon thread to the GPIO thread
gpio_queue = Queue()

led = gpiozero.LED(4)

# GPIO logic
def gpio_thread():
    while True:
        # Get a message from the queue
        message = gpio_queue.get()
        # Process the message
        if message == 'turn_on_led':
            led.on()
        elif message == 'turn_off_led':
            led.off()
        # Mark the message as processed
        gpio_queue.task_done()

# Falcon API
class GPIOControl:
    def on_post(self, req, resp):
        data = req.media
        
        if data['command']:
            command = data['command']
            commandList = command.split("_")
            try:
                if commandList [0] == "led":
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
                
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        resp.set_header("Access-Control-Allow-Headers", "Content-Type")
        

# Create a separate thread for GPIO logic
gpio_thread = threading.Thread(target=gpio_thread)
gpio_thread.daemon = True  # So that the thread dies when the main thread dies
gpio_thread.start()

# Create the Falcon app
app = falcon.App()
app.add_route('/API', GPIOControl())

# Run the Falcon app
if __name__ == '__main__':
    from wsgiref import simple_server
    with simple_server.make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()