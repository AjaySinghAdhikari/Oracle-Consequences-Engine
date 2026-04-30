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

class SynthesizerOutput(BaseModel):
    executive_summary: str = Field(description="2-3 sentences summarizing the overall picture")
    recommendation: str = Field(description="clear recommended course of action with reasoning")
    confidence_level: str = Field(description="percentage confidence in the recommendation with explanation")
    top_risks: list[str] = Field(description="list of top 3 risks ranked by likelihood times severity")
    top_opportunities: list[str] = Field(description="list of top 3 upsides")
    the_one_question: str = Field(description="the single most important question to answer before deciding")
    decision_tree: dict = Field(description="nested dict representing the consequence tree for D3.js visualization with structure: {name, type, probability, children: [{name, type, probability, children: [...]}]}")
    timeline_summary: dict[str, str] = Field(description="dict with each time horizon as key and 2-sentence summary as value")

def synthesize(decision: str, cartography: dict, precedents: dict, simulation: dict, devils_advocate: dict, reframer: dict) -> dict:
    """
    Aggregates all agent outputs into a final cohesive oracle verdict.
    
    Args:
        decision (str): The original decision.
        cartography (dict): The mapped decision landscape.
        precedents (dict): The historical precedents.
        simulation (dict): The simulated consequences.
        devils_advocate (dict): The adversarial critique.
        reframer (dict): The lateral reframing of the decision.
        
    Returns:
        dict: A JSON containing the executive summary, recommendation, confidence level, top risks/opportunities, and a D3 visualizable consequence tree.
    """
    llm = ChatGroq(model=LLM_MODEL, temperature=0.2)
    parser = JsonOutputParser(pydantic_object=SynthesizerOutput)
    
    prompt = PromptTemplate(
        template="""System prompt: You are the Oracle Synthesizer. Takes all agent outputs and produces the final structured result.

Decision: {decision}

Cartography:
{cartography}

Precedents:
{precedents}

Simulation:
{simulation}

Devil's Advocate:
{devils_advocate}

Reframer:
{reframer}

{format_instructions}
""",
        input_variables=["decision", "cartography", "precedents", "simulation", "devils_advocate", "reframer"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "decision": decision,
        "cartography": json.dumps(cartography, indent=2),
        "precedents": json.dumps(precedents, indent=2),
        "simulation": json.dumps(simulation, indent=2),
        "devils_advocate": json.dumps(devils_advocate, indent=2),
        "reframer": json.dumps(reframer, indent=2) if isinstance(reframer, dict) else str(reframer)
    })
