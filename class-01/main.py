from dotenv import load_dotenv
import os
from agents import Agent, Runner,  AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import asyncio


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

async def main():
    agent = Agent(
    name = "Translator Agent",
    instructions = "You are a translator agent. You translate English sentences, words into simple Urdu as per the user demands."
)

    response = await  Runner.run(
        agent,
        input = 'My name is Syeda Khansa Rahman. I am 18 years old.',
        run_config = config
        )
    print(response)

if __name__ == '__main__':
    asyncio.run(main())

    