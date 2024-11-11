module test10(x,y,z,f,o);
input x;
input y;
input z;
        
output o;
output f;
        
wire w1, w2, w3, w4;

xor #(6) g1 (w1, x, y);
and #(7) g2 (w2, x, y);
and #(8) g3 (w3, w1, z);
or #(6) g4 (f, w2, w3);
xor #(6) g5 (o, w1, z);
        
endmodule; 