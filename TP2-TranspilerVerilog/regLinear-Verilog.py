#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WIECLAW Manon
# TP2 IA
# 31.03.2023
#Script porte logique OU à deux entrées.
#------------------------------------------------------------------------------------------------------------------------------------------------------------



import joblib
import numpy as np
import os

model= joblib.load('regression.joblib')
is_lr = type(model)
print ("is lr : ", is_lr)

#---------------------------------------------------------------------------Récupération des features---------------------------------------------------------

features = []
features_python = []

print ("\nCombien de features souhaitez-vous saisir ?\n")
n_param = int(input())

for i in range (n_param):
    print ("\nfeatures", i, ":" )  
    a = int(input())
    features_python.append(a)
    a = bin(a)[2:].zfill(16)  #features sur 16 bits
    features.append(a)
print (features)

#------------------------------------------------------------------------Récupération des coefficients-----------------------------------------------------------------------


def get_coef(model):

    coef = [model.intercept_] + [coef for coef in model.coef_] 
    print(coef)
    for y in range (len(coef)):
        print("coef y :",coef[y])
        coef[y]=int(coef[y])
        if (coef[y]<0):                     #Si des features sont négatives alors features = 0
            coef[y] = bin(0)[2:].zfill(16)
        elif (coef[y]>65535) :              #Si des features sont supérieurs à 16 bits on les fixe au maximum sur 16 bits
            coef[y]=bin(65535)[2:].zfill(16) 
        elif (coef[y]>=0) :                 
            coef[y]=bin(coef[y])[2:].zfill(16)
    print ("coefficient :", coef)
    return (coef)


#-----------------------------------------------------------------Génération script verilog------------------------------------------------------------------------

def generate_verilog_function(model):
    coef = get_coef(model)

    s1 = f"""
    module add32(e1, e2, r, s, r1);

        input [31:0] e1;
        input [31:0] e2;
        input r; 

        output [31:0] s;
        output r1;
    
    assign  {{r1 ,s}} = e1 + e2 + r;   
    endmodule

    module multiplication16(e1, e2, s);

        input [15:0] e1;
        input [15:0] e2;
     
        output [31:0] s;

        assign  s = e1 * e2 ;  
    endmodule

    """
    s1 += f"""
    module reg_linear(features, predict_result);

        input [15:0] features;
        
        output [31:0] predict_result;
    """
    coef[0]= coef[0].zfill(15)
    s1 += f"""
    
        wire [15:0] theta0 = 16'b{coef[0]};
        wire [31:0] predict0 = theta0;
        wire r0 = 0;
        
    """
    i = 1
    while i<= n_param:
        print(i)
        s1 += f"""
        
        wire [15:0] theta{i} = 16'b{coef[i]};
        wire [15:0] features{i-1} = 16'b{features[i-1]};
        wire [31:0] tmp{i};
        wire [31:0] predict{i};
        wire r{i};

        multiplication16 mul{i}(theta{i}, features{i-1}, tmp{i});
        add32 adder{i}(predict{i-1}, tmp{i}, r{i-1},predict{i}, r{i});

        
        """
        i += 1
    s1 += f"""
    assign predict_result = predict{n_param};
    endmodule
    """

#-----------------------------------------------------------------Génération script testbench----------------------------------------------------------------------------

    s2= f""" 
    `timescale 1ns / 1ps
    module stimulus;
	// Inputs
	reg [15:0] features;
	
   
	// Outputs
    wire [31:0] predict_result;
	

	reg_linear uut (
		features [15:0],  
		predict_result [31:0]	   
	);
 
	initial begin
	$dumpfile("regression.vcd");
    $dumpvars(0,stimulus);

 
		#20;

	end  
 
	initial begin
		 $monitor("t=%3d  estimation : %d euros ",$time, predict_result);
	end
 
endmodule
    """

#------------------------------------------------------------------------------------------------------------------------------------------------------------


    if os.path.isfile('linear_regression_prediction.v'):
        os.remove('linear_regression_prediction.v')
    f = open('linear_regression_prediction.v', 'w')
    f.write(s1)
    f.close()

    if os.path.isfile('test_linear_regression_prediction.v'):
        os.remove('test_linear_regression_prediction.v')
    f = open('test_linear_regression_prediction.v', 'w')
    f.write(s2)
    f.close()

generate_verilog_function(model)

#-----------------------------------------------------------------prédiction python---------------------------------------------------------------------------


pred = model.predict(np.array(features_python).reshape(1, -1))
print("\n prix prédit en py :" + str(pred))