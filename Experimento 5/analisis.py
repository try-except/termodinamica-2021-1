# %%codecell
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% codecell
#leemos el excel y lo pasamos a un DataFrame de pandas
data = pd.read_excel(
    'set3-1.xlsx',
    index_col = 0
)
#limpiamos las columnas
data = data.dropna(how='any', axis=1)
data.index.name = 't'

#limpiamos los nombres de las columnas para que sea más fácil usarlas después
nuevas_col = [
'corriente',
'voltaje',
'potencia',
'temp',
'q_cold',
'q_cold_p',
'temp_h',
'q_hot_p',
'q_hot'
]

data.columns = nuevas_col

data

# %%codecell
keys = ['potencia', 'voltaje', 'corriente', 'temp', 'temp_h']
key_titles = {
    'potencia' : 'Potencia',
    'voltaje' : 'Voltaje',
    'corriente' : 'Corriente',
    'temp' : 'Temperatura 1',
    'temp_h' : 'Temperatura 2'
}
key_units = {
    'potencia' : 'W',
    'voltaje' : 'V',
    'corriente' : 'A',
    'temp' : '°C',
    'temp_h' : '°C'
}

for key in keys:
    fig, ax = plt.subplots()
    plt.title(f'{key_titles[key]} vs Tiempo')
    plt.ylabel(f'{key_titles[key]} (${key_units[key]}$)')
    plt.xlabel('Tiempo ($s$)')
    ax.plot(data.index, data[key], 'bo-')

    plt.savefig(f'{key}_tiempo', dpi=300, bbox_inches = 'tight')
    plt.show()
