#This is a hidrogen notebook
# %% codeblock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% codecell
#leemos el excel y lo pasamos a un DataFrame de pandas
data = pd.read_excel(
    'Experimento 3\Set 1_exp3-1.xlsx',
    header=1,
    index_col=1
)
#limpiamos las columnas
data = data.dropna(how='any', axis=1)
data.index.name = 'rep' #la columna de los indices indica la repeticion

#limpiamos los nombres de las columnas para que sea más fácil usarlas después
data.columns = data.columns.str[:2] #eliminamos las unidades
data.columns = data.columns.str.lower() #pasamos a minusculas
data #vemos nuestro DataFrame

# %%codecell
#obtención de valores para cada repetición
gammas, moles, ceves, cepes = list(), list(), list(), list()
R = 8.314472 # joule / mol kelvin
patm = 101325 # pascal
vol = 0.01 # m3
for index, row in data.iterrows():
    #gammas
    gam = row['h1'] / (row['h1'] - row['h2'])
    gammas.append(gam)
    #moles
    mol =  patm * vol / (R * (row['t2'] + 273)) #sumamos 273 para pasar a Kelvin
    moles.append(mol)
    #cv
    cv = mol * R / (gam - 1)
    ceves.append(cv)
    #cp
    cp = gam * mol * R / (gam - 1)
    cepes.append(cp)
#insertamos las columnas al DataFrame
data.insert(4, 'gamma', gammas)
data.insert(5, 'moles', moles)
data.insert(6, 'cv', ceves)
data.insert(7, 'cp', cepes)

data


# %%codecell
#calculo de promedios
data.loc[4] = [
    None, None, None, None, # los promedios de h1, h2, t1 y t2 no nos interesan
    data['gamma'].mean(), # promedio del indice adiabatico
    data['moles'].mean(),  # promedio de moles
    data['cv'].mean(),  # promedio de la capacidad calorífica a vol. constante
    data['cp'].mean() # promedio de la capacidad calorífica a presión constante
]
as_list = data.index.tolist()
idx = as_list.index(4)
as_list[idx] = 'promedio'
data.index = as_list

data # visualizamos

# %%codecell
# pasamos la tabla a LaTeX para incluirla en el documento
print(data.to_latex(decimal=','))
