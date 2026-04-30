# 👁️ ORACLE

> **Every decision has a shadow. ORACLE shows you what is hiding in it.**

![ORACLE UI Demo](docs/demo.gif)

## 🔮 The Philosophy: Second-Order Thinking
Most people stop at the immediate consequences of their actions. *If I quit my job, I lose my salary.* But what happens because you lost your salary? What happens because you have free time? Second-order thinking is the practice of looking past the immediate effects to the subsequent, often hidden, structural impacts of a decision. It matters because while first-order consequences are obvious and usually intended, second and third-order consequences are where the true, catastrophic risks and asymmetric opportunities lie.

## ⚙️ The Pipeline
ORACLE is powered by a coordinated swarm of 6 specialized LangGraph AI agents working in sequence:

```text
[START]
   │
   ▼
 🗺️ CARTOGRAPHER  ── Maps stakeholders, domains, and unstated assumptions
   │
   ▼
 📜 HISTORIAN     ── Pulls academic papers (ArXiv) & web base rates for precedents
   │
   ▼
 🌀 SIMULATOR     ── Runs the chaotic consequence tree across 4 time horizons
   │
   ▼
 ⚖️ ADVOCATE      ── Attacks the framing, exposes biases & worst-case scenarios
   │
   ▼
 💡 REFRAMER      ── Breaks the false dichotomy & finds the hidden 3rd option
   │
   ▼
 👁️ SYNTHESIZER   ── Aggregates into the final D3 Consequence Tree & Verdict
   │
[END]
```

## ✨ Features
- **Real-Time Pipeline Visualization**: Watch the agents hand off state via Server-Sent Events (SSE).
- **Interactive D3.js Causality Trees**: Explore consequence nodes sized by probability and severity.
- **Academic Grounding**: Automatically searches ArXiv for historical and psychological precedents.
- **Adversarial Critique**: Doesn't just validate your decision—it actively tries to find your blind spots.
- **Lateral Reframing**: Escapes binary thinking by proposing "minimum viable tests."
- **Beautiful Dark Aesthetic**: A single-file HTML/CSS/JS frontend without massive framework bloat.

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-f59e0b?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-4285F4?style=for-the-badge)
![D3.js](https://img.shields.io/badge/d3%20js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white)

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/oracle-consequences-engine.git
   cd oracle-consequences-engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Rename `.env.example` to `.env` or create a new `.env` file and add your keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

4. **Run the Oracle:**
   ```bash
   python server.py
   ```
   *Navigate to `http://localhost:8000` to consult the Oracle.*

## 📂 Project Structure
```
oracle-consequences-engine/
├── agents/
│   ├── cartographer.py     # Decision landscape mapping
│   ├── historian.py        # ArXiv/Web base rate analysis
│   ├── simulator.py        # Generates time-horizon consequences
│   ├── devils_advocate.py  # Adversarial framing attack
│   ├── reframer.py         # Lateral alternative generation
│   └── synthesizer.py      # Final aggregation & D3 structuring
├── graph/
│   └── oracle_graph.py     # LangGraph StateGraph orchestration
├── memory/
│   └── vector_store.py     # ChromaDB historical decision memory
├── tools/
│   ├── arxiv_tool.py       # ArXiv search wrapper
│   └── web_tool.py         # Tavily search wrapper
├── frontend/
│   └── index.html          # Stunning SSE streaming UI
├── config.py               # Central configuration variables
├── server.py               # FastAPI SSE streaming backend
└── requirements.txt
```

## 🧠 Example Queries

**1. "Drop out of college to start an AI startup"**
- *The Blindspot*: Failing to realize that college is a social network, not just education.
- *The Reframed Question*: "How can I build the startup while using university resources as my sandbox?"

**2. "Confront my co-founder about their lack of output"**
- *The Consequence Tree*: Confrontation → Defensiveness → Passive Aggression → Company Death (High Risk).
- *The Reframe*: "What structural incentive is currently making them avoid the work?"

**3. "Pivot the product to B2B Enterprise"**
- *The Base Rate Insight*: Enterprise sales cycles (9-12 months) routinely kill startups with less than 18 months of runway.
- *The Minimum Viable Test*: Sell an enterprise contract manually via cold-outreach before writing a single line of B2B code.

## 🔬 The Science Behind ORACLE

ORACLE is built on three core pillars of strategic foresight:

1. **Second-Order Thinking (Howard Marks):** The ability to model $N+1$ consequences. ORACLE enforces this by requiring the Simulator agent to explicitly link every consequence to a subsequent resulting consequence in the next time horizon (`leads_to`).
2. **Systems Theory:** Recognizing that interventions in complex systems (like careers, relationships, or markets) cause ripple effects across domains. The Cartographer forces the mapping of these domains before any analysis begins.
3. **Red Teaming & De-biasing:** Humans are structurally blind to their own motivated reasoning. The Devil's Advocate agent is prompted to be explicitly hostile, bypassing the typical sycophancy of LLMs to find the catastrophic risks the user is intentionally ignoring.
