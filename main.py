from agi_core import Tasker
from print_handler import PrintHandler as handler

def run():
    handler().print_welcome()
    try:
        prompt = input("Give me a task > ")
        conn = Tasker()
        conn.create_normal_tasks(prompt)
    except KeyboardInterrupt:
        print("\nBye!")
        exit()

if __name__ == "__main__":
    run()