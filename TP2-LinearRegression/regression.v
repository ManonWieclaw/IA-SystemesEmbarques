//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script permettant d'effectuer la régréssion linéaire suivantes : 10 000 + 5 000 x size.
//------------------------------------------------------------------------------------------------------------------------------------------------------------


module add32(e1, e2, r0, s, r1);

    input [31:0] e1;
    input [31:0] e2;
    input r0; 

    output [31:0] s;
    output r1;
    
   assign  {r1 ,s} = e1 + e2 + r0;   
endmodule

module multiplication16(e1, e2, s);

    input [15:0] e1;
    input [15:0] e2;
     
    output [31:0] s;

    assign  s = e1 * e2 ;  
endmodule

module and_gate(e1, e2, s);

    input e1;
    input e2;
    output s;

    assign s = e1 || e2;
endmodule

module reg_linear(features, n_param, r0, predict, r);

    input [15:0] features;
    input [7:0] n_param; 
    input r0; 

    output [31:0] predict;
    output r;

    wire [15:0] theta1 = 16'b1001110001000; //5 000
    wire [31:0] theta0 = 32'b00000000000000000010011100010000; //10 000
    wire [31:0] tmp1;
    
    multiplication16 mul1(features, theta1, tmp1);
    add32 adder1(theta0, tmp1, r0, predict, r);

endmodule