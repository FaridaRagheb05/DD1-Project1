module circuit_3(a, b, c, o);
input a;
input b;
input c;

output o;

wire w1, w2;
and #(5) g0 (w1, a, b);
or #(3) g1 (w2, w1, c);
buf #(2) g2 (o, w2);
endmodule;
