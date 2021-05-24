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
#calculo de gamma promedio
gamma_prom = data['gamma'].mean()
print(gamma_prom)

# %%codecell
#grafico promedio
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
vol = np.linspace(0.001, 0.01, 100) #rango de ploteo

moles = data['moles'].mean()
t1 = data['t1'].mean() + 273
t2 = data['t2'].mean() + 273
gamma = data['gamma'].mean()
#curvas
curva1 = (moles * t1  * R) / (vol * 1000) #multiplicamos por 1000 para pasar a kPa
curva2 = (moles * t2  * R) / ((vol + 0.001) * 1000) #multiplicamos por 1000 para pasar a kPa
proceso = (patm * )

#ploteamos
plt.plot(vol, curva1, 'r', label='$T_1$')
plt.plot(vol, curva2, 'b', label='$T_2$')
plt.plot(vol, proceso, 'g')
# plt.plot(vol, curva_proceso, 'g')
# plt.plot(
#     [punto1x], [punto1y],
#     marker='o', markersize=5,
#     color="black",
#     zorder=3 #zorder controla que el punto esté sobre la curva y no detrás
# )
# plt.plot(
#     [punto2x], [punto2y],
#     marker='o', markersize=5,
#     color="black",
#     zorder=3 #zorder controla que el punto esté sobre la curva y no detrás
# )

plt.legend(loc="upper right")
plt.savefig(f"graf_inventado", dpi=300, bbox_inches='tight')

#%% codecell
test = data.to_latex(decimal=',')
print(test)
