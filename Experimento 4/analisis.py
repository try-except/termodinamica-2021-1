# %%codecell
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
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
fig, ax = plt.subplots()
iterator = data.iterrows()
row = next(iterator)
plt.title('Diagrama $Masa/Altura$ del experimento')
plt.xlabel('Masa $(g)$')
plt.ylabel('Altura $(mm)$')
for _ in range(len(data) - 1):
    h1, m1 = row[1]
    n1 = row[0]
    row = next(iterator)
    h2, m2 = row[1]
    n2 = row[0]
    coordsA = 'data'
    coordsB = 'data'
    con = ConnectionPatch((m1, h1), (m2, h2), coordsA, coordsB,
                      arrowstyle="-|>", shrinkA=5, shrinkB=5,
                      mutation_scale=20, fc="w")
    ax.plot([m1, m2], [h1, h2], 'bo')
    ax.text(
        m1 + 1, h1 + 0.2, n1,
        verticalalignment='bottom', horizontalalignment = 'left',
        fontsize=12, fontweight = 'bold'#, fontfamily = 'serif'
    )
    ax.add_artist(con)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig('graf_ma', dpi=300, bbox_inches='tight')
plt.show()

# %% codecell
volumenes, presiones = list(), list()
for index, row in data.iterrows():
    #volumenes
    radio = (parametros.at['valores', 'd_p'] / 1000) / 2
    area_base = np.pi * radio**2
    volumen = area_base * (data.at[index, 'h'] / 1000)
    presion = ((data.at[index, 'masa'] / 1000) * 9.81) / area_base
    presion += parametros.at['valores', 'p_atm']
    volumenes.append(volumen)
    presiones.append(presion)
data.insert(2, 'V', volumenes) # m^3
data.insert(3, 'P', presiones) #Pa
data

# %% codecell
fig, ax = plt.subplots()
iterator = data.iterrows()
row = next(iterator)
plt.title('Diagrama $P/V$ del experimento')
plt.xlabel('Presion ($Pa$)')
plt.ylabel('Volumen ($10^{-5}m^3$)')
for _ in range(len(data) - 1):
    v1, p1 = row[1][2:]
    n1 = row[0]
    row = next(iterator)
    v2, p2 = row[1][2:]
    n2 = row[0]
    coordsA = 'data'
    coordsB = 'data'
    con = ConnectionPatch((p1, v1), (p2, v2), coordsA, coordsB,
                      arrowstyle="-|>", shrinkA=5, shrinkB=5,
                      mutation_scale=20, fc="w")
    plt.plot([p1, p2], [v1, v2], 'bo')
    ax.text(
        p1 + 20, v1, n1[:1],
        verticalalignment='bottom', horizontalalignment = 'left',
        fontsize=12, fontweight = 'bold'#, fontfamily = 'serif'
    )
    ax.add_artist(con)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig('graf_pv', dpi=300, bbox_inches = 'tight')
plt.show()
