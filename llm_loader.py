import os
from openai import OpenAI

class LLMLoader:
    def __init__(self,
                 api_base_url=None,
                 text_model=None,
                 code_model=None,
                 api_key=None
                ):
        self.api_base_url = api_base_url or os.getenv("LLM_API_BASE_URL", "http://llm:11434/v1")
        self.text_model = text_model or os.getenv("LLM_TEXT_MODEL", "mistral")
        self.code_model = code_model or os.getenv("LLM_CODE_MODEL", "codellama")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "ollama")
                     
        self.client = OpenAI(
            base_url = self.api_base_url,
            api_key = self.api_key
        )

    def chat(self, prompt, model=None):
        response = self.client.chat.completions.create(
            model=model or self.text_model,
            messages=[
                {
                    "role": "system",
                    "content": "Strictly follow the prompt instructions."
                               "You are generating Game Design Documents (GDD) based on established templates "
                               "To achieve the defined goals. Do not write dialogues, write only the GDD."
                               "Ever shows all 10 topics, and all subtopics."
                               "Create the GDD with maximum details possible."
                               "Dont use ** in markdown result."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    def code(self, prompt, model=None):
        response = self.client.chat.completions.create(
            model=model or self.code_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant specialized in generating games in JavaScript code."
                               "Create the game using the best practices from programming."
                               "Create comments on the code explain what the programmer can change, the goals and "
                               "how to do it."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    def artifact(self, prompt, model=None):
        response = self.client.chat.completions.create(
            model=model or self.text_model,
            messages=[
                {
                    "role": "system",
                    "content": "Strictly follow the prompt instructions."
                               "You are generating a unplugged/real game based on the Game Design Documents (GDD) "
                               "Write it with the rules and the steps needs to be followed."
                               "Define the win/end condition, number of players and aditional resources."
                               "Create the game with maximum details possible."
                               "Dont use ** in markdown result."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
