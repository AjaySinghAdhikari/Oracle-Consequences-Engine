import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LLM_MODEL

load_dotenv()

class CartographerOutput(BaseModel):
    decision_restated: str = Field(description="restate the decision clearly and precisely in one sentence")
    stakeholders: list[str] = Field(description="list of all people/entities affected by this decision")
    domains: list[str] = Field(description="list of life domains this touches - financial, social, psychological, career, health, relationships, legal, reputational")
    hidden_assumptions: list[str] = Field(description="list of 3-5 assumptions the decision-maker is making that they haven't stated - things they are taking for granted")
    what_is_not_being_considered: list[str] = Field(description="list of 2-3 angles completely absent from the decision framing")
    decision_type: str = Field(description="one of: reversible_low_stakes, reversible_high_stakes, irreversible_low_stakes, irreversible_high_stakes")

def map_decision(decision: str) -> dict:
    """
    Analyzes and maps the fundamental landscape of a given decision.
    
    Args:
        decision (str): The decision to map.
        
    Returns:
        dict: A JSON mapping of stakeholders, domains, hidden assumptions, and decision type.
    """
    llm = ChatGroq(model=LLM_MODEL, temperature=0.1)
    parser = JsonOutputParser(pydantic_object=CartographerOutput)
    
    prompt = PromptTemplate(
        template="System prompt: You are a decision space analyst. Your job is to map the full landscape of a decision before any analysis begins.\n\nDecision:\n{decision}\n\n{format_instructions}\n",
        input_variables=["decision"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({"decision": decision})
