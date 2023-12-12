from openai import OpenAI
from action import Actioner

class Tasker:
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
        Try to use shortcuts, example "Open the browser" -> "Win + R" -> "chrome" -> "Enter".
        When you create a primitive-task, if this is the type action "Type", you'll need to specify what to type, example "youtube.com".
        When you create a primitive-task, if this is the type action "Press", you'll need to specify what key to press, example "Enter", if it's a combination of keys, you'll need to specify them as an array ["Ctrl", "s"].

        If you open the browser with the terminal, you should change the window using Alt +
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
        self.client = OpenAI()
        self.actioner = Actioner()


    def createNormalTasks(self, super_task):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.__system_message},
                {"role": "user", "content": super_task},
            ]) 

        print(response.choices[0].message.content)
        json_response = self.actioner.parseJSON(response.choices[0].message.content)
        self.traverseTasks(json_response["list"])

    def traverseTasks(self, tasks):
        for task in tasks:
            if task["super-task"]:
                self.createNormalTasks(task["task"])
            else:
                self.createPrimitiveTask(task)

    def createPrimitiveTask(self, task):
        if task["action"] == "Move":
            #self.actioner.moveUsingAxis(task["x"], task["y"])
            pass
        elif task["action"] == "Press":
            self.actioner.pressKey(task["key"])
        elif task["action"] == "Type":
            self.actioner.typeText(task["text"])
        elif task["action"] == "Wait":
            self.actioner.wait(2)
        elif task["action"] == "Execute":
            self.actioner.execute(task["command"])

    def createVisionTasks(self, super_task):
        base64_image = self.actioner.takeScreenshot()

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
          max_tokens=800,
        )

        print(response.choices[0].message.content)
        