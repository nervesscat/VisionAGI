from openai import OpenAI
from action import Utils

class OpenAIConn:
    __system_message = ""
    __GPT4_NAME_MODEL = "gpt-4-1106-preview"
    __GPT3_NAME_MODEL = "gpt-3.5-turbo-1106"
    __GPTV_NAME_MODEL = "gpt-4-vision-preview"

    def __init__(self, system_message):
        self.client = OpenAI()
        self.util = Utils()
        self.__system_message = system_message

    def _create_text_completion(self, super_task, gpt4=False):
        if gpt4:
            model = self.__GPT4_NAME_MODEL
        else:
            model = self.__GPT3_NAME_MODEL

        response = self.client.chat.completions.create(
            model = model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.__system_message},
                {"role": "user", "content": super_task},
            ]) 

        return self.util.parse_json(response.choices[0].message.content)

    def _create_visual_completion(self, super_task, base64_image):
        response = self.client.chat.completions.create(
            model=self.__GPTV_NAME_MODEL,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text" : self.__system_message + "\n" + str(super_task)},
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

        return self.util.parse_and_clean(response.choices[0].message.content)

    def set_system_message(self, system_message):
        self.__system_message = system_message