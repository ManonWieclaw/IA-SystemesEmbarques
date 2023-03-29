#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WIECLAW Manon
# TP IA
# 31.03.2023
#Script permettant de générer un exécutable à partir de modèle de régrEssion linéaire, logistique et d'arbre de décision.
#------------------------------------------------------------------------------------------------------------------------------------------------------------

import joblib
import numpy as np
import os

print("\n")
print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
print("\n")
print ("Quel est le nom du fichier joblib de votre modele (sans le .joblib) ?")

print("\n")
print ("Les fichiers joblib pouvant être utilises sont : \n- regression_decisionTree.joblib \n- classification_decisionTree.joblib \n- regression_logistic1.joblib \n- regressionlinear.joblib\n")
print("\n")
print("Nom du fichier : ")
print("\n")

name = input()

file = name + '.joblib'

#chargement du modèle
model= joblib.load(file)
type = type(model)
print ("\nType du modele : ", type)
print (type)
print("\n")

if ("LinearRegression" in str(type)):
    type_model = 1
    print("\n--------------Linear regression model----------------\n")
    
elif ("logistic" in str(type)):
    type_model = 2
    print("\n--------------Logistic regression model---------------\n")

elif ("Tree" in str(type)):
    type_model = 3
    print("\n-------------------Decison Tree-----------------------\n")

is_classification = 0
if (type_model == 3) :
    print ("quelle est le type d'arbre de décision ? \n 0 pour regression \n 1 pour classification")
    is_classification = int(input())
    while (is_classification != 1 and is_classification != 0):
        print("saisir 1 ou 0")
        is_classification = int(input())

#--------------------definition des features-----------------------------------------------------------------------------------------------------------------

features = []

print ("\nCombien de features souhaitez-vous saisir ?\n (4 pour la regression logistique et l'arbre de decision 3 pour la regression lineaire)")
n_param = int(input())

if (type_model == 1) & (n_param !=3):
    while n_param !=3 :
        print ("\nVeuillez saisir le nombre de features correspondant au fichier csv 'houses.csv' (3 features)")
        n_param = int(input())

if (type_model == 3) & (n_param !=3) & (is_classification == 0):
    while n_param !=3 :
        print ("\nVeuillez saisir le nombre de features correspondant au fichier csv 'houses.csv' (3 features)")
        n_param = int(input())
    
if ((type_model == 2) & (n_param !=4)):
    while (n_param !=4) :
        print ("\nVeuillez saisir le nombre de features correspondant au fichier csv 'predictive_maintenance.csv' (4 features)")
        n_param = int(input())

if (type_model == 3) & (n_param !=4) & (is_classification == 1):
    while (n_param !=4) :
        print ("\nVeuillez saisir le nombre de features correspondant au fichier csv 'predictive_maintenance.csv' (4 features)")
        n_param = int(input())

for i in range (n_param):
    print ("\nfeatures", i, ":" )  
    a = input()
    features.append(float(a))
print("\nles features sont :")
print("\n")
print (features)

   

#------------------------------------------------coefficients----------------------------------------------------------------------------------------------------

def get_coef(model):
    coef = [model.intercept_] + [coef for coef in model.coef_]
    print ("coefficient :", coef)
    return (coef)

#------------------------------------------Récupération données des arbres de décisions---------------------------------------------------------------------------------------------------- 
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

#---------------------------------------------------transpile decision tree--------------------------------------------------------------------------------

def generate_c_function_decisiontree(model):
    feature = get_(model, 1)
    threshold = get_(model, 2)
    children_left = get_(model,3)
    children_right = get_(model, 4)
    values = get_value(model)

    s1 = f"""
        #include <stdio.h>

        #include <stdlib.h>

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
    """
    
    if (is_classification == 1):
        s1 += f"""float result;
            if (r <= 0.5) {{
                result = 0;
            }}
            else  {{
                result = 1;
            }}

            return result;
        }}
    """
    else :
         s1 += f"""return r; 
        }}
        """
    if (is_classification == 1):
        s1 += f"""int main() 
        {{
            float features [{n_param}] = {{{','.join(str(feature) for feature in features)}}};
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
    else : 
        s1 += f"""int main() 
        {{
            float features [{n_param}] = {{{','.join(str(feature) for feature in features)}}};
            int n_parameters  = sizeof(features)/sizeof(float);
            float pred = decision_tree (features, n_parameters);
            printf("Prix estime : %f", pred);
            return 0;
        }}
        """
    return(s1)
#--------------------------------------------------------transpile linear regression-----------------------------------------------------------------------

def generate_c_function_linear(model):

    coef = get_coef(model)
    #features = get_features(type_model)
    #n_param = len(features)
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
    return s1

#-----------------------------------------------------------------transpile logistic regression-----------------------------------------------------------

def generate_c_function_logistic(model):

    coef = get_coef(model)
    c1 = coef[0]
    c2 = coef[1]
    coef = np.append(c1, c2)

    #features = get_features(type_model)
    #n_param = len(features)
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

    for i in range (n_param):

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
        int main() {{
            float features [{n_param}] = {{{','.join(str(feature) for feature in features)}}};
            int n_parameters  = sizeof(features)/sizeof(float);
            float pred = logistic_regression_prediction(features, n_parameters);
            printf("Did break : %f", pred);
            return 0;
        }}
    """
    return s1
#-------------------------------------------------creation du script c-----------------------------------------------------------------------------------------------

if (type_model == 1):
    s1 = generate_c_function_linear(model)
    name = 'linear_regression_prediction'
    name_c = 'linear_regression_prediction.c'
    pred = model.predict(np.array(features).reshape(1, -1))
    print("\n prix de la maison estime :" + str(pred))

elif (type_model == 2):
    s1 = generate_c_function_logistic(model)
    name = 'logistic_regression_prediction'
    name_c = 'logistic_regression_prediction.c'
    pred = model.predict(np.array(features).reshape(1, -1))
    if (pred == 0):
        print("\n the machine will not break :" + str(pred)) 
    else : 
        print("\n the machine will break :" + str(pred)) 


elif (type_model == 3): 
    
    if (is_classification == 1):
    
        s1 =generate_c_function_decisiontree(model)
        name = 'classification_decision_tree_prediction'
        name_c = 'classification_decision_tree_prediction.c'
        pred = model.predict(np.array(features).reshape(1, -1))
        if (pred == 0):
            print("\n the machine will not break :" + str(pred)) 
        else : 
            print("\n the machine will break :" + str(pred)) 


    else : 
        s1 =generate_c_function_decisiontree(model)
        name = 'regression_decision_tree_prediction'
        name_c = 'regression_decision_tree_prediction.c'
        pred = model.predict(np.array(features).reshape(1, -1))
        print("\n prix de la maison estime :" + str(pred))

if os.path.isfile(name_c):
    os.remove(name_c)

f = open(name_c, 'w')
f.write(s1)
f.close()

print ("\nnom du fichier genere : ", name_c)

print ("\nPour executer le fichier c vous devez saisir dans l'invite de commande :")
print ('- la commande : gcc -o', name , name_c )
print ("- lancer l'executable genere:", name,".exe")

print("\n")
print("-----------------------------------------------------------------------------------------------------------------------------------------------------")

