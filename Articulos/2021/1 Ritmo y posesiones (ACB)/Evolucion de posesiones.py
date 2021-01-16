# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 12:20:47 2020

@author: jonbe
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# 1- Conexión a la base de datos
conexion = sqlite3.connect('ACB.db')
cursor = conexion.cursor()
table = cursor.execute(
        "select jm.id_matchweek, jt.id_match, jt.id_team, t.abrev_name, cast(jt.time_played/60 as float), "
        "jt.pt2_tried + jt.pt3_tried, jt.pt1_tried, jt.offensive_rebound, jt.deffensive_rebound, "
        "jt.pt2_success + jt.pt3_success, jt.turnovers, jt.difference, jt.result "
        "from j_teamstats jt "
        "inner join teams t on jt.id_team = t.id_team "
        "inner join j_matches jm on jt.id_match = jm.id_match "
        "inner join j_IDmatchweek jI on jm.id_matchweek = jI.id_matchweek "
        "where jI.id_competition = 'ACB' and jt.period = 0 "
        "group by jt.id_match, jt.id_team "
)
rows = cursor.fetchall()
conexion.commit()
conexion.close()

# 2- Generar una lista con la informacion recogida de la base de datos
tabla= []
for n in range(len(rows)):
    tabla.append([])
    tabla[n] = list(rows[n])


for n in range(len(tabla)):
        if n % 2 == 0:
                tabla[n].append(tabla[n+1][5])
                tabla[n].append(tabla[n + 1][6])
                tabla[n].append(tabla[n + 1][7])
                tabla[n].append(tabla[n + 1][8])
                tabla[n].append(tabla[n + 1][9])
                tabla[n].append(tabla[n + 1][10])
                tabla[n].append(tabla[n + 1][3])
        else:
                tabla[n].append(tabla[n - 1][5])
                tabla[n].append(tabla[n - 1][6])
                tabla[n].append(tabla[n - 1][7])
                tabla[n].append(tabla[n - 1][8])
                tabla[n].append(tabla[n - 1][9])
                tabla[n].append(tabla[n - 1][10])
                tabla[n].append(tabla[n - 1][3])
 
# 3- Rellenar un diccionario con la información de la lista anterior
table = {}
for n in range(len(tabla)):
    table[str(n)] = tabla[n]

# 4- Generar una tabla en pandas a partir del diccionario
df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['Matchweek', 'Id_Game', 'Id_Team', 'TeamName', 'Time', 'FGA', 'FTA', 'OR', 'DR', 'FG', 'Turnovers',
              'difference', 'result', 'rival_FGA', 'rival_FTA', 'rival_OR', 'rival_DR', 'rival_FG', 'rival_Turnovers', 'rivalName']

# 5- Generar el registro de posiciones a partir de la fórmula utilizada en la NBA para el cálculo de posesiones
df['Possessions1'] = 0.5*((df['FGA']+0.4*df['FTA']-1.07*(df['OR']/(df['OR']+df['rival_DR']))*(df['FGA']-df['FG'])+df['Turnovers'])
+(df['rival_FGA']+0.4*df['rival_FTA']-1.07*(df['rival_OR']/(df['rival_OR'] + df['DR']))*(df['rival_FGA']-df['rival_FG'])+df['rival_Turnovers']))



df['Pos1_40mins'] = df['Possessions1']/(df['Time']/5)*40



df.groupby(by="Id_Team")



# 6- Calcular la correlación de las diferentes métricas estudiadas con el número de posesiones
df_pos = df[['Time', 'FG', 'FGA', 'FTA', 'OR', 'DR', 'Turnovers',
             'Possessions1']]

df_pos.columns = ['Time', 'FG', 'FGA', 'FTA', 'OffReb', 'DefReb', 'Turnovers', 'Possessions']



sns.heatmap(df_pos.astype('float64').corr(), center=0)
plt.show()

sns.regplot(x="Time", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="FG", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="FGA", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="FTA", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="OffReb", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="DefReb", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()
sns.regplot(x="Turnovers", y="Possessions", data=df_pos.astype('float64'), order=1)
plt.show()


# 7. Generar una lista con todas las jornadas disputadas
j=16
jornadas=[]
for i in range(j):
    if i < 9:
        jornadas.append('A20RS0'+str(i+1))
    else:
        jornadas.append('A20RS' + str(i + 1))

jornadas[-1] = 'A20RS17'

# 8. Crear cuatro diccionarios con todas las jornadas disputadas como columnas(features) y todos los equipos como filas.
#    En cada diccionario se muestra:
#       - stats: Número de posesiones por cada 40 minutos.
#       - result: 1 para victoria, 0 para derrota.
#       - difference: Diferencia de puntos en el resultado final. Positivo para victoria, negativo para derrota.
#       - rival: Equipo rival.

stats = {}
result = {}
difference = {}
rival = {}
teams = []
teams_names = []
for index, row in df.iterrows():
     if row[2] not in teams:
             teams.append(row[2])
             teams_names.append(row[3])
             stats[row[2]] = [None]*(j)
             result[row[2]] = [None] * (j)
             difference[row[2]] = [None] * (j)
             rival[row[2]] = [None] * (j)
             pos = jornadas.index(str(row[0]))
             stats[row[2]][pos] = row[21]
             result[row[2]][pos] = row[12]
             difference[row[2]][pos] = row[11]
             rival[row[2]][pos] = row[19]
     else:
             pos = jornadas.index(str(row[0]))
             stats[row[2]][pos] = row[21]
             result[row[2]][pos] = row[12]
             difference[row[2]][pos] = row[11]
             rival[row[2]][pos] = row[19]

# 9. Se genera una tabla en pandas de cada uno de los diccionarios y se renombran las columnas
df_stats = pd.DataFrame(stats).T
df_results = pd.DataFrame(result).T
df_differences = pd.DataFrame(difference).T
df_rivals = pd.DataFrame(rival).T

columnas = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10'
                    , 'J11', 'J12', 'J13', 'J14', 'J15', 'J17']
df_stats.columns = columnas
df_results.columns = columnas
df_differences.columns = columnas
df_rivals.columns = columnas

# 10. Calcular la media de cada equipo
df_stats['mean'] = df_stats.mean(axis=1, skipna=True)

# 11. Generar otro pandas para utilizarlo en un gráfico de comparación de equipos
df_stats_comparative = df_stats.copy()
df_stats_comparative['ID'] = teams
df_stats_comparative['TEAMS'] = teams_names
df_stats_comparative = df_stats_comparative.sort_values('mean', ascending = False)
cols = df_stats_comparative.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_stats_comparative = df_stats_comparative[cols]

# 12. Calculo de la media de cada columna (feature)
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

# 13. Gráfico de comparación en el número de posesiones entre equipos
plt.bar(df_stats_comparative['TEAMS'], df_stats_comparative['mean'], align='center', alpha=1,
        color=['red' if (x > df_stats['mean'][19]) else 'blue' for x in df_stats_comparative['mean']])
plt.plot(df_stats_comparative['TEAMS'], [df_stats['mean'][19]]*19, label='Media de la Liga', color='black')
plt.xticks(df_stats_comparative['TEAMS'], rotation=90)
plt.ylabel('Nº posesiones por 40 minutos')
plt.title('Comparación del ritmo equipos ACB')
plt.legend()
plt.ylim(70, 80)
plt.show()

# 14. Generación de listas para el gráfico final de la evolución de las posesiones y resultado de los equipos
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


#15. Generar el gráfico final de la evolución de las posesiones y resultado de cada equipo
for n in range(len(y1)):
    plt.plot(x[n], y1[n], label='Media del equipo')
    plt.plot(x[n], y0[n], label='Media de la Liga')
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