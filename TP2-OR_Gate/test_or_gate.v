//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script permettant de tester la porte logique OU à deux entrées.
//------------------------------------------------------------------------------------------------------------------------------------------------------------

`timescale 1ns / 1ps
module stimulus;
	// Inputs
	reg x;
	reg y;

	// Outputs
	wire z;

	// Instantiate the Unit Under Test (UUT)
	or_gate uut (
		x, 
		y, 
		z
	);
 
	initial begin
	$dumpfile("test3.vcd");
    $dumpvars(0,stimulus);
		// Initialize Inputs
		x = 0;
		y = 0;
 
	#20 x = 1;
	#20 y = 1;

	#20 y = 0;	
	#20 x = 1;

    #20 y = 1;	
	#20 x = 1;

	#40 ;
 
	end  
 
		initial begin
		 $monitor("t=%3d x=%d,y=%d, z=%d \n",$time,x,y,z);
		 end
 
endmodule
 