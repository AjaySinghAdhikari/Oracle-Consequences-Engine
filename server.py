from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from dotenv import load_dotenv
import json, os

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    print("Environment loaded")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/api/analyze")
async def analyze(decision: str):
    from graph.oracle_graph import run_oracle
    async def generate():
        try:
            state = {"decision": decision}
            steps = ["cartograph", "historian", "simulate", "challenge", "reframe", "synthesize"]
            for step in steps:
                yield f"data: {json.dumps({'step': step, 'status': 'running'})}\n\n"
            
            # Note: The user provided code iterates twice. 
            # I will follow the user's provided structure.
            final = run_oracle(decision)
            
            for step in steps:
                # The user's code had a logical bug in the snippet (re-iterating steps after run_oracle)
                # but I will implement it as requested, assuming final contains keys corresponding to steps.
                yield f"data: {json.dumps({'step': step, 'status': 'complete', 'data': final})}\n\n"
            
            yield f"data: {json.dumps({'step': 'complete', 'status': 'complete', 'data': final})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'step': 'error', 'status': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
