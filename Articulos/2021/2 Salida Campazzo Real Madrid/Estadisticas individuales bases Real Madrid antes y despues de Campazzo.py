# Script para obtener las estadisticas individuales de los bases del Real Madrid antes y despues de la salida de Campazzo

# Importar librerias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from RadarChart import *



##### Datos antes de la salida de Campazzo ####################################


# Conexión a Base de datos
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales\ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select p.name_nick as Nombre_Jugador, "
                       "count(*) as Partidos_jugados, "
                       "round(cast(cast(sum(ps.time_played) as float)/count(*) as float),2) as Minutos, "
                       "round(cast(cast(sum(ps.points) as float)/count(*) as float),2) as Puntos, "
                       "round(cast(cast(sum(ps.pt2_success) as float)/count(*) as float),2) as pt2Anotados, "
                       "round(cast(cast(sum(ps.pt2_tried) as float)/count(*) as float),2) as pt2Intentados, "
                       "round(cast(cast(sum(ps.pt3_success) as float)/count(*) as float),2) as pt3Anotados, "
                       "round(cast(cast(sum(ps.pt3_tried) as float)/count(*) as float),2) as pt3Intentados, "
                       "round(cast(cast(sum(ps.pt1_success) as float)/count(*) as float),2) as pt1Anotados, "
                       "round(cast(cast(sum(ps.pt1_tried) as float)/count(*) as float),2) as pt1Intentados, "
                       "round(cast(cast(sum(ps.deffensive_rebound) as float)/count(*) as float),2) as DefReb, "
                       "round(cast(cast(sum(ps.offensive_rebound) as float)/count(*) as float),2) as OffReb, "
                       "round(cast(cast(sum(ps.assists) as float)/count(*) as float),2) as Asistencias, "
                       "round(cast(cast(sum(ps.steals) as float)/count(*) as float),2) as Robos, "
                       "round(cast(cast(sum(ps.turnovers) as float)/count(*) as float),2) as Perdidas, "
                       "round(cast(cast(sum(ps.blocks) as float)/count(*) as float),2) as Tapones, "
                       "round(cast(cast(sum(ps.received_blocks) as float)/count(*) as float),2) as Tapones_Recibidos, "
                       "round(cast(cast(sum(ps.personal_fouls) as float)/count(*) as float),2) as Faltas, "
                       "round(cast(cast(sum(ps.received_fouls) as float)/count(*) as float),2) as Faltas_Recibidas, "
                       "round(cast(cast(sum(ps.difference) as float)/count(*) as float),2) as Mas_Menos, "
                       "round(cast(cast(sum(ps.val) as float)/count(*) as float),2) as Valoracion "
                       "from j_playerstats ps "
                       "inner join p_players p on ps.id_player = p.id_player "
                       "inner join j_matches m on ps.id_match = m.id_match "
                       "where ps.period = 0 and (ps.id_player=20211947 or ps.id_player=20201774 or ps.id_player=20210357) and ps.time_played!='00:00' and m.start_date < '2020-11-21' "
                       "group by p.name_nick")
rows = cursor.fetchall()
conexion.commit()
conexion.close()

# Crear tabla en pandas a partir de la lectura de base de datos
table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]

df_totalsAbeforeC = pd.DataFrame(table).T
df_totalsAbeforeC.columns = ['Nombre_Jugador', 'Partidos_jugados', 'Minutos', 'Puntos', 'pt2Anotados', 'pt2Intentados', 'pt3Anotados',
                    'pt3Intentados', 'pt1Anotados', 'pt1Intentados', 'DefReb', 'OffReb',
                    'Asistencias', 'Robos', 'Perdidas', 'Tapones', 'Tapones_Recibidos',
                      'Faltas', 'Faltas_Recibidas', 'Diferencia', 'Valoracion']


# Formato de las diferentes columnas de la tabla en pandas
df_totalsAbeforeC['Nombre_Jugador'] = df_totalsAbeforeC.Nombre_Jugador.astype(str)
df_totalsAbeforeC['Partidos_jugados'] = df_totalsAbeforeC.Partidos_jugados.astype(int)
df_totalsAbeforeC['Minutos'] = df_totalsAbeforeC.Minutos.astype(float)
df_totalsAbeforeC['Puntos'] = df_totalsAbeforeC.Puntos.astype(float)
df_totalsAbeforeC['pt2Anotados'] = df_totalsAbeforeC.pt2Anotados.astype(float)
df_totalsAbeforeC['pt2Intentados'] = df_totalsAbeforeC.pt2Intentados.astype(float)
df_totalsAbeforeC['pt3Anotados'] = df_totalsAbeforeC.pt3Anotados.astype(float)
df_totalsAbeforeC['pt3Intentados'] = df_totalsAbeforeC.pt3Intentados.astype(float)
df_totalsAbeforeC['pt1Anotados'] = df_totalsAbeforeC.pt1Anotados.astype(float)
df_totalsAbeforeC['pt1Intentados'] = df_totalsAbeforeC.pt1Intentados.astype(float)
df_totalsAbeforeC['DefReb'] = df_totalsAbeforeC.DefReb.astype(float)
df_totalsAbeforeC['OffReb'] = df_totalsAbeforeC.OffReb.astype(float)
df_totalsAbeforeC['Asistencias'] = df_totalsAbeforeC.Asistencias.astype(float)
df_totalsAbeforeC['Robos'] = df_totalsAbeforeC.Robos.astype(float)
df_totalsAbeforeC['Perdidas'] = df_totalsAbeforeC.Perdidas.astype(float)
df_totalsAbeforeC['Tapones'] = df_totalsAbeforeC.Tapones.astype(float)
df_totalsAbeforeC['Tapones_Recibidos'] = df_totalsAbeforeC.Tapones_Recibidos.astype(float)
df_totalsAbeforeC['Faltas'] = df_totalsAbeforeC.Faltas.astype(float)
df_totalsAbeforeC['Faltas_Recibidas'] = df_totalsAbeforeC.Faltas_Recibidas.astype(float)
df_totalsAbeforeC['Diferencia'] = df_totalsAbeforeC.Diferencia.astype(float)
df_totalsAbeforeC['Valoracion'] = df_totalsAbeforeC.Valoracion.astype(float)


# Crear columnas nuevas en el panda con datos avanzados
df_totalsAbeforeC['PointsPerShoot'] = (2*df_totalsAbeforeC.pt2Anotados+3*df_totalsAbeforeC.pt3Anotados)/(df_totalsAbeforeC.pt2Intentados+df_totalsAbeforeC.pt3Intentados)
df_totalsAbeforeC['Versatility'] = (df_totalsAbeforeC.Puntos*(df_totalsAbeforeC.DefReb+df_totalsAbeforeC.OffReb)*df_totalsAbeforeC.Asistencias)**0.333
df_totalsAbeforeC['WinScore'] = (df_totalsAbeforeC.Puntos +(df_totalsAbeforeC.DefReb+df_totalsAbeforeC.OffReb) +df_totalsAbeforeC.Robos + 0.5*df_totalsAbeforeC.Asistencias
                        +0.5*df_totalsAbeforeC.Tapones - (df_totalsAbeforeC.pt2Intentados+df_totalsAbeforeC.pt3Intentados) -df_totalsAbeforeC.Perdidas
                        -0.5*df_totalsAbeforeC.pt1Intentados-0.5*df_totalsAbeforeC.Faltas)
df_totalsAbeforeC['EffectiveFieldGoalPercentage']=100*((df_totalsAbeforeC.pt2Anotados+df_totalsAbeforeC.pt3Anotados)+0.5*df_totalsAbeforeC.pt3Anotados)/(df_totalsAbeforeC.pt2Intentados+df_totalsAbeforeC.pt3Intentados)
df_totalsAbeforeC['RatioAsistenciasPerdidas']= df_totalsAbeforeC.Asistencias/df_totalsAbeforeC.Perdidas
df_totalsAbeforeC['DiferenciaX40Minutes']= 40*df_totalsAbeforeC.Diferencia/df_totalsAbeforeC.Minutos


############################################################################################################

##### Datos antes de la salida de Campazzo ####################################


# Conexión a Base de datos
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales\ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select p.name_nick as Nombre_Jugador, "
                       "count(*) as Partidos_jugados, "
                       "round(cast(cast(sum(ps.time_played) as float)/count(*) as float),2) as Minutos, "
                       "round(cast(cast(sum(ps.points) as float)/count(*) as float),2) as Puntos, "
                       "round(cast(cast(sum(ps.pt2_success) as float)/count(*) as float),2) as pt2Anotados, "
                       "round(cast(cast(sum(ps.pt2_tried) as float)/count(*) as float),2) as pt2Intentados, "
                       "round(cast(cast(sum(ps.pt3_success) as float)/count(*) as float),2) as pt3Anotados, "
                       "round(cast(cast(sum(ps.pt3_tried) as float)/count(*) as float),2) as pt3Intentados, "
                       "round(cast(cast(sum(ps.pt1_success) as float)/count(*) as float),2) as pt1Anotados, "
                       "round(cast(cast(sum(ps.pt1_tried) as float)/count(*) as float),2) as pt1Intentados, "
                       "round(cast(cast(sum(ps.deffensive_rebound) as float)/count(*) as float),2) as DefReb, "
                       "round(cast(cast(sum(ps.offensive_rebound) as float)/count(*) as float),2) as OffReb, "
                       "round(cast(cast(sum(ps.assists) as float)/count(*) as float),2) as Asistencias, "
                       "round(cast(cast(sum(ps.steals) as float)/count(*) as float),2) as Robos, "
                       "round(cast(cast(sum(ps.turnovers) as float)/count(*) as float),2) as Perdidas, "
                       "round(cast(cast(sum(ps.blocks) as float)/count(*) as float),2) as Tapones, "
                       "round(cast(cast(sum(ps.received_blocks) as float)/count(*) as float),2) as Tapones_Recibidos, "
                       "round(cast(cast(sum(ps.personal_fouls) as float)/count(*) as float),2) as Faltas, "
                       "round(cast(cast(sum(ps.received_fouls) as float)/count(*) as float),2) as Faltas_Recibidas, "
                       "round(cast(cast(sum(ps.difference) as float)/count(*) as float),2) as Mas_Menos, "
                       "round(cast(cast(sum(ps.val) as float)/count(*) as float),2) as Valoracion "
                       "from j_playerstats ps "
                       "inner join p_players p on ps.id_player = p.id_player "
                       "inner join j_matches m on ps.id_match = m.id_match "
                       "where ps.period = 0 and (ps.id_player=20211947 or ps.id_player=20201774 or ps.id_player=20210357) and ps.time_played!='00:00' and m.start_date > '2020-11-21' "
                       "group by p.name_nick")
rows = cursor.fetchall()
conexion.commit()
conexion.close()

# Crear tabla en pandas a partir de la lectura de base de datos
table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]

df_totalsAafterC = pd.DataFrame(table).T
df_totalsAafterC.columns = ['Nombre_Jugador', 'Partidos_jugados', 'Minutos', 'Puntos', 'pt2Anotados', 'pt2Intentados', 'pt3Anotados',
                    'pt3Intentados', 'pt1Anotados', 'pt1Intentados', 'DefReb', 'OffReb',
                    'Asistencias', 'Robos', 'Perdidas', 'Tapones', 'Tapones_Recibidos',
                      'Faltas', 'Faltas_Recibidas', 'Diferencia', 'Valoracion']

# Formato de las diferentes columnas de la tabla en pandas
df_totalsAafterC['Nombre_Jugador'] = df_totalsAafterC.Nombre_Jugador.astype(str)
df_totalsAafterC['Partidos_jugados'] = df_totalsAafterC.Partidos_jugados.astype(int)
df_totalsAafterC['Minutos'] = df_totalsAafterC.Minutos.astype(float)
df_totalsAafterC['Puntos'] = df_totalsAafterC.Puntos.astype(float)
df_totalsAafterC['pt2Anotados'] = df_totalsAafterC.pt2Anotados.astype(float)
df_totalsAafterC['pt2Intentados'] = df_totalsAafterC.pt2Intentados.astype(float)
df_totalsAafterC['pt3Anotados'] = df_totalsAafterC.pt3Anotados.astype(float)
df_totalsAafterC['pt3Intentados'] = df_totalsAafterC.pt3Intentados.astype(float)
df_totalsAafterC['pt1Anotados'] = df_totalsAafterC.pt1Anotados.astype(float)
df_totalsAafterC['pt1Intentados'] = df_totalsAafterC.pt1Intentados.astype(float)
df_totalsAafterC['DefReb'] = df_totalsAafterC.DefReb.astype(float)
df_totalsAafterC['OffReb'] = df_totalsAafterC.OffReb.astype(float)
df_totalsAafterC['Asistencias'] = df_totalsAafterC.Asistencias.astype(float)
df_totalsAafterC['Robos'] = df_totalsAafterC.Robos.astype(float)
df_totalsAafterC['Perdidas'] = df_totalsAafterC.Perdidas.astype(float)
df_totalsAafterC['Tapones'] = df_totalsAafterC.Tapones.astype(float)
df_totalsAafterC['Tapones_Recibidos'] = df_totalsAafterC.Tapones_Recibidos.astype(float)
df_totalsAafterC['Faltas'] = df_totalsAafterC.Faltas.astype(float)
df_totalsAafterC['Faltas_Recibidas'] = df_totalsAafterC.Faltas_Recibidas.astype(float)
df_totalsAafterC['Diferencia'] = df_totalsAafterC.Diferencia.astype(float)
df_totalsAafterC['Valoracion'] = df_totalsAafterC.Valoracion.astype(float)

# Crear columnas nuevas en el panda con datos avanzados
df_totalsAafterC['PointsPerShoot'] = (2*df_totalsAafterC.pt2Anotados+3*df_totalsAafterC.pt3Anotados)/(df_totalsAafterC.pt2Intentados+df_totalsAafterC.pt3Intentados)
df_totalsAafterC['Versatility'] = (df_totalsAafterC.Puntos*(df_totalsAafterC.DefReb+df_totalsAafterC.OffReb)*df_totalsAafterC.Asistencias)**0.333
df_totalsAafterC['WinScore'] = (df_totalsAafterC.Puntos +(df_totalsAafterC.DefReb+df_totalsAafterC.OffReb) +df_totalsAafterC.Robos + 0.5*df_totalsAafterC.Asistencias
                        +0.5*df_totalsAafterC.Tapones - (df_totalsAafterC.pt2Intentados+df_totalsAafterC.pt3Intentados) -df_totalsAafterC.Perdidas
                        -0.5*df_totalsAafterC.pt1Intentados-0.5*df_totalsAafterC.Faltas)
df_totalsAafterC['EffectiveFieldGoalPercentage']=100*((df_totalsAafterC.pt2Anotados+df_totalsAafterC.pt3Anotados)+0.5*df_totalsAafterC.pt3Anotados)/(df_totalsAafterC.pt2Intentados+df_totalsAafterC.pt3Intentados)
df_totalsAafterC['RatioAsistenciasPerdidas']= df_totalsAafterC.Asistencias/df_totalsAafterC.Perdidas
df_totalsAafterC['DiferenciaX40Minutes']= 40*df_totalsAafterC.Diferencia/df_totalsAafterC.Minutos


########################################################################################

# Crear Radar plotting de las estadisticas individuales de cada jugador con el antes y después de Campazzo

#### Alocen
fig1 = plt.figure(figsize=(6, 6))
variables = ('Minutos', 'Puntos', 'Rebotes',
             'Asistencias', 'Robos', 'Perdidas',
             'Valoración', 'TriplesAnotados', '% TirosCampo')
ranges = [(5, 25), (0, 15), (0, 4), (0, 7), (0, 2), (2.5, 0), (0, 15), (0, 2), (20, 55)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.Minutos[0], df_totalsAbeforeC.Puntos[0],df_totalsAbeforeC.DefReb[0]+df_totalsAbeforeC.OffReb[0],
             df_totalsAbeforeC.Asistencias[0],df_totalsAbeforeC.Robos[0],df_totalsAbeforeC.Perdidas[0],
             df_totalsAbeforeC.Valoracion[0], df_totalsAbeforeC.pt3Anotados[0],
        100*((df_totalsAbeforeC.pt2Anotados[0]+df_totalsAbeforeC.pt3Anotados[0])/(df_totalsAbeforeC.pt2Intentados[0]+df_totalsAbeforeC.pt3Intentados[0]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Despues Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.Minutos[0], df_totalsAafterC.Puntos[0],df_totalsAafterC.DefReb[0]+df_totalsAafterC.OffReb[0],
             df_totalsAafterC.Asistencias[0],df_totalsAafterC.Robos[0],df_totalsAafterC.Perdidas[0],
             df_totalsAafterC.Valoracion[0], df_totalsAafterC.pt3Anotados[0],
        100*((df_totalsAafterC.pt2Anotados[0]+df_totalsAafterC.pt3Anotados[0])/(df_totalsAafterC.pt2Intentados[0]+df_totalsAafterC.pt3Intentados[0]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('ALOCÉN - Con y después de Campazzo (Estadísticas Indiviuales) - ACB')
plt.show()

#### Laprovittola
fig1 = plt.figure(figsize=(6, 6))
variables = ('Minutos', 'Puntos', 'Rebotes',
             'Asistencias', 'Robos', 'Perdidas',
             'Valoración', 'TriplesAnotados', '% TirosCampo')
ranges = [(5, 25), (0, 15), (0, 4), (0, 7), (0, 2), (2.5, 0), (0, 15), (0, 2), (20, 55)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.Minutos[1], df_totalsAbeforeC.Puntos[1],df_totalsAbeforeC.DefReb[1]+df_totalsAbeforeC.OffReb[1],
             df_totalsAbeforeC.Asistencias[1],df_totalsAbeforeC.Robos[1],df_totalsAbeforeC.Perdidas[1],
             df_totalsAbeforeC.Valoracion[1], df_totalsAbeforeC.pt3Anotados[1],
        100*((df_totalsAbeforeC.pt2Anotados[1]+df_totalsAbeforeC.pt3Anotados[1])/(df_totalsAbeforeC.pt2Intentados[1]+df_totalsAbeforeC.pt3Intentados[1]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Despues Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.Minutos[1], df_totalsAafterC.Puntos[1],df_totalsAafterC.DefReb[1]+df_totalsAafterC.OffReb[1],
             df_totalsAafterC.Asistencias[1],df_totalsAafterC.Robos[1],df_totalsAafterC.Perdidas[1],
             df_totalsAafterC.Valoracion[1], df_totalsAafterC.pt3Anotados[1],
        100*((df_totalsAafterC.pt2Anotados[1]+df_totalsAafterC.pt3Anotados[1])/(df_totalsAafterC.pt2Intentados[1]+df_totalsAafterC.pt3Intentados[1]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('ACB              ', color='blue')
plt.show()

##### Llull
fig1 = plt.figure(figsize=(6, 6))
variables = ('Minutos', 'Puntos', 'Rebotes',
             'Asistencias', 'Robos', 'Perdidas',
             'Valoración', 'TriplesAnotados', '% TirosCampo')
ranges = [(5, 25), (0, 15), (0, 4), (0, 7), (0, 2), (2.5, 0), (0, 15), (0, 2), (20, 55)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.Minutos[2], df_totalsAbeforeC.Puntos[2],df_totalsAbeforeC.DefReb[2]+df_totalsAbeforeC.OffReb[2],
             df_totalsAbeforeC.Asistencias[2],df_totalsAbeforeC.Robos[2],df_totalsAbeforeC.Perdidas[2],
             df_totalsAbeforeC.Valoracion[2], df_totalsAbeforeC.pt3Anotados[2],
        100*((df_totalsAbeforeC.pt2Anotados[2]+df_totalsAbeforeC.pt3Anotados[2])/(df_totalsAbeforeC.pt2Intentados[2]+df_totalsAbeforeC.pt3Intentados[2]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Despues Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.Minutos[2], df_totalsAafterC.Puntos[2],df_totalsAafterC.DefReb[2]+df_totalsAafterC.OffReb[2],
             df_totalsAafterC.Asistencias[2],df_totalsAafterC.Robos[2],df_totalsAafterC.Perdidas[2],
             df_totalsAafterC.Valoracion[2], df_totalsAafterC.pt3Anotados[2],
        100*((df_totalsAafterC.pt2Anotados[2]+df_totalsAafterC.pt3Anotados[2])/(df_totalsAafterC.pt2Intentados[2]+df_totalsAafterC.pt3Intentados[2]))]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('LLULL - Con y después de Campazzo (Estadísticas Indiviuales) - ACB')
plt.show()




########################################################################################

# Crear Radar plotting de las estadisticas individuales avanzadas de cada jugador con el antes y después de Campazzo


#### ALOCEN
fig1 = plt.figure(figsize=(6, 6))
variables = ('Puntos x Tiro', 'Versatilidad', 'WinScore',
             '%EFGP', 'Ratio Asist-Perd', 'Diferencia')
ranges = [(0.5, 1.5), (0, 6), (-2.5, 6), (25, 70), (0.5, 6), (-15, 25)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.PointsPerShoot[0], df_totalsAbeforeC.Versatility[0],df_totalsAbeforeC.WinScore[0],
        df_totalsAbeforeC.EffectiveFieldGoalPercentage[0],df_totalsAbeforeC.RatioAsistenciasPerdidas[0], df_totalsAbeforeC.DiferenciaX40Minutes[0]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Después Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.PointsPerShoot[0], df_totalsAafterC.Versatility[0],df_totalsAafterC.WinScore[0],
        df_totalsAafterC.EffectiveFieldGoalPercentage[0],df_totalsAafterC.RatioAsistenciasPerdidas[0], df_totalsAafterC.DiferenciaX40Minutes[0]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('ALOCÉN - Con y después de Campazzo (Estadísticas Indiviuales Avanzadas) - ACB')
plt.show()

##### LAPROVITTOLA
fig1 = plt.figure(figsize=(6, 6))
variables = ('Puntos x Tiro', 'Versatilidad', 'WinScore',
             '%EFGP', 'Ratio Asist-Perd', 'Diferencia')
ranges = [(0.5, 1.5), (0, 6), (-2.5, 6), (25, 70), (0.5, 6), (-15, 25)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.PointsPerShoot[1], df_totalsAbeforeC.Versatility[1],df_totalsAbeforeC.WinScore[1],
        df_totalsAbeforeC.EffectiveFieldGoalPercentage[1],df_totalsAbeforeC.RatioAsistenciasPerdidas[1], df_totalsAbeforeC.DiferenciaX40Minutes[1]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Después Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.PointsPerShoot[1], df_totalsAafterC.Versatility[1],df_totalsAafterC.WinScore[1],
        df_totalsAafterC.EffectiveFieldGoalPercentage[1],df_totalsAafterC.RatioAsistenciasPerdidas[1], df_totalsAafterC.DiferenciaX40Minutes[1]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('LAPROVITTOLA - Con y después de Campazzo (Estadísticas Indiviuales Avanzadas) - ACB')
plt.show()

#### LLULL
fig1 = plt.figure(figsize=(6, 6))
variables = ('Puntos x Tiro', 'Versatilidad', 'WinScore',
             '%EFGP', 'Ratio Asist-Perd', 'Diferencia')
ranges = [(0.5, 1.5), (0, 6), (-2.5, 6), (25, 70), (0.5, 6), (-15, 25)]
radar = ComplexRadar(fig1, variables, ranges)
# Antes Campazzo
legend = "Con Campazzo"
data = [df_totalsAbeforeC.PointsPerShoot[2], df_totalsAbeforeC.Versatility[2],df_totalsAbeforeC.WinScore[2],
        df_totalsAbeforeC.EffectiveFieldGoalPercentage[2],df_totalsAbeforeC.RatioAsistenciasPerdidas[2], df_totalsAbeforeC.DiferenciaX40Minutes[2]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
# Después Campazzo
legend = "Sin Campazzo"
data = [df_totalsAafterC.PointsPerShoot[2], df_totalsAafterC.Versatility[2],df_totalsAafterC.WinScore[2],
        df_totalsAafterC.EffectiveFieldGoalPercentage[2],df_totalsAafterC.RatioAsistenciasPerdidas[2], df_totalsAafterC.DiferenciaX40Minutes[2]]
radar.plot(data, legend)
radar.fill(data, alpha=0.2)
plt.title('LLULL - Con y después de Campazzo (Estadísticas Indiviuales Avanzadas) - ACB')
plt.show()



