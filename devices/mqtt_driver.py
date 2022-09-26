import random
from paho.mqtt import client as mqtt_client
from light_controller import LightController
from light import Light
import time
import json

ROOT_TOPIC = '/lighting/driver'

# subscribes to these topics
UPDATE_CONTROLLER = 'updateController'
CREATE_CONTROLLER = 'createController'
LOAD_CONTROLLERS = 'loadControllers'

# publishes to these topics
CONTROLLER_UPDATED = 'controllerUpdated'


def connect_mqtt(username, password, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


class Driver:
    def __init__(self, client, root_topic=ROOT_TOPIC):
        self.client = client
        self.root_topic = root_topic
        self.controllers = {}
        self.subscribe_to_topics()
        

    def subscribe_to_topics(self):
        self.client.subscribe(f"{self.root_topic}/{UPDATE_CONTROLLER}")
        self.client.subscribe(f"{self.root_topic}/{CREATE_CONTROLLER}")
        self.client.subscribe(f"{self.root_topic}/{LOAD_CONTROLLERS}")

        self.client.on_message = self.on_message


    def on_message(self, client, userdata, msg):
        topic = msg.topic
        json_data = json.loads(str(msg.payload.decode("utf-8", "ignore")))

        action = topic.split('/')[-1]
        print(action)

        if action == UPDATE_CONTROLLER:
            print('updated controller')
            ctrl_id = json_data['id']

            # turn the lights for the designated controller on
            # as if motion had been detected in the room
            # this allows the controller to still scale the brightness automatically, depending on the light already in the room
            # but also allows a user to manually turn a light on using a webpage
            self.controllers[ctrl_id].force_motion()

        if action == CREATE_CONTROLLER:
            print('added controller')
            ctrl_id = json_data['id']

            self.add_controller(ctrl_id)

        if action == LOAD_CONTROLLERS:
            print('loaded controllers')
            self.load_controllers(json_data)



    def main_loop(self):
        while True:
            self.client.loop_start()
            for id, ctrl in self.controllers.items():
                update = ctrl.get_update()
                if(update):
                    self.publish_update(update)
                time.sleep(1)

            time.sleep(10)

            

    def publish_update(self, update):
        topic = f"{self.root_topic}/{CONTROLLER_UPDATED}"
        msg = json.dumps(update)
        result = self.client.publish(topic, msg)
    

    def add_controller(self, ctrl_id):
        ctrl = LightController(ctrl_id)
        self.controllers.update({ctrl_id:ctrl})


    def load_controllers(self, id_list):
        if(len(self.controllers) == 0):
            for id in id_list:
                self.add_controller(id)

    # def add_light(self, ctrl_id, light_id):
    #     light = Light(light_id)
    #     self.controllers[ctrl_id].lights.append(light)



if __name__ == '__main__':
    broker = 'broker.emqx.io'
    port = 1883
    username = 'emqx'
    password = 'public'
    client = connect_mqtt(username, password, broker, port)
    d = Driver(client)
    d.main_loop()

