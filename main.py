from agi_core import Tasker
from print_handler import PrintHandler as handler
import uuid
def run():
    id = uuid.uuid4()
    handler().print_welcome()
    try:
        prompt = input("Give me a task > ")
        conn = Tasker(str(id)+".png")
        conn.create_vision_tasks(prompt)
        
    except KeyboardInterrupt:
        print("\nBye!")
        exit()

if __name__ == "__main__":
    run()