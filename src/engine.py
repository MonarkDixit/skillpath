#src/engine.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose:
#This is the core pipeline that ties all modules together.
#Given a user's current skills and a target job role, the engine:
#   1. Loads the required skills for the target role from the dataset
#   2. Builds the skill dependency subgraph for those skills
#   3. Runs cycle detection to ensure the graph is a valid DAG
#   4. Runs BFS to find the minimum skills the user still needs
#   5. Runs topological sort to determine the correct learning order
#   6. Returns a structured roadmap ready for the Streamlit UI

#This is the single function the UI calls. Everything else is internal.

#------------------------------------------------------------------------------

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import build_graph_from_edges, DirectedGraph
from src.cycle_detect import detect_and_remove_cycles
from src.topo_sort import topological_sort
from src.bfs_path import bfs_shortest_path, get_skills_needed
from src.data_loader import build_role_skills_map, get_top_skills_for_role
from data.skill_edges import SKILL_EDGES


def build_base_graph() -> DirectedGraph:
    """
    Builds and validates the full skill dependency graph.
    Runs cycle detection automatically before returning.

    Returns:
        DirectedGraph: A clean DAG ready for algorithm use.
    """
    graph = build_graph_from_edges(SKILL_EDGES)
    detect_and_remove_cycles(graph)
    return graph


def get_roadmap(
    current_skills: list,
    target_role: str,
    role_skills_map: dict,
    graph: DirectedGraph,
) -> dict:
    """
    Generates a personalized skill learning roadmap for a target role.

    This is the main function called by the Streamlit UI. It combines BFS shortest path and topological sort to produce an ordered list
    of skills the user needs to learn to qualify for the role.

    Args:
        current_skills (list): Skills the user already has.
        target_role (str): The job role the user is targeting.
        role_skills_map (dict): Output of build_role_skills_map().
        graph (DirectedGraph): The pre-built skill dependency graph.

    Returns:
        dict with the following keys:
            "role" (str): The target role title.
            "required_skills" (list): All skills needed for the role.
            "already_have" (list): Required skills the user already has.
            "missing_skills" (list): Required skills the user lacks.
            "roadmap" (list): Ordered list of skills to learn (topo sorted).
            "top_skills" (list): Most in-demand skills for this role.
            "coverage_pct" (float): % of required skills user already has.
            "is_qualified" (bool): True if user meets all requirements.
            "error" (str or None): Error message if something went wrong.
    """
    current_skills = {s.strip().lower() for s in current_skills}
    target_role = target_role.strip().lower()

    #Step 1: Get required skills for the target role from dataset
    required_skills = set(role_skills_map.get(target_role, []))

    if not required_skills:
        return {
            "role": target_role,
            "required_skills": [],
            "already_have": [],
            "missing_skills": [],
            "roadmap": [],
            "top_skills": [],
            "coverage_pct": 0.0,
            "is_qualified": False,
            "error": f"No skill data found for role: '{target_role}'",
        }

    #Only keep skills that exist in our dependency graph
    #Skills from the dataset that are not in our edge list are still
    #included as standalone nodes with no prerequisites
    graph_skills = graph.get_all_nodes()
    known_required = required_skills & graph_skills
    unknown_required = required_skills - graph_skills

    #Step 2: Determine what the user already has vs what they need
    already_have = current_skills & required_skills
    missing_skills = required_skills - current_skills

    #Step 3: Run BFS to find skills needed and their distances
    bfs_result = bfs_shortest_path(graph, current_skills, known_required)

    #Step 4: Get the full ordered list of skills to acquire
    skills_to_learn = get_skills_needed(graph, current_skills, known_required)

    #Step 5: Run topological sort on the subgraph of missing skills
    #This gives the correct prerequisite-respecting learning order
    missing_subgraph = graph.get_subgraph_for_skills(
        {s for s in skills_to_learn if s in graph_skills}
    )
    topo_order = topological_sort(missing_subgraph)

    #Build the final roadmap: skills in topo order, excluding already known
    roadmap = [s for s in topo_order if s not in current_skills]

    #Add any missing skills not in the graph as standalone items at the end
    for skill in sorted(unknown_required - current_skills):
        if skill not in roadmap:
            roadmap.append(skill)

    #Step 6: Compute coverage percentage
    coverage_pct = (len(already_have) / len(required_skills) * 100) if required_skills else 0.0
    is_qualified = len(missing_skills) == 0

    #Step 7: Get top skills frequency for this role
    top_skills = get_top_skills_for_role(role_skills_map, target_role, top_n=10)

    return {
        "role": target_role,
        "required_skills": sorted(required_skills),
        "already_have": sorted(already_have),
        "missing_skills": sorted(missing_skills),
        "roadmap": roadmap,
        "top_skills": top_skills,
        "coverage_pct": round(coverage_pct, 1),
        "is_qualified": is_qualified,
        "error": None,
    }


# =============================================================================
#Entry Point: Validation

if __name__ == "__main__":
    from src.data_loader import build_role_skills_map, get_all_roles

    print("-" * 65)
    print("  SkillPath: Engine Validation")
    print("-" * 65)

    print("\n[SETUP] Loading dataset and building graph...")
    role_skills_map = build_role_skills_map()
    graph = build_base_graph()
    all_roles = get_all_roles(role_skills_map)

    print(f"  Roles loaded:   {len(all_roles):,}")
    print(f"  Graph nodes:    {graph.get_stats()['node_count']}")
    print(f"  Graph edges:    {graph.get_stats()['edge_count']}")

    #Test 1: User with no skills targeting sales manager
    print("\n[TEST 1] No skills -> sales manager")
    result1 = get_roadmap(
        current_skills=[],
        target_role="sales manager",
        role_skills_map=role_skills_map,
        graph=graph,
    )
    print(f"  Required skills:  {result1['required_skills']}")
    print(f"  Already have:     {result1['already_have']}")
    print(f"  Coverage:         {result1['coverage_pct']}%")
    print(f"  Roadmap:")
    for i, skill in enumerate(result1["roadmap"], 1):
        print(f"    {i}. {skill}")

    #Test 2: User with some skills targeting data analyst
    print("\n[TEST 2] Has {finance, information technology} -> data analyst")
    result2 = get_roadmap(
        current_skills=["finance", "information technology"],
        target_role="data analyst",
        role_skills_map=role_skills_map,
        graph=graph,
    )
    print(f"  Coverage:         {result2['coverage_pct']}%")
    print(f"  Already have:     {result2['already_have']}")
    print(f"  Roadmap:")
    for i, skill in enumerate(result2["roadmap"], 1):
        print(f"    {i}. {skill}")

    #Test 3: Fully qualified user
    print("\n[TEST 3] Checking is_qualified flag")
    all_required = result1["required_skills"]
    result3 = get_roadmap(
        current_skills=all_required,
        target_role="sales manager",
        role_skills_map=role_skills_map,
        graph=graph,
    )
    print(f"  Is qualified:     {result3['is_qualified']}")
    print(f"  Coverage:         {result3['coverage_pct']}%")

    print("\n" + "-" * 65)
    print("  Engine validation complete.")
    print("-" * 65)