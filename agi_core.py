from action import Actioner, Utils
from grafics import GraphicsTools
from configuration import Configuration
from openai_conn import OpenAIConn
from print_handler import PrintHandler as handler

class Tasker(OpenAIConn):
    __system_message = Configuration.SYSTEM_MESSAGE_TASKER
    
    def __init__(self):
        super().__init__(self.__system_message)
        self.__actioner = Actioner()
        self.__util = Utils()
        self.__print_handler = handler()

    def create_normal_tasks(self, super_task):
        self.__print_handler.print_loading()
        todo = self._create_text_completion(super_task)
        self.__print_handler.break_loading()
        self.__print_handler.print_super_task(super_task, len(todo["list"]))
        self.traverse_tasks(todo["list"])

    def traverse_tasks(self, tasks):
        for task in tasks:
            handler().print_task(task["id"], task["task"])
            if task["super-task"]:
                self.create_normal_tasks(task["task"])
            else:
                self.create_primitive_task(task)

    def create_primitive_task(self, task):
        if task["action"] == "Move":
            #self.__actioner.moveUsingAxis(task["x"], task["y"])
            pass
        elif task["action"] == "Press":
            self.__actioner.press_keys(task["key"])
        elif task["action"] == "Type":
            self.__actioner.type_text(task["text"])
        elif task["action"] == "Wait":
            self.__actioner.wait(2)
        elif task["action"] == "Execute":
            self.__actioner.execute(task["command"])

    def create_vision_tasks(self, super_task):
        base64_image = self.__util.encode_image('screenshot.png')
        todo = self._create_visual_completion(super_task, base64_image)
        self.traverse_tasks(todo["list"])
        
class VisualAI(OpenAIConn):
    __system_message = Configuration.SYSTEM_MESSAGE_VISUAL

    def __init__(self):
        super().__init__(self.__system_message2)
        self.__actioner = Actioner()
        self.__util = Utils()

    def create_visual_tasks(self, super_task):
        GraphicsTools("screenshot.png").add_grid("screenmod.png")
        base64_image = self.__util.encode_image('screenmod.png')
        todo = self._create_visual_completion(super_task, base64_image)
        (x, y) = (todo["coordinates"]["x"], todo["coordinates"]["y"])
        GraphicsTools("screenshot.png").insert_mouse_cursor(x, y, "screenshot_cursor.png")

class TaskerTest:
    __system_message = """
        
    """

    def __init__(self):
        self.conn = Tasker()

    def visual_confirmation(self, super_task, super_test):
        pass