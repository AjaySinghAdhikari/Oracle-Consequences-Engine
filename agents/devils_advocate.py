import os
import sys
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LLM_MODEL

load_dotenv()

class Assumption(BaseModel):
    assumption: str = Field(description="what they believe")
    reality: str = Field(description="what evidence suggests")
    danger_level: int = Field(description="1-10")

class DevilsAdvocateOutput(BaseModel):
    false_assumptions: list[Assumption] = Field(description="list of dicts with assumption, reality, and danger_level")
    emotional_biases: list[str] = Field(description="list of cognitive biases likely affecting this decision with explanation of how")
    worst_case_scenario: str = Field(description="detailed description of how this goes catastrophically wrong, with probability")
    what_they_are_avoiding: str = Field(description="the uncomfortable truth the decision-maker is probably not wanting to face")
    critical_questions: list[str] = Field(description="list of 3 questions that if honestly answered would change the decision")

def challenge_decision(decision: str, cartography: dict, simulation: dict) -> dict:
    """
    Provides an adversarial critique of the decision framing and assumptions.
    
    Args:
        decision (str): The decision being evaluated.
        cartography (dict): The mapped decision landscape.
        simulation (dict): The simulated consequences.
        
    Returns:
        dict: A JSON containing false assumptions, emotional biases, worst-case scenarios, and critical questions.
    """
    llm = ChatGroq(model=LLM_MODEL, temperature=0.4)
    parser = JsonOutputParser(pydantic_object=DevilsAdvocateOutput)
    
    prompt = PromptTemplate(
        template="""System prompt: You are an adversarial analyst. Your job is to find everything wrong with how this decision is being framed. You are NOT trying to be balanced. You are specifically looking for what the decision-maker is missing, avoiding, or getting wrong. Be direct and uncomfortable.

Decision: {decision}

Cartography:
{cartography}

Simulation:
{simulation}

{format_instructions}
""",
        input_variables=["decision", "cartography", "simulation"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "decision": decision,
        "cartography": json.dumps(cartography, indent=2),
        "simulation": json.dumps(simulation, indent=2)
    })
