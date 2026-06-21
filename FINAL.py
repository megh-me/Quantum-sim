import numpy as np
import time

MAX_QUBITS = 3  

# Gate matrices 
I2 = np.array([[1, 0], [0, 1]], dtype=complex)                     #identity matrix
X  = np.array([[0, 1], [1, 0]], dtype=complex)                      # NOT gate
Z  = np.array([[1, 0], [0, -1]], dtype=complex)                      # phase flip
H  = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)    # HADAMARD

# CNOT gate: control=qubit1, target=qubit0
CNOT_10 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# CNOT gate: control=qubit0, target=qubit1
CNOT_01 = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]
], dtype=complex)

class QuantumCircuit:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits                            #number of Qubits considered in the simulator
        self.state_size  = 2 ** num_qubits                      #number of possible state vectors
        self.state = np.zeros(self.state_size, dtype=complex)   #probaibility vector initialized to an array of zeros
        self.state[0] = 1.0                                     #considering the state where all Qubits are 0
        self.gate_time_ms = 0.0                                 # total time spent applying gates

    def probabilities(self):
       probs = np.abs(self.state) ** 2                 
       return probs                                            # squares each amplitude to get the probability of each state

    def _expand(self, gate, target):                            #expansion for multi qubit operations
        ops = [gate if q == target else I2 for q in range(self.num_qubits - 1, -1, -1)]
        M = ops[0]
        for op in ops[1:]:
            M = np.kron(M, op)                                  #taking tensor product here
        return M                                                #final expanded operation 

    def apply_h(self, qubit):                                   #applying H
        t = time.perf_counter()
        self.state = self._expand(H, qubit) @ self.state
        self.gate_time_ms += (time.perf_counter() - t) * 1000

    def apply_x(self, qubit):                                   #applying X (NOT)
        t = time.perf_counter()
        self.state = self._expand(X, qubit) @ self.state
        self.gate_time_ms += (time.perf_counter() - t) * 1000

    def apply_z(self, qubit):                                    #applying Z
        t = time.perf_counter()
        self.state = self._expand(Z, qubit) @ self.state
        self.gate_time_ms += (time.perf_counter() - t) * 1000

    def apply_cnot(self, control: int, target: int):             #CNOT gate, only available to 2 qubit systems
        if self.num_qubits != 2:
            raise ValueError(f"CNOT is only available for 2-qubit systems. This circuit has {self.num_qubits} qubits.")
        if control not in (0, 1) or target not in (0, 1) or control == target:
            raise ValueError("For a 2-qubit system, control and target must be 0 or 1 and must differ.")
        t = time.perf_counter()
         # Selecting the CNOT matrix based on which qubit is control
        if control == 1 and target == 0:
            self.state = CNOT_10 @ self.state
        else: #control=0 and target=1
            self.state = CNOT_01 @ self.state
        self.gate_time_ms += (time.perf_counter() - t) * 1000

    def state_vector(self):                                                                 #readable representation of state vctor
        labels = [f"|{format(i, f'0{self.num_qubits}b')}⟩" for i in range(self.state_size)]
        terms = []                                                                          #stores the non-zero terms
        for amp, label in zip(self.state, labels):   
            if abs(amp) < 1e-10:                                                            #if the amplitude is too small, skips to the next iteration
                continue
            r, im = amp.real, amp.imag                                                      #splitting amplitutde into real and imaginary parts
            if abs(im) < 1e-10:
                terms.append(f"({r:+.4f}      ){label}")
            elif abs(r) < 1e-10:
                terms.append(f"({im:+.4f}j     ){label}")
            else:
                terms.append(f"({r:+.4f}{im:+.4f}j){label}") 
        if terms:                                                                            # if the list has anything in it
           return " + ".join(terms)
        else:
           return "0"

    def measure(self, shots=1024):                                                           #probability based measurement
        probs = np.abs(self.state) ** 2
        labels = [format(i, f'0{self.num_qubits}b') for i in range(self.state_size)]
        outcomes = np.random.choice(self.state_size, size=shots, p=probs)
        counts = {}
        for o in outcomes:
            counts[labels[o]] = counts.get(labels[o], 0) + 1
        return dict(sorted(counts.items()))

    def probability_correctness(self):
        # 1 - sum of all probabilities, should be 0.0 if state is valid
        error = 1 - np.sum(self.probabilities())
        print(f"  Probability Error : {error:.6f} (should be 0)")

    def gate_execution_time(self):
        print(f"  Gate Execution Time : {self.gate_time_ms:.6f} ms")


def run_single_gate(qubit=0,n=1,shots=1024): #Running a single gate of your choice
    t_start = time.perf_counter() 
    qb = QuantumCircuit(n) #currently for a single gate 
    qb.apply_x(qubit) #you can change the gate to whatever you wish

    total_time_ms = (time.perf_counter() - t_start) * 1000 #execution time in milliseconds
    measurements = qb.measure(shots)
    sv = qb.state_vector()

    print(" SINGLE GATE SIMULATION")
    print(f"Gate Applied : X on qubit {qubit}")
    print(f"Outputs      : {measurements}")
    print(f"State Vector : {sv}")
    print(f"Memory Used  : {qb.state_size * 16} bytes")
    print(f"Total Time   : {total_time_ms:.4f} ms")
    qb.probability_correctness()
    qb.gate_execution_time()


def run_bell_state(shots=1024):
    t_start = time.perf_counter()
    
    qc = QuantumCircuit(2)
    qc.apply_h(1)
    qc.apply_cnot(1, 0)

    total_time_ms = (time.perf_counter() - t_start) * 1000 #execution time in milliseconds
    measurements = qc.measure(shots=shots)
    sv = qc.state_vector()

    print(" BELL STATE SIMULATION  ")
    print(f"Circuit      : H(q1) + CNOT(ctrl=q1, tgt=q0)")
    print(f"Outputs      : {measurements}")
    print(f"State Vector : {sv}")
    print(f"Memory Used  : {qc.state_size * 16} bytes")
    print(f"Total Time   : {total_time_ms:.4f} ms")
    qc.probability_correctness()
    qc.gate_execution_time()


print("\nRunning Single Gate")
run_single_gate(qubit=0,n=1, shots=1024)

print("\nRunning Bell State")
run_bell_state(shots=1024)