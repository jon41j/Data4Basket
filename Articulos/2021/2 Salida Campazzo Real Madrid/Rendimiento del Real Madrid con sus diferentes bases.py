# Script para obtener el rendimiento del equipo con cada base del Real Madrid

# Importar librerias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from RadarChart import *


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
df_totals['NombreLocal'] = df_totals.NombreLocal.astype(str)
df_totals['NombreVisitante'] = df_totals.NombreVisitante.astype(str)

# Generar panda vacio con las columnas de cada quinteto utilizado por el Real Madrid y sus posibles acciones
df_quintetos = pd.DataFrame(columns=['Jugadores', 'NombresJugadores', 'Rival', 'TiempoJugado', 'canasta2pt', 'fallo2pt', 'canasta3pt', 'fallo3pt',
                                     'canasta1pt', 'fallo1pt', 'off_reb', 'def_reb', 'assist2pt', 'assist3pt', 'assistFault', 'robo', 'perd', 'block',
                                     'blockAgainst', 'mate', 'cta2pt', 'cta3pt', 'ctaFallo2pt', 'ctaFallo3pt', 'ctaFalta', 'ctaPerd', 'faltaRec', 'pers0tl',
                                     'pers1tl', 'pers2tl', 'pers3tl', 'tecnica', 'antideportiva', 'r_canasta2pt', 'r_fallo2pt', 'r_canasta3pt', 'r_fallo3pt',
                                     'r_canasta1pt', 'r_fallo1pt', 'r_off_reb', 'r_def_reb', 'r_assist2pt', 'r_assist3pt', 'r_assistFault', 'r_robo', 'r_perd',
                                     'r_block', 'r_blockAgainst', 'r_mate', 'r_cta2pt', 'r_cta3pt', 'r_ctaFallo2pt', 'r_ctaFallo3pt', 'r_ctaFalta', 'r_ctaPerd',
                                     'r_faltaRec', 'r_pers0tl', 'r_pers1tl', 'r_pers2tl', 'r_pers3tl', 'r_tecnica', 'r_antideportiva'])


# Rellenar panda con todos los quintetos utilizados por el Real Madrid y sus jugadas realizadas
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





# Obtener de todos los quintetos utilizados por el Real Madrid todas las combinaciones de bases posibles y sus estadisticas durante ese tiempo

campazzo = [0]*59
lapro = [0]*59
llull = [0]*59
alocen = [0]*59
campazzo_lapro = [0]*59
campazzo_llull = [0]*59
campazzo_alocen = [0]*59
lapro_llull = [0]*59
lapro_alocen = [0]*59
llull_alocen = [0]*59
campazzo_lapro_llull = [0]*59
campazzo_lapro_alocen = [0]*59
campazzo_llull_alocen = [0]*59
lapro_llull_alocen = [0]*59
campazzo_lapro_llull_alocen = [0]*59
otros = [0]*59
for s in range(len(df_quintetos)):
    #campazzo
    if 20211331 in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        campazzo += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        lapro += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        llull += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        campazzo_lapro += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        campazzo_llull += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        campazzo_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        lapro_llull += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        lapro_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        llull_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 not in df_quintetos.Jugadores[s]:
        campazzo_lapro_llull += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 not in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        campazzo_lapro_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 not in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        campazzo_llull_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 not in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        lapro_llull_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    elif 20211331 in df_quintetos.Jugadores[s] and 20211947 in df_quintetos.Jugadores[s] and 20201774 in df_quintetos.Jugadores[s] and 20210357 in df_quintetos.Jugadores[s]:
        campazzo_lapro_llull_alocen += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])
    else:
        otros += df_quintetos.iloc[s].drop(['Jugadores', 'NombresJugadores', 'Rival'])


# Generar panda con todas las combinaciones de bases utilizadas por el Real Madrid
df_playmakers = pd.DataFrame({'Campazzo': campazzo, 'Laprovittola': lapro, 'Llull': llull, 'Alocén': alocen,
                              'Campazzo + Lapro': campazzo_lapro, 'Campazzo + Llull': campazzo_llull, 'Campazzo + Alocén': campazzo_alocen,
                              'Lapro + Llull': lapro_llull, 'Lapro + Alocén': lapro_alocen, 'Llull + Alocén': llull_alocen,
                              'Campazzo + Lapro + Llull': campazzo_lapro_llull, 'Campazzzo + Lapro + Alocén': campazzo_lapro_alocen,
                              'Campazzo + Llull + Alocén': campazzo_llull_alocen, 'Lapro + Llull + Alocén': lapro_llull_alocen,
                              'Campazzo + Lapro + Llull + Alocén': campazzo_lapro_llull_alocen, 'Otro Base': otros}).T
df_playmakers.columns = ['TiempoJugado', 'canasta2pt', 'fallo2pt', 'canasta3pt', 'fallo3pt',
                                     'canasta1pt', 'fallo1pt', 'off_reb', 'def_reb', 'assist2pt', 'assist3pt', 'assistFault', 'robo', 'perd', 'block',
                                     'blockAgainst', 'mate', 'cta2pt', 'cta3pt', 'ctaFallo2pt', 'ctaFallo3pt', 'ctaFalta', 'ctaPerd', 'faltaRec', 'pers0tl',
                                     'pers1tl', 'pers2tl', 'pers3tl', 'tecnica', 'antideportiva', 'r_canasta2pt', 'r_fallo2pt', 'r_canasta3pt', 'r_fallo3pt',
                                     'r_canasta1pt', 'r_fallo1pt', 'r_off_reb', 'r_def_reb', 'r_assist2pt', 'r_assist3pt', 'r_assistFault', 'r_robo', 'r_perd',
                                     'r_block', 'r_blockAgainst', 'r_mate', 'r_cta2pt', 'r_cta3pt', 'r_ctaFallo2pt', 'r_ctaFallo3pt', 'r_ctaFalta', 'r_ctaPerd',
                                     'r_faltaRec', 'r_pers0tl', 'r_pers1tl', 'r_pers2tl', 'r_pers3tl', 'r_tecnica', 'r_antideportiva']

# Eliminar combinaciones con 0 minutos disputados
df_playmakers = df_playmakers[df_playmakers.TiempoJugado != 0]

# Gráfico barras comparación minutos ACB combinaciones de bases
plt.bar(df_playmakers.index, df_playmakers.TiempoJugado, align='center', alpha=0.8,
        color=['orange' if (x > 60) else 'blue' for x in df_playmakers.TiempoJugado])
plt.xticks(df_playmakers.index, rotation=80)
plt.ylabel('Nº de minutos disputados como base')
plt.title('Distrubición de minutos de los bases del Real Madrid en ACB')
plt.show()

# Nuevo dataFrame con los bases agrupados 
df_playmakers = pd.DataFrame({'Campazzo': campazzo+campazzo_lapro+campazzo_llull, 'Laprovittola': lapro+lapro_llull,
                              'Llull': llull, 'Alocén': alocen+llull_alocen}).T

# Gráfico barras comparación minutos ACB bases agrupados
plt.bar(df_playmakers.index, df_playmakers.TiempoJugado, align='center', alpha=0.8,
        color=['orange' if (x > 150) else 'blue' for x in df_playmakers.TiempoJugado])
plt.xticks(df_playmakers.index, rotation=80)
plt.ylabel('Nº de minutos disputados como base')
plt.title('Distrubición de minutos de los bases del Real Madrid en ACB')
plt.show()

# Generar nuevas columnas en el pandas de bases agrupados con metricas de rendimiento del equipo
df_playmakers['Possessions'] = ((0.96*((df_playmakers['canasta2pt']+df_playmakers['canasta3pt']+df_playmakers['fallo2pt']+df_playmakers['fallo3pt']+df_playmakers['mate']+df_playmakers['blockAgainst']
                               +df_playmakers['cta2pt']+df_playmakers['cta3pt']+df_playmakers['ctaFallo2pt']+df_playmakers['ctaFallo3pt'])+ df_playmakers['perd'] + df_playmakers['ctaPerd'] +0.44*(df_playmakers['canasta1pt']+df_playmakers['fallo1pt'])
                              -df_playmakers['off_reb']) + 0.96*((df_playmakers['r_canasta2pt']+df_playmakers['r_canasta3pt']+df_playmakers['r_fallo2pt']+df_playmakers['r_fallo3pt']+df_playmakers['r_mate']+df_playmakers['r_blockAgainst']
                               +df_playmakers['r_cta2pt']+df_playmakers['r_cta3pt']+df_playmakers['r_ctaFallo2pt']+df_playmakers['r_ctaFallo3pt'])+ df_playmakers['r_perd']+ df_playmakers['r_ctaPerd']+0.44*(df_playmakers['r_canasta1pt']+df_playmakers['r_fallo1pt'])
                              -df_playmakers['r_off_reb']))/2)
df_playmakers['Pace'] = df_playmakers['Possessions']/df_playmakers['TiempoJugado']*40
df_playmakers['AssistRatio'] = (df_playmakers['assist2pt']+df_playmakers['assist3pt']+df_playmakers['assistFault'])*100/((df_playmakers['canasta2pt']+df_playmakers['canasta3pt']+df_playmakers['fallo2pt']+df_playmakers['fallo3pt']+df_playmakers['mate']+df_playmakers['blockAgainst']
                               +df_playmakers['cta2pt']+df_playmakers['cta3pt']+df_playmakers['ctaFallo2pt']+df_playmakers['ctaFallo3pt']+0.44*(df_playmakers['canasta1pt']+df_playmakers['fallo1pt'])) + (df_playmakers['assist2pt']+df_playmakers['assist3pt']+df_playmakers['assistFault'])
                               + df_playmakers['perd'])
df_playmakers['Offensive_Effiency'] = 100*((2*df_playmakers['canasta2pt']+3*df_playmakers['canasta3pt']+2*df_playmakers['mate']+2*df_playmakers['cta2pt']+3*df_playmakers['cta3pt']+df_playmakers['canasta1pt'])/df_playmakers['Possessions'])
df_playmakers['Deffensive_Effiency'] = 100*((2*df_playmakers['r_canasta2pt']+3*df_playmakers['r_canasta3pt']+2*df_playmakers['r_mate']+2*df_playmakers['r_cta2pt']+3*df_playmakers['r_cta3pt']+df_playmakers['r_canasta1pt'])/df_playmakers['Possessions'])

df_playmakers['EffectiveFieldGoalPercentage'] = 100*((df_playmakers['canasta2pt']+df_playmakers['canasta3pt']+df_playmakers['mate']+df_playmakers['cta2pt']+df_playmakers['cta3pt'])+0.5*(df_playmakers['canasta3pt']+df_playmakers['cta3pt']))/(df_playmakers['canasta2pt']+
                                              df_playmakers['canasta3pt']+df_playmakers['fallo2pt']+df_playmakers['fallo3pt']+df_playmakers['mate']+df_playmakers['blockAgainst']+df_playmakers['cta2pt']+df_playmakers['cta3pt']+df_playmakers['ctaFallo2pt']+df_playmakers['ctaFallo3pt'])

df_playmakers['TurnoverRatio'] = 100*(df_playmakers['perd']+ df_playmakers['ctaPerd'])/df_playmakers['Possessions']

df_playmakers['3pointRatio'] = 100*(df_playmakers['canasta3pt']+df_playmakers['fallo3pt']+df_playmakers['cta3pt']+df_playmakers['ctaFallo3pt'])/df_playmakers['Possessions']

df_playmakers['FreeThrowRate'] = 100*(df_playmakers['canasta1pt']+df_playmakers['fallo1pt'])/(df_playmakers['canasta2pt']+df_playmakers['canasta3pt']+df_playmakers['fallo2pt']+df_playmakers['fallo3pt']+df_playmakers['mate']+df_playmakers['blockAgainst']
                               +df_playmakers['cta2pt']+df_playmakers['cta3pt']+df_playmakers['ctaFallo2pt']+df_playmakers['ctaFallo3pt'])

df_playmakers['Points_Difference_per_Game'] = 40*((2*df_playmakers['canasta2pt']+3*df_playmakers['canasta3pt']+2*df_playmakers['mate']+2*df_playmakers['cta2pt']+3*df_playmakers['cta3pt']+df_playmakers['canasta1pt'])-(2*df_playmakers['r_canasta2pt']+3*df_playmakers['r_canasta3pt']+2*df_playmakers['r_mate']+2*df_playmakers['r_cta2pt']+3*df_playmakers['r_cta3pt']+df_playmakers['r_canasta1pt']))/df_playmakers['TiempoJugado']



# NuevoDataFrame solo con las columnas interesantes para la comparación:

df_playmakersACB = df_playmakers[['TiempoJugado', 'Possessions', 'Pace', 'AssistRatio', 'Offensive_Effiency', 'Deffensive_Effiency',
                                 'EffectiveFieldGoalPercentage', 'TurnoverRatio', '3pointRatio', 'FreeThrowRate', 'Points_Difference_per_Game']]


# Radar plotting para comparar estas metricas del rendimiento del equipo com los diferentes bases
fig1 = plt.figure(figsize=(4, 6))
variables = ('Pace', 'Offensive Efficiency', 'Deffensive Efficiency',
             'Difference per Game', '%EFGP', 'Assist Ratio',
             'Turnover Ratio', '3pt Ratio', 'FT Ratio')
ranges = [(75, 85), (90, 132.5), (122.5, 80), (-17.5, 30), (45, 65), (7.5, 20), (10, 22.5), (30, 45), (20, 45)]
radar = ComplexRadar(fig1, variables, ranges)
for p in range(len(df_playmakersACB)):
    legend = df_playmakersACB.index[p]
    data = [df_playmakersACB.Pace[p], df_playmakersACB.Offensive_Effiency[p],df_playmakersACB.Deffensive_Effiency[p],
                 df_playmakersACB.Points_Difference_per_Game[p],df_playmakersACB.EffectiveFieldGoalPercentage[p],df_playmakersACB.AssistRatio[p],
                 df_playmakersACB.TurnoverRatio[p], df_playmakersACB['3pointRatio'][p],df_playmakersACB.FreeThrowRate[p]]
    radar.plot(data, legend)
    radar.fill(data, alpha=0.2)
plt.title('Comparación métricas avanzadas entre bases - ACB')
plt.show()

