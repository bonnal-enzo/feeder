import time
import sys
import random
from pynput.mouse import Button, Controller, Listener

class ClicPoint:

    actions_delay_seconds = 1
    mouse = Controller()

    def __init__(self, coords):
        self.coords = coords
    
    def delay(self):
        # sleep minimum actions_delay_seconds and up to 150% of actions_delay_seconds
        time.sleep(self.actions_delay_seconds * (1 + random.random() / 2))

    def point_at(self, exit_if_moved=True):
        self.mouse.position = self.coords.tuple
        self.delay()
        if exit_if_moved and abs(self.mouse.position[0] - self.coords.tuple[0]) > 5:
           sys.exit(0)

    def clic(self):
       self.point_at()
       
       self.mouse.click(Button.left, 1)
       self.delay()
       
    def double_clic(self):
       self.point_at()
       self.mouse.click(Button.left, 2)
       self.delay()

    def drag_and_drop(self, target_point):
       self.point_at()
       self.mouse.press(Button.left)
       self.delay()
       target_point.point_at()
       self.mouse.release(Button.left)
       self.delay()

class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = (x, y)

    def minus(self, coords):
        return Coords(self.x - coords.x, self.y - coords.y)
    
    def plus(self, coords):
        return Coords(self.x + coords.x, self.y + coords.y)
    
    def times(self, scalar):
        return Coords(scalar * self.x, scalar * self.y)


class DragAndDropsRecorder:
    def __init__(self):
        self.clicks = []
        on_click = lambda x, y, button, pressed: self.clicks.append((x, y))
        self.listener: Listener = Listener(on_click=on_click)

    def start(self):
        self.listener.start()
    
    def stop(self):
        self.listener.stop()
        time.sleep(0.1)

    def last_origin(self):
        """
        Origin of the last drag and drop event
        """
        return Coords(*self.clicks[-2])

    def last_vector(self):
        """
        Vector of the last drag and drop event
        """
        return Coords(
            self.clicks[-1][0] - self.clicks[-2][0],
            self.clicks[-1][1] - self.clicks[-2][1]
        )
