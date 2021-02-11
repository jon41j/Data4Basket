import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


## 1. Tenerife
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select jm.id_matchweek, jt.id_match, jt.id_team, t.abrev_name, "
        "jt.pt2_tried, jt.rival_3pt_tried, jt.difference, jt.result "
        "from j_teamstats jt "
        "inner join teams t on jt.id_team = t.id_team "
        "inner join j_matches jm on jt.id_match = jm.id_match "
        "inner join j_IDmatchweek jI on jm.id_matchweek = jI.id_matchweek "
        "where jI.id_competition = 'ACB' and jt.period = 0 "
        "group by jt.id_match, jt.id_team "
)
rows = cursor.fetchall()

table = {}
tabla= []
for n in range(len(rows)):
    tabla.append([])
    tabla[n] = list(rows[n])
conexion.commit()
conexion.close()

for n in range(len(tabla)):
        if n % 2 == 0:
                tabla[n].append(tabla[n + 1][3])
        else:
                tabla[n].append(tabla[n - 1][3])

for n in range(len(tabla)):
    table[str(n)] = tabla[n]

df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['Matchweek', 'Id_Game', 'Id_Team', 'TeamName', 'T2atemps', 'T3atemps', 'difference', 'result', 'rivalName']

df['rel2a3'] = df['T2atemps']/df['T3atemps']

df.groupby(by="Id_Team")

j=23
jornadas=[]
for i in range(j):
    if i < 9:
        jornadas.append('A20RS0'+str(i+1))
    else:
        jornadas.append('A20RS' + str(i + 1))


stats = {}
result = {}
difference = {}
rival = {}
teams = []
teams_names = []
for index, row in df.iterrows():
     if row['Id_Team'] not in teams:
             teams.append(row['Id_Team'])
             teams_names.append(row['TeamName'])
             stats[row['Id_Team']] = [None]*(j)
             result[row['Id_Team']] = [None] * (j)
             difference[row['Id_Team']] = [None] * (j)
             rival[row['Id_Team']] = [None] * (j)
             pos = jornadas.index(str(row['Matchweek']))
             stats[row['Id_Team']][pos] = row['T3atemps']
             result[row['Id_Team']][pos] = row['result']
             difference[row['Id_Team']][pos] = row['difference']
             rival[row['Id_Team']][pos] = row['rivalName']
     else:
             pos = jornadas.index(str(row['Matchweek']))
             stats[row['Id_Team']][pos] = row['T3atemps']
             result[row['Id_Team']][pos] = row['result']
             difference[row['Id_Team']][pos] = row['difference']
             rival[row['Id_Team']][pos] = row['rivalName']

df_stats = pd.DataFrame(stats).T
df_results = pd.DataFrame(result).T
df_differences = pd.DataFrame(difference).T
df_rivals = pd.DataFrame(rival).T


columnas = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10',
            'J11', 'J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18',
            'J19', 'J20', 'J21', 'J22', 'J23']
df_stats.columns = columnas
df_results.columns = columnas
df_differences.columns = columnas
df_rivals.columns = columnas

df_stats['mean'] = df_stats.mean(axis=1, skipna=True)

df_stats_comparative = df_stats.copy()
df_stats_comparative['ID'] = teams
df_stats_comparative['TEAMS'] = teams_names
df_stats_comparative = df_stats_comparative.sort_values('mean', ascending = False)
cols = df_stats_comparative.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats_comparative = df_stats_comparative[cols]


media = {}
for col in df_stats:
    media[col] = df_stats[col].mean(skipna=True)

df_stats = df_stats.append(media, ignore_index=True)

teams.append('Mean')
teams_names.append('Mean')
df_stats['ID'] = teams
df_stats['TEAMS'] = teams_names

cols = df_stats.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats = df_stats[cols]

plt.bar(df_stats_comparative['TEAMS'], df_stats_comparative['mean'], align='center', alpha=1,
        color=['red' if (x > df_stats['mean'][19]) else 'blue' for x in df_stats_comparative['mean']])
plt.plot(df_stats_comparative['TEAMS'], [df_stats['mean'][19]]*19, label='Media de la Liga', color='black')
plt.xticks(df_stats_comparative['TEAMS'], rotation=90)
plt.ylabel('Nº posesiones por 40 minutos')
plt.title('Comparación del ritmo equipos ACB')
plt.legend()
plt.ylim(70, 80)
#plt.show()

x = []
y0 = []
y1 = []
y2 = []
v = []
labels = []
lx = []
for index, row in df_stats.iterrows():
    if index < len(df_stats)-1:
        x.append([])
        y0.append([])
        y1.append([])
        y2.append([])
        v.append([])
        y2.append([])
        labels.append([])
        lx.append([])
        for n in range(j):
            x[index].append(n + 1)
            y0[index].append(df_stats['mean'][len(df_stats) - 1])
            y1[index].append(row['mean'])
            y2[index].append(row[str(columnas[n])])
            labels[index].append(df_differences[str(columnas[n])][index])
            lx[index].append(str(columnas[n]) + ' - ' + str(df_rivals[str(columnas[n])][index]))
            if df_results[str(columnas[n])][index] == 1:
                v[index].append(1)
            else:
                v[index].append(0)

colores = ["#ff0000",  # Verde
           "#00cc44"]  # Rojo

for n in range(len(y1)):
    if n==0 or(df_stats['TEAMS'][n] == 'Tenerife'):
        plt.plot(x[n], y1[n], label='Media del equipo')
        #plt.plot(x[n], y0[n], label='Media de la Liga')
        plt.scatter(x[n], y2[n], c=np.take(colores, v[n]))

        for i, txt in enumerate(labels[n]):
            # plt.annotate(txt, xy=(x[i], y2[i]), xytext=(-20, 20))
            plt.annotate(txt,
                         xy=(x[n][i], y2[n][i]),
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5))  # distance from text to points (x,y))

        plt.xticks(range(1, len(y2[n]) + 1, 1), lx[n], rotation=45)
        plt.ylabel("Triples Intentados Rivales")
        plt.title(str(df_stats['TEAMS'][n]))
        plt.legend()
        plt.show()













##### 2. Importancia de Tavares:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from RadarChart import *


#######ACB
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

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]

df_totals = pd.DataFrame(table).T
df_totals.columns = ['Partido', 'NumEvento', 'Cuarto', 'Minutos', 'Segundos', 'EquipoLocal', 'NombreLocal',
                    'EquipoVisitante', 'NombreVisitante', 'PuntosLocal', 'PuntosVisitante', 'EquipoEjecutor',
                    'JugadorEjecutor', 'NombreJugador', 'IdJugada', 'DescripcionJugada']
df_totals['Cuarto'] = df_totals.Cuarto.astype(int)
df_totals['Minutos'] = df_totals.Minutos.astype(int)
df_totals['Segundos'] = df_totals.Segundos.astype(int)
df_totals['EquipoEjecutor'] = df_totals.EquipoEjecutor.astype(int)
df_totals['JugadorEjecutor'] = df_totals.JugadorEjecutor.astype(int)
df_totals['IdJugada'] = df_totals.IdJugada.astype(int)
df_totals['EquipoLocal'] = df_totals.EquipoLocal.astype(int)
df_totals['EquipoVisitante'] = df_totals.EquipoVisitante.astype(int)
df_totals['NombreLocal'] = df_totals.NombreLocal.astype(str)
df_totals['NombreVisitante'] = df_totals.NombreVisitante.astype(str)

df_quintetos = pd.DataFrame(columns=['Jugadores', 'NombresJugadores', 'Rival', 'TiempoJugado', 'canasta2pt', 'fallo2pt', 'canasta3pt', 'fallo3pt',
                                     'canasta1pt', 'fallo1pt', 'off_reb', 'def_reb', 'assist2pt', 'assist3pt', 'assistFault', 'robo', 'perd', 'block',
                                     'blockAgainst', 'mate', 'cta2pt', 'cta3pt', 'ctaFallo2pt', 'ctaFallo3pt', 'ctaFalta', 'ctaPerd', 'faltaRec', 'pers0tl',
                                     'pers1tl', 'pers2tl', 'pers3tl', 'tecnica', 'antideportiva', 'r_canasta2pt', 'r_fallo2pt', 'r_canasta3pt', 'r_fallo3pt',
                                     'r_canasta1pt', 'r_fallo1pt', 'r_off_reb', 'r_def_reb', 'r_assist2pt', 'r_assist3pt', 'r_assistFault', 'r_robo', 'r_perd',
                                     'r_block', 'r_blockAgainst', 'r_mate', 'r_cta2pt', 'r_cta3pt', 'r_ctaFallo2pt', 'r_ctaFallo3pt', 'r_ctaFalta', 'r_ctaPerd',
                                     'r_faltaRec', 'r_pers0tl', 'r_pers1tl', 'r_pers2tl', 'r_pers3tl', 'r_tecnica', 'r_antideportiva'])

index = 0
for me in range(len(df_totals)):
    try:
        if df_totals.Partido[me] != df_totals.Partido[me-1]:
            rival = df_totals.NombreVisitante[me-1] if df_totals.EquipoLocal[me-1] == 3387 else df_totals.NombreLocal[me-1]
            df_quintetos.loc[index] = [lista_jugadores, nombre_jugadores, rival, (tiempo_f - 600 * (4 - df_totals.Cuarto[me-1])) / 60,
                                       canasta2pt, fallo2pt, canasta3pt, fallo3pt, canasta1pt, fallo1pt, off_reb,
                                       def_reb, assist2pt, assist3pt,
                                       assistFault, robo, perd, block, blockAgainst, mate, cta2pt, cta3pt, ctaFallo2pt,
                                       ctaFallo3pt, ctaFalta,
                                       ctaPerd, faltaRec, pers0tl, pers1tl, pers2tl, pers3tl, tecnica, antideportiva,
                                       r_canasta2pt, r_fallo2pt, r_canasta3pt, r_fallo3pt, r_canasta1pt, r_fallo1pt,
                                       r_off_reb, r_def_reb, r_assist2pt, r_assist3pt,
                                       r_assistFault, r_robo, r_perd, r_block, r_blockAgainst, r_mate, r_cta2pt,
                                       r_cta3pt, r_ctaFallo2pt, r_ctaFallo3pt, r_ctaFalta,
                                       r_ctaPerd, r_faltaRec, r_pers0tl, r_pers1tl, r_pers2tl, r_pers3tl, r_tecnica,
                                       r_antideportiva]
            index += 1
            lista_jugadores = []
            nombre_jugadores = []
    except:
        lista_jugadores = []
        nombre_jugadores = []
    if df_totals.EquipoEjecutor[me] == 3387 and df_totals.IdJugada[me] == 599:
        lista_jugadores.append(df_totals.JugadorEjecutor[me])
        nombre_jugadores.append(df_totals.NombreJugador[me])
        if len(lista_jugadores) == 5:
            tiempo_f = 600 * (4 - df_totals.Cuarto[me]) + (60 * df_totals.Minutos[me] + df_totals.Segundos[me])
            canasta2pt = 0
            fallo2pt = 0
            canasta3pt = 0
            fallo3pt = 0
            canasta1pt = 0
            fallo1pt = 0
            off_reb = 0
            def_reb = 0
            assist2pt = 0
            assist3pt = 0
            assistFault = 0
            robo = 0
            perd = 0
            block = 0
            blockAgainst = 0
            mate = 0
            cta2pt = 0
            cta3pt = 0
            ctaFallo2pt = 0
            ctaFallo3pt = 0
            ctaFalta = 0
            ctaPerd = 0
            faltaRec = 0
            pers0tl = 0
            pers1tl = 0
            pers2tl = 0
            pers3tl = 0
            tecnica = 0
            antideportiva = 0
            r_canasta2pt = 0
            r_fallo2pt = 0
            r_canasta3pt = 0
            r_fallo3pt = 0
            r_canasta1pt = 0
            r_fallo1pt = 0
            r_off_reb = 0
            r_def_reb = 0
            r_assist2pt = 0
            r_assist3pt = 0
            r_assistFault = 0
            r_robo = 0
            r_perd = 0
            r_block = 0
            r_blockAgainst = 0
            r_mate = 0
            r_cta2pt = 0
            r_cta3pt = 0
            r_ctaFallo2pt = 0
            r_ctaFallo3pt = 0
            r_ctaFalta = 0
            r_ctaPerd = 0
            r_faltaRec = 0
            r_pers0tl = 0
            r_pers1tl = 0
            r_pers2tl = 0
            r_pers3tl = 0
            r_tecnica = 0
            r_antideportiva = 0
    if df_totals.EquipoEjecutor[me] == 3387 and df_totals.IdJugada[me] == 115:
        rival = df_totals.NombreVisitante[me] if df_totals.EquipoLocal[me]== 3387 else df_totals.NombreLocal[me]
        jugadores = lista_jugadores.copy()
        njugadores = nombre_jugadores.copy()
        lista_jugadores.remove(df_totals.JugadorEjecutor[me])
        nombre_jugadores.remove(df_totals.NombreJugador[me])
        if len(lista_jugadores) == 4:
            df_quintetos.loc[index] = [jugadores, njugadores, rival,
                                   (tiempo_f- (600 * (4 - df_totals.Cuarto[me]) + (60 * df_totals.Minutos[me] + df_totals.Segundos[me])))/60,
                                   canasta2pt, fallo2pt, canasta3pt, fallo3pt, canasta1pt, fallo1pt, off_reb, def_reb, assist2pt, assist3pt,
                                   assistFault, robo, perd, block, blockAgainst, mate, cta2pt, cta3pt, ctaFallo2pt, ctaFallo3pt, ctaFalta,
                                   ctaPerd, faltaRec, pers0tl, pers1tl, pers2tl, pers3tl, tecnica, antideportiva,
                                   r_canasta2pt, r_fallo2pt, r_canasta3pt, r_fallo3pt, r_canasta1pt, r_fallo1pt, r_off_reb, r_def_reb, r_assist2pt, r_assist3pt,
                                   r_assistFault, r_robo, r_perd, r_block, r_blockAgainst, r_mate, r_cta2pt, r_cta3pt, r_ctaFallo2pt, r_ctaFallo3pt, r_ctaFalta,
                                   r_ctaPerd, r_faltaRec, r_pers0tl, r_pers1tl, r_pers2tl, r_pers3tl, r_tecnica, r_antideportiva]
            index += 1
    if df_totals.EquipoEjecutor[me] == 3387 and df_totals.IdJugada[me] == 112:
        lista_jugadores.append(df_totals.JugadorEjecutor[me])
        nombre_jugadores.append(df_totals.NombreJugador[me])
        if len(lista_jugadores) == 5:
            tiempo_f = 600 * (4 - df_totals.Cuarto[me]) + (60 * df_totals.Minutos[me] + df_totals.Segundos[me])
            canasta2pt = 0
            fallo2pt = 0
            canasta3pt = 0
            fallo3pt = 0
            canasta1pt = 0
            fallo1pt = 0
            off_reb = 0
            def_reb = 0
            assist2pt = 0
            assist3pt = 0
            assistFault = 0
            robo = 0
            perd = 0
            block = 0
            blockAgainst = 0
            mate = 0
            cta2pt = 0
            cta3pt = 0
            ctaFallo2pt = 0
            ctaFallo3pt = 0
            ctaFalta = 0
            ctaPerd = 0
            faltaRec = 0
            pers0tl = 0
            pers1tl = 0
            pers2tl = 0
            pers3tl = 0
            tecnica = 0
            antideportiva = 0
            r_canasta2pt = 0
            r_fallo2pt = 0
            r_canasta3pt = 0
            r_fallo3pt = 0
            r_canasta1pt = 0
            r_fallo1pt = 0
            r_off_reb = 0
            r_def_reb = 0
            r_assist2pt = 0
            r_assist3pt = 0
            r_assistFault = 0
            r_robo = 0
            r_perd = 0
            r_block = 0
            r_blockAgainst = 0
            r_mate = 0
            r_cta2pt = 0
            r_cta3pt = 0
            r_ctaFallo2pt = 0
            r_ctaFallo3pt = 0
            r_ctaFalta = 0
            r_ctaPerd = 0
            r_faltaRec = 0
            r_pers0tl = 0
            r_pers1tl = 0
            r_pers2tl = 0
            r_pers3tl = 0
            r_tecnica = 0
            r_antideportiva = 0
    if len(lista_jugadores) == 5 and df_totals.EquipoEjecutor[me] == 3387:
        canasta2pt += 1 if df_totals.IdJugada[me] == 93 else 0
        fallo2pt += 1 if df_totals.IdJugada[me] == 97 else 0
        canasta3pt += 1 if df_totals.IdJugada[me] == 94 else 0
        fallo3pt += 1 if df_totals.IdJugada[me] == 98 else 0
        canasta1pt += 1 if df_totals.IdJugada[me] == 92 else 0
        fallo1pt += 1 if df_totals.IdJugada[me] == 96 else 0
        off_reb += 1 if df_totals.IdJugada[me] == 101 else 0
        def_reb += 1 if df_totals.IdJugada[me] == 104 else 0
        assist2pt += 1 if df_totals.IdJugada[me] == 107 else 0
        assist3pt += 1 if df_totals.IdJugada[me] == 108 else 0
        assistFault += 1 if df_totals.IdJugada[me] == 109 else 0
        robo += 1 if df_totals.IdJugada[me] == 103 else 0
        perd += 1 if df_totals.IdJugada[me] == 106 else 0
        block += 1 if df_totals.IdJugada[me] == 102 else 0
        blockAgainst += 1 if df_totals.IdJugada[me] == 105 else 0
        mate += 1 if df_totals.IdJugada[me] == 100 else 0
        cta2pt += 1 if df_totals.IdJugada[me] == 130 else 0
        cta3pt += 1 if df_totals.IdJugada[me] == 131 else 0
        ctaFallo2pt += 1 if df_totals.IdJugada[me] == 132 else 0
        ctaFallo3pt += 1 if df_totals.IdJugada[me] == 133 else 0
        ctaFalta += 1 if df_totals.IdJugada[me] == 134 else 0
        ctaPerd += 1 if df_totals.IdJugada[me] == 135 else 0
        faltaRec += 1 if df_totals.IdJugada[me] == 110 else 0
        pers0tl += 1 if df_totals.IdJugada[me] == 159 else 0
        pers1tl += 1 if df_totals.IdJugada[me] == 160 else 0
        pers2tl += 1 if df_totals.IdJugada[me] == 161 else 0
        pers3tl += 1 if df_totals.IdJugada[me] == 162 else 0
        tecnica += 1 if df_totals.IdJugada[me] == 537 else 0
        antideportiva += 1 if df_totals.IdJugada[me] == 166 else 0
    if len(lista_jugadores) == 5 and df_totals.EquipoEjecutor[me] != 3387:
        r_canasta2pt += 1 if df_totals.IdJugada[me] == 93 else 0
        r_fallo2pt += 1 if df_totals.IdJugada[me] == 97 else 0
        r_canasta3pt += 1 if df_totals.IdJugada[me] == 94 else 0
        r_fallo3pt += 1 if df_totals.IdJugada[me] == 98 else 0
        r_canasta1pt += 1 if df_totals.IdJugada[me] == 92 else 0
        r_fallo1pt += 1 if df_totals.IdJugada[me] == 96 else 0
        r_off_reb += 1 if df_totals.IdJugada[me] == 101 else 0
        r_def_reb += 1 if df_totals.IdJugada[me] == 104 else 0
        r_assist2pt += 1 if df_totals.IdJugada[me] == 107 else 0
        r_assist3pt += 1 if df_totals.IdJugada[me] == 108 else 0
        r_assistFault += 1 if df_totals.IdJugada[me] == 109 else 0
        r_robo += 1 if df_totals.IdJugada[me] == 103 else 0
        r_perd += 1 if df_totals.IdJugada[me] == 106 else 0
        r_block += 1 if df_totals.IdJugada[me] == 102 else 0
        r_blockAgainst += 1 if df_totals.IdJugada[me] == 105 else 0
        r_mate += 1 if df_totals.IdJugada[me] == 100 else 0
        r_cta2pt += 1 if df_totals.IdJugada[me] == 130 else 0
        r_cta3pt += 1 if df_totals.IdJugada[me] == 131 else 0
        r_ctaFallo2pt += 1 if df_totals.IdJugada[me] == 132 else 0
        r_ctaFallo3pt += 1 if df_totals.IdJugada[me] == 133 else 0
        r_ctaFalta += 1 if df_totals.IdJugada[me] == 134 else 0
        r_ctaPerd += 1 if df_totals.IdJugada[me] == 135 else 0
        r_faltaRec += 1 if df_totals.IdJugada[me] == 110 else 0
        r_pers0tl += 1 if df_totals.IdJugada[me] == 159 else 0
        r_pers1tl += 1 if df_totals.IdJugada[me] == 160 else 0
        r_pers2tl += 1 if df_totals.IdJugada[me] == 161 else 0
        r_pers3tl += 1 if df_totals.IdJugada[me] == 162 else 0
        r_tecnica += 1 if df_totals.IdJugada[me] == 537 else 0
        r_antideportiva += 1 if df_totals.IdJugada[me] == 166 else 0

rival = df_totals.NombreVisitante[len(df_totals)-1] if df_totals.EquipoLocal[len(df_totals)-1] == 3387 else df_totals.NombreLocal[len(df_totals)-1]
df_quintetos.loc[index] = [lista_jugadores, nombre_jugadores, rival,
                           (tiempo_f - 600 * (4 - df_totals.Cuarto[len(df_totals)-1])) / 60,
                           canasta2pt, fallo2pt, canasta3pt, fallo3pt, canasta1pt, fallo1pt, off_reb,
                           def_reb, assist2pt, assist3pt,
                           assistFault, robo, perd, block, blockAgainst, mate, cta2pt, cta3pt, ctaFallo2pt,
                           ctaFallo3pt, ctaFalta,
                           ctaPerd, faltaRec, pers0tl, pers1tl, pers2tl, pers3tl, tecnica, antideportiva,
                           r_canasta2pt, r_fallo2pt, r_canasta3pt, r_fallo3pt, r_canasta1pt, r_fallo1pt,
                           r_off_reb, r_def_reb, r_assist2pt, r_assist3pt,
                           r_assistFault, r_robo, r_perd, r_block, r_blockAgainst, r_mate, r_cta2pt,
                           r_cta3pt, r_ctaFallo2pt, r_ctaFallo3pt, r_ctaFalta,
                           r_ctaPerd, r_faltaRec, r_pers0tl, r_pers1tl, r_pers2tl, r_pers3tl, r_tecnica,
                           r_antideportiva]


conTaveres = [0]*59
sinTaveres = [0]*59

for s in range(len(df_quintetos)):
    #Tavaress
    if 20209407 in df_quintetos.Jugadores[s]:
        conTaveres += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    else:
        sinTaveres += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])

df_comparacion = pd.DataFrame({'conTaveres': conTaveres, 'sinTaveres': sinTaveres}).T

# Gráfico barras comparación minutos ACB
plt.bar(df_comparacion.index, df_comparacion['TiempoJugado'], align='center', alpha=0.8,
        color=['orange' if (x > 350) else 'blue' for x in df_comparacion.TiempoJugado])
plt.xticks(df_comparacion.index, rotation=80)
plt.ylabel('Minutos')
plt.title('')
plt.show()

df_comparacion['Possessions'] = ((0.96*((df_comparacion['canasta2pt']+df_comparacion['canasta3pt']+df_comparacion['fallo2pt']+df_comparacion['fallo3pt']+df_comparacion['mate']+df_comparacion['blockAgainst']
                               +df_comparacion['cta2pt']+df_comparacion['cta3pt']+df_comparacion['ctaFallo2pt']+df_comparacion['ctaFallo3pt'])+ df_comparacion['perd'] + df_comparacion['ctaPerd'] +0.44*(df_comparacion['canasta1pt']+df_comparacion['fallo1pt'])
                              -df_comparacion['off_reb']) + 0.96*((df_comparacion['r_canasta2pt']+df_comparacion['r_canasta3pt']+df_comparacion['r_fallo2pt']+df_comparacion['r_fallo3pt']+df_comparacion['r_mate']+df_comparacion['r_blockAgainst']
                               +df_comparacion['r_cta2pt']+df_comparacion['r_cta3pt']+df_comparacion['r_ctaFallo2pt']+df_comparacion['r_ctaFallo3pt'])+ df_comparacion['r_perd']+ df_comparacion['r_ctaPerd']+0.44*(df_comparacion['r_canasta1pt']+df_comparacion['r_fallo1pt'])
                              -df_comparacion['r_off_reb']))/2)
df_comparacion['Pace'] = df_comparacion['Possessions']/df_comparacion['TiempoJugado']*40

df_comparacion['Offensive_Effiency'] = 100*((2*df_comparacion['canasta2pt']+3*df_comparacion['canasta3pt']+2*df_comparacion['mate']+2*df_comparacion['cta2pt']+3*df_comparacion['cta3pt']+df_comparacion['canasta1pt'])/df_comparacion['Possessions'])
df_comparacion['Deffensive_Effiency'] = 100*((2*df_comparacion['r_canasta2pt']+3*df_comparacion['r_canasta3pt']+2*df_comparacion['r_mate']+2*df_comparacion['r_cta2pt']+3*df_comparacion['r_cta3pt']+df_comparacion['r_canasta1pt'])/df_comparacion['Possessions'])

df_comparacion['RivalPercentages'] = 100*((df_comparacion['r_canasta2pt']+df_comparacion['r_canasta3pt']+df_comparacion['r_mate']+df_comparacion['r_cta2pt']+df_comparacion['r_cta3pt'])/(df_comparacion['r_canasta2pt']+
                                              df_comparacion['r_canasta3pt']+df_comparacion['r_fallo2pt']+df_comparacion['r_fallo3pt']+df_comparacion['r_mate']+df_comparacion['r_blockAgainst']+df_comparacion['r_cta2pt']+df_comparacion['r_cta3pt']+df_comparacion['r_ctaFallo2pt']+df_comparacion['r_ctaFallo3pt']))

df_comparacion['BlocksRatio'] = (df_comparacion['block'])/df_comparacion['TiempoJugado']*40

df_comparacion['Points_Difference_per_Game'] = 40*((2*df_comparacion['canasta2pt']+3*df_comparacion['canasta3pt']+2*df_comparacion['mate']+2*df_comparacion['cta2pt']+3*df_comparacion['cta3pt']+df_comparacion['canasta1pt'])-(2*df_comparacion['r_canasta2pt']+3*df_comparacion['r_canasta3pt']+2*df_comparacion['r_mate']+2*df_comparacion['r_cta2pt']+3*df_comparacion['r_cta3pt']+df_comparacion['r_canasta1pt']))/df_comparacion['TiempoJugado']

df_comparacion['Rival_relT2vsT3'] = ((df_comparacion['r_canasta2pt']+df_comparacion['r_fallo2pt']+df_comparacion['r_mate']+df_comparacion['r_cta2pt']+df_comparacion['r_ctaFallo2pt'])/(df_comparacion['r_canasta3pt']+
                                              df_comparacion['r_fallo3pt']+df_comparacion['r_cta3pt']+df_comparacion['r_ctaFallo3pt']))

# Radar plotting
fig1 = plt.figure(figsize=(4, 6))
variables = ('Ritmo', 'Rend. Ofensivo', '+- por partido',
             'Rend. Defensivo', '%FG Rivales',
             'Tapones por 40min', 'Rel. T2/T3 Rivales')
ranges = [(75, 80), (110, 125), (0, 20), (120, 95), (50, 37.5), (1, 4.5), (1, 2)]
radar = ComplexRadar(fig1, variables, ranges)
for p in range(len(df_comparacion)):
    legend = df_comparacion.index[p]
    data = [df_comparacion.Pace[p], df_comparacion.Offensive_Effiency[p], df_comparacion.Points_Difference_per_Game[p],
                 df_comparacion.Deffensive_Effiency[p],df_comparacion.RivalPercentages[p],df_comparacion.BlocksRatio[p],
                 df_comparacion.Rival_relT2vsT3[p]]
    radar.plot(data, legend)
    radar.fill(data, alpha=0.2)
plt.show()

print(df_comparacion.head(4))









## 1. Baskonia P.Henry
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select jm.id_matchweek, jt.id_match, " 
        "jp.assists, jt.difference, jt.result, "
        "t1.abrev_name, t2.abrev_name "
        "from j_teamstats jt "   
        "inner join teams t on jt.id_team = t.id_team "
        "inner join j_matches jm on jt.id_match = jm.id_match "
        "inner join teams t1 on jm.id_localteam = t1.id_team " 
        "inner join teams t2 on jm.id_visitorteam = t2.id_team " 
        "inner join j_IDmatchweek jI on jm.id_matchweek = jI.id_matchweek "
        "inner join j_playerstats jp on  jt.id_match = jp.id_match "
        "where jI.id_competition = 'ACB' and jt.period = 0 and t.id_team=3396 and jp.id_player =30000034 and jp.period=0 "
        "group by jt.id_match, jt.id_team "
        "order by jp.assists desc"
)
rows = cursor.fetchall()

table = {}
tabla= []
for n in range(len(rows)):
    tabla.append([])
    tabla[n] = list(rows[n])
conexion.commit()
conexion.close()

for n in range(len(tabla)):
    if tabla[n][5] == 'Baskonia':
        tabla[n].pop(5)
        tabla[n].append('L')
    else:
        tabla[n].pop(6)
        tabla[n].append('V')

for n in range(len(tabla)):
    table[str(n)] = tabla[n]

df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['Matchweek', 'Id_Game', 'Henry', 'difference', 'result', 'rivalName', 'campo']

df = df.sort_values('Matchweek')

media = df['Henry'].mean()


x = []
y1 = []
y2 = []
v = []
labels = []
lx = []
for n in range(df.shape[0]):
    x.append(n + 1)
    y1.append(media)
    y2.append(df['Henry'][n])
    labels.append(df['Henry'][n])
    lx.append(df['campo'][n] + ' - ' + df['rivalName'][n])
    if df['result'][n]==1:
        v.append(1)
    else:
        v.append(0)

colores = ["#ff0000",  # Verde
           "#00cc44"]  # Rojo



plt.plot(x, y1, label='Media Asistencias P. Henry')
plt.scatter(x, y2, c=np.take(colores, v))

for i, txt in enumerate(labels):
    # plt.annotate(txt, xy=(x[i], y2[i]), xytext=(-20, 20))
    plt.annotate(txt,
                 xy=(x[i], y2[i]),
                 textcoords="offset points",  # how to position the text
                 xytext=(5, 5))  # distance from text to points (x,y))

plt.xticks(range(1, len(y2) + 1, 1), lx, rotation=45)
plt.ylabel("Asistencias P. Henry")
plt.legend()
plt.show()




## 1. Tenerife
conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select jm.id_matchweek, jt.id_match, jt.id_team, t.abrev_name, "
        "jt.pt2_tried, jt.pt3_tried, jt.rival_3pt_tried, jt.difference, jt.result "
        "from j_teamstats jt "
        "inner join teams t on jt.id_team = t.id_team "
        "inner join j_matches jm on jt.id_match = jm.id_match "
        "inner join j_IDmatchweek jI on jm.id_matchweek = jI.id_matchweek "
        "where jI.id_competition = 'ACB' and jt.period = 0 "
        "group by jt.id_match, jt.id_team "
)
rows = cursor.fetchall()

table = {}
tabla= []
for n in range(len(rows)):
    tabla.append([])
    tabla[n] = list(rows[n])
conexion.commit()
conexion.close()

for n in range(len(tabla)):
        if n % 2 == 0:
                tabla[n].append(tabla[n + 1][3])
        else:
                tabla[n].append(tabla[n - 1][3])

for n in range(len(tabla)):
    table[str(n)] = tabla[n]

df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['Matchweek', 'Id_Game', 'Id_Team', 'TeamName', 'T2atemps', 'T3atemps', 'T3rivalAtemps', 'difference', 'result', 'rivalName']

df['rel2a3'] = df['T2atemps']/df['T3atemps']

df.groupby(by="Id_Team")

j=23
jornadas=[]
for i in range(j):
    if i < 9:
        jornadas.append('A20RS0'+str(i+1))
    else:
        jornadas.append('A20RS' + str(i + 1))


stats = {}
stats1 = {}
result = {}
difference = {}
rival = {}
teams = []
teams_names = []
for index, row in df.iterrows():
     if row['Id_Team'] not in teams:
             teams.append(row['Id_Team'])
             teams_names.append(row['TeamName'])
             stats[row['Id_Team']] = [None]*(j)
             stats1[row['Id_Team']] = [None] * (j)
             result[row['Id_Team']] = [None] * (j)
             difference[row['Id_Team']] = [None] * (j)
             rival[row['Id_Team']] = [None] * (j)
             pos = jornadas.index(str(row['Matchweek']))
             stats[row['Id_Team']][pos] = row['rel2a3']
             stats1[row['Id_Team']][pos] = row['T3rivalAtemps']
             result[row['Id_Team']][pos] = row['result']
             difference[row['Id_Team']][pos] = row['difference']
             rival[row['Id_Team']][pos] = row['rivalName']
     else:
             pos = jornadas.index(str(row['Matchweek']))
             stats[row['Id_Team']][pos] = row['rel2a3']
             stats1[row['Id_Team']][pos] = row['T3rivalAtemps']
             result[row['Id_Team']][pos] = row['result']
             difference[row['Id_Team']][pos] = row['difference']
             rival[row['Id_Team']][pos] = row['rivalName']

df_stats = pd.DataFrame(stats).T
df_stats1 = pd.DataFrame(stats1).T
df_results = pd.DataFrame(result).T
df_differences = pd.DataFrame(difference).T
df_rivals = pd.DataFrame(rival).T


columnas = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10',
            'J11', 'J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18',
            'J19', 'J20', 'J21', 'J22', 'J23']
df_stats.columns = columnas
df_stats1.columns = columnas
df_results.columns = columnas
df_differences.columns = columnas
df_rivals.columns = columnas

df_stats['mean'] = df_stats.mean(axis=1, skipna=True)
df_stats1['mean'] = df_stats1.mean(axis=1, skipna=True)

df_stats_comparative = df_stats.copy()
df_stats_comparative['ID'] = teams
df_stats_comparative['TEAMS'] = teams_names
df_stats_comparative = df_stats_comparative.sort_values('mean', ascending = False)
cols = df_stats_comparative.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats_comparative = df_stats_comparative[cols]

df_stats_comparative1 = df_stats1.copy()
df_stats_comparative1['ID'] = teams
df_stats_comparative1['TEAMS'] = teams_names
df_stats_comparative1 = df_stats_comparative1.sort_values('mean', ascending = False)
cols = df_stats_comparative1.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats_comparative = df_stats_comparative1[cols]


media = {}
for col in df_stats:
    media[col] = df_stats[col].mean(skipna=True)

df_stats = df_stats.append(media, ignore_index=True)

teams.append('Mean')
teams_names.append('Mean')
df_stats['ID'] = teams
df_stats['TEAMS'] = teams_names

cols = df_stats.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats = df_stats[cols]

plt.bar(df_stats_comparative['TEAMS'], df_stats_comparative['mean'], align='center', alpha=1,
        color=['red' if (x > df_stats['mean'][19]) else 'blue' for x in df_stats_comparative['mean']])
plt.plot(df_stats_comparative['TEAMS'], [df_stats['mean'][19]]*19, label='Media de la Liga', color='black')
plt.xticks(df_stats_comparative['TEAMS'], rotation=90)
plt.ylabel('Nº posesiones por 40 minutos')
plt.title('Comparación del ritmo equipos ACB')
plt.legend()
plt.ylim(70, 80)
#plt.show()

x = []
y0 = []
y1 = []
y2 = []
v = []
labels = []
lx = []
for index, row in df_stats.iterrows():
    if index < len(df_stats)-1:
        x.append([])
        y0.append([])
        y1.append([])
        y2.append([])
        v.append([])
        y2.append([])
        labels.append([])
        lx.append([])
        for n in range(j):
            x[index].append(n + 1)
            y0[index].append(df_stats['mean'][len(df_stats) - 1])
            y1[index].append(row['mean'])
            y2[index].append(row[str(columnas[n])])
            labels[index].append(df_differences[str(columnas[n])][index])
            lx[index].append(str(columnas[n]) + ' - ' + str(df_rivals[str(columnas[n])][index]))
            if df_results[str(columnas[n])][index] == 1:
                v[index].append(1)
            else:
                v[index].append(0)

colores = ["#ff0000",  # Verde
           "#00cc44"]  # Rojo

for n in range(len(y1)):
    if n==0 or(df_stats['TEAMS'][n] == 'Barsa'):
        plt.plot(x[n], y1[n], label='Media del equipo')
        #plt.plot(x[n], y0[n], label='Media de la Liga')
        plt.scatter(x[n], y2[n], c=np.take(colores, v[n]))

        for i, txt in enumerate(labels[n]):
            # plt.annotate(txt, xy=(x[i], y2[i]), xytext=(-20, 20))
            plt.annotate(txt,
                         xy=(x[n][i], y2[n][i]),
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5))  # distance from text to points (x,y))

        plt.xticks(range(1, len(y2[n]) + 1, 1), lx[n], rotation=45)
        plt.title(str(df_stats['TEAMS'][n]))
        plt.ylabel("Relación Tiros 2pt intentados / Tiros 3 pt intentados")
        plt.legend()
        plt.show()






media = {}
for col in df_stats1:
    media[col] = df_stats1[col].mean(skipna=True)

df_stats1 = df_stats1.append(media, ignore_index=True)

#teams.append('Mean')
#teams_names.append('Mean')
df_stats1['ID'] = teams
df_stats1['TEAMS'] = teams_names

cols = df_stats1.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats1 = df_stats1[cols]

plt.bar(df_stats_comparative1['TEAMS'], df_stats_comparative1['mean'], align='center', alpha=1,
        color=['red' if (x > df_stats1['mean'][19]) else 'blue' for x in df_stats_comparative1['mean']])
plt.plot(df_stats_comparative1['TEAMS'], [df_stats1['mean'][19]]*19, label='Media de la Liga', color='black')
plt.xticks(df_stats_comparative1['TEAMS'], rotation=90)
plt.ylabel('Nº posesiones por 40 minutos')
plt.title('Comparación del ritmo equipos ACB')
plt.legend()
plt.ylim(70, 80)
#plt.show()

x = []
y0 = []
y1 = []
y2 = []
v = []
labels = []
lx = []
for index, row in df_stats1.iterrows():
    if index < len(df_stats1)-1:
        x.append([])
        y0.append([])
        y1.append([])
        y2.append([])
        v.append([])
        y2.append([])
        labels.append([])
        lx.append([])
        for n in range(j):
            x[index].append(n + 1)
            y0[index].append(df_stats1['mean'][len(df_stats1) - 1])
            y1[index].append(row['mean'])
            y2[index].append(row[str(columnas[n])])
            labels[index].append(df_differences[str(columnas[n])][index])
            lx[index].append(str(columnas[n]) + ' - ' + str(df_rivals[str(columnas[n])][index]))
            if df_results[str(columnas[n])][index] == 1:
                v[index].append(1)
            else:
                v[index].append(0)

colores = ["#ff0000",  # Verde
           "#00cc44"]  # Rojo

for n in range(len(y1)):
    if n==0 or(df_stats1['TEAMS'][n] == 'Barsa'):
        plt.plot(x[n], y1[n], label='Media del equipo')
        #plt.plot(x[n], y0[n], label='Media de la Liga')
        plt.scatter(x[n], y2[n], c=np.take(colores, v[n]))

        for i, txt in enumerate(labels[n]):
            # plt.annotate(txt, xy=(x[i], y2[i]), xytext=(-20, 20))
            plt.annotate(txt,
                         xy=(x[n][i], y2[n][i]),
                         textcoords="offset points",  # how to position the text
                         xytext=(5, 5))  # distance from text to points (x,y))

        plt.xticks(range(1, len(y2[n]) + 1, 1), lx[n], rotation=45)
        plt.title(str(df_stats['TEAMS'][n]))
        plt.legend()
        plt.show()