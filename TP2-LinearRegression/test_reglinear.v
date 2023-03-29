//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script permettant de tester la régréssion linéaire suivantes : 10 000 + 5 000 x size.
//------------------------------------------------------------------------------------------------------------------------------------------------------------


`timescale 1ns / 1ps
module stimulus;
	// Inputs
	reg [15:0] features = 16'b0000000000000000;
	reg [7:0] n_param = 8'b00000000;
    reg r0;
   
	// Outputs
    wire [31:0] predict;
	wire r;

	// Instantiate the Unit Under Test (UUT)
	reg_linear uut (
		features [15:0], 
		n_param [7:0],
		r0, 
		predict [31:0],
		r    
	);
 
	initial begin
	$dumpfile("regression.vcd");
    $dumpvars(0,stimulus);
		// Initialize Inputs
		features = 16'b0000000000000000;
		n_param = 8'b00000000;
        r0 = 0;
 
		#20;

		features = 16'b0000000011111010; //250
		n_param = 8'b00000001; //1 seul paramètre

		#20;

 
	end  
 
	initial begin
		 $monitor("t=%3d taille de la maison=%d, n_param=%d, estimation : %d euros  \n",$time,features,n_param, predict);
	end
 
endmodule