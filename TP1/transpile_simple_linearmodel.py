#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WIECLAW Manon
# TP IA
# 31.03.2023
#Script permettant de générer un exécutable à partir d'un modèle de régression linéaire.
#------------------------------------------------------------------------------------------------------------------------------------------------------------




import joblib
import numpy as np
import os

model= joblib.load('regressionlinear.joblib')
is_lr = type(model)
print ("is lr : ", is_lr)

features = [194.4, 2, 1]
n_param = len(features)


def get_coef(model):
    coef = [model.intercept_] + [coef for coef in model.coef_]
    print ("coefficient :", coef)
    return (coef)
    

def generate_c_function(model):
    coef = get_coef(model)
    s1 = f"""
        #include <stdio.h>
        #include <stdlib.h>

        float linear_regression_prediction (float* features, int n_parameters){{
            float result = {coef[0]};
    """

    for i in range (n_param):

        s1 += f" result += features[{i}] * {coef[i+1]};"

    s1 += f"\nreturn result; }}"

    s1+= f""" 
        \tint main() {{
            float features [{n_param}] = {{{','.join(str(feature) for feature in features)}}};
            int n_parameters  = sizeof(features)/sizeof(float);
            float pred = linear_regression_prediction (features, n_parameters);
            printf("Prix estime : %f", pred);
            return 0;
        }}
    
    """
    if os.path.isfile('linear_regression_prediction.c'):
        os.remove('linear_regression_prediction.c')
    f = open('linear_regression_prediction.c', 'w')
    f.write(s1)
    f.close()

generate_c_function(model)

pred = model.predict(np.array(features).reshape(1, -1))
print("\n prix prédit en py :" + str(pred))