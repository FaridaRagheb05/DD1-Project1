module circuit_2(a, b, o);
input a;
input b;

output o;

wire w;
or #(5) g0 (w, a, b);
not #(2) g1 (o, w);
endmodule;
