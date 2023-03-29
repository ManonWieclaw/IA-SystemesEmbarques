#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WIECLAW Manon
# TP IA
# 31.03.2023
#Script permettant de générer un exécutable à partir de modèle de régression logistique.
#------------------------------------------------------------------------------------------------------------------------------------------------------------



import joblib
import numpy as np
import os

model= joblib.load('regression_logistic1.joblib')
is_lr = type(model)
print ("is lr : ", is_lr)                                                                                                                                                                                                                                                                                                                                           

features = [1.43, 33, 120, 79]
n_params = len(features)


def get_coef(model):
    coef = [model.intercept_] + [coef for coef in model.coef_]
    c1 = coef[0]
    c2 = coef[1]
    tabcoef = np.append(c1, c2)
    return (tabcoef)
    

def generate_c_function(model):
    coef = get_coef(model)
    s1 = f"""
        #include <stdio.h>
        #include <stdlib.h>

        float exponentielle(float x, int n_term){{
        
            float factorielle = 1.0;
            float expo = 1.0;
            float puissance = 1.0;

            for (int i=1; i<=n_term; i++){{
                
                puissance *= x;
                factorielle *= i;

                expo += puissance / factorielle;
            }}

            return(expo);

        }}

        float logistic_regression_prediction(float* features, int n_parameters){{
            float coef[] = {{{', '.join(str(c) for c in coef)}}};
            float result = {coef[0]};
    """

    for i in range (n_params):

        s1 += f"result += features[{i}] * {coef[i+1]};"

    s1 += f"""


        //fonction sigmoid :

        float e = exponentielle(-result, 30);
        float sig =  1/(1+e);
        
        if ((sig <0.5) && (sig >= 0)){{
            result = 0;
        }}
        else if ((sig >= 0.5) && (sig <= 1)){{
            result = 1;

        }}
        return result; }}"""

    s1+= f""" 
        \tint main() {{
            float features [{n_params}] = {{{','.join(str(feature) for feature in features)}}};
            int n_parameters  = sizeof(features)/sizeof(float);
            float pred = decision_tree (features, n_parameters);
            if (pred == 0){{
                printf("the machine will not break : %f", pred);

            }}
            else {{
                printf("the machine will break : %f", pred);
            }}

            return 0;
        }}
    
    """
    if os.path.isfile('logistic_regression_prediction.c'):
        os.remove('logistic_regression_prediction.c')
    f = open('logistic_regression_prediction.c', 'w')
    f.write(s1)
    f.close()

generate_c_function(model)

pred = model.predict(np.array(features).reshape(1, -1))
