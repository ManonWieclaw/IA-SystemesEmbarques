//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script porte logique ET à trois entrées.
//------------------------------------------------------------------------------------------------------------------------------------------------------------



module and_gate3 (e1, e2, e3, s);
    input e1;
    input e2;
    input e3;
    output s;

    assign s = e1 & e2 & e3;

endmodule
