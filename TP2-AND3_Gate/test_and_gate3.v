//------------------------------------------------------------------------------------------------------------------------------------------------------------
// WIECLAW Manon
// TP2 IA
// 31.03.2023
//Script permettant de tester la porte logique ET à trois entrées.
//------------------------------------------------------------------------------------------------------------------------------------------------------------

`timescale 1ns / 1ps
module stimulus;
	// Inputs
	reg x;
	reg y;
    reg v;
	// Outputs
	wire z;
	// Instantiate the Unit Under Test (UUT)
	and_gate3 uut (
		x, 
		y, 
        v,
		z
	);
 
	initial begin
	$dumpfile("test3.vcd");
    $dumpvars(0,stimulus);
		// Initialize Inputs
		x = 0;
		y = 0;
        v = 0;
 
	#20 x = 1;
	#20 y = 1;
    #20 v = 0;

	#20 y = 0;	
	#20 x = 1;
    #20 v = 1;	

    #20 y = 1;	
	#20 x = 1;
    #20 v = 1;	

	#40 ;
 
	end  
 
		initial begin
		 $monitor("t=%3d x=%d,y=%d,v=%d, z=%d \n",$time,x,y,v,z, );
		 end
 
endmodule
 
 
