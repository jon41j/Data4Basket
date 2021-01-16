# Script para obtener la comparación de estadisiticas individuales entre bases Real Madrid

# Importar librerias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from RadarChart import *


#######Conexión a base de datos ACB
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
                       "where ps.period = 0 and (ps.id_player=20211331 or ps.id_player=20211947 or ps.id_player=20201774 or ps.id_player=20210357) and ps.time_played!='00:00' "
                       "group by p.name_nick")
rows = cursor.fetchall()
conexion.commit()
conexion.close()

# Crear tabla en pandas a partir de la lectura de base de datos
table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]

df_totalsA = pd.DataFrame(table).T
df_totalsA.columns = ['Nombre_Jugador', 'Partidos_jugados', 'Minutos', 'Puntos', 'pt2Anotados', 'pt2Intentados', 'pt3Anotados',
                    'pt3Intentados', 'pt1Anotados', 'pt1Intentados', 'DefReb', 'OffReb',
                    'Asistencias', 'Robos', 'Perdidas', 'Tapones', 'Tapones_Recibidos',
                      'Faltas', 'Faltas_Recibidas', 'Diferencia', 'Valoracion']

# Formato de las diferentes columnas de la tabla en pandas
df_totalsA['Nombre_Jugador'] = df_totalsA.Nombre_Jugador.astype(str)
df_totalsA['Partidos_jugados'] = df_totalsA.Partidos_jugados.astype(int)
df_totalsA['Minutos'] = df_totalsA.Minutos.astype(float)
df_totalsA['Puntos'] = df_totalsA.Puntos.astype(float)
df_totalsA['pt2Anotados'] = df_totalsA.pt2Anotados.astype(float)
df_totalsA['pt2Intentados'] = df_totalsA.pt2Intentados.astype(float)
df_totalsA['pt3Anotados'] = df_totalsA.pt3Anotados.astype(float)
df_totalsA['pt3Intentados'] = df_totalsA.pt3Intentados.astype(float)
df_totalsA['pt1Anotados'] = df_totalsA.pt1Anotados.astype(float)
df_totalsA['pt1Intentados'] = df_totalsA.pt1Intentados.astype(float)
df_totalsA['DefReb'] = df_totalsA.DefReb.astype(float)
df_totalsA['OffReb'] = df_totalsA.OffReb.astype(float)
df_totalsA['Asistencias'] = df_totalsA.Asistencias.astype(float)
df_totalsA['Robos'] = df_totalsA.Robos.astype(float)
df_totalsA['Perdidas'] = df_totalsA.Perdidas.astype(float)
df_totalsA['Tapones'] = df_totalsA.Tapones.astype(float)
df_totalsA['Tapones_Recibidos'] = df_totalsA.Tapones_Recibidos.astype(float)
df_totalsA['Faltas'] = df_totalsA.Faltas.astype(float)
df_totalsA['Faltas_Recibidas'] = df_totalsA.Faltas_Recibidas.astype(float)
df_totalsA['Diferencia'] = df_totalsA.Diferencia.astype(float)
df_totalsA['Valoracion'] = df_totalsA.Valoracion.astype(float)



# Radar plotting para cada base (estadisticas individuales)
fig1 = plt.figure(figsize=(6, 6))
variables = ('Minutos', 'Puntos', 'Rebotes',
             'Asistencias', 'Robos', 'Perdidas',
             'Valoración', 'TriplesAnotados', '% TirosCampo')
ranges = [(7.5, 27.5), (0, 17.5), (0, 4), (0, 7.5), (0, 2.5), (0.5, 3), (0, 20), (0, 2), (25, 50)]
radar = ComplexRadar(fig1, variables, ranges)
for p in range(len(df_totalsA)):
    legend = df_totalsA.Nombre_Jugador[p]
    data = [df_totalsA.Minutos[p], df_totalsA.Puntos[p],df_totalsA.DefReb[p]+df_totalsA.OffReb[p],
                 df_totalsA.Asistencias[p],df_totalsA.Robos[p],df_totalsA.Perdidas[p],
                 df_totalsA.Valoracion[p], df_totalsA.pt3Anotados[p],
            100*((df_totalsA.pt2Anotados[p]+df_totalsA.pt3Anotados[p])/(df_totalsA.pt2Intentados[p]+df_totalsA.pt3Intentados[p]))]
    radar.plot(data, legend)
    radar.fill(data, alpha=0.2)
plt.title('Comparación estadísticas individuales entre bases - ACB')
plt.show()



# Añadir nuevas columnas al pandas con estadisticas individuales avanzadas
df_totalsA['PointsPerShoot'] = (2*df_totalsA.pt2Anotados+3*df_totalsA.pt3Anotados)/(df_totalsA.pt2Intentados+df_totalsA.pt3Intentados)
df_totalsA['Versatility'] = (df_totalsA.Puntos*(df_totalsA.DefReb+df_totalsA.OffReb)*df_totalsA.Asistencias)**0.333
df_totalsA['WinScore'] = (df_totalsA.Puntos +(df_totalsA.DefReb+df_totalsA.OffReb) +df_totalsA.Robos + 0.5*df_totalsA.Asistencias
                        +0.5*df_totalsA.Tapones - (df_totalsA.pt2Intentados+df_totalsA.pt3Intentados) -df_totalsA.Perdidas
                        -0.5*df_totalsA.pt1Intentados-0.5*df_totalsA.Faltas)
df_totalsA['EffectiveFieldGoalPercentage']=100*((df_totalsA.pt2Anotados+df_totalsA.pt3Anotados)+0.5*df_totalsA.pt3Anotados)/(df_totalsA.pt2Intentados+df_totalsA.pt3Intentados)
df_totalsA['RatioAsistenciasPerdidas']= df_totalsA.Asistencias/df_totalsA.Perdidas
df_totalsA['DiferenciaX40Minutes']= 40*df_totalsA.Diferencia/df_totalsA.Minutos

# Radar plotting para cada base (estadisticas individuales avanzadas)
fig1 = plt.figure(figsize=(6, 6))
variables = ('Puntos x Tiro', 'Versatilidad', 'WinScore',
             '%EFGP', 'Ratio Asist-Perd', 'Diferencia')
ranges = [(0.5, 1.5), (0, 6), (-1, 6), (30, 65), (1, 5), (-15, 30)]
radar = ComplexRadar(fig1, variables, ranges)
for p in range(len(df_totalsA)):
    legend = df_totalsA.Nombre_Jugador[p]
    data = [df_totalsA.PointsPerShoot[p], df_totalsA.Versatility[p],df_totalsA.WinScore[p],
            df_totalsA.EffectiveFieldGoalPercentage[p],df_totalsA.RatioAsistenciasPerdidas[p], df_totalsA.DiferenciaX40Minutes[p]]
    radar.plot(data, legend)
    radar.fill(data, alpha=0.2)
plt.title('Comparación estadísticas individuales avanzadas entre bases - ACB')
plt.show()

