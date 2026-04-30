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

class AlternativeDecision(BaseModel):
    decision: str
    rationale: str

class ReframerOutput(BaseModel):
    false_dichotomy: str = Field(description="explanation of the either/or trap the decision-maker is in")
    alternative_decisions: list[AlternativeDecision] = Field(description="list of 2-3 completely different decisions they haven't considered, each with rationale")
    reframed_question: str = Field(description="the better question they should actually be asking")
    minimum_viable_test: str = Field(description="the smallest possible action that would give them the information they need before making the full decision")
    historical_reframe_example: str = Field(description="a famous case where someone reframed a similar decision and got a breakthrough result")

def reframe_decision(decision: str, cartography: dict, devils_advocate: dict) -> dict:
    """
    Uses lateral thinking to break false dichotomies and find alternative decisions.
    
    Args:
        decision (str): The original decision.
        cartography (dict): The mapped decision landscape.
        devils_advocate (dict): The adversarial critique.
        
    Returns:
        dict: A JSON containing the false dichotomy, alternative decisions, a reframed question, and a minimum viable test.
    """
    llm = ChatGroq(model=LLM_MODEL, temperature=0.5)
    parser = JsonOutputParser(pydantic_object=ReframerOutput)
    
    prompt = PromptTemplate(
        template="""System prompt: You are a lateral thinking strategist. Most people frame decisions as binary choices when better options exist. Your job is to find the third option, the false dichotomy, the completely different question that makes the original decision irrelevant.

Decision: {decision}

Cartography:
{cartography}

Devil's Advocate Challenge:
{devils_advocate}

{format_instructions}
""",
        input_variables=["decision", "cartography", "devils_advocate"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "decision": decision,
        "cartography": json.dumps(cartography, indent=2),
        "devils_advocate": json.dumps(devils_advocate, indent=2)
    })
