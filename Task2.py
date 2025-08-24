import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
import itertools
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

console = Console()

@dataclass
class PetriNet:
    places: Set[str]
    transitions: Set[str]
    arcs: Set[Tuple[str, str]]  # (source, target)

class AlphaAlgorithm:
    def __init__(self, event_log: List[List[str]]):
        """
        Initialize Alpha Algorithm with an event log.
        event_log: List of traces, where each trace is a list of activities
        """
        self.event_log = event_log
        self.unique_traces = self._get_unique_traces()
        self.footprint_matrix = {}
        self._build_footprint_matrix()
    
    def _get_unique_traces(self) -> Dict[Tuple[str, ...], int]:
        """Convert event log into unique traces and their frequencies"""
        trace_counts = Counter(tuple(trace) for trace in self.event_log)
        return trace_counts
    
    def _build_footprint_matrix(self):
        """Build the footprint matrix showing relationships between activities"""
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
                        self.footprint_matrix[a1][a2] = "||"  # Parallel relationship
                    else:
                        self.footprint_matrix[a1][a2] = "->"  # Causality relationship
                elif a2 in direct_succession and a1 in direct_succession[a2]:
                    self.footprint_matrix[a1][a2] = "<-"  # Inverse causality relationship
                else:
                    self.footprint_matrix[a1][a2] = "#"  # Choice relationship
    
    def discover(self) -> PetriNet:
        """
        Implementation of the 8 steps of the Alpha Algorithm
        Returns a PetriNet object
        """
        # Step 1: Get all transitions (activities)
        T = set(activity for trace in self.event_log for activity in trace)
        
        # Step 2: Get initial transitions (activities that appear at start)
        TI = set(trace[0] for trace in self.event_log)
        
        # Step 3: Get final transitions (activities that appear at end)
        TO = set(trace[-1] for trace in self.event_log)
        
        # Step 4: Find pairs of sets (A, B) that meet the conditions
        X = set()
        for size_a in range(1, len(T) + 1):
            for size_b in range(1, len(T) + 1):
                for A in itertools.combinations(T, size_a):
                    for B in itertools.combinations(T, size_b):
                        if self._check_conditions(set(A), set(B)):
                            X.add((frozenset(A), frozenset(B)))
        
        # Step 5: Find maximal pairs (YL)
        YL = self._find_maximal_pairs(X)
        
        # Step 6: Create places (PL)
        places = {f"p_{i}" for i in range(len(YL))}
        places.add("start")
        places.add("end")
        
        # Step 7: Create arcs (FL)
        arcs = set()
        
        # Add arcs from start place to initial transitions (TI)
        for t in TI:
            arcs.add(("start", t))
            
        # Add arcs from final transitions (TO) to end place
        for t in TO:
            arcs.add((t, "end"))
            
        # Add arcs for internal places
        for i, (A, B) in enumerate(YL):
            place = f"p_{i}"
            for a in A:
                arcs.add((a, place))
            for b in B:
                arcs.add((place, b))
        
        # Step 8: Return the Petri net
        return PetriNet(places=places, transitions=T, arcs=arcs)
    
    def _check_conditions(self, A: Set[str], B: Set[str]) -> bool:
        """Check if sets A and B meet the conditions for creating a place"""
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
    
    def _find_maximal_pairs(self, X: Set[Tuple[frozenset, frozenset]]) -> Set[Tuple[frozenset, frozenset]]:
        """Find maximal pairs from set X"""
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

def generate_abbreviation(activity: str) -> str:
    """
    Generate an abbreviation for an activity name.
    - Splits camel-case names (e.g., GetOrder -> GO).
    - For non-camel case, takes the first two letters.
    """
    words = re.findall(r'[A-Z][^A-Z]*', activity)
    if words:
        # If camel case, use the first letters of each word
        return ''.join(word[0] for word in words).upper()
    # Otherwise, take the first two letters
    return activity[:2].upper()

def read_event_log(file_path: str) -> List[List[str]]:
    """Read event log from a file."""
    with open(file_path, "r") as file:
        event_log = [line.strip().split(",") for line in file.readlines()]
    return event_log

def main():
    # Read event log from event_log.txt
    event_log = read_event_log("event_log.txt")
    
    # Create Alpha Algorithm instance
    alpha = AlphaAlgorithm(event_log)
    
    # Display Event Log
    console.rule("[bold blue]Event Log (L) with Frequencies[/bold blue]")
    table = Table(title="Event Log")
    table.add_column("Trace")
    table.add_column("Frequency")
    for trace, freq in alpha.unique_traces.items():
        table.add_row(str(trace), str(freq))
    console.print(table)

    # Display Footprint Matrix with proper abbreviations
    console.rule("[bold blue]Footprint Matrix[/bold blue]")
    activities = sorted(set(act for trace in event_log for act in trace))
    
    # Create proper abbreviations
    activity_mapping = {activity: generate_abbreviation(activity) for activity in activities}
    abbreviated_activities = [activity_mapping[activity] for activity in activities]

    # Display activity mapping
    console.rule("[bold blue]Activity Abbreviations[/bold blue]")
    table_abbreviations = Table(title="Activity Abbreviations")
    table_abbreviations.add_column("Activity")
    table_abbreviations.add_column("Abbreviation")
    for activity, abbreviation in activity_mapping.items():
        table_abbreviations.add_row(activity, abbreviation)
    console.print(table_abbreviations)

    # Replace task names with abbreviations in matrix headers and rows
    matrix_headers = [" "] + abbreviated_activities
    matrix_rows = [
        [activity_mapping[a1]] + [alpha.footprint_matrix[a1][a2] for a2 in activities]
        for a1 in activities
    ]
    
    # Render footprint matrix with Tabulate (can replace with Rich table if preferred)
    matrix_output = tabulate(
        matrix_rows, 
        headers=matrix_headers, 
        tablefmt="grid", 
        maxcolwidths=15  # Adjust column width if necessary
    )
    console.print(matrix_output)

    # Extract unique events, initial, and final transitions
    TI = set(trace[0] for trace in event_log)
    TO = set(trace[-1] for trace in event_log)
    console.rule("[bold blue]Transitions[/bold blue]")
    console.print(f"Unique Events (TL): {activities}")
    console.print(f"Initial Events (TI): {TI}")
    console.print(f"Final Events (TO): {TO}")

    # Plain sets (X) and Maximal Sets (Y)
    console.rule("[bold blue]Plain Sets (X)[/bold blue]")
    X = set()
    T = set(activities)
    for size_a in range(1, len(T) + 1):
        for size_b in range(1, len(T) + 1):
            for A in itertools.combinations(T, size_a):
                for B in itertools.combinations(T, size_b):
                    if alpha._check_conditions(set(A), set(B)):
                        X.add((frozenset(A), frozenset(B)))
    for A, B in X:
        console.print(f"({A}, {B})")

    console.rule("[bold blue]Maximal Sets (Y)[/bold blue]")
    Y = alpha._find_maximal_pairs(X)
    for A, B in Y:
        console.print(f"({A}, {B})")
    
    # Save discovered pairs to file
    with open("discoveredpairs.txt", "w") as file:
        for A, B in Y:
            file.write(f"({set(A)}, {set(B)})\n")

    # Build and display Petri net
    petri_net = alpha.discover()
    console.rule("[bold blue]Petri Net Structure[/bold blue]")

    table_places = Table(title="Places")
    table_places.add_column("Places")
    for place in sorted(petri_net.places):
        table_places.add_row(place)
    console.print(table_places)

    table_transitions = Table(title="Transitions")
    table_transitions.add_column("Transitions")
    for transition in sorted(petri_net.transitions):
        table_transitions.add_row(transition)
    console.print(table_transitions)

    table_arcs = Table(title="Arcs")
    table_arcs.add_column("From")
    table_arcs.add_column("To")
    for arc in sorted(petri_net.arcs):
        table_arcs.add_row(*arc)
    console.print(table_arcs)

if __name__ == "__main__":
    main()
