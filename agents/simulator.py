import os
import sys
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LLM_MODEL, TIME_HORIZONS

load_dotenv()

class Consequence(BaseModel):
    description: str
    type: str = Field(description="positive/negative/uncertain")
    probability: float = Field(description="0.0-1.0")
    severity: int = Field(description="1-10")
    causes: list[str] = Field(description="list of what directly causes this")
    leads_to: list[str] = Field(description="list of what this consequence itself causes in the next time horizon")
    domain: str = Field(description="which life domain")

class SimulatorOutput(BaseModel):
    consequences: dict[str, list[Consequence]] = Field(description="dict with time horizon as key, each value is a list of consequence objects")
    cascade_chains: list[str] = Field(description="list of the 3 most important causal chains as strings like 'A -> B -> C -> D'")
    highest_risk: str = Field(description="the single most dangerous consequence with explanation")
    highest_upside: str = Field(description="the single best possible outcome with explanation")

def simulate_consequences(decision: str, cartography: dict, precedents: dict) -> dict:
    """
    Simulates second-order consequences over multiple time horizons.
    
    Args:
        decision (str): The decision to simulate.
        cartography (dict): The mapped decision landscape.
        precedents (dict): The historical precedents and base rates.
        
    Returns:
        dict: A JSON containing time-horizon consequence lists, causal chains, and highest risk/upside.
    """
    llm = ChatGroq(model=LLM_MODEL, temperature=0.3)
    parser = JsonOutputParser(pydantic_object=SimulatorOutput)
    
    prompt = PromptTemplate(
        template="""System prompt: You are a consequence simulator trained in systems thinking, chaos theory, and strategic forecasting. 
For each consequence you identify, you must also identify what that consequence itself causes — building a causal chain.

Decision: {decision}

Cartography:
{cartography}

Historical Precedents:
{precedents}

Time Horizons to consider: {time_horizons}

{format_instructions}
""",
        input_variables=["decision", "cartography", "precedents", "time_horizons"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "decision": decision,
        "cartography": json.dumps(cartography, indent=2),
        "precedents": json.dumps(precedents, indent=2),
        "time_horizons": ", ".join(TIME_HORIZONS)
    })
