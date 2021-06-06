# %%codecell
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np

# %% codecell
#leemos el excel y lo pasamos a un DataFrame de pandas
data = pd.read_excel(
    'Set_3-exp_4.xlsx',
)
#limpiamos las columnas

#limpiamos los nombres de las columnas para que sea más fácil usarlas después
data.columns = data.columns.str[:2] #eliminamos las unidades
data.columns = data.columns.str.lower() #pasamos a minusculas
data #vemos nuestro DataFrame

# %% codecell
#pasamos los parametros a un dataframe separado
unidades_parametros = data.iloc[0:4, 2].tolist()
valores_parametros = data.iloc[0:4, 3].tolist()
parametros = pd.DataFrame(
    index=['valores'], columns=unidades_parametros
)
parametros.loc['valores'] = valores_parametros
#limpiamos los nombres de las columnas
parametros.columns = parametros.columns.str[:-6]
parametros.columns = parametros.columns.str.strip('(')
parametros.columns = parametros.columns.str.strip()

#Y limpiamos el DataFrame
data = data.drop(index=[0,1,2,3,4])
data = data.dropna(how='any', axis=1) #borramos las columnas vacias

#elegimos la primera fila como los nombres de las columnas
nuevas_col = data.iloc[0].tolist()[1:]
#borramos la fila de que contenía los nombres de las columnas
data = data.drop(index=data.index[0], axis=0)
nuevas_col = [''] + nuevas_col
data.columns = nuevas_col

#Y la primera columna como los indices
data = data.set_index(keys='')
data.index.name = 'pos' #la columna de los indices indica la posicion

data.columns = data.columns.str[:-4] #eliminamos las unidades
data.columns = data.columns.str.strip()

display(data)
display(parametros)

# %%codecell
