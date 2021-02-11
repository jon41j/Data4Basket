import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select t.abrev_name as equipo, "
                        "points as puntos, pt2_success as pt2ano, pt2_tried as pt2int, pt2_percentage as pt2por, "
                        "pt3_success as pt3ano, pt3_tried as pt3intentados, pt3_percentage as pt3por, "
                        "pt1_success as pt1anotados, pt1_tried as pt1intentados, pt1_percentage as pt1por, "
                        "deffensive_rebound as rdef, offensive_rebound as roff, total_rebound as rtot, "
                        "assists as ast, steals as rob, turnovers as tur, dunks as mat, blocks as tap_f, received_blocks as tap_c, "
                        "personal_fouls as falt, received_fouls as falt_rec, val as valoracion, "
                        "rival_points as r_puntos, rival_2pt_success as r_pt2ano, rival_2pt_tried as r_pt2int, rival_2pt_percentage as r_pt2por, "
                        "rival_3pt_success as r_pt3ano, rival_3pt_tried as r_pt3intentados, rival_3pt_percentage as r_pt3por, "
                        "rival_1pt_success as r_pt1anotados, rival_1pt_tried as r_pt1intentados, rival_1pt_percentage as r_pt1por, "
                        "rival_deffensive_rebound as r_rdef, rival_offensive_rebound as r_roff, rival_total_rebound as r_rtot, "
                        "rival_assists as r_ast, rival_steals as r_rob, rival_turnovers as r_tur, rival_dunks as r_mat, rival_val as r_valoracion, difference as dif, "
                        "100*cast(bench_points as float)/cast(points as float) as banq_points, 100*cast(points_fastbreak as float)/cast(points as float) as ca_points, "
                        "100*cast(points_aftersteal as float)/cast(points as float) as steal_points, 100*cast(points_secondchance as float)/cast(points as float) as op2_points, "
                        "100*cast(points_in_the_paint as float)/cast(points as float) as paint_points, 100*cast(points_fastbreak_against as float)/cast(points as float) as r_ca_points, "
                        "100*cast(points_aftersteal_against as float)/cast(points as float) as r_steal_points, 100*cast(points_secondchance_against as float)/cast(points as float) as r_op2_points, "
                        "100*cast(points_in_the_paint_against as float)/cast(points as float) as r_paint_points, result as res "
                        "from j_teamstats "
                        "inner join teams t on t.id_team=j_teamstats.id_team "
                        "where period =0")
rows = cursor.fetchall()

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]
conexion.commit()
conexion.close()


df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['equipo', 'puntos', 'pt2ano', 'pt2int', 'pt2por', 'pt3ano', 'pt3int', 'pt3por',
              'pt1ano', 'pt1int', 'pt1por', 'rdef', 'roff', 'rtot',
              'ast', 'ste', 'tur', 'mat', 'tap_f', 'tap_c', 'falt', 'r_falt', 'val',
              'r_puntos', 'r_pt2ano', 'r_pt2int', 'r_pt2por', 'r_pt3ano', 'r_pt3int', 'r_pt3por',
              'r_pt1ano', 'r_pt1int', 'r_pt1por', 'r_rdef', 'r_roff', 'r_rtot',
              'r_ast', 'r_ste', 'r_tur', 'r_mat', 'r_val',
              'dif', 'banq_points', 'ca_points', 'steal_points', 'op2_points', 'paint_points',
              'r_ca_points', 'r_steal_points', 'r_op2_points', 'r_paint_points', 'res']

df['reb_def'] = 1.96+100*(df['rdef']/(df['r_pt2int']+df['r_pt3int']-df['r_pt2ano']-df['r_pt3ano']+0.4*(df['r_pt1int']-df['r_pt1ano'])))
df['reb_off'] = 1.96+100*(df['roff']/(df['pt2int']+df['pt3int']-df['pt2ano']-df['pt3ano']+0.4*(df['pt1int']-df['pt1ano'])))
df['r_reb_off'] = 1.96+100*(df['r_roff']/(df['r_pt2int']+df['r_pt3int']-df['r_pt2ano']-df['r_pt3ano']+0.4*(df['r_pt1int']-df['r_pt1ano'])))
df['r_reb_def'] = 1.96+100*(df['r_rdef']/(df['pt2int']+df['pt3int']-df['pt2ano']-df['pt3ano']+0.4*(df['pt1int']-df['pt1ano'])))
df['reb_tot'] = 1.96+100*(df['rtot']/(df['pt2int']+df['pt3int']-df['pt2ano']-df['pt3ano']+0.4*(df['pt1int']-df['pt1ano'])+df['r_pt2int']+df['r_pt3int']-df['r_pt2ano']-df['r_pt3ano']+0.4*(df['r_pt1int']-df['r_pt1ano'])))
df['r_reb_tot'] = 1.96+100*(df['r_rtot']/(df['pt2int']+df['pt3int']-df['pt2ano']-df['pt3ano']+0.4*(df['pt1int']-df['pt1ano'])+df['r_pt2int']+df['r_pt3int']-df['r_pt2ano']-df['r_pt3ano']+0.4*(df['r_pt1int']-df['r_pt1ano'])))
df['pt2-pt3'] = 100*(df['pt2int']/df['pt3int'])
df['r_pt2-pt3'] = 100*(df['r_pt2int']/df['r_pt3int'])


df_team = df[df['equipo'] == 'Unicaja'].copy()

df_stats=df_team.drop(['equipo'], axis=1).copy()

def mean_norm(df_input):
    return df_input.apply(lambda x: (x-x.mean())/ x.std(), axis=0)

df_stats = mean_norm(df_stats)


#representar las correlaciones matematicas de forma grafica a través de un mapa binario en donde veremos mucho mejor estas correlaciones
sns.heatmap(df_stats.astype('float64').corr(), center=0)
#plt.show()


stats = ['pt2int', 'pt2por', 'pt3int', 'pt3por',
              'pt1int', 'pt1por', 'reb_def', 'reb_off', 'reb_tot',
              'ast', 'ste', 'tur', 'mat', 'tap_f', 'tap_c', 'falt', 'r_falt',
              'r_pt2int', 'r_pt2por', 'r_pt3int', 'r_pt3por',
              'r_pt1int', 'r_pt1por', 'r_reb_def', 'r_reb_off', 'r_reb_tot',
              'r_ast', 'r_ste', 'r_tur', 'r_mat',
              'banq_points', 'ca_points', 'steal_points', 'op2_points', 'paint_points',
              'r_ca_points', 'r_steal_points', 'r_op2_points', 'r_paint_points', 'pt2-pt3', 'r_pt2-pt3']


df_stats=df_stats.astype('float64')
correlation=[]
for st in stats:
    cor= df_stats['res'].corr(df_stats[st])
    correlation.append(cor)

df_correlations= pd.DataFrame(data = list(zip(stats,correlation)),
                    columns = ["Stat","Correlation"])

df_correlations = df_correlations.sort_values('Correlation',ascending=False)

print