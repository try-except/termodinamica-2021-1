#This is a hidrogen notebook
# %% codeblock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% codecell
data = pd.read_excel(
    '/home/try_except/Documents/termo/Exp3/Set 1_exp3-1.xlsx',
    header=1,
    index_col=1
)
#limpiamos las columnas
data = data.dropna(how='any', axis=1)
data.index.name = 'rep'
data.columns = data.columns.str[:2]
data.columns = data.columns.str.lower()
data

# %%codecell
gammas, moles, ceves, cepes = list(), list(), list(), list()
R = 8.314472 # joule / mol kelvin
patm = 101325 #pascal
vol = 0.01 #m3
for index, row in data.iterrows():
    #gammas
    gam = row['h1'] / (row['h1'] - row['h2'])
    gammas.append(gam)
    #moles
    mol =  patm * vol / (R * (row['t2'] + 273))
    moles.append(mol)
    #cv
    cv = mol * R / (gam - 1)
    ceves.append(cv)
    #cp
    cp = gam * mol * R / (gam - 1)
    cepes.append(cp)
data.insert(4, 'gamma', gammas)
data.insert(5, 'moles', moles)
data.insert(6, 'cv', ceves)
data.insert(7, 'cp', cepes)

data

# %%codecell
#graficos de cada repeticion
for i, row in data.iterrows():
    plt.figure(figsize=(10, 7))
    plt.title(f'Gráfico P/V para la repeticion {i}')
    plt.xlabel('Volumen ($m^3$)')
    plt.ylabel('Presión ($kPa$)')

    vol = np.linspace(1, 10, 100)
    #primer grafico
    curva1 = (data.at[i, 'moles'] * (data.at[i, 't1'] + 273)  * R) \
    / (vol**data.at[i, 'gamma'] * 1000)
    curva2 = (data.at[i, 'moles'] * (data.at[i, 't2'] + 273) * R) \
    / (vol**data.at[i, 'gamma'] * 1000)

    plt.plot(vol, curva1, 'r')
    plt.plot(vol, curva2, 'b')

    plt.savefig(f"graf_{i}", dpi=300, bbox_inches='tight')

# %%codecell
plt.figure(figsize=(20,10))

vol = np.linspace(1, 10, 100)
curva1 = (data.at[1, 'moles'] * 20 * R) / vol**data.at[1, 'gamma']
curva2 = (data.at[1, 'moles'] * 50 * R) / vol**data.at[1, 'gamma']

plt.plot(vol, curva1, 'r')
plt.plot(vol, curva2, 'b')
plt.show()
