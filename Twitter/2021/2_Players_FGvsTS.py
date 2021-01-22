import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm



#Conexión a Base de datos para obtener los datos
conexion = sqlite3.connect('../../../Euroleague_BDD/Europe.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select p.name_nick as NombreJugador, "
        "sum(ps.time_played) as MinutosTotales, "
        "sum(ps.pt2_tried+ps.pt3_tried)/sum(ps.time_played)*30 as TirosX30minutos, "
        "0.5*(sum(ps.points)/(sum(ps.pt2_tried+ps.pt3_tried)+0.44*sum(ps.pt1_tried))) as TruePercentage "
        "from j_playerstats ps "
        "inner join p_players p on ps.id_player = p.id_player "
        "where ps.period=0 " 
        "group by ps.id_player "
        "order by TirosX30minutos desc")
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
     # Nombre Jugador
     # Minutos Totales
     # Tiros por 30minutos
     # TruePercentage
for n in range(len(tabla)):
    table[str(n)] = tabla[n]

df = pd.DataFrame(table).T
df.columns = ['Player', 'Minutos', 'FG', 'TS']

# Cambiar formato de las columnas
df['Player'] = df.Player.astype(str)
df['Minutos'] = df.Minutos.astype(float)
df['FG'] = df.FG.astype(float)
df['TS'] = df.TS.astype(float)

# Eliminar jugadores con menos de 100 minutos disputados
df.drop(df[df.Minutos<100].index, inplace = True)

# Eliminar jugadores con menos de 10 tiros por 30 minutos
df.drop(df[df.FG<11].index, inplace = True)

# Gráfico de puntos
ax = df.plot.scatter(x='FG', y='TS', c='Minutos', colormap='coolwarm')

# Añadir nombre del equipo a cada punto
for r in range(len(df)):
    ax.text(df.FG[r], df.TS[r], df.Player[r], horizontalalignment='center', verticalalignment='baseline')

# Calcular línea de tendencia
model = sm.formula.ols(formula="TS ~ FG", data=df)
res = model.fit()
df.assign(fit=res.fittedvalues).plot(x="FG", y="fit", ax=ax)

# Formato del gráfico
ax.legend_.remove()
ax.set_xlabel("Cantidad de tiros de campo(FGA por 30 Minutos)")
ax.set_ylabel("Porcentaje de tiro real (%TS)")
ax.set_title("Máximos lanzadores de la Euroliga (Mínimo 100 minutos disputados y más de 10 tiros por 30 minutos)")

plt.show()
