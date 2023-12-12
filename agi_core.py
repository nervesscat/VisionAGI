from openai import OpenAI
from action import Actioner, Utils
from grafics import GraphicsTools

class OpenAIConn:
    __system_message = ""
    __gpt4_name_model = "gpt-4-1106-preview"
    __gpt3_name_model = "gpt-3.5-turbo-1106"
    __gptv_name_model = "gpt-4-vision-preview"

    def __init__(self, system_message):
        self.client = OpenAI()
        self.util = Utils()
        self.__system_message = system_message

    def _create_text_completion(self, super_task, gpt4=False):
        if gpt4:
            model = self.__gpt4_name_model
        else:
            model = self.__gpt3_name_model

        print(self.__system_message)

        response = self.client.chat.completions.create(
            model = model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.__system_message},
                {"role": "user", "content": super_task},
            ]) 

        print(response.choices[0].message.content)
        return self.util.parse_json(response.choices[0].message.content)

    def _create_visual_completion(self, super_task, base64_image):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text" : self.__system_message + "\n" + super_task},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                        },
                    },
                ],
            }
        ],
          max_tokens=500,
        )

        print(response.choices[0].message.content)
        return self.util.parse_and_clean(response.choices[0].message.content)

    def set_system_message(self, system_message):
        self.__system_message = system_message

class Tasker(OpenAIConn):
    __system_message = """
        The prompt given to you'll be called as the prompt-super-task and you also be probably given an image.
        Let say that a primitive task is a task that can be done in a single step, this will only be the following: Move Mouse, Type, Press, Wait or Execute some command in the terminal.
        Let say that the super-task (non primitive-task) is a complex task that can be broken down into multiple primitive tasks, example "Open ...".
        You'll create a TODO (A list of primitive-task or super-task) in order to complete the prompt-super-task, example "1- Move Mouse ... <- \n2- Type ...".
        Make sure that the list is in the correct order.
        If the prompt-super-task is too complex (for ex. Open A Youtube Video of ...), you can break it down into multiple other super-tasks.
        Avoid creating a list of more than 10 tasks.
        You'll also include what do you expect when the TODO is done, example "The browser should be opened".
        You know that a super-task will be non-deterministic, so you'll not know whether finishing a super-task will lead to the expected result or not, 
        so you'll need to create a test for each super-task, example "The browser should be opened".
        Try to use shortcuts, example "Open the browser" -> "Win + R" -> "firefox" -> "Enter".
        When you create a primitive-task, if this is the type action "Type", you'll need to specify what to type, example "youtube.com".
        When you create a primitive-task, if this is the type action "Press", you'll need to specify what key to press, example "Enter", if it's a combination of keys, you'll need to specify them as an array ["Ctrl", "s"].
        If you open a program using the terminal, you should use the Execute primitive command instead of open a new terminal
        Every time you open the browser, you'll create a new tab, so you'll need to create a primitive-task for that.
        Your response will be in a JSON format (Don't add another text!! Only the JSON is allowed), example:
        {
            "task": "Open Youtube",
            "super-task": true,
            "super-test": "Youtube main page should be shown",
            "list": [
                {
                    "id": 1,
                    "task": "Open the browser (firefox)",
                    "super-task": false,
                    "action": "Execute",
                    "command": "firefox",
                },
                {
                    "id": 2,
                    "task": "Wait for the browser to open",
                    "super-task": false,
                    "action": "Wait",
                },
                {
                    "id": 3,
                    "task": "Change window",
                    "super-task": false,
                    "action": "Press",
                    "key": ["Alt", "Tab"]
                },
                {
                    "id": 4,
                    "task": "Create a new tab",
                    "super-task": false,
                    "action": "Press",
                    "key": ["Ctrl", "T"]
                },
                {
                    "id": 5,
                    "task": "Type youtube.com",
                    "super-task": false,
                    "action": "Type",
                    "text": "youtube.com",
                },
                {
                    "id": 6,
                    "task": "Wait for the page to load",
                    "super-task": false,
                    "action": "Wait",
                },
            ]
        }
        """
    
    def __init__(self):
        super().__init__(self.__system_message)
        self.actioner = Actioner()
        self.util = Utils()

    def create_normal_tasks(self, super_task):
        todo = self._create_text_completion(super_task)
        self.traverse_tasks(todo["list"])

    def traverse_tasks(self, tasks):
        for task in tasks:
            if task["super-task"]:
                self.create_normal_tasks(task["task"])
            else:
                self.create_primitive_task(task)

    def create_primitive_task(self, task):
        if task["action"] == "Move":
            #self.actioner.moveUsingAxis(task["x"], task["y"])
            pass
        elif task["action"] == "Press":
            self.actioner.press_keys(task["key"])
        elif task["action"] == "Type":
            self.actioner.type_text(task["text"])
        elif task["action"] == "Wait":
            self.actioner.wait(2)
        elif task["action"] == "Execute":
            self.actioner.execute(task["command"])

    def create_vision_tasks(self, super_task):
        base64_image = self.util.encode_image('screenshot.png')
        todo = self._create_visual_completion(super_task, base64_image)
        self.traverse_tasks(todo["list"])
        
class VisualAI(OpenAIConn):
    __system_message = """
        You're an expert in the visual domain and coordinates, you're an expert in follow grids correctly.
        The prompt given to you'll be called as the prompt-task.
        You will have understand how to complete the prompt-task using the image, for example if the task is close the browser, 
        you'll need to find the close button and then in a JSON format you'll need to specify the coordinates of the close button.

        The image that you'll be given will be a screenshot of the screen, it has a grid to help you to find the coordinates of the elements.
        Remember, you're an expert in the visual domain, so you'll need to find the coordinates of the elements in the image following the grid.

        Create a reasoning of where the element is located in the image and then the JSON format

        The blue lines are not taged, the red lines are taged, the red lines are 200px scale, the blue lines are 100px scale.

        Remainder: Obviusly a lot of elements don't touch the lines, so as an expert in finding coordinates
        don't be afraid to give a coordinate that is not exactly in the line, but it's near by the line.

        Response example:

        The close button is the x in the right top corner of the browser, this is near by the first blue row (100px) but it didn't touch it, it's at the middle,
        also it's near by the last blue column (1900px) but it barely touch it, so the coordinates are (1898, 63).

        ```json
        {
            "task": "Close the browser",
            "coordinates": {
                "x": 100,
                "y": 200
            }
        }
        ```
    """
    def __init__(self):
        super().__init__(self.__system_message)
        self.actioner = Actioner()
        self.util = Utils()

    def create_visual_tasks(self, super_task):
        GraphicsTools("screenshot.png").add_grid("screenmod.png")
        base64_image = self.util.encode_image('screenmod.png')
        todo = self._create_visual_completion(super_task, base64_image)
        (x, y) = (todo["coordinates"]["x"], todo["coordinates"]["y"])
        GraphicsTools("screenshot.png").insert_mouse_cursor(x, y, "screenshot_cursor.png")
        #self.traverse_tasks(todo["list"])