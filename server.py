import os
import sys
import json
import asyncio
import threading
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Ensure we can import from graph
sys.path.append(os.path.dirname(__file__))
from graph.oracle_graph import oracle_graph, run_oracle
from config import LLM_MODEL

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    print("✅ Environment loaded")
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    missing = []
    if not groq_key or groq_key == "your_key_here":
        missing.append("GROQ_API_KEY")
    if not tavily_key or tavily_key == "your_key_here":
        missing.append("TAVILY_API_KEY")
        
    if missing:
        print(f"❌ CRITICAL ERROR: Missing required API keys in .env: {', '.join(missing)}")
        print("Please configure them before making API requests.")
    else:
        print("✅ Environment variables loaded successfully.")
        
        # Test Groq Connection
        print("Running Groq API health check...")
        try:
            llm = ChatGroq(model=LLM_MODEL, max_retries=1)
            llm.invoke([HumanMessage(content="Hello, testing connection.")])
            print("✅ SUCCESS: Connected to Groq API.")
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Failed to connect to Groq API. Please verify your GROQ_API_KEY. Details: {e}")
    yield
    # shutdown

app = FastAPI(title="Oracle Consequences Engine", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main frontend UI."""
    with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/analyze")
async def analyze(decision: str):
    """SSE endpoint that streams agent execution results in real-time."""
    async def generate():
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
        
        final_synthesis = {}
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue = asyncio.Queue()
        stop_event = threading.Event()

        def stream_in_executor():
            try:
                for event in oracle_graph.stream(initial_state):
                    if stop_event.is_set():
                        break
                    loop.call_soon_threadsafe(queue.put_nowait, ("event", event))
                loop.call_soon_threadsafe(queue.put_nowait, ("done", None))
            except Exception as e:
                loop.call_soon_threadsafe(queue.put_nowait, ("error", e))
        
        try:
            stream_future = loop.run_in_executor(None, stream_in_executor)
            while True:
                kind, payload = await queue.get()
                if kind == "event":
                    for node_name, state_update in payload.items():
                        # Handle any captured errors from the graph execution
                        if "error" in state_update and state_update["error"]:
                            yield f'data: {json.dumps({"step": node_name, "status": "error", "error": state_update["error"]})}\n\n'
                            stop_event.set()
                            return
                        
                        # Map the node name to the actual data key in the state dict
                        key_map = {
                            "cartograph": "cartography",
                            "historian": "precedents",
                            "simulate": "simulation",
                            "challenge": "devils_advocate",
                            "reframe": "reframe",
                            "synthesize": "synthesis",
                        }
                        data_key = key_map.get(node_name, node_name)
                        
                        step_result = state_update.get(data_key, {})
                        
                        # Store the final synthesis to yield at the very end
                        if node_name == "synthesize":
                            final_synthesis = step_result
                            
                        yield f'data: {json.dumps({"step": node_name, "status": "complete", "data": step_result})}\n\n'
                        # Small non-blocking sleep to ensure smooth buffering
                        await asyncio.sleep(0.01)
                elif kind == "error":
                    yield f'data: {json.dumps({"step": "system", "status": "error", "error": str(payload)})}\n\n'
                    stop_event.set()
                    return
                elif kind == "done":
                    # Final completion event
                    yield f'data: {json.dumps({"step": "complete", "status": "complete", "data": final_synthesis})}\n\n'
                    break
            await stream_future
        except asyncio.CancelledError:
            stop_event.set()
            raise
        except Exception as e:
            yield f'data: {json.dumps({"step": "system", "status": "error", "error": str(e)})}\n\n'

    # Stream the generator as SSE
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
