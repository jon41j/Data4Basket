import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc
import numpy as np


conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select t.abrev_name as equipo, "
                       "posY as posx, "
                       "posX as posy, "
                       "result as result "
                       "from j_shoots "
                       "inner join teams t on t.id_team=j_shoots.id_team "
                       "where (id_action!=92 and id_action!=96)")
rows = cursor.fetchall()

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]
conexion.commit()
conexion.close()


df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['equipo', 'posx', 'posy', 'result']
df['equipo'] = df.equipo.astype(str)
df['posx'] = df.posx.astype(float)
df['posy'] = df.posy.astype(float)
#df['result'] = df.result.astype(float)>

df['posx'] = (df['posx']+7500)/100
df['posy'] = df['posy']/100
df['posx0'] = df['posx']-75

def cancha_ACB(ax=None, color='black', lw=2, outer_lines=False):
    # if an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # create the various parts of an NBA basketball court

    # create the basketball hoop
    # diameter of a hoop is 18" so it has a radius of 9", which is a value of 7.5 in our coordinate system
    hoop = Circle((75, 5), radius=2.5, linewidth=lw, color=color, fill=False)

    # create backboard
    backboard = Rectangle((65, 2.5), 20, -0.5, linewidth=lw, color=color)

    # the paint

    # create the inner box of the paint, width=12 ft, hieght=19ft
    inner_box = Rectangle((45, -2.5), 60, 51.5, linewidth=lw, color=color, fill=False)

    # create the free throw top arc
    top_free_throw = Arc((75, 49), 36, 36, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # create the free throw bottom arc
    bottom_free_throw = Arc((75, 49), 36, 36, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    # restricted zone, arc with 4 ft radius from center of the hoop
    restricted = Arc((75, 6.5), 27.5, 27.5, theta1=0, theta2=180, linewidth=lw, color=color)

    # three point line
    # create the side 3 point lines, 14 ft long before they before they begin to arc
    corner_three_a = Rectangle((10, -2.5), 0, 22.5, linewidth=lw, color=color)

    corner_three_b = Rectangle((140, -2.5), 0, 22.5, linewidth=lw, color=color)

    # three point arc, center of the arc will be the hoop, arc is 23 ft 9 inches away from the hoop
    three_arc = Arc((75, 5), 133, 131, theta1=12.5, theta2=167.5, linewidth=lw, color=color)

    # center court
    center_outer_arc = Arc((75, 115), 30, 30, theta1=180, theta2=0, linewidth=lw, color=color)

    # list of court elements to be poltted onto the axes
    court_elements = [hoop, backboard, inner_box, top_free_throw, bottom_free_throw,
                      restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, ]

    # draw the half court line, baseline and side out bound lines
    outer_lines = Rectangle((0, -2.5), 150, 117.5, linewidth=lw, color=color, fill=False)
    court_elements.append(outer_lines)

    # add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def tiros_equipo(datos, grafico):
    if grafico == 1:
        joint_shot_chart = sns.jointplot(x=datos["posx"], y=datos["posy"], kind='scatter', space=0, alpha=0.5)
        joint_shot_chart.fig.set_size_inches(25, 19.99)
        ax = joint_shot_chart.ax_joint
        ax.set_ylim(-2.5, 115)
        ax.set_xlim(0, 150)
        cancha_ACB(ax)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelbottom='off', labelleft='off')
    elif grafico == 2:
        joint_shot_chart = sns.jointplot(data=datos, x=datos["posx"], y=datos["posy"], kind="hex", color='limegreen')
        joint_shot_chart.fig.set_size_inches(25, 19.99)
        ax = joint_shot_chart.ax_joint
        ax.set_ylim(-2.5, 115)
        ax.set_xlim(0, 150)
        cancha_ACB(ax)
    elif grafico == 3:
        joint_shot_chart = sns.jointplot(data=datos, x=datos["posx"], y=datos["posy"], hue=datos["result"],
                                         palette=["red", "green"])
        joint_shot_chart.fig.set_size_inches(25, 19.99)
        ax = joint_shot_chart.ax_joint
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_ylim([-2.5, 115])
        ax.set_xlim([0, 150])
        cancha_ACB(ax)
    elif grafico == 4:
        joint_shot_chart = sns.jointplot(data=datos, x="posx", y="posy", kind="hist", color='limegreen')
        joint_shot_chart.fig.set_size_inches(25, 19.99)
        ax = joint_shot_chart.ax_joint
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_ylim(-2.5, 115)
        ax.set_xlim(0, 150)
        cancha_ACB(ax)
    return plt.show()

df_team = df[df['equipo'] == 'Unicaja'].copy()


tiros_equipo(df_team, 4)


df_outzone=df_team[np.sqrt(df_team['posx0']**2+df_team['posy']**2) > 30].copy()
tiros_equipo(df_outzone, 2)
