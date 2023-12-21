from agi_core import Tasker, VisualAI, TaskerTest
from action import Actioner, Utils
from grafics import GraphicsTools
import time
import uuid
import sys

def run():
    #conn.create_vision_tasks('Open the browser (Hint: Youre using linux and firefox installed) and go to the unah virtual campus')
    #GraphicsTools("screenshot.png").insert_mouse_cursor(1895, 64, "screenshot_cursor.png")
    #VisualAI().create_visual_tasks('Find the login button')
    # wait 3 seconds
    # uuid
    id = uuid.uuid4()
    time.sleep(5)
    # Print system info
    print(sys.version_info)
    # linux or windows
    print(sys.platform)
    print(sys.version)
    print(sys.version_info)
    Actioner().take_screenshot(str(id)+".png")
    TaskerTest().visual_confirmation('Search Jazz music in the bar', 'Youtube searched elements will be shown', 'Click on the first video', str(id)+".png")
    VisualAI().locate_coordinates('Click on the first video', str(id)+".png")

    # Delete image

if __name__ == "__main__":
    run()