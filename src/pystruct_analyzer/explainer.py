from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SourceCodeExplainer:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4o-mini"
        self.messages = [
            {"role": "system", "content": "あなたは優秀なコードエキスパートです。"},
            {"role": "user", "content": "次のコードを50文字以内で説明してください。"},
        ]
        self.max_tokens = 64

    def explain(self, source_code: str):
        self.messages.append({"role": "user", "content": f"{source_code}\nこの関数は"})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
