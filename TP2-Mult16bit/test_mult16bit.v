//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script permettant de tester la multiplication de deux nombres de 16 bits.
//------------------------------------------------------------------------------------------------------------------------------------------------------------



`timescale 1ns / 1ps
module stimulus;
	// Inputs
	reg [15:0] e1 ;
	reg [15:0] e2;
   
	// Outputs
	wire [31:0] s;
    
	// Instantiate the Unit Under Test (UUT)
	multiplication16 uut (
		e1 [15:0], 
		e2 [15:0], 
		s [31:0]
        
	);
 
	initial begin
	$dumpfile("mult16bit.vcd");
    $dumpvars(0,stimulus);
		// Initialize Inputs
	e1 = 16'b0000000000000000;
	e2 = 16'b0000000000000000;

	#20 e1 = 16'b0000001010010110;
	#0 e2 = 16'b0000000111000011;
 
	#20 e1 = 16'b1110000010000110;
	#0 e2 = 16'b0001000111000000;
    
    #20 
    #20 e1 = 16'b0100011000000001;
	#20 e2 = 16'b1000000001000010;

    #20 e1 = 16'b1010110000010000;
	#10 e2 = 16'b1100000100010010;
    
	#40 ;
 
	end  
 
	initial begin
        $monitor("t= %3d e1= %b x e2 = %b = %b \n",$time,e1,e2,s);
	end
 
endmodule
 

 
