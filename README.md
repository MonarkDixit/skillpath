# SkillPath: Career Skill Dependency Mapper

**Course:** MSML606 - Data Structures and Algorithms, Spring 2026
**Author:** Monark Dixit (UID: 122259645)
**Submission:** Extra Credit Project 2 - Individual

---

## The Problem I Wanted to Solve

Every time I look at a job posting, it lists 10 to 15 required skills in no particular order. Python. SQL. Machine Learning. Statistics. Communication. They are all there in a flat list, as if they are equally accessible to someone starting from scratch. But they are not. You cannot meaningfully learn Machine Learning before you understand Statistics. You cannot use Python for data work before you understand what data analysis actually involves. There is a hidden order to all of it, and job postings never tell you what it is.

SkillPath is my attempt to surface that hidden order. You tell it what job you want and what you already know, and it gives you a numbered list of skills to learn, in the right sequence, with the most important ones prioritized based on how often they appear in real job listings.

---

## How It Works

The core insight is that skills form a Directed Acyclic Graph. Some skills are prerequisites for others. If you model that structure correctly, two graph algorithms do the rest of the work.

**Step 1: BFS Shortest Path**
Starting from the skills the user already has, BFS propagates forward through the dependency graph. Each layer represents one step away from what the user already knows. The first time BFS reaches a required skill for the target role, that is the shortest path to it. This tells us which skills the user needs and how far they are from each one.

**Step 2: Topological Sort (Kahn's Algorithm)**
Once we know which skills are missing, topological sort orders them. Kahn's algorithm works by processing nodes with no remaining prerequisites first, then unlocking their dependents one at a time. The result is a linear ordering where every prerequisite appears before the skill that depends on it. This is the roadmap.

Both algorithms are implemented entirely from scratch. No external graph libraries.

---

## Project Structure

```
skillpath/
├── src/
│   ├── __init__.py
│   ├── graph.py          # Directed graph with adjacency list, from scratch
│   ├── topo_sort.py      # Kahn's topological sort, from scratch
│   ├── bfs_path.py       # BFS shortest path on DAG, from scratch
│   ├── cycle_detect.py   # DFS cycle detection with three-color marking
│   ├── data_loader.py    # Loads role-skill mappings
│   └── engine.py         # Core pipeline that connects everything
├── data/
│   ├── skill_edges.py    # Manually defined prerequisite relationships
│   └── role_skills.py    # Clean role to skill frequency mappings
├── tests/
│   └── test_graph.py
├── app.py                # Streamlit frontend
├── requirements.txt
├── AI_USAGE_DISCLOSURE.md
└── README.md
```

---

## Setup and Installation

**Requirements:** Python 3.11+

**Step 1: Clone the repo**
```bash
git clone https://github.com/MonarkDixit/skillpath.git
cd skillpath
```

**Step 2: Create and activate a virtual environment**
```bash
# Windows
python -m venv venv --without-pip
venv\Scripts\activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Using SkillPath

The app has two screens.

On the home screen, pick a job role from the dropdown or use one of the four quick-select buttons. Then select any skills you already have from the checklist. Click "Show Me My Roadmap."

The results screen shows three things. Your skill coverage percentage tells you how much of the role you already meet. Your learning roadmap is the numbered list of skills to acquire, in the correct order. The in-demand skills panel shows which skills appear most frequently across real job listings for that role, so you know which ones to prioritize.

There is a back button to return to the home screen and try a different role.

---

## Validating the Algorithms

Each module has its own validation script you can run independently:

```bash
# Validate graph construction
python src/graph.py

# Validate cycle detection
python src/cycle_detect.py

# Validate topological sort and verify ordering
python src/topo_sort.py

# Validate BFS shortest path
python src/bfs_path.py

# Run the full engine pipeline
python src/engine.py
```

---

## The Hardest Part

The individual algorithms were not too difficult to implement once I understood the theory. The hard part was connecting all of them into a single working pipeline where the output of one feeds correctly into the next.

Cycle detection has to run before topological sort, otherwise Kahn's algorithm loops forever. BFS has to run on the full graph before the subgraph is extracted, otherwise you miss transitive prerequisites. The subgraph has to be built correctly before topological sort runs on it, otherwise the ordering is wrong. Getting all of those dependencies between the modules right, and making sure they all used consistent node naming, took more time than any individual piece.

There was also a real data quality problem partway through. The LinkedIn job postings dataset tagged roles with broad industry categories like "health care provider" and "other" rather than actual skills. A data analyst role would list "health care provider" as a required skill simply because the company posting the job was in the healthcare industry. That made the roadmaps nonsensical. The fix was to replace the noisy dataset-derived skill labels with a clean, manually curated skill mapping that I defined myself in `data/role_skills.py`.

---

## Dependencies

```
streamlit
pandas
numpy
networkx
pyvis
```

All graph algorithm code is written from scratch. No graph libraries are used for the core BFS, topological sort, or cycle detection logic.

---

## AI Usage Disclosure

See `AI_USAGE_DISCLOSURE.md` for a full account of how AI assistance was used in this project.

---

## Course Context

This project was built for MSML606 Extra Credit Project 2. The requirement was to apply graph algorithms or dynamic programming to a real-world problem. SkillPath uses both BFS shortest path and topological sort as the central mechanism, not as decorative additions. The problem it solves, helping people navigate career transitions by ordering skill dependencies, is one I genuinely think is worth solving.