# src/cycle_detect.py
# SkillPath: Career Skill Dependency Mapper
# Author: Monark Dixit (UID: 122259645)
# Course: MSML606, Spring 2026
#
# PURPOSE:
#   Implements DFS-based cycle detection on the skill dependency graph.
#   A cycle in a skill graph means "Skill A requires Skill B requires
#   Skill A" which is logically impossible and would cause topological
#   sort to loop forever.
#
#   This runs at graph construction time. Any back edges that form
#   cycles are identified and removed before any algorithm runs.
#
# ALGORITHM: DFS with three-color marking
#   WHITE (0): Node has not been visited yet
#   GRAY  (1): Node is currently being explored (in the DFS stack)
#   BLACK (2): Node and all its descendants have been fully explored
#
#   A cycle is detected when DFS reaches a GRAY node, meaning we
#   have found a back edge that leads back to an ancestor currently
#   on the recursion stack.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import DirectedGraph

# Color constants for DFS three-color marking
WHITE = 0   # Not yet visited
GRAY  = 1   # Currently in the DFS stack
BLACK = 2   # Fully processed


def detect_and_remove_cycles(graph: DirectedGraph) -> list:
    """
    Detects all cycles in the graph using DFS three-color marking
    and removes the back edges that cause them.

    For each back edge found, it is immediately removed from the graph
    so that topological sort can run safely afterward.

    Args:
        graph (DirectedGraph): The skill dependency graph to check.

    Returns:
        list: List of (from_node, to_node) tuples representing the
              back edges that were removed. Empty list means no cycles.
    """
    # Initialize all nodes as WHITE (unvisited)
    color = {node: WHITE for node in graph.get_all_nodes()}
    removed_edges = []

    def dfs(node: str):
        """
        Recursive DFS from a given node.
        Marks the node GRAY on entry and BLACK on exit.
        Detects and removes back edges when a GRAY node is reached.
        """
        # Mark this node as currently being explored
        color[node] = GRAY

        for neighbor in list(graph.get_neighbors(node)):
            if color[neighbor] == GRAY:
                # We found a back edge: node -> neighbor forms a cycle
                # Remove this edge to break the cycle
                graph.remove_edge(node, neighbor)
                removed_edges.append((node, neighbor))

            elif color[neighbor] == WHITE:
                # Neighbor has not been visited yet, continue DFS
                dfs(neighbor)

        # Mark this node as fully processed
        color[node] = BLACK

    # Run DFS from every unvisited node to cover disconnected components
    for node in list(graph.get_all_nodes()):
        if color[node] == WHITE:
            dfs(node)

    return removed_edges


def is_dag(graph: DirectedGraph) -> bool:
    """
    Returns True if the graph is a Directed Acyclic Graph (DAG).
    Runs cycle detection on a copy of the graph without modifying it.

    A DAG is required for topological sort to work correctly.

    Args:
        graph (DirectedGraph): The graph to check.

    Returns:
        bool: True if the graph has no cycles, False otherwise.
    """
    # Run detection on the actual graph
    # Since we only call this after detect_and_remove_cycles,
    # this should always return True in normal operation
    color = {node: WHITE for node in graph.get_all_nodes()}
    has_cycle = [False]

    def dfs_check(node: str):
        color[node] = GRAY
        for neighbor in graph.get_neighbors(node):
            if color[neighbor] == GRAY:
                has_cycle[0] = True
                return
            elif color[neighbor] == WHITE:
                dfs_check(neighbor)
        color[node] = BLACK

    for node in graph.get_all_nodes():
        if color[node] == WHITE:
            dfs_check(node)

    return not has_cycle[0]


# =============================================================================
# ENTRY POINT: VALIDATION
# =============================================================================

if __name__ == "__main__":
    from src.graph import build_graph_from_edges
    from data.skill_edges import SKILL_EDGES

    print("-" * 65)
    print("  SkillPath: Cycle Detection Validation")
    print("-" * 65)

    # Test 1: Run on the real skill graph
    print("\n[TEST 1] Running on real skill dependency graph")
    graph = build_graph_from_edges(SKILL_EDGES)
    removed = detect_and_remove_cycles(graph)

    if removed:
        print(f"  Cycles detected. Removed {len(removed)} back edge(s):")
        for edge in removed:
            print(f"    {edge[0]} -> {edge[1]}")
    else:
        print(f"  No cycles detected. Graph is a valid DAG.")

    print(f"  Is DAG after cleanup: {is_dag(graph)}")

    # Test 2: Manually inject a cycle and verify detection
    print("\n[TEST 2] Injecting artificial cycle: a -> b -> c -> a")
    test_graph = DirectedGraph()
    test_graph.add_edge("a", "b")
    test_graph.add_edge("b", "c")
    test_graph.add_edge("c", "a")   # this creates a cycle

    removed_test = detect_and_remove_cycles(test_graph)
    print(f"  Removed edges: {removed_test}")
    print(f"  Is DAG after cleanup: {is_dag(test_graph)}")

    print("\n" + "-" * 65)
    print("  Cycle detection validation complete.")
    print("-" * 65)