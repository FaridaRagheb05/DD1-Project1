import os
import re
import heapq  # For the priority queue

# Enum-like dictionary for gate types
GATE_TYPES = {
    "and": "AND",
    "or": "OR",
    "xor": "XOR",
    "nand": "NAND",
    "nor": "NOR",
    "xnor": "XNOR",
    "buf": "BUF",
    "not": "NOT"
}

class Gate:
    def __init__(self, type, delay, output, inputs):
        self.type = type
        self.delay = delay
        self.output = output
        self.inputs = inputs

    def evaluate(self, values):
        inputs = [values.get(inp, 0) for inp in self.inputs]
        if self.type == "AND":
            return int(all(inputs))
        elif self.type == "OR":
            return int(any(inputs))
        elif self.type == "XOR":
            return int(inputs[0] ^ inputs[1])
        elif self.type == "NAND":
            return int(not all(inputs))
        elif self.type == "NOR":
            return int(not any(inputs))
        elif self.type == "XNOR":
            return int(inputs[0] == inputs[1])
        elif self.type == "BUF":
            return inputs[0]
        elif self.type == "NOT":
            return int(not inputs[0])

class Circuit:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.gates = []

    def display(self):
        print(f"\nCircuit name: {self.name}")
        print("Inputs:", " ".join(self.inputs))
        print("Outputs:", " ".join(self.outputs))
        print("Wires:", " ".join(self.wires))
        print("Gates:")
        for gate in self.gates:
            print(f"  Type: {gate.type}, Delay: {gate.delay}, Output: {gate.output}, Inputs: {' '.join(gate.inputs)}")

    def simulate(self, events, output_file):
        # Initialize signal values
        values = {name: 0 for name in self.inputs + self.wires + self.outputs}
        # Initialize event queue
        event_queue = []
        # Initialize event ID counter
        event_id = 0
        # Add input events to the queue
        for time, input_name, value in events:
            heapq.heappush(event_queue, (time, 'input', event_id, input_name, value))
            event_id += 1

        # Keep track of scheduled gate evaluations to avoid redundant evaluations
        scheduled_gate_evaluations = {}

        # Simulation time
        current_time = 0
        # Output lines
        output_lines = []

        # While there are events in the queue
        while event_queue:
            # Get the next event
            time, event_type, _, *event_data = heapq.heappop(event_queue)
            current_time = time
            # Process all events at this time
            signal_changes = {}
            # Collect events that occur at the same time
            current_events = [(event_type, event_data)]
            while event_queue and event_queue[0][0] == current_time:
                _, evt_type, _, *evt_data = heapq.heappop(event_queue)
                current_events.append((evt_type, evt_data))

            # Process each event
            for evt_type, evt_data in current_events:
                if evt_type == 'input':
                    input_name, value = evt_data
                    if values[input_name] != value:
                        # Record the input change
                        output_lines.append(f"{current_time}, {input_name}, {value}")
                        values[input_name] = value
                        # Schedule gate evaluations affected by this input
                        for gate in self.gates:
                            if input_name in gate.inputs:
                                output_time = current_time + gate.delay
                                # Avoid scheduling duplicate evaluations
                                key = (gate.output, output_time)
                                if scheduled_gate_evaluations.get(key) != values[input_name]:
                                    heapq.heappush(event_queue, (output_time, 'gate', event_id, gate))
                                    event_id += 1
                                    scheduled_gate_evaluations[key] = values[input_name]
                elif evt_type == 'gate':
                    gate = evt_data[0]
                    # Evaluate gate output
                    output_value = gate.evaluate(values)
                    if values[gate.output] != output_value:
                        values[gate.output] = output_value
                        # Record the output change in the specified format
                        output_lines.append(f"{current_time}, {gate.output}, {output_value}")
                        # Schedule evaluations for gates that use this output
                        for g in self.gates:
                            if gate.output in g.inputs:
                                output_time = current_time + g.delay
                                # Avoid scheduling duplicate evaluations
                                key = (g.output, output_time)
                                if scheduled_gate_evaluations.get(key) != values[gate.output]:
                                    heapq.heappush(event_queue, (output_time, 'gate', event_id, g))
                                    event_id += 1
                                    scheduled_gate_evaluations[key] = values[gate.output]

        # Write the outputs to the output file
        with open(output_file, 'w') as out_file:
            out_file.write("\n".join(output_lines))

        print("\nSimulation results saved to", output_file)

def parse_verilog_file(file_content):
    lines = [line.strip() for line in file_content.split('\n') if line.strip()]

    circuit = None
    for line in lines:
        line = line.split('//')[0].strip()
        if not line:
            continue

        if line.startswith('module'):
            match = re.match(r'module\s+(\w+)\s*\((.*?)\);', line)
            if match:
                circuit_name = match.group(1)
                circuit = Circuit(circuit_name)

        elif line.startswith('input'):
            input_line = line.rstrip(';').replace('input', '').strip()
            input_names = [name.strip() for name in input_line.split(',')]
            for input_name in input_names:
                if input_name not in circuit.inputs:
                    circuit.inputs.append(input_name)

        elif line.startswith('output'):
            output_line = line.rstrip(';').replace('output', '').strip()
            output_names = [name.strip() for name in output_line.split(',')]
            for output_name in output_names:
                circuit.outputs.append(output_name)

        elif line.startswith('wire'):
            wire_line = line.rstrip(';').replace('wire', '').strip()
            wire_names = [name.strip() for name in wire_line.split(',')]
            for wire_name in wire_names:
                circuit.wires.append(wire_name)

        elif any(line.startswith(gate) for gate in GATE_TYPES.keys()):
            parts = line.split()
            gate_type = parts[0]

            delay = 0
            delay_idx = 1
            if parts[1].startswith('#'):
                delay = int(parts[1].strip('#()'))
                delay_idx += 1

            # Get gate instance name (optional)
            if '(' not in parts[delay_idx]:
                delay_idx += 1  # Skip the instance name if present

            ports_str = ' '.join(parts[delay_idx:])
            ports_match = re.match(r'\((.*?)\);', ports_str)
            if ports_match:
                ports = [p.strip() for p in ports_match.group(1).split(',')]
                output_wire = ports[0]
                input_wires = ports[1:]

                gate = Gate(GATE_TYPES.get(gate_type, gate_type), delay, output_wire, input_wires)
                circuit.gates.append(gate)

    return circuit

def parse_stimulus_file(file_content):
    events = []
    for line in file_content.split('\n'):
        line = line.strip()
        if line:
            match = re.match(r'#(\d+)\s+(\w+)=(\d);', line)
            if match:
                time = int(match.group(1))
                input_name = match.group(2)
                value = int(match.group(3))
                events.append((time, input_name, value))
    return events

def main():
    # Keep prompting for the Verilog file until a valid file is provided
    while True:
        v_file_name = input("Enter the name of the .v file (e.g., circuit1.v): ")
        if not os.path.isfile(v_file_name):
            print(f"File '{v_file_name}' not found. Please enter a valid .v file name.")
        else:
            break

    # Keep prompting for the stimulus file until a valid file is provided
    while True:
        stim_file_name = input("Enter the name of the .stim file (e.g., circuit1.stim): ")
        if not os.path.isfile(stim_file_name):
            print(f"File '{stim_file_name}' not found. Please enter a valid .stim file name.")
        else:
            break

    # Automatically generate the output file name
    output_file_name = os.path.splitext(v_file_name)[0] + '.sim'

    # Read the content of the Verilog file
    with open(v_file_name, 'r') as v_file:
        v_content = v_file.read()

    # Read the content of the stimulus file
    with open(stim_file_name, 'r') as stim_file:
        stim_content = stim_file.read()

    # Parse the circuit and events
    circuit = parse_verilog_file(v_content)
    events = parse_stimulus_file(stim_content)

    # Display the circuit details
    circuit.display()

    # Simulate the circuit with the provided events
    circuit.simulate(events, output_file_name)

if __name__ == "__main__":
    main()