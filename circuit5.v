module circuit_5(a, b, c, d, o);
input a;
input b;
input c;
input d;

output o;

wire w1, w2, w3, w4;

and #(5) g0 (w1, a, b);
or #(3) g1 (w2, b, c);
nand #(7) g2 (w3, w1, d);
xor #(1) g3 (w4, w2, w3);
buf #(2) g4 (o, w4);
endmodule;
