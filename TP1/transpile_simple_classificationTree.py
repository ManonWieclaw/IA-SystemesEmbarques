#------------------------------------------------------------------------------------------------------------------------------------------------------------

# WIECLAW Manon

# TP IA

# 31.03.2023

#Script permettant de générer un exécutable à partir de modèle d'arbre de décision.

#------------------------------------------------------------------------------------------------------------------------------------------------------------





import joblib

import numpy as np

import pandas as pd

import os



print ("Decision Tree")

model= joblib.load('classification_decisionTree.joblib')



features = [0.75, 12, 132, 79]

n_params = len(features)



def get_value(model):
    tab= "{"
    temp = [coef for coef in model.tree_.value]

    for i in range (len(temp)-1):
        tab = tab + str(temp[i][0][0]) + ','
    tab += str(temp[(len(temp) - 1)][0][0]) + "}"

    return tab  

def get_(model, type):

    tab= "{"
    if type == 1:
        temp = [coef for coef in model.tree_.feature]
    elif type == 2:
        temp = [coef for coef in model.tree_.threshold]
    elif type == 3:
        temp = [coef for coef in model.tree_.children_left]
    elif type == 4:
        temp = [coef for coef in model.tree_.children_right]


    for i in range (len(temp)-1):
        tab = tab + str(temp[i]) + ','
    tab += str(temp[(len(temp) - 1)]) + "}"

    return tab  



def generate_c_function(model):
    feature = get_(model, 1)
    threshold = get_(model, 2)
    children_left = get_(model,3)
    children_right = get_(model, 4)
    values = get_value(model)

    
    print(values)
    print(feature)
    print(threshold)
    print(children_left)
    print(children_right)

    s1 = f"""
        #include <stdio.h>

        #include <stdlib.h>

         /*float exponentielle(float x, int n_term){{
        
            float factorielle = 1.0;
            float expo = 1.0;
            float puissance = 1.0;

            for (int i=1; i<=n_term; i++){{
                
                puissance *= x;
                factorielle *= i;

                expo += puissance / factorielle;
            }}

            return(expo);

        }}*/
        float decision_tree (float* features, int n_parameters)  
        {{
            int feature[] = {feature};
            float threshold[] = {threshold};
            int children_left[] = {children_left};
            int children_right[] = {children_right};
            float values[] = {values};


            int new_node = 0;
            int node = 0;

        while(feature[new_node]>=0)
        {{
            node = new_node;
            if(features[feature[new_node]] <= threshold[new_node])
            {{
                new_node= children_left[node];
            }}
            else
            {{
                new_node= children_right[node];
            }}
        }}
        
        float r = values[new_node];
        float result;
        if (r <= 0.5) {{
            result = 0;
        }}
        else  {{
            result = 1;
        }}
        //fonction sigmoid :

        /*float e = exponentielle(-result, 30);
        float sig =  1/(1+e);
        
        if ((sig <0.5) && (sig >= 0)){{
           result = 0;
        }}
        else if ((sig >= 0.5) && (sig <= 1)){{
            result = 1;

        }}*/
        return result; }}
        """

    s1 += f"""int main() 
        {{
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


    if os.path.isfile('tree_classification_prediction.c'):

        os.remove('tree_classification_prediction.c')

    f = open('tree_classification_prediction.c', 'w')

    f.write(s1)

    f.close()



generate_c_function(model)



pred = model.predict(np.array(features).reshape(1, -1))

if (pred == 0):
    print("\n the machine will not break :" + str(pred)) 
else : 
    print("\n the machine will break :" + str(pred)) 
