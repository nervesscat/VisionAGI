from agi_core import Tasker
from print_handler import PrintHandler as handler
from grafics import GraphicsTools
import uuid
import argparse

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='run in test in every task')
    args = parser.parse_args()

    id = uuid.uuid4()
    handler().print_welcome()
    try:
        prompt = input("Give me a task > ")
        conn = Tasker(str(id)+".png", args.test)
        conn.create_vision_tasks(prompt)
    except KeyboardInterrupt:
        print("\nBye!")
        exit()
    finally:
        print("\nBye!")
        GraphicsTools(str(id)+".png").delete_all_images()
        exit()

if __name__ == "__main__":
    run()