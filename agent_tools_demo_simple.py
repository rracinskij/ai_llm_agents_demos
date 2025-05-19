"""
This script demonstrates an Agno agent interacting with simple tools.
The agent uses the OpenRouter model and can increment or decrement a number by a random value between 0 and 3.
The agent is tasked to use these tools to reach a target number starting from 10.
Read the debug output to see the tool calls and their results.
"""

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
import random

import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def increment(n: int) -> int:
    try:
        return n + random.randint(0, 3)
    except Exception:
        raise ValueError(f"Input must be an integer, got {n}.")

def decrement(n: int) -> int:
    try:
        return n - random.randint(0, 3)
    except Exception:
        raise ValueError(f"Input must be an integer, got {n}.")

agent = Agent(tools=[increment, decrement],
              model = OpenRouter(id="google/gemini-2.0-flash-001", api_key=OPENROUTER_API_KEY),
              show_tool_calls=True,
              debug_mode=True,
              reasoning=False)

task = "You've got an initial number, that is 10. The increment and decrement tools increment and decrement the input by a random number between 0 and 3 respectively. Use the tools until you get 12."
agent.print_response(task)
