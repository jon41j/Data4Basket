import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm



#Conexión a Base de datos para obtener los datos
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select t.abrev_name as NombreEquipo, "
        "sum(cast(0.96*((ts.pt2_tried+ts.pt3_tried)+ts.turnovers+0.44*(ts.pt1_tried)-ts.offensive_rebound) as float)) as Posesiones1, "
        "sum(ts.points) as PuntosAnotados, "
        "sum(ts.rival_points) as PuntosRecibidos, "
        "sum(ts.result) as Victorias "
        "from j_teamstats ts "
        "inner join teams t on ts.id_team = t.id_team "
        "where period=0 "
        "group by ts.id_team ")
rows = cursor.fetchall()

#Rellenar tabla con los datos obtenidos
table = {}
tabla= []
for n in range(len(rows)):
    tabla.append([])
    tabla[n] = list(rows[n])
conexion.commit()
conexion.close()

# Crear tabla en pandas con las siguientes columnaspara cada equipo:
     # Equipo
     # Total de posesiones
     # Total de puntos anotados
     # Total de puntos recibidos
     # Nº de Victorias del equipo
for n in range(len(tabla)):
    table[str(n)] = tabla[n]

df = pd.DataFrame(table).T
df.columns = ['Team', 'Posesiones', 'PuntosAnotados', 'PuntosRecibidos', 'Victorias']

# Cambiar formato de las columnas
df['Posesiones'] = df.Posesiones.astype(float)
df['PuntosAnotados'] = df.PuntosAnotados.astype(int)
df['PuntosRecibidos'] = df.PuntosRecibidos.astype(int)
df['Victorias'] = df.Victorias.astype(int)

# Crear nueva columna con el Offensive efficiency (Puntos anotados por cada 100 posesiones)
df['Offensive_Efficiency'] = round(100*df['PuntosAnotados']/df['Posesiones'], 1)

# Crear nueva columna con el Deffensive efficiency (Puntos recibidos por cada 100 posesiones)
df['Defensive_Efficiency'] = round(100*df['PuntosRecibidos']/df['Posesiones'], 1)


# Gráfico de puntos
ax = df.plot.scatter(x='Offensive_Efficiency', y='Defensive_Efficiency', c='Victorias', colormap='coolwarm')

# Añadir nombre del equipo a cada punto
for r in range(len(df)):
    ax.text(df.Offensive_Efficiency[r], df.Defensive_Efficiency[r], df.Team[r], horizontalalignment='center', verticalalignment='baseline')

# Calcular línea de tendencia
model = sm.formula.ols(formula="Defensive_Efficiency ~ Offensive_Efficiency", data=df)
res = model.fit()
df.assign(fit=res.fittedvalues).plot(x="Offensive_Efficiency", y="fit", ax=ax)

# Formato del gráfico
ax.legend_.remove()
ax.set_xlabel("Offensive Efficiency (Puntos anotados por 100 posesiones)")
ax.set_ylabel("Defensive Efficiency (Puntos recibidos por 100 posesiones)")

plt.show()
