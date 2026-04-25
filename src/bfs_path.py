#src/bfs_path.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose:
#Implements BFS shortest path on the skill dependency DAG.

#What does this solve?
#Given the skills a user already has and the skills required by a target role, this module finds the MINIMUM set of additional skills the user 
#needs to learn and how many steps it takes to get there.

#How BFS works here:
#We treat the user's current skills as the starting layer (layer 0).
#BFS propagates forward through the dependency graph, layer by layer. Each layer represents one prerequisite step away from what the 
#user already knows. The first time we reach a required skill, that is the shortest path to it.

#Example:
#  User has: {finance}
#  Target role needs: {advertising}
#  BFS finds:
#    Layer 0: finance (already known)
#    Layer 1: business development, accounting, ...
#    Layer 2: sales, marketing
#    Layer 3: advertising
#  Shortest path length to advertising = 3 steps

#COMPLEXITY: O(V + E) where V = nodes, E = edges
#---------------------------------------------------------------------------------------

import sys
import os
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import DirectedGraph


def bfs_shortest_path(
    graph: DirectedGraph,
    current_skills: set,
    target_skills: set,
) -> dict:
    """
    Runs BFS from the user's current skills toward the target skills.

    Finds the minimum number of prerequisite steps needed to reach each target skill from the user's current knowledge base.

    Args:
        graph (DirectedGraph): The full skill dependency graph.
        current_skills (set): Skills the user already has.
        target_skills (set): Skills required by the target role.

    Returns:
        dict with the following keys:
            "missing_skills" (set): Target skills the user does not have yet.
            "already_have" (set): Target skills the user already has.
            "reachable" (set): Missing skills reachable via prerequisites.
            "unreachable" (set): Missing skills with no path from current skills.
            "distances" (dict): {skill: min steps to reach it} for all visited nodes.
            "skills_to_acquire" (list): Ordered list of skills to learn,
                                        sorted by distance (closest first).
    """
    current_skills = {s.strip().lower() for s in current_skills}
    target_skills = {s.strip().lower() for s in target_skills}

    #Separate target skills into already known and missing
    already_have = current_skills & target_skills
    missing_skills = target_skills - current_skills

    #BFS initialization
    #Distance 0 = skills the user already has
    distances = {skill: 0 for skill in current_skills}
    queue = deque(current_skills)
    visited = set(current_skills)

    #BFS forward through the graph
    while queue:
        node = queue.popleft()
        current_dist = distances[node]

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)

    #Determine which missing target skills are reachable
    reachable = {s for s in missing_skills if s in distances}
    unreachable = missing_skills - reachable

    #Build the ordered list of skills to acquire
    #Sort by distance so closest skills come first
    skills_to_acquire = sorted(
        reachable,
        key=lambda s: distances.get(s, float("inf"))
    )

    return {
        "missing_skills": missing_skills,
        "already_have": already_have,
        "reachable": reachable,
        "unreachable": unreachable,
        "distances": distances,
        "skills_to_acquire": skills_to_acquire,
    }


def get_skills_needed(
    graph: DirectedGraph,
    current_skills: set,
    target_skills: set,
) -> list:
    """
    Returns only the intermediate skills the user needs to acquire to reach all target skills, excluding skills they already have.

    This is the minimal set of skills to learn, in order of how soon they become available based on prerequisites.

    Args:
        graph (DirectedGraph): The skill dependency graph.
        current_skills (set): Skills the user already has.
        target_skills (set): Skills required by the target role.

    Returns:
        list: Skills to acquire in order from closest to furthest.
    """
    result = bfs_shortest_path(graph, current_skills, target_skills)

    #Include all skills along the path, not just the final targets
    #This means intermediate prerequisites are included too
    all_needed = set()
    for skill in result["skills_to_acquire"]:
        all_needed.add(skill)
        #Walk backwards to find all prerequisites not yet owned
        queue = deque([skill])
        while queue:
            node = queue.popleft()
            for pred in graph.get_predecessors(node):
                if pred not in current_skills and pred not in all_needed:
                    all_needed.add(pred)
                    queue.append(pred)

    #Sort by BFS distance so the ordering reflects shortest path
    return sorted(
        all_needed,
        key=lambda s: result["distances"].get(s, float("inf"))
    )


# =============================================================================
#Entry Point: Validation

if __name__ == "__main__":
    from src.graph import build_graph_from_edges
    from src.cycle_detect import detect_and_remove_cycles
    from data.skill_edges import SKILL_EDGES

    print("-" * 65)
    print("  SkillPath: BFS Shortest Path Validation")
    print("-" * 65)

    graph = build_graph_from_edges(SKILL_EDGES)
    detect_and_remove_cycles(graph)

    #Test 1: User has finance, wants to reach advertising
    print("\n[TEST 1] User has: {finance}")
    print("         Target role needs: {advertising, public relations}")
    current = {"finance"}
    target = {"advertising", "public relations"}
    result = bfs_shortest_path(graph, current, target)

    print(f"  Already have:      {result['already_have']}")
    print(f"  Missing:           {result['missing_skills']}")
    print(f"  Reachable:         {result['reachable']}")
    print(f"  Unreachable:       {result['unreachable']}")
    print(f"  Steps to each:")
    for skill in sorted(result["missing_skills"]):
        dist = result["distances"].get(skill, "unreachable")
        print(f"    {skill}: {dist} step(s)")

    needed = get_skills_needed(graph, current, target)
    print(f"  Full learning path: {needed}")

    #Test 2: User already has most skills
    print("\n[TEST 2] User has: {finance, sales, marketing}")
    print("         Target role needs: {advertising, public relations, retail}")
    current2 = {"finance", "sales", "marketing"}
    target2 = {"advertising", "public relations", "retail"}
    result2 = bfs_shortest_path(graph, current2, target2)

    print(f"  Already have:      {result2['already_have']}")
    print(f"  Missing:           {result2['missing_skills']}")
    needed2 = get_skills_needed(graph, current2, target2)
    print(f"  Skills to acquire: {needed2}")

    #Test 3: User has everything needed
    print("\n[TEST 3] User already has all required skills")
    current3 = {"finance", "sales", "marketing", "advertising"}
    target3 = {"advertising", "marketing"}
    result3 = bfs_shortest_path(graph, current3, target3)
    print(f"  Already have:      {result3['already_have']}")
    print(f"  Missing:           {result3['missing_skills']}")
    needed3 = get_skills_needed(graph, current3, target3)
    print(f"  Skills to acquire: {needed3}")

    print("\n" + "-" * 65)
    print("  BFS shortest path validation complete.")
    print("-" * 65)