# ORACLE — Second-Order Consequences Engine



![Demo Placeholder](demo.gif)

First-order thinking is fast, easy, and focuses on the immediate, visible effects of a decision. Second-order thinking is deliberate and looks at the consequences of those consequences. In complex systems, the first-order consequence is often a false signal—what feels good in the short term may create disastrous long-term effects. ORACLE forces you to step outside the immediate moment, mapping out the cascading effects of your choices across time, domains, and hidden assumptions so you can navigate uncertainty with clarity.

## The 6-Agent Pipeline

```text
[ DECISION ] 
       │
       ▼
[ CARTOGRAPHER ] ─────► Maps the decision landscape (Domains, Stakeholders)
       │
       ▼
[ HISTORIAN ] ────────► Extracts precedents from History & ArXiv
       │
       ▼
[ SIMULATOR ] ────────► Projects consequences across 4 time horizons
       │
       ▼
[ DEVIL'S ADVOCATE ] ─► Audits for blind spots, biases, and systemic risks
       │
       ▼
[ REFRAMER ] ─────────► Generates lateral alternatives and paradigm shifts
       │
       ▼
[ SYNTHESIZER ] ──────► Compiles the final oracle verdict and D3 tree
```

## Features

- **6 Specialized Agents**: A LangGraph orchestrated pipeline of specialized intelligences working sequentially.
- **Consequence Mapping**: Projections across 4 distinct time horizons (0-3 months, 3-12 months, 1-3 years, 3-10 years).
- **Historical Precedents**: Contextual grounding via ArXiv research and web intelligence.
- **Adversarial Blind Spot Detection**: A dedicated "Devil's Advocate" agent designed to stress-test your assumptions.
- **Accordion UI**: Clean, immersive intelligence briefing interface that shows the Synthesis Verdict first, allowing deep dives into individual agent findings.
- **D3 Consequence Tree**: Interactive visual representation of cascading effects.

## Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge&logo=groq&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-000000?style=for-the-badge&logo=chroma&logoColor=white)
![D3.js](https://img.shields.io/badge/d3%20js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white)

## Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**: Create a `.env` file in the root directory and add:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
4. **Launch ORACLE**:
   ```bash
   python server.py
   ```
5. **Access the Interface**: Open your browser and navigate to `http://localhost:8000`.

## Project Structure

```text
oracle-consequences-engine/
├── agents/           # Specialized LangGraph LLM nodes
├── frontend/         # HTML interface
├── graph/            # Workflow orchestration (oracle_graph.py)
├── memory/           # Memory storage
├── static/           # CSS, JS, and D3 visualizers
├── tools/            # Research and utility tools
├── config.py         # Global parameters
├── server.py         # FastAPI backend with SSE streaming
└── requirements.txt  # Python dependencies
```

## The Science Behind ORACLE

**Second-Order Thinking**  
Coined by Howard Marks and championed by decision theorists, second-order thinking recognizes that interventions in complex systems always have unintended consequences. ORACLE automates the cognitive friction required to look past the immediate reward.

**Systems Theory**  
A decision in one domain (e.g., career) inevitably perturbs adjacent domains (e.g., relationships, health). ORACLE’s Cartographer maps these interconnected nodes so the Simulator can accurately predict cascading ripple effects.

**Red Teaming**  
Humans are wired for confirmation bias—we seek evidence that supports our desired outcome. The Devil's Advocate agent serves as an automated "Red Team," structurally incentivized to destroy your assumptions and identify existential blind spots before they occur in reality.

## Example Queries

1. **"Drop out of college to start an AI startup."**
   - **First order**: Freedom, excitement, potential wealth.
   - **Second order (ORACLE)**: High probability of burnout, loss of credential safety net, strain on social networks outside the tech bubble.

2. **"Move my engineering team to a fully remote, asynchronous workflow."**
   - **First order**: Reduced overhead, happy employees, broader hiring pool.
   - **Second order (ORACLE)**: Degradation of tacit knowledge transfer, increased isolation, communication bottlenecks hiding behind text, potential divergence of company culture.

3. **"Introduce a strict performance ranking system in my company."**
   - **First order**: Clear metrics, weed out low performers.
   - **Second order (ORACLE)**: Hyper-competition, destruction of team cohesion, gaming the metrics, exodus of top talent who dislike toxic environments.
