import os
import paho.mqtt.client as mqtt
from picamera import PiCamera
from time import sleep
from datetime import datetime

# Camera setup
camera = PiCamera()
camera.resolution = (1024, 768)

# MQTT setup
MQTT_BROKER = '9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
MQTT_TOPIC = 'scout'
CLIENT_ID = 'cropscout'
USERNAME = 'sergiu.doncila'
PASSWORD = 'QWEasd!@#123'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.connected_flag = True

def on_publish(client, userdata, mid):
    print("Message Published...")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.tls_set('mqtt.crt')
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

current_time = datetime.now()
dir_name = current_time.strftime('%d-%m-%Y-%H-%M-%S')
photo_dir = f'/home/pi/drone_photos/{dir_name}'
os.makedirs(photo_dir, exist_ok=True)

try:
    for i in range(10):
        image_path = os.path.join(photo_dir, f'image_{i}.jpg')
        camera.capture(image_path)
        print(f'Captured {image_path}')

        with open(image_path, 'rb') as file:
            image_content = file.read()

        info = client.publish(MQTT_TOPIC, image_content)
        info.wait_for_publish()
        if info.is_published():
            os.remove(image_path)
            print(f"File {image_path} successfully uploaded and deleted.")

        sleep(60)
finally:
    camera.close()
    client.loop_stop()
    client.disconnect()
