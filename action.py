import pyautogui
import os
import json
import re
import base64

class Actioner:
    def move_using_axis(self, x, y):
        pyautogui.moveTo(x, y)
    
    def click_position(self):
        pyautogui.click()

    def press_keys(self, key):
        if type(key) == list:
            key = [k.lower() for k in key]
            if len(key) == 2:
                pyautogui.hotkey(key[0], key[1])
            elif len(key) == 3:
                pyautogui.hotkey(key[0], key[1], key[2])
        else:
            pyautogui.press(key.lower())
        self.wait(2)

    def execute(self, command):
        os.system(command)
        self.wait(2)

    def type_text(self, text):
        pyautogui.write(text)
        self.wait(2)

    def take_screenshot(self, filename):
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

    def wait(self, sec):
        pyautogui.sleep(sec)

class Utils:
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def parse_json(self, textToParse):
        return json.loads(textToParse)

    def parse_and_clean(self, textToParse):
        pattern = r'```json\s*([\s\S]*?)\s*```'
        match = re.search(pattern, textToParse)
        if match:
            lines = match.group(0).splitlines()
            cleaned_lines = lines[1:-1]
            cleaned_text = '\n'.join(cleaned_lines)
            return self.parse_json(cleaned_text)
        else:
            raise Exception("No JSON found")
            return None
