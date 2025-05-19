"""
This script demonstrates an Agno agent interacting with simple tools.
The agent uses the OpenRouter model and can increment or decrement a number by a random value between 0 and 3.
The agent is tasked to use these tools to reach a target number starting from 10.
In this example, the agent uses a session state to store the current counter value.
Read the debug output to see the tool calls and their results.
"""


from agno.agent import Agent
from agno.models.openrouter import OpenRouter
import random
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def set_counter(agent: Agent, value: str) -> str:
    """Set the counter to the given integer value."""
    try:
        n = int(value)
    except ValueError:
        return f"'{value}' is not a valid integer."
    agent.session_state["counter"] = n
    return f"Counter set to {n}"

def increment(agent: Agent) -> str:
    """Increment counter by 0–3 and return the new value."""
    delta = random.randint(0, 3)
    agent.session_state["counter"] += delta
    return f"Incremented by {delta}, counter is now {agent.session_state['counter']}"

def decrement(agent: Agent) -> str:
    """Decrement counter by 0–3 and return the new value."""
    delta = random.randint(0, 3)
    agent.session_state["counter"] -= delta
    return f"Decremented by {delta}, counter is now {agent.session_state['counter']}"

agent = Agent(
    model=OpenRouter(id="google/gemini-2.0-flash-001", api_key=OPENROUTER_API_KEY),
    session_state={"counter": 0},
    tools=[set_counter, increment, decrement],
    instructions="Current counter value: {counter}. Use increment/decrement to reach 12.",
    add_state_in_messages=True,
    show_tool_calls=True,
    debug_mode=True,
)

task = "Set the initial session state to 10. Then use the tools until you get 12."
agent.print_response(task)

print(f"Final counter: {agent.session_state['counter']}")
