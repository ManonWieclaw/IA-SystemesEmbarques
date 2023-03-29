`timescale 1ns / 1ps
module stimulus;
	// Inputs
	reg e1;
	reg e2;
   
	// Outputs
	wire s;
    wire r1;
	// Instantiate the Unit Under Test (UUT)
	operation uut (
		e1, 
		e2, 
		s,
        r1
	);
 
	initial begin
	$dumpfile("test3.vcd");
    $dumpvars(0,stimulus);
		// Initialize Inputs
		e1 = 0;
		e2 = 0;
     
 
	#20 e1 = 1;
	#20 e2 = 1;
   

	#20 e1 = 0;	
	#20 e2 = 0;


	#40 ;
 
	end  
 
		initial begin
		 $monitor("t=%3d e1=%d,e2=%d,s=%d, r1=%d \n",$time,e1,e2,s,r1 );
		 end
 
endmodule
 
 
