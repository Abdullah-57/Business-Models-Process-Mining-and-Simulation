from graphviz import Digraph
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, FrozenSet
from collections import defaultdict, Counter
import itertools

@dataclass
class PetriNet:
    places: Set[str]
    transitions: Set[str]
    arcs: Set[Tuple[str, str]]

def read_event_log(file_path: str) -> List[List[str]]:
    """Read event log from a file"""
    with open(file_path, 'r') as file:
        # Read each line, strip newline, and split by commas
        event_log = [line.strip().split(',') for line in file.readlines()]
    return event_log

class AlphaAlgorithm:
    def __init__(self, event_log: List[List[str]]):
        self.event_log = event_log
        self.unique_traces = self._get_unique_traces()
        self.footprint_matrix = {}
        self._build_footprint_matrix()
    
    def _get_unique_traces(self) -> Dict[Tuple[str, ...], int]:
        trace_counts = Counter(tuple(trace) for trace in self.event_log)
        return trace_counts
    
    def _build_footprint_matrix(self):
        direct_succession = defaultdict(set)
        activities = set()
        
        for trace in self.event_log:
            activities.update(trace)
            for i in range(len(trace) - 1):
                direct_succession[trace[i]].add(trace[i + 1])
        
        for a1 in activities:
            self.footprint_matrix[a1] = {}
            for a2 in activities:
                if a1 in direct_succession and a2 in direct_succession[a1]:
                    if a2 in direct_succession and a1 in direct_succession[a2]:
                        self.footprint_matrix[a1][a2] = "||"
                    else:
                        self.footprint_matrix[a1][a2] = "->"
                elif a2 in direct_succession and a1 in direct_succession[a2]:
                    self.footprint_matrix[a1][a2] = "<-"
                else:
                    self.footprint_matrix[a1][a2] = "#"
    
    def discover(self) -> PetriNet:
        # Step 1: Get all transitions
        T = set(activity for trace in self.event_log for activity in trace)
        
        # Step 2: Get initial transitions
        TI = set(trace[0] for trace in self.event_log)
        
        # Step 3: Get final transitions
        TO = set(trace[-1] for trace in self.event_log)
        
        # Step 4: Find pairs of sets (A, B) that meet the conditions
        X = set()
        for size_a in range(1, len(T) + 1):
            for size_b in range(1, len(T) + 1):
                for A in itertools.combinations(T, size_a):
                    for B in itertools.combinations(T, size_b):
                        if self._check_conditions(set(A), set(B)):
                            X.add((frozenset(A), frozenset(B)))
        
        # Step 5: Find maximal pairs
        YL = self._find_maximal_pairs(X)
        
        # Step 6: Create places
        places = {f"p_{i}" for i in range(len(YL))}
        places.add("start")
        places.add("end")
        
        # Step 7: Create arcs
        arcs = set()
        
        # Add arcs from start place to initial transitions
        for t in TI:
            arcs.add(("start", t))
        
        # Add arcs from final transitions to end place
        for t in TO:
            arcs.add((t, "end"))
        
        # Add arcs for internal places
        for i, (A, B) in enumerate(YL):
            place = f"p_{i}"
            for a in A:
                arcs.add((a, place))
            for b in B:
                arcs.add((place, b))
        
        return PetriNet(places=places, transitions=T, arcs=arcs)
    
    def _check_conditions(self, A: Set[str], B: Set[str]) -> bool:
        # Condition 1: All elements in A should never follow each other
        for a1, a2 in itertools.product(A, A):
            if self.footprint_matrix[a1][a2] != "#":
                return False
        
        # Condition 2: All elements in B should never follow each other
        for b1, b2 in itertools.product(B, B):
            if self.footprint_matrix[b1][b2] != "#":
                return False
        
        # Condition 3: Every element in A should have causality with every element in B
        for a, b in itertools.product(A, B):
            if self.footprint_matrix[a][b] != "->":
                return False
        
        return True
    
    def _find_maximal_pairs(self, X: Set[Tuple[FrozenSet, FrozenSet]]) -> Set[Tuple[FrozenSet, FrozenSet]]:
        Y = set()
        for pair1 in X:
            is_maximal = True
            A1, B1 = pair1
            
            for pair2 in X:
                if pair1 == pair2:
                    continue
                A2, B2 = pair2
                if A1.issubset(A2) and B1.issubset(B2):
                    is_maximal = False
                    break
            
            if is_maximal:
                Y.add(pair1)
        
        return Y

def visualize_petri_net(places: Set[str], transitions: Set[str], arcs: Set[Tuple[str, str]], filename: str = "petri_net"):
    """Create a visualization of a Petri net using Graphviz"""
    dot = Digraph(comment='Petri Net')
    
    # Set graph attributes
    dot.attr(rankdir='LR')
    dot.attr('node', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Add places
    for place in places:
        if place == "start":
            dot.node(place, "", shape='circle', style='filled', fillcolor='lightgrey', 
                    width='0.5', height='0.5')
        elif place == "end":
            dot.node(place, "", shape='doublecircle', width='0.5', height='0.5')
        else:
            dot.node(place, "", shape='circle', width='0.5', height='0.5')
    
    # Add transitions
    for transition in transitions:
        dot.node(transition, transition, shape='box', height='0.5', 
                style='filled', fillcolor='lightblue')
    
    # Add arcs
    for source, target in arcs:
        dot.edge(source, target)
    
    # Save the visualization
    dot.render(filename, format='pdf', cleanup=True)
    dot.render(filename, format='png', cleanup=True)

def main():
    # Path to the event log file (replace with your actual file path)
    event_log_file = 'event_log.txt'
    
    # Read event log from file
    event_log = read_event_log(event_log_file)
    
    # Create Alpha Algorithm instance
    alpha = AlphaAlgorithm(event_log)
    
    # Get the Petri net
    petri_net = alpha.discover()
    
    # Create visualization
    visualize_petri_net(
        places=petri_net.places,
        transitions=petri_net.transitions,
        arcs=petri_net.arcs,
        filename="process_model"
    )

if __name__ == "__main__":
    main()
