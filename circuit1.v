module circuit_1(a, b, o);
input a;
input b;

output o;

wire w;
and #(5) g0 (w, a, b);
buf #(2) g1 (o, w);
endmodule;
