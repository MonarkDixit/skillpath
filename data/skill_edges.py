# =============================================================================
# data/skill_edges.py
# SkillPath: Career Skill Dependency Mapper
# Author: Monark Dixit (UID: 122259645)
# Course: MSML606, Spring 2026
#
# PURPOSE:
#   Defines the directed prerequisite edges between skills.
#   Each tuple (A, B) means "you should learn A before B".
#
#   All skill names here match exactly the skill names used in
#   role_skills.py so the graph and the role mappings are consistent.
#
#   This is an original contribution of the SkillPath project.
# =============================================================================

SKILL_EDGES = [

    # --- FOUNDATIONS ---
    # These are entry-level skills everything else builds on
    ("problem solving", "programming"),
    ("problem solving", "statistics"),
    ("problem solving", "communication"),
    ("communication", "leadership"),
    ("communication", "marketing"),
    ("communication", "project management"),

    # --- DATA TRACK ---
    # The natural progression from basics to advanced data skills
    ("statistics", "data analysis"),
    ("excel", "data analysis"),
    ("data analysis", "sql"),
    ("sql", "databases"),
    ("databases", "python"),
    ("python", "data visualization"),
    ("data analysis", "data visualization"),
    ("python", "machine learning"),
    ("statistics", "machine learning"),
    ("machine learning", "deep learning"),

    # --- ENGINEERING TRACK ---
    # From programming fundamentals to advanced engineering
    ("programming", "python"),
    ("programming", "software engineering"),
    ("python", "software engineering"),
    ("software engineering", "databases"),
    ("databases", "cloud computing"),
    ("software engineering", "cloud computing"),

    # --- BUSINESS TRACK ---
    # From foundational tools to management and strategy
    ("excel", "statistics"),
    ("data analysis", "project management"),
    ("project management", "leadership"),
    ("leadership", "sales"),
    ("marketing", "sales"),

    # --- CROSS TRACK CONNECTIONS ---
    ("statistics", "data visualization"),
    ("sql", "python"),
    ("data analysis", "machine learning"),
    ("problem solving", "data analysis"),
    ("communication", "project management"),
    ("excel", "data analysis"),
]