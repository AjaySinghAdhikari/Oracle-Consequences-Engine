import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LLM_MODEL
from tools.web_tool import search_web
from tools.arxiv_tool import search_arxiv

load_dotenv()

class PrecedentCase(BaseModel):
    case_description: str
    what_was_decided: str
    what_actually_happened: str
    key_lesson: str
    source_url: str

class HistorianOutput(BaseModel):
    precedents: list[PrecedentCase] = Field(description="list of case dicts (3-4 historical cases)")
    base_rate_insight: str = Field(description="one paragraph about what typically happens in decisions like this")
    surprising_finding: str = Field(description="the most counterintuitive thing found")

def find_historical_precedents(decision: str, domains: list) -> dict:
    """
    Searches for historical precedents and base rate insights using Web and ArXiv tools.
    
    Args:
        decision (str): The decision being evaluated.
        domains (list): A list of relevant life/business domains affected.
        
    Returns:
        dict: A JSON containing 3-4 historical precedents, base rate insight, and surprising findings.
    """
    # Gather information using our tools
    personal_query = f"similar personal decisions outcomes '{decision}'"
    business_query = f"similar business decisions outcomes case studies '{decision}'"
    academic_query = f"research on decision making outcomes '{decision}'"
    
    web_results = []
    web_results.extend(search_web(personal_query, max_results=2))
    web_results.extend(search_web(business_query, max_results=2))
    web_results.extend(search_web(academic_query, max_results=2))
    
    arxiv_results = search_arxiv(academic_query, max_results=2)
    
    # Format context for the LLM
    context = "Web Results:\n"
    for r in web_results:
        context += f"- Title: {r['title']}\n  URL: {r['url']}\n  Content: {r['content']}\n\n"
    
    context += "ArXiv Results:\n"
    for r in arxiv_results:
        context += f"- Title: {r['title']}\n  URL: {r['url']}\n  Summary: {r['summary']}\n\n"

    llm = ChatGroq(model=LLM_MODEL, temperature=0.2)
    parser = JsonOutputParser(pydantic_object=HistorianOutput)
    
    prompt = PromptTemplate(
        template="""System prompt: You are a historical decision analyst. Given a decision, its domains, and some search context, extract 3-4 historical precedents, provide base rate insights, and find surprising findings.

Decision: {decision}
Domains: {domains}

Search Context:
{context}

{format_instructions}
""",
        input_variables=["decision", "domains", "context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({
        "decision": decision, 
        "domains": ", ".join(domains) if domains else "",
        "context": context
    })
