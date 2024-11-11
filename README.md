# DD1-Project1
Event-driven logic circuit simulator
Project Requirements and Purpose: 
Introduction
A simulator allows users to create a virtual representation of a digital circuit and observe its behavior under
different conditions without physically building the circuit. There are a few ways to construct a logic circuit
simulator. An event-driven logic simulator models the behavior of digital circuits based on events. In digital
circuits, events occur when signals change their logical states. The simulator processes these events and
updates the circuit accordingly. This approach is beneficial for simulating the dynamic behavior of digital
systems where changes happen discretely in response to specific triggers. To demonstrate the idea,
consider the following circuit, which has three inputs A, B, and C, and the output Y, and four gates, G0, an
inverter with C as the input and w1 as the output, G1, an AND gate with A and w1 as its inputs and w2 as
its output, G2, an AND gate, with B and C as its inputs, and w3 as its output, and finally, G3, an OR gate
with w2 and w3 as its inputs, and Y as its output:
Initially, inputs A, B, and C are set to "0"; accordingly, the output, Y, is at "0". The output will never change
unless the inputs change. We refer to this change at the input as an event. This event will cause a series
of other events (the change of the outputs of the circuit gates), and finally, the circuit output, Y, changes.
To elaborate on this, assume that the event we have on the input is the change of A from "0" to "1" (A:
0→1). This event will cause the change of w2 after the delay of G1, say 1ns. The change of w1 is an event
(w2: 0→1), which in turn will cause the change of Y to "1" after the delay of G3. The change of Y is also an
event (Y: 0→1). After the change of Y, there will be no more events, and Y stays at "1" till an event happens
at the input.
The Project
The purpose of this project is to build an event-driven logic circuit simulator satisfying the following
requirements:
1) The simulator accepts two input files:
a. The circuit, a Verilog file (.v) that describes the circuit using the Verilog primitives: and, or,
xor, nand, nor, xnor, buf, & not.
b. The stimuli file (.stim) which gives the events happening on the circuit’s inputs.
When the simulation is done, the simulator outputs the simulation file (.sim)
2) The stimuli file lists the external events (stimuli) applied to the inputs using the following format:
#<delay in ps> <input>=<logic_value> ;
An example of the file content is given below:
#0 A=0;
#0 B=0;
#0 C=1;
#500 A=1;
#800 B=1;
#1300 C=1;
.
.
3) The simulation file (.sim) contains the simulation output by recording the events on an input, an
output, or a wire. An event is recorded by storing the time stamp and the new value. An example
of such a file is given below:
500, A, 1
700, w2, 1
800, B, 1
900, Y, 1
