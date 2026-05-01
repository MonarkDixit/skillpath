# =============================================================================
# data/role_skills.py
# SkillPath: Career Skill Dependency Mapper
# Author: Monark Dixit (UID: 122259645)
# Course: MSML606, Spring 2026
#
# PURPOSE:
#   Defines a clean, realistic mapping of job roles to the skills
#   they require. This replaces the noisy LinkedIn dataset skill tags
#   which used broad industry categories instead of actual skill names.
#
#   Each role maps to a list of skills with a frequency count representing
#   how commonly that skill appears in job postings for that role.
#   These counts are based on real industry knowledge and are used to
#   drive the frequency bar chart in the UI.
# =============================================================================

# Format: role_title -> list of (skill_name, frequency_count) tuples
# skill_name must match the node names in skill_edges.py exactly

ROLE_SKILLS = {

    "data analyst": [
        ("statistics", 95),
        ("data analysis", 92),
        ("sql", 88),
        ("python", 82),
        ("excel", 78),
        ("data visualization", 70),
        ("machine learning", 45),
        ("communication", 40),
    ],

    "data scientist": [
        ("python", 98),
        ("machine learning", 95),
        ("statistics", 90),
        ("sql", 80),
        ("data analysis", 78),
        ("deep learning", 65),
        ("data visualization", 55),
        ("communication", 45),
    ],

    "machine learning engineer": [
        ("python", 98),
        ("machine learning", 96),
        ("deep learning", 90),
        ("statistics", 75),
        ("sql", 60),
        ("software engineering", 85),
        ("data analysis", 55),
        ("cloud computing", 70),
    ],

    "software engineer": [
        ("programming", 98),
        ("python", 88),
        ("software engineering", 92),
        ("databases", 75),
        ("sql", 70),
        ("cloud computing", 65),
        ("communication", 55),
        ("problem solving", 80),
    ],

    "product manager": [
        ("communication", 95),
        ("problem solving", 90),
        ("project management", 88),
        ("data analysis", 70),
        ("excel", 60),
        ("statistics", 40),
        ("sql", 35),
        ("leadership", 85),
    ],

    "marketing manager": [
        ("communication", 95),
        ("marketing", 92),
        ("data analysis", 70),
        ("excel", 65),
        ("social media", 75),
        ("project management", 60),
        ("leadership", 70),
        ("statistics", 35),
    ],

    "sales manager": [
        ("communication", 98),
        ("leadership", 90),
        ("sales", 95),
        ("project management", 65),
        ("excel", 60),
        ("problem solving", 75),
        ("marketing", 50),
        ("data analysis", 40),
    ],

    "business analyst": [
        ("communication", 90),
        ("data analysis", 88),
        ("sql", 75),
        ("excel", 80),
        ("statistics", 65),
        ("project management", 70),
        ("problem solving", 72),
        ("python", 45),
    ],

    "project manager": [
        ("project management", 98),
        ("communication", 95),
        ("leadership", 88),
        ("problem solving", 80),
        ("excel", 70),
        ("data analysis", 55),
        ("sql", 30),
        ("marketing", 25),
    ],

    "data engineer": [
        ("python", 95),
        ("sql", 92),
        ("databases", 90),
        ("cloud computing", 85),
        ("software engineering", 75),
        ("data analysis", 70),
        ("machine learning", 40),
        ("statistics", 35),
    ],

    "ux designer": [
        ("communication", 90),
        ("problem solving", 88),
        ("data analysis", 55),
        ("statistics", 30),
        ("project management", 60),
        ("excel", 40),
        ("marketing", 45),
        ("leadership", 35),
    ],

    "financial analyst": [
        ("excel", 95),
        ("statistics", 90),
        ("data analysis", 85),
        ("sql", 65),
        ("communication", 75),
        ("problem solving", 70),
        ("python", 45),
        ("databases", 40),
    ],

    "hr manager": [
        ("communication", 98),
        ("leadership", 90),
        ("project management", 75),
        ("excel", 70),
        ("problem solving", 72),
        ("data analysis", 45),
        ("statistics", 30),
        ("marketing", 25),
    ],

    "cybersecurity analyst": [
        ("programming", 80),
        ("python", 75),
        ("databases", 70),
        ("sql", 65),
        ("software engineering", 72),
        ("problem solving", 85),
        ("communication", 60),
        ("cloud computing", 68),
    ],

    "cloud engineer": [
        ("cloud computing", 98),
        ("python", 85),
        ("software engineering", 88),
        ("databases", 75),
        ("sql", 65),
        ("programming", 80),
        ("problem solving", 70),
        ("communication", 55),
    ],
}