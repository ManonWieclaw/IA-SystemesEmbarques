module operation(e1, e2, s, r1);

    input e1;
    input e2;
    output s;
    output r1;

    assign r1 = (e1 & e2); 
    assign s = e1 ^ e2;


endmodule

