import random

def parse_process_description(description):
    """
    Parse the process description into a structured list of steps or constructs.
    
    Args:
    - description (str): Process description in the format "Start With(Task1), Then(Task2), Parallel(Task3, Task4), And(Task5, Task6), XOR(Task7, Task8)"
    
    Returns:
    - list: Parsed process description as a list of steps or constructs.
    """
    constructs = []
    for segment in description.split("),"):
        segment = segment.strip()
        if segment.startswith("Start With("):
            constructs.append(segment[11:].strip(")"))
        elif segment.startswith("Then("):
            constructs.append(segment[5:].strip(")"))
        elif segment.startswith("Parallel("):
            tasks = [task.strip() for task in segment[9:].strip(")").split(",")]
            constructs.append(("Parallel", tasks))
        elif segment.startswith("And("):
            tasks = [task.strip() for task in segment[4:].strip(")").split(",")]
            constructs.append(("And", tasks))
        elif segment.startswith("XOR("):
            tasks = [task.strip() for task in segment[4:].strip(")").split(",")]
            constructs.append(("XOR", tasks))
    return constructs

def generate_trace(constructs, num_paths, noise_steps, uncommon_steps, noise_frequency, uncommon_paths_frequency):
    """
    Generate traces with specified steps, parallel XOR, AND steps,
    and include noise and uncommon paths in between steps with user-defined frequencies.
    
    Args:
    - constructs (list): List of steps or constructs parsed from the process description.
    - num_paths (int): Number of traces to generate.
    - noise_steps (list): List of noise steps.
    - uncommon_steps (list): List of uncommon steps.
    - noise_frequency (float): Frequency (0 to 1) for adding noise.
    - uncommon_paths_frequency (float): Frequency (0 to 1) for adding uncommon paths.
    
    Returns:
    - list of generated traces.
    """
    traces = []
    
    for _ in range(num_paths):
        trace = []
        for construct in constructs:
            if isinstance(construct, str):
                # Regular step
                trace.append(construct)
            elif isinstance(construct, tuple):
                if construct[0] == "Parallel":
                    # Parallel: Randomize the order
                    trace.extend(random.sample(construct[1], len(construct[1])))
                elif construct[0] == "And":
                    # And: Add all tasks sequentially
                    trace.extend(construct[1])
                elif construct[0] == "XOR":
                    # XOR: Pick one task randomly
                    trace.append(random.choice(construct[1]))
            
            # Randomly add noise or uncommon paths
            if random.random() < noise_frequency:
                trace.append(random.choice(noise_steps))
            if random.random() < uncommon_paths_frequency:
                trace.append(random.choice(uncommon_steps))
        
        traces.append(",".join(trace))
    
    return traces

def save_to_file(traces, filename="event_log.txt"):
    """Save the generated traces to a file."""
    with open(filename, "w") as file:
        for trace in traces:
            file.write(f"{trace}\n")

# Input from user
noise_frequency = float(input("Enter the frequency (0 to 1) for noise (e.g., 0.3 for 30% chance): "))
uncommon_paths_frequency = float(input("Enter the frequency (0 to 1) for uncommon paths (e.g., 0.2 for 20% chance): "))

process_description = input("Enter the process description (e.g., Start With(Receive Order), Then(Process Payment), Parallel(Verify Payment, Prepare Package), And(Generate Shipping Label, Confirm Delivery), XOR(Dispatch by Courier, Enable In-store Pickup)): ")
constructs = parse_process_description(process_description)

noise_steps = [step.strip() for step in input("Enter noise steps (comma-separated, e.g., 'System Error, Connection Timeout'): ").split(",")]
uncommon_steps = [step.strip() for step in input("Enter uncommon steps (comma-separated, e.g., 'Alternate Path Taken, Manual Override'): ").split(",")]

num_paths = int(input("Enter the number of traces to generate: "))

# Generate traces
traces = generate_trace(constructs, num_paths, noise_steps, uncommon_steps, noise_frequency, uncommon_paths_frequency)

# Save and output the generated traces
save_to_file(traces)
for trace in traces:
    print(trace)
