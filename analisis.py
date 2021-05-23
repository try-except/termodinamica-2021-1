#This is a hidrogen notebook
# %% codeblock
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% codecell
#leemos el excel y lo pasamos a un DataFrame de pandas
data = pd.read_excel(
    'Set 1_exp3-1.xlsx',
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
gammas, moles, ceves, cepes = list(), list(), list(), list()
R = 8.314472 # joule / mol kelvin
patm = 101325 #pascal
vol = 0.01 #m3
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
#graficos de cada repeticion
for i, row in data.iterrows():
    plt.figure(figsize=(10, 7))
    plt.title(f'Gráfico P/V para la repeticion {i}')
    plt.xlabel('Volumen ($m^3$)')
    plt.ylabel('Presión ($kPa$)')

    vol = np.linspace(1, 10, 100) #rango de ploteo
    #primer grafico
    #n*T*R / v = P
    curva1 = (data.at[i, 'moles'] * (data.at[i, 't1'] + 273)  * R) \
    / (vol**data.at[i, 'gamma'] * 1000) #multiplicamos por 1000 para pasar a kPa
    curva2 = (data.at[i, 'moles'] * (data.at[i, 't2'] + 273) * R) \
    / (vol**data.at[i, 'gamma'] * 1000)

    plt.plot(vol, curva1, 'r')
    plt.plot(vol, curva2, 'b')
    '''
    Estos gráficos son muy poco útiles, porque la diferencia de temperatura es
    muy pequeña, por lo que las presiones son casi iguales. Si se cambia el rango
    a `vol = np.linspace(3.9, 4, 100)`, el gráfico 1 sigue con las curvas casi pegadas.
    '''

    plt.savefig(f"graf_{i}", dpi=300, bbox_inches='tight')

# %%codecell
#grafico con gammas inventadas
plt.figure(figsize=(10, 7))
plt.title('Gráfico $P/V$')
plt.xlabel('Volumen ($m^3$)')
plt.ylabel('Presión ($kPa$)')

plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False, # labels along the bottom edge are off
    left=False,        # ticks along the left edge are off
    right=False,       # ticks along the right edge are off
    labelleft=False    # labels along the left edge are off
)
vol = np.linspace(1, 4, 100) #rango de ploteo
#primer grafico (n*T*R / v = P)
#curvas
curva1 = (data.at[2, 'moles'] * (data.at[2, 't1'] + 273)  * R) \
/ (vol**1.4 * 1000) #multiplicamos por 1000 para pasar a kPa
curva2 = (data.at[2, 'moles'] * (data.at[2, 't2'] + 273) * R) \
/ ((vol+1)**1.4 * 1000) #para obligar a la curva a separarse, alteramos el volumen

#puntos
punto1x, punto1y = 2, (data.at[2, 'moles'] * (data.at[2, 't1'] + 273)  * R) \
/ (2**1.4 * 1000)
punto2x, punto2y = 3, (data.at[2, 'moles'] * (data.at[2, 't2'] + 273)  * R) \
/ (4**1.4 * 1000)

#ploteamos
plt.plot(vol, curva1, 'r', label='$T_1$')
plt.plot(vol, curva2, 'b', label='$T_2$')
plt.plot(
    [punto1x], [punto1y],
    marker='o', markersize=5,
    color="black",
    zorder=3 #zorder controla que el punto esté sobre la curva y no detrás
)
plt.plot(
    [punto2x], [punto2y],
    marker='o', markersize=5,
    color="black",
    zorder=3 #zorder controla que el punto esté sobre la curva y no detrás
)

plt.legend(loc="upper right")
plt.savefig(f"graf_inventado", dpi=300, bbox_inches='tight')
