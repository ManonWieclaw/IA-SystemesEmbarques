//WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script porte logique ET à deux entrées.
//------------------------------------------------------------------------------------------------------------------------------------------------------------


module and_gate (e1, e2, s);
    input e1;
    input e2;
    output s;

    assign s = e1 & e2;

endmodule
