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

#%%codecell
#punto de cambio de modo
punto_de_cambio = data.loc[50:]['potencia'].idxmin()
print(punto_de_cambio)


#%%codecell
#calculo de trabajo (heat pump)
trabajo = 0
for index, row in data.iterrows():
    trabajo += 0.05 * row['potencia']
    if index == 86: break

print(trabajo)

#%%codecell
#calculo de calor (heat pump)
e_lost = list()
potencia_acumulada = 0
for index, row in data.iterrows():
    potencia_acumulada += row['potencia']
    calor_perdido = row['q_hot_p'] - (row['q_cold_p'] + 0.05 * potencia_acumulada)
    e_lost.append(calor_perdido)

data.insert(len(data.columns), 'e_lost', e_lost)
print(data.at[86, 'q_hot_p'])
print(data.at[86, 'q_cold_p'] + trabajo)
print(data.at[86, 'e_lost'])
print(data.at[86, 'q_cold_p'] + trabajo + data.at[86, 'e_lost'])
data

#%%codecell
#calculo de trabajo (maquina termica)
trabajo_maquina = list()
for index, row in data.iterrows():
    trabajo_t = row['q_hot'] - row['q_cold']
    if index < 86.05: trabajo_t = 0
    trabajo_maquina.append(trabajo_t)
data.insert(len(data.columns), 'w_maq', trabajo_maquina)
print(data.at[218.8, 'w_maq'])
print(9.050000000000011 / 90.78600446949991)
print(1 - data.at[218.8, 'q_cold'] / data.at[218.8, 'q_hot'])
#%%codecell
