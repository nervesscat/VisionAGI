from agi_core import Tasker as T
from action import Actioner as A

def run():
    conn = T()
    conn.createNormalTasks('Search (Hint: Im using linux).')

if __name__ == "__main__":
    run()