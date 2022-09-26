import random
import time

# after 60 minutes with no motion detected, the lights will automatically turn off
MOTION_DETECT_THRESHOLD_MINS = 60

class LightController:
    def __init__(self, id):
        self.id = id
        self.lights = []
        self.last_motion_detected = time.time() # if this value is past a certain threshold, automatically switch off the controlled lights
        self.light_harvested = 0 # if this value is past a certain threshold, scale light brightness down

        self.set_brightness = 100
        self.motion_detected = False


    def __str__(self):
        return f"\nID: {self.id}\nBrightness: {self.set_brightness}\nMotion Detected: {self.motion_detected}\nLight harvested: {self.light_harvested}"
        
    def force_motion(self):
        self.last_motion_detected = time.time()
        self.handle_motion()
        self.scale_brightness()
        self.update_lights()

    def get_update(self):
        update = {}
        if(self.random_update()):
            update = {
                'id': self.id,
                'brightness': self.set_brightness,
                'last_motion_detected': self.last_motion_detected
            }

        return update


    def update_lights(self):
        for light in self.lights:
            light.brightness = self.set_brightness

    def random_update(self):
        should_update = False
        if(random.randint(0, 10) > 8):
            self.last_motion_detected = time.time()
            should_update = True

        if(random.randint(0, 10) > 4):
            self.light_harvested = random.randint(1, 100)
            should_update = True

        self.handle_motion()
        self.scale_brightness()

        return should_update


    def scale_brightness(self):
        # if motion has been detected recently
        if(self.motion_detected):
            # scale down set brightness as light increases
            self.set_brightness = max(1, 100 - self.light_harvested)
        else:
            # no motion has been found recently, turn off lights by reducing brightness to 0
            self.set_brightness = 0

    def handle_motion(self):
        last_motion_secs = time.time() - self.last_motion_detected
        # last_motion_mins = last_motion_secs // 60 
        # for testing purposes, last motion in measured in seconds
        # for practical purposes, it would be measured in minutes
        self.motion_detected = (last_motion_secs < MOTION_DETECT_THRESHOLD_MINS)


if __name__ == "__main__":
    l_ctrl = LightController(1)
    while True:
        l_ctrl.random_update()
        time.sleep(3)

