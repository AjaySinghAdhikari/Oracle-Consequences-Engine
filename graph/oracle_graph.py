import os
import sys
import time
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# Ensure we can import modules from the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.cartographer import map_decision
from agents.historian import find_historical_precedents
from agents.simulator import simulate_consequences
from agents.devils_advocate import challenge_decision
from agents.reframer import reframe_decision
from agents.synthesizer import synthesize

# Load environment variables
load_dotenv()

class OracleState(TypedDict):
    decision: str
    cartography: dict
    precedents: dict
    simulation: dict
    devils_advocate: dict
    reframe: dict
    synthesis: dict
    current_step: str
    error: str

def with_retry(func, *args, **kwargs):
    """Executes a function with up to 3 retries and a 2-second delay to handle Groq rate limits gracefully."""
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"Error calling agent '{func.__name__}', retrying in 2 seconds... ({e})")
            time.sleep(2)

def node_cartograph(state: OracleState) -> dict:
    """Executes the cartographer agent to map the decision landscape."""
    try:
        cartography = with_retry(map_decision, state["decision"])
        return {"cartography": cartography, "current_step": "cartograph"}
    except Exception as e:
        return {"error": str(e), "current_step": "cartograph"}

def node_historian(state: OracleState) -> dict:
    """Executes the historian agent to find precedents."""
    if state.get("error"): return {"error": state["error"]}
    try:
        domains = state.get("cartography", {}).get("domains", [])
        precedents = with_retry(find_historical_precedents, state["decision"], domains)
        return {"precedents": precedents, "current_step": "historian"}
    except Exception as e:
        return {"error": str(e), "current_step": "historian"}

def node_simulate(state: OracleState) -> dict:
    """Executes the simulator agent to generate consequences."""
    if state.get("error"): return {"error": state["error"]}
    try:
        simulation = with_retry(simulate_consequences, state["decision"], state["cartography"], state["precedents"])
        return {"simulation": simulation, "current_step": "simulate"}
    except Exception as e:
        return {"error": str(e), "current_step": "simulate"}

def node_challenge(state: OracleState) -> dict:
    """Executes the devil's advocate agent to challenge assumptions."""
    if state.get("error"): return {"error": state["error"]}
    try:
        devils_advocate = with_retry(challenge_decision, state["decision"], state["cartography"], state["simulation"])
        return {"devils_advocate": devils_advocate, "current_step": "challenge"}
    except Exception as e:
        return {"error": str(e), "current_step": "challenge"}

def node_reframe(state: OracleState) -> dict:
    """Executes the reframer agent to find lateral alternatives."""
    if state.get("error"): return {"error": state["error"]}
    try:
        reframe = with_retry(reframe_decision, state["decision"], state["cartography"], state["devils_advocate"])
        return {"reframe": reframe, "current_step": "reframe"}
    except Exception as e:
        return {"error": str(e), "current_step": "reframe"}

def node_synthesize(state: OracleState) -> dict:
    """Executes the synthesizer agent to generate the final oracle verdict."""
    if state.get("error"): return {"error": state["error"]}
    try:
        synthesis = with_retry(synthesize,
            state["decision"],
            state["cartography"],
            state["precedents"],
            state["simulation"],
            state["devils_advocate"],
            state["reframe"]
        )
        return {"synthesis": synthesis, "current_step": "synthesize"}
    except Exception as e:
        return {"error": str(e), "current_step": "synthesize"}

# Build StateGraph
builder = StateGraph(OracleState)

# Add Nodes
builder.add_node("cartograph", node_cartograph)
builder.add_node("historian", node_historian)
builder.add_node("simulate", node_simulate)
builder.add_node("challenge", node_challenge)
builder.add_node("reframe", node_reframe)
builder.add_node("synthesize", node_synthesize)

# Wire Edges
builder.add_edge(START, "cartograph")
builder.add_edge("cartograph", "historian")
builder.add_edge("historian", "simulate")
builder.add_edge("simulate", "challenge")
builder.add_edge("challenge", "reframe")
builder.add_edge("reframe", "synthesize")
builder.add_edge("synthesize", END)

# Compile Graph
oracle_graph = builder.compile()

def run_oracle(decision: str) -> OracleState:
    """Executes the complete Oracle LangGraph consequence engine."""
    initial_state = {
        "decision": decision,
        "cartography": {},
        "precedents": {},
        "simulation": {},
        "devils_advocate": {},
        "reframe": {},
        "synthesis": {},
        "current_step": "start",
        "error": ""
    }
    
    try:
        # StateGraph.invoke returns the final state dict
        return oracle_graph.invoke(initial_state)
    except Exception as e:
        initial_state["error"] = str(e)
        return initial_state
