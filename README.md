# QUANTUM CIRCUIT SIMULATOR
A 3 qubit simulator for 3 Gate operations (X,Z,H) except CNOT (only for a 2 qubit system) along with KPI's and a Bell circuit simulation

## Circuits included
- Single Gate Demo: applies X gate to a target qubit, flips |0⟩ to |1⟩
- Bell State: H on qubit 1 + CNOT → produces 50% |00⟩, 50% |11⟩

## 📋 Prerequisites
Before running the script, make sure you have Python installed. This project requires:
* Python 3.7 
* Numpy library


## How to run
pip install numpy
python simulator.py

## KPIs measured
- Execution time (milliseconds)
- Memory usage (bytes) — calculated as state_size x 16
- State vector size — grows as 2^n with each qubit added
- Gate execution time (milliseconds)
- Probabaility Error/correctness



## Example output
i ran the single gate simulation for a 3 qubit system, targetting the 2nd qubit
Running Single Gate
 SINGLE GATE SIMULATION
Gate Applied : X on qubit 1
Outputs      : {'010': 1024}
State Vector : (+1.0000      )|010⟩
Memory Used  : 128 bytes
Total Time   : 0.9728 ms
  Probability Error : 0.000000 (should be 0)
  Gate Execution Time : 0.923200 ms

Running Bell State
 BELL STATE SIMULATION  
Circuit      : H(q1) + CNOT(ctrl=q1, tgt=q0)
Outputs      : {'00': 517, '11': 507}
State Vector : (+0.7071      )|00⟩ + (+0.7071      )|11⟩
Memory Used  : 64 bytes
Total Time   : 0.1721 ms
  Probability Error : 0.000000 (should be 0)
  Gate Execution Time : 0.146400 ms
