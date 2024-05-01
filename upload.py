# pip install paho-mqtt

import os
import paho.mqtt.client as mqtt

# MQTT settings
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

# Set TLS settings: With HiveMQ Cloud, TLS is mandatory
client.tls_set('mqtt.crt')  # This line configures the client to use encrypted communication

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

image_path = 'average_fafer.jpeg'

# Read the image binary
with open(image_path, 'rb') as file:
    image_content = file.read()

# Publish the image
info = client.publish(MQTT_TOPIC, image_content)

# Wait until the message is published
info.wait_for_publish()

# Delete the file after successful upload
if info.is_published():
    # os.remove(image_path)
    print("File successfully uploaded.")

# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()
