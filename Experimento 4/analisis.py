# %%codecell
import pandas as pd

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
#pasamos los parametros a variables
d_p = 32.5 #mm
m_pi_pla = 35 #g
p_atm = 101325 #Pa
m_cuerpo = 100.26 #g

#Y limpiamos el DataFrame
data.drop(index=[0,1,2,3,4], inplace=True)
data = data.dropna(how='any', axis=1) #borramos las columnas vacias

#elegimos la primera fila como los nombres de las columnas
data.columns = data.iloc[0]
#Y la primera columna como los indices
data = data.set_index(keys='Posición')

#borramos la fila de que contenía los nombres de las columnas
data.drop(index=data.index[0],
        axis=0,
        inplace=True)

data.columns = data.columns.str[:-4] #eliminamos las unidades
data.columns = data.columns.str.strip()

data
