# Process Mining and Simulation: Event Log Generation and Alpha Algorithm

This repository contains the deliverables for **Process Mining and Simulation** practices applied to a Shipment and Delivery process chain. The project focuses on generating event logs with noise and uncommon paths, applying the Alpha Algorithm to mine a Petri Net, and visualizing the results using Graphviz.

---

## 🌐 Project Overview

**Objective**: Develop an event log generator to simulate process traces with noise and uncommon paths, apply the Alpha Algorithm to mine a Petri Net, and evaluate the model’s fitness, precision, and accuracy for a given process description.

---

## 📋 Process Description

The process modeled is an order fulfillment workflow:

🔹 **Sequential Steps**: Start with *Receive Order* → *Process Payment*.\
🔹 **Parallel Execution**: *Verify Payment* and *Prepare Package*.\
🔹 **AND-Split**: *Generate Shipping Label* and *Confirm Delivery*.\
🔹 **XOR-Split**: *Dispatch by Courier* or *Enable In-store Pickup*.

🔹 **Input Parameters**:

- Noise Frequency: 20% (0.2, introduces *SysErr*).
- Uncommon Path Frequency: 10% (0.1, introduces *ManualOverride*).
- Number of Traces: 70.
- Noise Step: *SysErr*.
- Uncommon Step: *ManualOverride*.

---

## 🌟 Key Features

### 1. Preprocessing Steps

- **Parsing**: Convert the process description into a structured format for trace generation.
- **Noise and Uncommon Paths**: Simulate real-world deviations with *SysErr* (noise) and *ManualOverride* (uncommon paths).
- **Input Validation**: Ensure consistency of parameters (noise frequency, uncommon paths, trace counts).

### 2. Design Choices

🔹 **Input Parameters**: Noise (20%) and uncommon path (10%) frequencies reflect real-world variability.\
🔹 **Frozensets**: Used for transitions to ensure data immutability.\
🔹 **Probabilistic Execution**: Models XOR and AND splits for diverse pathways.\
🔹 **Visualization**: Graphviz for clear, distinguishable Petri Net representations (places, transitions, arcs).

### 3. Event Log Generator

- Generates 70 traces based on the process description, incorporating noise (*SysErr*) and uncommon paths (*ManualOverride*).
- Handles sequential, parallel, and split (XOR/AND) activities.

### 4. Alpha Algorithm

🔹 Mines a Petri Net from event logs by:

- Calculating direct succession and footprint matrix.
- Extracting unique traces and their frequencies.
- Identifying maximal pairs for Petri Net places.

### 5. Visualization

- Uses Graphviz to visualize the Petri Net, clearly distinguishing places, transitions, and arcs.
- Represents sequential dependencies, concurrency, and probabilistic splits.

### 6. Integration

- Combines event log generation, Alpha Algorithm, and visualization into a cohesive pipeline.
- Outputs parsed logs, mined Petri Nets, and visual models.

---

## 📈 Model Outputs

🔹 **Petri Net Structure**: Includes transitions as frozensets (e.g., {Verify Payment}, {Prepare Package}, {SysErr}).\
🔹 **Key Observations**:

- Captures sequential dependencies (*Receive Order* → *Process Payment*).
- Represents concurrent activities (*Verify Payment*, *Prepare Package*).
- Models XOR (*Dispatch by Courier* or *Enable In-store Pickup*) and AND splits (*Generate Shipping Label*, *Confirm Delivery*).
- Incorporates noise (*SysErr*) and uncommon steps (*ManualOverride*).

---

## 🔍 Evaluation

### Fitness

🔹 **Strengths**: Accurately reproduces sequential and concurrent components; handles noise and uncommon paths.\
🔹 **Challenges**: Noise (*SysErr*) may introduce unexplainable transitions, risking overfitting.\
🔹 **Conclusion**: Good fitness, but noisy traces may cause misalignment.

### Precision

🔹 **Strengths**: Explicit XOR/AND splits and isolated uncommon paths prevent excessive generalization.\
🔹 **Challenges**: High noise frequency (20%) may dilute precision by introducing excessive *SysErr* transitions.\
🔹 **Conclusion**: Moderate precision, improvable by reducing noise.

### Accuracy and Generalization

🔹 **Strengths**: Robust for real-world scenarios with clear concurrency and split representations.\
🔹 **Weaknesses**: Excessive noise/uncommon paths may hinder generalization.\
🔹 **Conclusion**: High accuracy, but needs refined noise and split probabilities.

---

## ⚠️ Challenges

- **Concurrency Handling**: Modeling parallel tasks (*Verify Payment*, *Prepare Package*) without ambiguous execution order.
- **Noise/Uncommon Paths**: Balancing interpretability with *SysErr* and *ManualOverride* integration.
- **Split Representation**: Accurately capturing probabilistic XOR/AND splits.
- **Scalability**: Managing complex processes with increasing transitions.

---

## 💡 Recommendations for Improvement

🔹 **Reduce Noise Frequency**: Lower to \~10% to prevent overfitting and improve precision.\
🔹 **Refine Probabilities**: Assign realistic probabilities to XOR/AND splits.\
🔹 **Concurrency Clarity**: Add explicit constraints for parallel tasks.\
🔹 **Validate Against Real Logs**: Compare outputs with actual traces to refine transitions.\
🔹 **Visual Enhancements**: Use annotations to highlight noisy/uncommon steps in visualizations.

---

## 📁 Project Structure

```plaintext
.
├── src/
│   ├── event_log_generator.py  # Generates traces with noise/uncommon paths
│   ├── alpha_algorithm.py      # Implements Alpha Algorithm for Petri Net mining
│   ├── visualization.py        # Graphviz visualization of Petri Nets
│   └── utils.py                # Utility functions for parsing and validation
├── data/
│   ├── event_logs.txt          # Generated event logs
│   ├── petri_net.dot           # Petri Net visualization source
│   └── petri_net.png           # Rendered Petri Net image
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Installation

### Prerequisites

🔹 **Python**: v3.8 or later\
🔹 **Graphviz**: For visualization\
🔹 **Dependencies**: Listed in `requirements.txt`

### Setup

- **Clone the Repository**:

  ```bash
  git clone https://github.com/username/process-mining-alpha.git
  cd process-mining-alpha
  ```

- **Install Dependencies**:

  ```bash
  pip install -r requirements.txt
  ```

- **Install Graphviz**:

  - Follow Graphviz installation instructions.

- **Run the Pipeline**:

  ```bash
  python src/main.py
  ```

---

## 📖 Usage

- **Generate Event Logs**: Run `event_log_generator.py` to create traces with specified noise (20%) and uncommon path (10%) frequencies.
- **Mine Petri Net**: Use `alpha_algorithm.py` to process event logs and generate a Petri Net.
- **Visualize**: Run `visualization.py` to create a Graphviz-based Petri Net diagram (`data/petri_net.png`).
- **View Outputs**: Check `data/event_logs.txt` for traces and `data/petri_net.png` for the visual model.

---

## 🏁 Conclusion

The project successfully generates event logs, mines a Petri Net using the Alpha Algorithm, and visualizes the results. The model shows strong fitness and moderate precision, with high overall accuracy. Refinements in noise frequency and split probabilities could further enhance performance.

---
## 👨‍💻 Contributors
- **Abdullah Daoud (22I-2626)**  
- **Talha Mukhtiar (22I-2720)**  
- **Faizan Rasheed (22I-2734)**
- **Dawood Hussain (22I-2410)**

---

## ⚖️ License
This project is for **academic and personal skill development purposes only**.  
Reuse is allowed for **learning and research** with proper credit.

---
