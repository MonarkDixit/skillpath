#src/topo_sort.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose:
#Implements Kahn's algorithm for topological sorting from scratch.

#WHAT IS TOPOLOGICAL SORT?
#Given a DAG, topological sort produces a linear ordering of all nodes such that for every directed edge (A -> B), node A appears
#before node B in the ordering.

#In SkillPath this means: if "finance" must be learned before "accounting", then "finance" will always appear earlier in the
#learning roadmap than "accounting".

#KAHN'S ALGORITHM:
# 1. Compute the in-degree of every node
# 2. Add all nodes with in-degree 0 to a queue (no prerequisites)
# 3. While the queue is not empty:
#     a. Remove a node from the queue
#     b. Add it to the result ordering
#     c. For each neighbor of that node, decrement its in-degree by 1
#     d. If a neighbor's in-degree hits 0, add it to the queue
# 4. If result contains all nodes, the sort is complete
# If not, the graph has a cycle (should not happen after cycle detection)

# COMPLEXITY: O(V + E) where V = nodes, E = edges

#----------------------------------------------------------------------

import sys
import os
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import DirectedGraph


def topological_sort(graph: DirectedGraph) -> list:
    """
    Performs topological sort on a DAG using Kahn's algorithm.

    Returns a valid learning order where every prerequisite skill appears before the skills that depend on it.

    Args:
        graph (DirectedGraph): A DAG of skill dependencies.
                               Must have no cycles.

    Returns:
        list: Ordered list of skill names in valid learning sequence.
              Returns partial list if a cycle exists (should not happen
              after cycle detection runs).
    """
    #Step 1: Copy in-degree counts so we do not modify the graph
    in_degree = {node: graph.get_in_degree(node) for node in graph.get_all_nodes()}

    #Step 2: Initialize the queue with all nodes that have no prerequisites
    #These are the skills you can start learning right away
    queue = deque()
    for node, degree in in_degree.items():
        if degree == 0:
            queue.append(node)

    #Sort the initial queue alphabetically for deterministic output
    #This ensures the same input always produces the same ordering
    queue = deque(sorted(queue))

    result = []

    #Step 3: Process nodes one by one
    while queue:
        #Take the next node with no remaining prerequisites
        node = queue.popleft()
        result.append(node)

        #For each skill that depends on this node, reduce its in-degree
        #Sort neighbors for deterministic output
        for neighbor in sorted(graph.get_neighbors(node)):
            in_degree[neighbor] -= 1

            #If this neighbor now has no remaining prerequisites, it is ready to be learned next
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result


def topological_sort_subgraph(graph: DirectedGraph, target_skills: set) -> list:
    """
    Runs topological sort on only the subgraph relevant to the given target skills and their prerequisites.

    This is what the UI calls: given the skills required for a role, return the valid learning order for just those skills.

    Args:
        graph (DirectedGraph): The full skill dependency graph.
        target_skills (set): Skills required by the target role.

    Returns:
        list: Ordered skill names from first to learn to last.
    """
    subgraph = graph.get_subgraph_for_skills(target_skills)
    return topological_sort(subgraph)


#----------------------------------------------------------------------
#Entry Point: Validation


if __name__ == "__main__":
    from src.graph import build_graph_from_edges
    from src.cycle_detect import detect_and_remove_cycles
    from data.skill_edges import SKILL_EDGES

    print("-" * 65)
    print("  SkillPath: Topological Sort Validation")
    print("-" * 65)

    graph = build_graph_from_edges(SKILL_EDGES)
    detect_and_remove_cycles(graph)

    #Test 1: Full graph sort
    print("\n[TEST 1] Topological sort of full skill graph")
    order = topological_sort(graph)
    print(f"  Total skills in order: {len(order)}")
    print(f"  Learning sequence:")
    for i, skill in enumerate(order, 1):
        print(f"    {i:2}. {skill}")

    #Test 2: Subgraph sort for a specific role
    print("\n[TEST 2] Sort for target skills: sales, marketing, advertising")
    target = {"sales", "marketing", "advertising"}
    sub_order = topological_sort_subgraph(graph, target)
    print(f"  Subgraph learning sequence:")
    for i, skill in enumerate(sub_order, 1):
        print(f"    {i:2}. {skill}")

    #Test 3: Verify prerequisite ordering is respected
    print("\n[TEST 3] Verifying prerequisite ordering")
    violations = 0
    for from_node, to_node in SKILL_EDGES:
        if from_node in order and to_node in order:
            if order.index(from_node) > order.index(to_node):
                print(f"  VIOLATION: {from_node} appears after {to_node}")
                violations += 1
    if violations == 0:
        print(f"  All prerequisite orderings respected.")

    print("\n" + "-" * 65)
    print("  Topological sort validation complete.")
    print("-" * 65)