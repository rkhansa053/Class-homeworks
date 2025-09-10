import os
from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()


# -----------------------------------Exercise 1: Medical Consultation Assistant (Intermediate)--------------------------#

class Person(BaseModel):
    name: str
    user_level: str

personOne = Person(
    name = "Ali",
    user_level="Doctor"
    )

def get_instructions(ctx: RunContextWrapper[Person], agent: Agent):
    if ctx.context.user_level == 'Patient':
        return """
            Use simple, non-technical language. Explain medical terms in everyday words. Be empathetic and reassuring.
        """
    elif ctx.context.user_level == "Medical Student":
        return """ 
            Use moderate medical terminology with explanations. Include learning opportunities.
         """
    elif ctx.context.user_level == "Doctor":
        return """
        Use full medical terminology, abbreviations, and clinical language. Be concise and professional.
         """

medical_consultation_agent = Agent(
    name = "Medical Consultation Agent",
    instructions= get_instructions,
)

async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            medical_consultation_agent, 
            'What is hypertension?',
            run_config=config,
            context = personOne #Local context
            )
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())


# --------------------------------Exercise 2: Airline Seat Preference Agent (Intermediate-Advanced)-------------------------------------#

class Passenger(BaseModel):
    seat_preference: str
    travel_experience: str

passenger = Passenger(
    seat_preference="window",
    travel_experience="first_time"
)

def get_instructions(ctx: RunContextWrapper[Passenger], agent: Agent):
    seat = ctx.context.seat_preference.lower()
    experience = ctx.context.travel_experience.lower()

    # Window + First-time flyer
    if seat == "window" and experience == "first_time":
        return """
        Highlight the benefits of a window seat — scenic views, calming experience. 
        Reassure the traveler about flying, explain what to expect in simple, comforting language.
        """

    # Middle + Frequent flyer
    elif seat == "middle" and experience == "frequent":
        return """
        Acknowledge the compromise of the middle seat. 
        Suggest strategies for comfort (e.g., noise-cancelling headphones, early boarding). 
        Offer alternatives such as aisle or exit-row upgrades.
        """

    # Any seat + Premium traveler
    elif seat == "any" and experience == "premium":
        return """
        Highlight premium travel benefits: luxury seating, upgrade options, lounge access, 
        priority boarding, and personalized service. 
        Keep the tone professional and service-oriented.
        """

    # Default fallback
    else:
        return """
        Be a friendly airline booking assistant. Tailor responses to seat preference 
        and travel experience when possible.
        """

airline_agent = Agent(
    name="Airline Seat Preference Agent",
    instructions=get_instructions,
)

async def main():
    with trace("Dynamic Airline Instructions"):
        result = await Runner.run(
            airline_agent,
            "Which seat would you recommend for my journey?",
            context=passenger
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


#-----------------------------------Exercise 3: Travel Planning Assistant (Intermediate-Advanced------------------------------------------------#


# ------------------ Context Model ------------------ #
class Traveler(BaseModel):
    trip_type: str
    traveler_profile: str

# Example traveler
traveler = Traveler(
    trip_type="adventure",
    traveler_profile="solo"
)

# ------------------ Dynamic Instructions ------------------ #
def get_instructions(ctx: RunContextWrapper[Traveler], agent: Agent):
    trip = ctx.context.trip_type.lower()
    profile = ctx.context.traveler_profile.lower()

    if trip == "adventure" and profile == "solo":
        return """
        Suggest thrilling outdoor activities like hiking, rafting, or climbing. 
        Focus on safety tips for solo travelers. 
        Recommend social hostels and guided group tours to help them meet new people.
        """

    elif trip == "cultural" and profile == "family":
        return """
        Highlight educational and family-friendly experiences such as museums, 
        interactive exhibits, and cultural festivals. 
        Recommend accommodations with family rooms and easy access to public transport.
        """

    elif trip == "business" and profile == "executive":
        return """
        Emphasize efficiency and convenience. 
        Prioritize hotels near airports or business districts, 
        with access to business centers, high-speed WiFi, and premium lounges. 
        Keep tone professional and concise.
        """

    else:
        return """
        Be a friendly travel planning assistant. Provide recommendations tailored to 
        trip type and traveler profile when possible.
        """

travel_agent = Agent(
    name="Travel Planning Assistant",
    instructions=get_instructions,
)

async def main():
    with trace("Dynamic Travel Instructions"):
        result = await Runner.run(
            travel_agent,
            "Can you suggest destinations for my trip?",
            context=traveler
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
