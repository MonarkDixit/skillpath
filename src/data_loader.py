# =============================================================================
# src/data_loader.py
# SkillPath: Career Skill Dependency Mapper
# Author: Monark Dixit (UID: 122259645)
# Course: MSML606, Spring 2026
#
# PURPOSE:
#   Loads role to skill mappings from the clean role_skills.py definition.
#   Provides helper functions used by the engine and UI.
# =============================================================================

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import Counter
from data.role_skills import ROLE_SKILLS


def build_role_skills_map() -> dict:
    """
    Builds a dictionary mapping each role to a flat list of skill names.
    Skills are repeated according to their frequency count so that
    Counter-based frequency analysis works correctly downstream.

    Returns:
        dict: { role_title (str): [skill_name, skill_name, ...] }
    """
    role_map = {}
    for role, skill_freq_list in ROLE_SKILLS.items():
        expanded = []
        for skill, freq in skill_freq_list:
            expanded.extend([skill] * freq)
        role_map[role] = expanded
    return role_map


def get_top_skills_for_role(role_skills_map: dict, role: str, top_n: int = 8):
    """
    Returns the top N most frequently required skills for a given role.

    Args:
        role_skills_map (dict): Output of build_role_skills_map()
        role (str): Role title (lowercase)
        top_n (int): Number of top skills to return

    Returns:
        list of (skill_name, count) tuples sorted by frequency descending
    """
    skills = role_skills_map.get(role.lower(), [])
    return Counter(skills).most_common(top_n)


def get_all_roles(role_skills_map: dict) -> list:
    """
    Returns a sorted list of all unique role titles.
    Used to populate the role dropdown in the UI.
    """
    return sorted(role_skills_map.keys())


def get_all_skills(role_skills_map: dict) -> list:
    """
    Returns a sorted list of all unique skill names across all roles.
    """
    all_skills = set()
    for skills in role_skills_map.values():
        all_skills.update(skills)
    return sorted(all_skills)


def audit_dataset():
    """Prints a summary of the clean role skills dataset."""
    print("=" * 65)
    print("  SkillPath: Role Skills Audit")
    print("=" * 65)

    role_map = build_role_skills_map()
    all_skills = get_all_skills(role_map)

    print(f"\n  Total roles:           {len(role_map)}")
    print(f"  Total unique skills:   {len(all_skills)}")

    print(f"\n  ROLES AND THEIR TOP 3 SKILLS:")
    for role, skills in role_map.items():
        top = Counter(skills).most_common(3)
        top_str = ", ".join(f"{s} ({c})" for s, c in top)
        print(f"    {role:<30} {top_str}")

    print("\n" + "=" * 65)
    print("  Audit complete.")
    print("=" * 65)


if __name__ == "__main__":
    audit_dataset()