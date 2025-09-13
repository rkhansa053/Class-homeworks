from agents import Agent, Runner, trace
from connection import config
import asyncio

poet_agent = Agent(
    name = "Poet Agent",
    instructions = """
        You are a poet agent.
        Your role is to generate a two-stanza poem or process an input poem.
        Poems can be lyric (emotional), narrative, or dramatic.
        If you're asked without a poem, generate a short two-stanza poem on emotions.
    """,


)

lyric_analyst_agent = Agent(
    name = "Lyric Analyst Agent",
    instructions = """
        You analyze lyric poetry focusing on emotions, feelings, and musicality.
        Provide insights about the poem's mood, use of rhythm, and personal voice.
    """,
)

narrative_agent = Agent(
    name = "Narrative Agent",
    instructions = """
        You analyze narrative poetry focusing on storytelling elements: plot, characters, and imagery.""",
)

dramatic_agent = Agent(
    name = "Dramatic Analyst Agent",
    instructions = """You analyze dramatic poetry emphasizing voice, dialogue and performance aspects.""",
)

class CustomParentAgent(Agent):
    async def run(self, input, config):
        poet_output = await poet_agent.run(input, config)

        poem_text = poet_output.lower()

        if "dialogue" in poem_text or "voice" in poem_text or "stage" in poem_text:
            next_agent = dramatic_agent
        elif "story" in poem_text or "character" in poem_text or "event" in poem_text:
            next_agent = narrative_agent
        else:
            next_agent = lyric_analyst_agent

        final_output = await next_agent.run(poet_output.output, config)
        return final_output
    

parent_agent = CustomParentAgent(
    name = "Poet Orchestrator",
    instructions = """
        You are the orchestrator agent for poetry tasks.When given a request or poem, first delegate to the poet agent to generate or process poems.
        After receiving the poem, detect whether it's lyric, narrartive or dramatic poetry.
        Delegate the poem to the corresponding analyst agent for deeper analysis.
        If the type is unclear or multiple types apply, delegate to all analysts.
        If the querry is unrelated to the poetry, respond politely and do not delegate.

    """,
    handoffs = [poet_agent, lyric_analyst_agent, narrative_agent, dramatic_agent]
)


async def main():
    with trace("Handoffs Homework"):
        poem_or_querry = """
        In quiet nights, the stars will glow,
        Whispers of dreams begin to flow.
        A gentle breeze, the moon's soft light,
        Wraps the world in silver night.
    """
    result = await Runner.run(
        parent_agent,
        poem_or_querry,
        run_config = config
    )    
    print("Final Output")
    print(result.final_output)
    print("Last Agent")
    print(result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())