import pyautogui
import os
import json
import re

class Actioner:
    def moveUsingAxis(self, x, y):
        pyautogui.moveTo(x, y)
    
    def clickOnPosition():
        pyautogui.click()

    def pressKey(self, key):
        if type(key) == list:
            key = [k.lower() for k in key]
            if len(key) == 2:
                pyautogui.hotkey(key[0], key[1])
            elif len(key) == 3:
                pyautogui.hotkey(key[0], key[1], key[2])
        else:
            pyautogui.press(key.lower())
        pyautogui.sleep(1)

    def execute(self, command):
        os.system(command)

    def takeScreenshot():
        screenshot = pyautogui.screenshot()

    def parseJSON(textToParse):
        return json.loads(textToParse)

    #! Check this
    def parseAndClean(self, textToParse):
            pattern = r'json\s*([\s\S]*?)\s*'
            match = re.search(pattern, textToParse)
            if match:
                return match.group(1)
            else:
                return None

    def wait(sec):
        pyautogui.sleep(sec)

    
