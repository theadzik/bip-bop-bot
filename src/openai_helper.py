import os

import openai
from dotenv import load_dotenv
from pydantic import BaseModel

from custom_logger import get_logger

load_dotenv()

client = openai.OpenAI()
logger = get_logger(__name__)


class WordCheckerResponse(BaseModel):
    explanation: str
    correct_word: str
    used_word: str
    is_correct: bool


class BullyingDetectorResponse(BaseModel):
    is_bullying: bool
    response: str


class BadBotResponse(BaseModel):
    response: str


class OpenAIChecker:
    def __init__(self):
        with open(
            os.getenv("REDDIT_CHECKER_PROMPT_PATH"), mode="r", encoding="utf-8"
        ) as file:
            self.checker_prompt = file.read().strip()
            logger.debug(f"Loaded checker prompt:\n{self.checker_prompt}")

        with open(
            os.getenv("REDDIT_BULLY_PROMPT_PATH"), mode="r", encoding="utf-8"
        ) as file:
            self.bully_prompt = file.read().strip()
            logger.debug(f"Loaded bully prompt:\n{self.bully_prompt}")

        with open(
            os.getenv("REDDIT_BAD_BOT_PROMPT_PATH"), mode="r", encoding="utf-8"
        ) as file:
            self.bad_bot_prompt = file.read().strip()
            logger.debug(f"Loaded bad bot prompt:\n{self.bad_bot_prompt}")

        self.reasoning_effort = self.get_reasoning_effort()
        self.model_version = self.get_model_version()

    def send_request(self, prompt: list, response_format: type[BaseModel]):
        response = client.responses.parse(
            model=self.model_version,
            text_format=response_format,
            input=prompt,
            reasoning=self.reasoning_effort,
        )
        content = response.output_parsed
        logger.debug(content)
        return content

    @staticmethod
    def get_reasoning_effort():
        effort = os.getenv("OPENAI_EFFORT", None)
        if not effort:
            return None

        if effort in ["low", "medium", "high"]:
            return {"effort": effort}
        else:
            raise ValueError("OPENAI_EFFORT must be low, medium or high")

    @staticmethod
    def get_model_version():
        return os.getenv("OPENAI_MODEL", "o4-mini-2025-04-16")

    def get_bullying_response(self, body: str) -> BullyingDetectorResponse:
        logger.debug(f"I got this body:\n{body}")

        prompt = [
            {"role": "system", "content": self.bully_prompt},
            {"role": "user", "content": body},
        ]

        return self.send_request(
            prompt=prompt, response_format=BullyingDetectorResponse
        )

    def get_bad_bot_response(self, body: str) -> BadBotResponse:
        logger.debug(f"I got this body:\n{body}")

        prompt = [
            {"role": "system", "content": self.bad_bot_prompt},
            {"role": "user", "content": body},
        ]

        return self.send_request(prompt=prompt, response_format=BadBotResponse)

    def get_explanation(
        self, word: str, body: str, extra_info: str = ""
    ) -> WordCheckerResponse:
        logger.debug(f"I got this body:\n{body}")
        prompt = [
            {"role": "system", "content": self.checker_prompt},
            {"role": "system", "content": f"<zasady>{extra_info}</zasady>"},
            {"role": "system", "content": f"<wyrażenie>{word}</wyrażenie>"},
            {"role": "user", "content": body},
        ]

        return self.send_request(prompt=prompt, response_format=WordCheckerResponse)


if __name__ == "__main__":
    import json

    with open(os.getenv("REDDIT_DICTIONARY_PATH")) as file:
        dictionary = json.load(file)
    checker = OpenAIChecker()
    word = "dobrzy"
    rules = " ".join(dictionary[word]["explanations"])
    body = "Polscy programiści są dobzi. Lepsi nawet niż OpenAI."
    explanation = checker.get_explanation(word=word, extra_info=rules, body=body)
    print(explanation)
