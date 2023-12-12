from agi_core import Tasker, VisualAI 
from action import Actioner, Utils
from grafics import GraphicsTools

def run():
    conn = Tasker()
    #conn.create_normal_tasks('Open discord app and then write la pampara')
    #conn.create_vision_tasks('Open the browser (Hint: Youre using linux and firefox installed) and go to the unah virtual campus')
    #GraphicsTools("screenshot.png").insert_mouse_cursor(1895, 64, "screenshot_cursor.png")
    VisualAI().create_visual_tasks('Find the login button')

if __name__ == "__main__":
    run()