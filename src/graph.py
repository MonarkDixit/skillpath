#src/graph.py
#SkillPath: Career Skill Dependency Mapper
#Author: Monark Dixit (UID: 122259645)
#Course: MSML606, Spring 2026

#Purpose:
#1. Implements a directed graph using an adjacency list from scratch
#2. This graph represents the skill dependency network where each node is a skill and each 
#directed edge (A -> B) means A is a prerequisite for B. No external graph libraries are 
#used for the core structure.

#Data Structure:
#Adjacency list: a dictionary where each key is a node (skill name) and the value is a 
#set of neighbors (skills that depend on it).

#Example: 
#   graph["python"] = {"pandas", "numpy", "tensorflow"}
#   graph["numpy"]  = {"tensorflow", "scikit-learn"}

#We also maintain a reverse adjacency list (predecessors) and an in-degree counter, 
#both of which are required by Kahn's topological sort algorithm.

#--------------------------------------------------------------------
from collections import defaultdict

class DirectedGraph:
    """
    A directed graph implemented from scratch using an adjacency list. Nodes represent 
    skills. A directed edge from A to B means A must be learned before B. 
    The graph supports:
        - Node and edge insertion
        - Neighbor lookup (forward and reverse)
        - In-degree computation (used by topological sort)
        - Subgraph extraction for a target role
        - Basic graph statistics
    """
    def __init__(self):
        """
        Initializes an empty directed graph.

        self.adj: forward adjacency list  { node: set of successors }
        self.radj: reverse adjacency list { node: set of predecessors }
        self.in_degree: in-degree counter { node: int }
        self.nodes: set of all nodes in the graph
        """
        self.adj = defaultdict(set)
        self.radj = defaultdict(set)
        self.in_degree = defaultdict(int)
        self.nodes = set()

    def add_node(self, node: str):
        """
        Adds a node to the graph if it does not already exist. Initializes its adjacency 
        list entry and in-degree to 0.

        Args:
            node (str): The skill name to add as a node.
        """
        node = node.strip().lower()
        if node not in self.nodes:
            self.nodes.add(node)
            # Ensure the node has an entry even if it has no edges
            if node not in self.adj:
                self.adj[node] = set()
            if node not in self.radj:
                self.radj[node] = set()
            if node not in self.in_degree:
                self.in_degree[node] = 0

    def add_edge(self, from_node: str, to_node: str):
        """
        Adds a directed edge from from_node to to_node. This means from_node is a 
        prerequisite for to_node.

        Also updates:
            - The reverse adjacency list (to_node -> from_node)
            - The in-degree of to_node (incremented by 1)

        Duplicate edges are ignored since we use sets.

        Args:
            from_node (str): The prerequisite skill.
            to_node (str): The skill that depends on from_node.
        """
        from_node = from_node.strip().lower()
        to_node = to_node.strip().lower()

        #Make sure both nodes exist before adding the edge
        self.add_node(from_node)
        self.add_node(to_node)

        #Only update in-degree if this is a new edge
        if to_node not in self.adj[from_node]:
            self.adj[from_node].add(to_node)
            self.radj[to_node].add(from_node)
            self.in_degree[to_node] += 1

    def remove_edge(self, from_node: str, to_node: str):
        """
        Removes a directed edge from from_node to to_node. Used by cycle detection to 
        remove offending back edges.

        Args:
            from_node (str): The source node.
            to_node (str): The destination node.
        """
        from_node = from_node.strip().lower()
        to_node = to_node.strip().lower()

        if to_node in self.adj.get(from_node, set()):
            self.adj[from_node].discard(to_node)
            self.radj[to_node].discard(from_node)
            self.in_degree[to_node] = max(0, self.in_degree[to_node] - 1)

    def get_neighbors(self, node: str) -> set:
        """
        Returns the set of skills that directly depend on this node. These are the skills 
        you can unlock after learning this one.

        Args:
            node (str): The skill name.

        Returns:
            set: Set of successor skill names.
        """
        return self.adj.get(node.strip().lower(), set())
    
    def get_predecessors(self, node: str) -> set:
        """
        Returns the set of skills that are prerequisites for this node. These are the 
        skills you need to learn before this one.

        Args:
            node (str): The skill name.

        Returns:
            set: Set of predecessor skill names.
        """
        return self.radj.get(node.strip().lower(), set())
    
    def get_in_degree(self, node: str) -> int:
        """
        Returns the in-degree of a node (number of prerequisite skills). A node with 
        in-degree 0 has no prerequisites.

        Args:
            node (str): The skill name.

        Returns:
            int: Number of incoming edges.
        """
        return self.in_degree.get(node.strip().lower(), 0)
    
    def get_all_nodes(self) -> set:
        #Returns the set of all skill nodes in the graph.
        return self.nodes.copy()
    
    def get_subgraph_for_skills(self, target_skills: set) -> "DirectedGraph":
        """
        Extracts a subgraph containing only the target skills and all their transitive prerequisites.

        This is used to build a focused view of the dependency graph for a specific job 
        role, rather than showing the entire graph.

        Algorithm:
            Starting from the target skills, walk backwards through the reverse adjacency 
            list (predecessors) using BFS until no new prerequisite nodes are found.

        Args:
            target_skills (set): Set of skill names required by the role.

        Returns:
            DirectedGraph: A new graph containing only relevant nodes and edges.
        """
        #Collect all nodes relevant to these target skills
        relevant_nodes = set()
        queue = list(target_skills)

        while queue:
            node = queue.pop()
            node = node.strip().lower()
            if node not in relevant_nodes and node in self.nodes:
                relevant_nodes.add(node)
                #Walk backwards to include all prerequisites
                for pred in self.get_predecessors(node):
                    if pred not in relevant_nodes:
                        queue.append(pred)

        #Build a new subgraph with only the relevant nodes and edges
        subgraph = DirectedGraph()
        for node in relevant_nodes:
            subgraph.add_node(node)
            for neighbor in self.get_neighbors(node):
                if neighbor in relevant_nodes:
                    subgraph.add_edge(node, neighbor)

        return subgraph
    
    def get_stats(self) -> dict:
        """
        Returns basic statistics about the graph. Used for validation and debugging.

        Returns:
            dict: node count, edge count, avg in-degree, avg out-degree
        """
        node_count = len(self.nodes)
        edge_count = sum(len(neighbors) for neighbors in self.adj.values())
        avg_in = sum(self.in_degree.values()) / node_count if node_count > 0 else 0
        avg_out = edge_count / node_count if node_count > 0 else 0

        return {
            "node_count": node_count,
            "edge_count": edge_count,
            "avg_in_degree": round(avg_in, 2),
            "avg_out_degree": round(avg_out, 2),
        }
    
    def __repr__(self):     
        #Provides a concise string representation of the graph for debugging purposes.
        return (
            f"DirectedGraph("
            f"nodes={len(self.nodes)}, "
            f"edges={sum(len(v) for v in self.adj.values())})"
        )
    
#---------------------------------------------------------------------
#Graph Builder: Constructs the full skill dependency graph from the edge list.

def build_graph_from_edges(edges: list) -> DirectedGraph:
    """
    Builds a DirectedGraph from a list of (from_node, to_node) tuples.

    Args:
        edges (list): List of (prerequisite, dependent) string tuples.

    Returns:
        DirectedGraph: The fully constructed skill dependency graph.
    """
    graph = DirectedGraph()
    for from_node, to_node in edges:
        graph.add_edge(from_node, to_node)
    return graph

#---------------------------------------------------------------------
#Entry Point: Validation

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data.skill_edges import SKILL_EDGES

    print("-" * 65)
    print("  SkillPath: Graph Construction Validation")
    print("-" * 65)

    graph = build_graph_from_edges(SKILL_EDGES)
    stats = graph.get_stats()

    print(f"\n  Nodes (unique skills): {stats['node_count']}")
    print(f"  Edges (dependencies):  {stats['edge_count']}")
    print(f"  Avg in-degree:         {stats['avg_in_degree']}")
    print(f"  Avg out-degree:        {stats['avg_out_degree']}")

    print(f"\n  NODES WITH NO PREREQUISITES (starting points):")
    roots = [n for n in graph.get_all_nodes() if graph.get_in_degree(n) == 0]
    for r in sorted(roots):
        print(f"    {r}")

    print(f"\n  SAMPLE NEIGHBOR LOOKUPS:")
    samples = ["management", "finance", "sales", "information technology"]
    for skill in samples:
        neighbors = graph.get_neighbors(skill)
        print(f"    {skill} -> {sorted(neighbors)}")

    print("\n" + "-" * 65)
    print("  Graph validation complete.")
    print("-" * 65)