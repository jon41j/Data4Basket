import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from RadarChart import *



conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select t.abrev_name as Equipo, "
        "cast(sum(0.96*((ts.pt2_tried+ts.pt3_tried)+ts.turnovers+0.44*(ts.pt1_tried)-ts.offensive_rebound))as float)/cast(sum(ts.time_played)as float)*200 as Ritmo, "
        "cast(sum(ts.points)as float)/cast(sum(0.96*((ts.pt2_tried+ts.pt3_tried)+ts.turnovers+0.44*(ts.pt1_tried)-ts.offensive_rebound))as float)*100 as OfEf, "
        "cast(sum(ts.rival_points)as float)/cast(sum(0.96*((ts.pt2_tried+ts.pt3_tried)+ts.turnovers+0.44*(ts.pt1_tried)-ts.offensive_rebound))as float)*100 as DefEf, "
        "cast(sum(ts.difference)as float)/count(*) as Diferencia, "
        "cast(sum(ts.assists)as float)/cast(sum(ts.turnovers) as float) as RatioAstPerd, "
        "1.96+100*cast(sum(ts.total_rebound)as float)/cast(sum(ts.pt2_tried+ts.pt3_tried-ts.pt2_success-ts.pt3_success+0.4*(ts.pt1_tried-ts.pt1_success)+ts.rival_2pt_tried+ts.rival_3pt_tried-ts.rival_2pt_success-ts.rival_3pt_success+0.4*(ts.rival_1pt_tried-ts.rival_1pt_success))as float) as RebPorcentaje, "
        "100*cast(sum(ts.points) as float)/cast(sum(2*(ts.pt2_tried+ts.pt3_tried)+0.44*(ts.pt1_tried)) as float) as TShooting "
        "from j_teamstats ts "
        "inner join teams t on ts.id_team = t.id_team "
        "where period=0 "
        "group by ts.id_team"
)
rows = cursor.fetchall()

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]
conexion.commit()
conexion.close()


df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['Equipo', 'Ritmo', 'OfEf', 'DefEf', 'Diferencia', 'RatioAstPerd', 'RebPorcentaje', 'TShooting']

df['Equipo'] = df.Equipo.astype(str)
df['Ritmo'] = df.Ritmo.astype(float)
df['OfEf'] = df.OfEf.astype(float)
df['DefEf'] = df.DefEf.astype(float)
df['Diferencia'] = df.Diferencia.astype(float)
df['RatioAstPerd'] = df.RatioAstPerd.astype(float)
df['RebPorcentaje'] = df.RebPorcentaje.astype(float)
df['TShooting'] = df.TShooting.astype(float)

a=df.RebPorcentaje.mean()

## GRÁFICOS RADAR

# TENERIFE VS BURGOS

fig1 = plt.figure(figsize=(6, 6))
variables = ('Ritmo', 'Rend. Ofensivo', '+- por partido',
             'Rend. Defensivo', 'Ratio Asit/Perd', '% Rebotes',
             '% True Shooting')
ranges = [(68, 75), (115, 125), (0, 14), (118, 102), (1.11, 1.48), (47, 54), (60, 68)]
radar = ComplexRadar(fig1, variables, ranges)

    # Tenerife
legend = df.Equipo[12]
data = [df.Ritmo[12], df.OfEf[12], df.Diferencia[12], df.DefEf[12], df.RatioAstPerd[12], df.RebPorcentaje[12], df.TShooting[12]]
radar.plot(data, legend, color='gold')
radar.fill(data, alpha=0.2, color='gold')

    # Burgos
legend = df.Equipo[13]
data = [df.Ritmo[13], df.OfEf[13], df.Diferencia[13], df.DefEf[13], df.RatioAstPerd[13], df.RebPorcentaje[13], df.TShooting[13]]
radar.plot(data, legend, color='royalblue')
radar.fill(data, alpha=0.2, color='royalblue')

plt.show()




# MADRID VS VALENCIA

fig1 = plt.figure(figsize=(6, 6))
variables = ('Ritmo', 'Rend. Ofensivo', '+- por partido',
             'Rend. Defensivo', 'Ratio Asit/Perd', '% Rebotes',
             '% True Shooting')
ranges = [(68, 75), (115, 125), (0, 14), (118, 102), (1.11, 1.48), (47, 54), (60, 68)]
radar = ComplexRadar(fig1, variables, ranges)

    # Madrid
legend = df.Equipo[6]
data = [df.Ritmo[6], df.OfEf[6], df.Diferencia[6], df.DefEf[6], df.RatioAstPerd[6], df.RebPorcentaje[6], df.TShooting[6]]
radar.plot(data, legend, color='royalblue')
radar.fill(data, alpha=0.2, color='royalblue')

    # Valencia
legend = df.Equipo[2]
data = [df.Ritmo[2], df.OfEf[2], df.Diferencia[2], df.DefEf[2], df.RatioAstPerd[2], df.RebPorcentaje[2], df.TShooting[2]]
radar.plot(data, legend, color='darkorange')
radar.fill(data, alpha=0.2, color='darkorange')

plt.show()



# BASKONIA VS JOVENTUT

fig1 = plt.figure(figsize=(6, 6))
variables = ('Ritmo', 'Rend. Ofensivo', '+- por partido',
             'Rend. Defensivo', 'Ratio Asit/Perd', '% Rebotes',
             '% True Shooting')
ranges = [(68, 75), (115, 125), (0, 14), (118, 102), (1.11, 1.48), (47, 54.5), (60, 68)]
radar = ComplexRadar(fig1, variables, ranges)

    # Baskonia
legend = df.Equipo[15]
data = [df.Ritmo[15], df.OfEf[15], df.Diferencia[15], df.DefEf[15], df.RatioAstPerd[15], df.RebPorcentaje[15], df.TShooting[15]]
radar.plot(data, legend, color='firebrick')
radar.fill(data, alpha=0.2, color='firebrick')

    # Joventut
legend = df.Equipo[7]
data = [df.Ritmo[7], df.OfEf[7], df.Diferencia[7], df.DefEf[7], df.RatioAstPerd[7], df.RebPorcentaje[7], df.TShooting[7]]
radar.plot(data, legend, color='forestgreen')
radar.fill(data, alpha=0.2, color='forestgreen')

plt.show()




# BARCA VS UNICAJA

fig1 = plt.figure(figsize=(6, 6))
variables = ('Ritmo', 'Rend. Ofensivo', '+- por partido',
             'Rend. Defensivo', 'Ratio Asit/Perd', '% Rebotes',
             '% True Shooting')
ranges = [(68, 75), (115, 125), (0, 14), (118, 102), (1.11, 1.48), (47, 54), (60, 68)]
radar = ComplexRadar(fig1, variables, ranges)

    # Barca
legend = df.Equipo[16]
data = [df.Ritmo[16], df.OfEf[16], df.Diferencia[16], df.DefEf[16], df.RatioAstPerd[16], df.RebPorcentaje[16], df.TShooting[16]]
radar.plot(data, legend, color='darkred')
radar.fill(data, alpha=0.2, color='darkred')

    # Unicaja
legend = df.Equipo[1]
data = [df.Ritmo[1], df.OfEf[1], df.Diferencia[1], df.DefEf[1], df.RatioAstPerd[1], df.RebPorcentaje[1], df.TShooting[1]]
radar.plot(data, legend, color='limegreen')
radar.fill(data, alpha=0.2, color='limegreen')

plt.show()