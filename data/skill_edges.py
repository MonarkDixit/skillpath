#data/skill_edges.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose:
#1. Defines the directed prerequisite edges between skills.
#2. Each tuple (A, B) indicates that skill A is a prerequisite for skill B.
#3. These edges are based on real-world learning dependencies observed across job postings
#4. This is my own original contribution of the SkillPath project, based on my analysis of the dataset and domain knowledge.

#Skills are grouped into 6 families:
#1. Core Foundations
#2. Data and Analytics
#3. Engineering and Technology
#4. Business and Management
#5. Marketing and Sales
#6. Health and Operations

#--------------------------------------------------------------------

SKILL_EDGES = [
    #----Core Foundations: These are entry level skills that feed into almost every other domain---
    ("finance", "accounting"),
    ("finance", "business development"),
    ("finance", "strategy/planning"),
    ("management", "project management"),
    ("management", "strategy/planning"),
    ("management", "consulting"),
    ("information technology", "engineering"),
    ("information technology", "manufacturing"),
    ("information technology", "research"),
    
    #----Data and Analytics Family---
    ("information technology", "data analysis"),
    ("data analysis", "research"),
    ("research", "consulting"),
    ("data analysis", "strategy/planning"),

    #----Engineering and Technology Family---
    ("engineering", "manufacturing"),
    ("engineering", "design"),
    ("information technology", "design"),
    ("design", "advertising"),
    ("manufacturing", "operations"),

    #----Business and Management Family---
    ("business development", "sales"),
    ("sales", "marketing"),
    ("marketing", "advertising"),
    ("marketing", "strategy/planning"),
    ("management", "human resources"),
    ("human resources", "staffing and recruiting"),
    ("finance", "purchasing"),
    ("Operations", "management"),
    ("strategy/planning", "consulting"),
    
    #----Marketing and Sales Family---
    ("sales", "customer service"),
    ("marketing", "public relations"),
    ("advertising", "public relations"),
    ("business development", "marketing"),
    ("customer service", "retail"),

    #---Health and Operations Family---
    ("health care provider", "nonprofit organization management"),
    ("health care provider", "research"),
    ("operations", "supply chain"),
    ("manufacturing", "supply chain"),
    ("finance", "insurance"),
    ("management", "nonprofit organization management"),

    #---Cross Domain Connections---
    ("research", "nonprofit organization management"),
    ("design", "marketing"),
    ("operations", "management"),
    ("finance", "strategy/planning"),
]