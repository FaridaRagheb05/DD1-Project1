module circuit_4(a, b, c, o);
input a;
input b;
input c;

output o;

wire w1, w2, w3;
and #(5) g0 (w1, a, b);
not #(2) g1 (w2, c);
or #(3) g2 (w3, w1, w2);
buf #(2) g3 (o, w3);
endmodule;
