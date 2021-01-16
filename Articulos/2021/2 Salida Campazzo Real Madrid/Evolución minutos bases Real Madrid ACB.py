# Script para obtener gráfico de la evolución de minutos de los 4 bases del Real Madrid en todos los partidos jugados por el Real Madrid hasta la fecha.

# Importar librerias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a Base de datos
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales\ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select me.id_match as Partido, me.id_event as NumEvento, me.period as Cuarto, me.minute as Minutos, "
        "me.second as Segundos, jm.id_localteam as EquipoLocal, t1.abrev_name as NombreLocal, "
        "jm.id_visitorteam as EquipoVisitante, t2.abrev_name as NombreVisitante, me.score_local as PuntosLocal, "
        "me.score_visitor as PuntosVisitante, me.id_team as EquipoEjecutor, me.id_player as JugadorEjecutor, "
        "p.name_nick as NombreJugador, me.id_playbyplaytype as IdJugada, pbp.description "
        "from j_matchevents me "
        "inner join j_matches jm on me.id_match = jm.id_match "
        "inner join teams t1 on jm.id_localteam = t1.id_team "
        "inner join teams t2 on jm.id_visitorteam = t2.id_team "
        "inner join p_players p on me.id_player = p.id_player "
        "inner join t_playbyplay pbp on me.id_playbyplaytype = pbp.id_playbyplaytype "
        "where jm.id_localteam=3387  or jm.id_visitorteam=3387 "
        "order by jm.start_date")
rows = cursor.fetchall()
conexion.commit()
conexion.close()

# Crear tabla en pandas a partir de la lectura de base de datos
table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]

df_totals = pd.DataFrame(table).T
df_totals.columns = ['Partido', 'NumEvento', 'Cuarto', 'Minutos', 'Segundos', 'EquipoLocal', 'NombreLocal',
                    'EquipoVisitante', 'NombreVisitante', 'PuntosLocal', 'PuntosVisitante', 'EquipoEjecutor',
                    'JugadorEjecutor', 'NombreJugador', 'IdJugada', 'DescripcionJugada']

# Formato de las diferentes columnas de la tabla en pandas
df_totals['Cuarto'] = df_totals.Cuarto.astype(int)
df_totals['Minutos'] = df_totals.Minutos.astype(int)
df_totals['Segundos'] = df_totals.Segundos.astype(int)
df_totals['EquipoEjecutor'] = df_totals.EquipoEjecutor.astype(int)
df_totals['JugadorEjecutor'] = df_totals.JugadorEjecutor.astype(int)
df_totals['IdJugada'] = df_totals.IdJugada.astype(int)
df_totals['EquipoLocal'] = df_totals.EquipoLocal.astype(int)
df_totals['EquipoVisitante'] = df_totals.EquipoVisitante.astype(int)

# Diferentes tipos de jugadas existentes
t_playTypes = df_totals['IdJugada'].unique()
t_playTypesDescripcion = df_totals['DescripcionJugada'].unique().T
df_playTypes = pd.DataFrame({'IdJugada': t_playTypes, 'DescripcionJugada': t_playTypesDescripcion},
                  columns=['IdJugada', 'DescripcionJugada'])


 # Partidos jugados por el Madrid (local y visitante)
t_games = df_totals['Partido'].unique()
t_rivals = []
t_side = []
l_games = []
for me in range(len(df_totals)):
        if df_totals.Partido[me] not in l_games:
                l_games.append(df_totals.Partido[me])
                if df_totals.EquipoLocal[me] == 3387:
                        t_rivals.append(df_totals.NombreVisitante[me])
                        t_side.append('Loc')
                else:
                        t_rivals.append(df_totals.NombreLocal[me])
                        t_side.append('Vis')
df_games = pd.DataFrame({'Partidos': t_games, 'Rivales': t_rivals, 'Lado': t_side},
                  columns=['Partidos', 'Rivales', 'Lado'])


# Crear tabla con minutos de los bases
df_playmakers = pd.DataFrame({'Players': [20211331, 20211947, 20201774, 20210357, 100],
                              'PlayersName': ['Campazzo', 'Laprovitola', 'Llull', 'Alocén', 'Otro']},
                  columns=['Players', 'PlayersName'])

# Obtener los minutos jugados por cada base en cada partido de la temporada y rellenar panda df_playmakers
g = 0
l_games = []
for me in range(len(df_totals)):
        if df_totals.Partido[me] not in l_games:
                if g>0:
                        if campazzo:
                                tiempo_campazzo = tiempo_campazzo + tiempo_campazzo1 - tiempo_f
                        if laprovittola:
                                tiempo_laprovittola = tiempo_laprovittola + tiempo_laprovittola1 - tiempo_f
                        if llull:
                                tiempo_llull= tiempo_llull + tiempo_llull1 - tiempo_f
                        if alocen:
                                tiempo_alocen = tiempo_alocen + tiempo_alocen1 - tiempo_f
                        df_playmakers[str(df_games.Lado[g-1]) + ': ' + str(df_games.Rivales[g-1])] = [tiempo_campazzo/60, tiempo_laprovittola/60, tiempo_llull/60, tiempo_alocen/60, 0]
                campazzo = False
                tiempo_campazzo = 0
                tiempo_campazzo1 = 0
                laprovittola = False
                tiempo_laprovittola = 0
                tiempo_laprovittola1 = 0
                llull = False
                tiempo_llull = 0
                tiempo_llull1 = 0
                alocen = False
                tiempo_alocen = 0
                tiempo_alocen1 = 0
                l_games.append(df_totals.Partido[me])
                g +=1
        if df_totals.Cuarto[me] <= 4:
                tiempo_f = 600*(4 - df_totals.Cuarto[me]) + (60 * df_totals.Minutos[me] + df_totals.Segundos[me])
        else:
                tiempo_f = 300 * (4 - df_totals.Cuarto[me]) + (60 * df_totals.Minutos[me] + df_totals.Segundos[me])
        if df_totals.IdJugada[me] == 599:
                if df_totals.JugadorEjecutor[me] == 20211331:
                        campazzo = True
                        tiempo_campazzo1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20211947:
                        laprovittola = True
                        tiempo_laprovittola1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20201774:
                        llull = True
                        tiempo_llull1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20210357:
                        alocen = True
                        tiempo_alocen1 = tiempo_f
        if df_totals.IdJugada[me] == 112:
                if df_totals.JugadorEjecutor[me] == 20211331:
                        campazzo = True
                        tiempo_campazzo1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20211947:
                        laprovittola = True
                        tiempo_laprovittola1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20201774:
                        llull = True
                        tiempo_llull1 = tiempo_f
                elif df_totals.JugadorEjecutor[me] == 20210357:
                        alocen = True
                        tiempo_alocen1 = tiempo_f
        if df_totals.IdJugada[me] == 115:
                if df_totals.JugadorEjecutor[me] == 20211331:
                        campazzo = False
                        tiempo_campazzo = tiempo_campazzo + tiempo_campazzo1 - tiempo_f
                        tiempo_campazzo1 = 0
                elif df_totals.JugadorEjecutor[me] == 20211947:
                        laprovittola = False
                        tiempo_laprovittola = tiempo_laprovittola + tiempo_laprovittola1 - tiempo_f
                        tiempo_laprovittola1 = 0
                elif df_totals.JugadorEjecutor[me] == 20201774:
                        llull = False
                        tiempo_llull = tiempo_llull + tiempo_llull1 - tiempo_f
                        tiempo_llull1 = 0
                elif df_totals.JugadorEjecutor[me] == 20210357:
                        alocen = False
                        tiempo_alocen = tiempo_alocen + tiempo_alocen1 - tiempo_f
                        tiempo_alocen1 = 0
if campazzo:
        tiempo_campazzo = tiempo_campazzo + tiempo_campazzo1 - tiempo_f
if laprovittola:
        tiempo_laprovittola = tiempo_laprovittola + tiempo_laprovittola1 - tiempo_f
if llull:
        tiempo_llull = tiempo_llull + tiempo_llull1 - tiempo_f
if alocen:
        tiempo_alocen = tiempo_alocen + tiempo_alocen1 - tiempo_f
df_playmakers[str(df_games.Lado[g - 1]) + ': ' + str(df_games.Rivales[g - 1])] = [tiempo_campazzo / 60, tiempo_laprovittola / 60, tiempo_llull / 60, tiempo_alocen / 60, 0]


#Graficar evolución de minutos bases Real Madrid en los diferentes partidos ACB
for g in range(len(df_playmakers.T)-2):
        plt.bar(df_playmakers.columns[g+2], df_playmakers.values[0][g+2], color = 'red')
        plt.bar(df_playmakers.columns[g + 2], df_playmakers.values[1][g + 2], bottom=df_playmakers.values[0][g+2], color='green')
        plt.bar(df_playmakers.columns[g + 2], df_playmakers.values[2][g + 2], bottom=df_playmakers.values[0][g+2]+df_playmakers.values[1][g + 2], color='yellow')
        plt.bar(df_playmakers.columns[g + 2], df_playmakers.values[3][g + 2], bottom=df_playmakers.values[0][g+2]+df_playmakers.values[1][g + 2]+df_playmakers.values[2][g + 2], color='blue')
plt.legend(['Campazzo', 'Laprovittola', 'Llull', 'Alocen'])
plt.xticks(rotation=75)
plt.ylabel("Minutos disputados")
plt.show()

