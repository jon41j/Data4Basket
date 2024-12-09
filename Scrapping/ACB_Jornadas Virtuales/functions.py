import math
import pandas as pd
import mysql.connector
import sqlite3

from variables import *

def conectar_BDD():
    if BBDD_SQL_NUBE == 'oficial':
        conexion = mysql.connector.connect(user='uzfuvo3wnw2qsqgd', password='8g8ndC072WJBeIfwpTzm',
                                host='beostcahrwcz9dae7kmf-mysql.services.clever-cloud.com',
                                database='beostcahrwcz9dae7kmf', port=20228,
                                auth_plugin='mysql_native_password')
    else:
        conexion = mysql.connector.connect(user='ufc7fu3ucxzlwylb', password='9HxeGd083Mt9HfEFrRhR',
                                host='btl1apzm6l0f84vtabdc-mysql.services.clever-cloud.com',
                                database='btl1apzm6l0f84vtabdc', port=3306,
                                auth_plugin='mysql_native_password')
    cursor = conexion.cursor()
    return(conexion, cursor)

def conectar_BDD_2():
    conexion = sqlite3.connect(BBDD_SQL_LOCAL)
    cursor = conexion.cursor()
    return(conexion, cursor)


def comprobarExistPartido(match):
    [conexion, cursor] = conectar_BDD()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM j_matches WHERE id_match = '{}')".format(match))
    rows = cursor.fetchall()
    conexion.commit()
    conexion.close()
    repetido = rows[0][0]
    return(repetido)

def get_image(list_images, type_image):
    img_url = ''
    for img in list_images:
        if img != None:
            if img['type'] == type_image:  
                img_url = str(img['url']) 
    return img_url

def generarListOfTuples_from_ListOfDicts(listOfDicts, listOfKeys):
    listOfTuples = []
    for d in listOfDicts:
        list_tuple = []
        for k in listOfKeys:
            list_tuple.append(d[k]) 
        tuplex = tuple(list_tuple)
        listOfTuples.append(tuplex)
    return listOfTuples


def obtenerSubstitutionsTeam(team, jmatchevents, period):
    substitutions = 0
    rivalSubstitutions = 0
    for me in range(len(jmatchevents)):
        if jmatchevents[me]['id_playbyplaytype'] == 'subsOut':
            if period == 0:
                if jmatchevents[me]['id_team'] == team['id_team']:
                    substitutions = substitutions + 1
                else:
                    rivalSubstitutions = rivalSubstitutions + 1
            else:
                if jmatchevents[me]['period'] == period:
                    if jmatchevents[me]['id_team'] == team['id_team']:
                        substitutions = substitutions + 1
                    else:
                        rivalSubstitutions = rivalSubstitutions + 1
    
    return [substitutions, rivalSubstitutions]



def obtenerPointsAfterAssistsTeam(team, jassistPlayer, period):
    points_afterassist = 0
    points_afterassist_against = 0
    for assist in jassistPlayer:
        if period == 0:
            if assist['id_team'] == team['id_team']:      
                if assist['id_playbyplaytype'] == 't2in':
                    points_afterassist = points_afterassist + 2
                elif assist['id_playbyplaytype'] == 't3in':  
                    points_afterassist = points_afterassist + 3
            else:
                if assist['id_playbyplaytype'] == 't2in':
                    points_afterassist_against = points_afterassist_against + 2
                elif assist['id_playbyplaytype'] == 't3in':  
                    points_afterassist_against = points_afterassist_against + 3
        else:
            if assist['period'] == period:
                if assist['id_team'] == team['id_team']:      
                    if assist['id_playbyplaytype'] == 't2in':
                        points_afterassist = points_afterassist + 2
                    elif assist['id_playbyplaytype'] == 't3in':  
                        points_afterassist = points_afterassist + 3
                else:
                    if assist['id_playbyplaytype'] == 't2in':
                        points_afterassist_against = points_afterassist_against + 2
                    elif assist['id_playbyplaytype'] == 't3in':  
                        points_afterassist_against = points_afterassist_against + 3
    
    return [points_afterassist, points_afterassist_against]



def obtenerPuntosPinturaPlayer(id_player, jshoots, period):
    puntosPintura = 0
    jshoots = pd.DataFrame(jshoots)
    if period == 0:
        jshootsPlayer = jshoots[(jshoots['id_player']==id_player) & (jshoots['id_action']=='t2in')].reset_index()
    else:
        jshootsPlayer = jshoots[(jshoots['id_player']==id_player) & (jshoots['id_action']=='t2in') & (jshoots['period']==period)].reset_index()
    for index, me in jshootsPlayer.iterrows():
        if me['posY'] < 50:
            distanciaTiro = math.sqrt((me['posX']-50)**2 + (me['posY'])**2)
        else:
            distanciaTiro = math.sqrt((me['posX']-50)**2 + (100 - me['posY'])**2)
        
        if distanciaTiro <= 20:
            puntosPintura = puntosPintura + 2
    
    return puntosPintura


def obtenerPuntosTrasAsistenciaPlayer(id_player, jassistPlayer, period):
    points_afterassist = 0
    for assist in jassistPlayer:
        if assist['id_player_shot'] == id_player: 
            if period == 0:     
                if assist['id_playbyplaytype'] == 't2in':
                    points_afterassist = points_afterassist + 2
                elif assist['id_playbyplaytype'] == 't3in':  
                    points_afterassist = points_afterassist + 3
            else:
                if assist['period'] == period:
                    if assist['id_playbyplaytype'] == 't2in':
                        points_afterassist = points_afterassist + 2
                    elif assist['id_playbyplaytype'] == 't3in':  
                        points_afterassist = points_afterassist + 3
    
    return points_afterassist


def obtenerPuntosSegundaOportunidadPlayer(id_player, jmatchevents, period):
    puntos2Oportunidad = 0
    for me in range(len(jmatchevents)):
        if jmatchevents[me]['id_playbyplaytype'] == 'rebO':
            if (jmatchevents[me+1]['id_playbyplaytype'] in ['t2in', 't3in']) and (jmatchevents[me+1]['id_player'] == id_player):
                if period == 0:
                    if jmatchevents[me+1]['id_playbyplaytype'] == 't2in':
                        puntos2Oportunidad = puntos2Oportunidad + 2
                    else:
                        puntos2Oportunidad = puntos2Oportunidad + 3
                else:
                    if jmatchevents[me]['period'] == period:
                        if jmatchevents[me+1]['id_playbyplaytype'] == 't2in':
                            puntos2Oportunidad = puntos2Oportunidad + 2
                        else:
                            puntos2Oportunidad = puntos2Oportunidad + 3
    
    return puntos2Oportunidad


def obtenerPuntosTrasRoboPlayer(id_player, jmatchevents, period):
    puntosTrasRobo = 0
    for me in range(len(jmatchevents)):
        if jmatchevents[me]['id_playbyplaytype'] == 'stl':
            if (jmatchevents[me+1]['id_playbyplaytype'] in ['t2in', 't3in']) and (jmatchevents[me]['id_player'] == id_player):
                if period == 0:
                    if jmatchevents[me+1]['id_playbyplaytype'] == 't2in':
                        puntosTrasRobo = puntosTrasRobo + 2
                    else:
                        puntosTrasRobo = puntosTrasRobo + 3
                else:
                    if jmatchevents[me]['period'] == period:
                        if jmatchevents[me+1]['id_playbyplaytype'] == 't2in':
                            puntosTrasRobo = puntosTrasRobo + 2
                        else:
                            puntosTrasRobo = puntosTrasRobo + 3
    
    return puntosTrasRobo


def obtenerPuntosCAPlayer(id_player, jmatchevents, period):
    puntosCA = 0
    for me in range(len(jmatchevents)):
        if jmatchevents[me]['id_playbyplaytype'] == 'ca2':
                if period == 0:
                    puntosCA = puntosCA + 2
                else:
                    if jmatchevents[me]['period'] == period:
                        puntosCA = puntosCA + 2
        elif jmatchevents[me]['id_playbyplaytype'] == 'ca3':
                if period == 0:
                    puntosCA = puntosCA + 3
                else:
                    if jmatchevents[me]['period'] == period:
                        puntosCA = puntosCA + 3
    
    return puntosCA


def obtenerPuntosPinturaFive(jshoots, id_player, period, minute, second):
    jshootsFive = jshoots[(jshoots['id_player']==id_player) & (jshoots['id_action']=='t2in') & (jshoots['period']==period) & (jshoots['repetido']==False)].iloc[:1]
    puntosPintura = 0
    if jshootsFive.shape[0] > 0:
        for index, me in jshootsFive.iterrows():
            key_shoot = me['key_shoot']
            if me['posY'] < 50:
                distanciaTiro = math.sqrt((me['posX']-50)**2 + (me['posY'])**2)
            else:
                distanciaTiro = math.sqrt((me['posX']-50)**2 + (100 - me['posY'])**2)
            
            if distanciaTiro <= 20:
                puntosPintura = puntosPintura + 2
        jshoots.loc[jshoots['key_shoot'] == key_shoot, 'repetido'] = True
    return [puntosPintura, jshoots]


def coloresTeams (): 
    
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        cursor.execute("UPDATE teams "
                            "SET primary_color  = CASE "
                            "WHEN id_club = 'ACB_22' THEN '#0165BA' "
                            "WHEN id_club = 'ACB_14' THEN '#3D9C35' "
                            "WHEN id_club = 'ACB_12' THEN '#A51A14' "
                            "WHEN id_club = 'ACB_16' THEN '#C8102E' "
                            "WHEN id_club = 'ACB_28' THEN '#E9CD5F' "
                            "WHEN id_club = 'ACB_5' THEN '#FFB718' "
                            "WHEN id_club = 'ACB_592' THEN '#FF1235' "
                            "WHEN id_club = 'ACB_3' THEN '#C8102E' "
                            "WHEN id_club = 'ACB_13' THEN '#FC6C0F' "
                            "WHEN id_club = 'ACB_10' THEN '#D5001E' "
                            "WHEN id_club = 'ACB_25' THEN '#85ADEA' "
                            "WHEN id_club = 'ACB_2' THEN '#154284' "
                            "WHEN id_club = 'ACB_4' THEN '#000000' "
                            "WHEN id_club = 'ACB_8' THEN '#2F8E62' "
                            "WHEN id_club = 'ACB_9' THEN '#FFFFFF' "
                            "WHEN id_club = 'ACB_591' THEN '#F14A49' "
                            "WHEN id_club = 'ACB_657' THEN '#FF5100' "
                            "WHEN id_club = 'ACB_658' THEN '#AB1254' "
                            "END ")
        conexion.commit()
        conexion.close()
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        cursor2.execute("UPDATE teams "
                            "SET primary_color  = CASE "
                            "WHEN id_club = 'ACB_22' THEN '#0165BA' "
                            "WHEN id_club = 'ACB_14' THEN '#3D9C35' "
                            "WHEN id_club = 'ACB_12' THEN '#A51A14' "
                            "WHEN id_club = 'ACB_16' THEN '#C8102E' "
                            "WHEN id_club = 'ACB_28' THEN '#E9CD5F' "
                            "WHEN id_club = 'ACB_5' THEN '#FFB718' "
                            "WHEN id_club = 'ACB_592' THEN '#FF1235' "
                            "WHEN id_club = 'ACB_3' THEN '#C8102E' "
                            "WHEN id_club = 'ACB_13' THEN '#FC6C0F' "
                            "WHEN id_club = 'ACB_10' THEN '#D5001E' "
                            "WHEN id_club = 'ACB_25' THEN '#85ADEA' "
                            "WHEN id_club = 'ACB_2' THEN '#154284' "
                            "WHEN id_club = 'ACB_4' THEN '#000000' "
                            "WHEN id_club = 'ACB_8' THEN '#2F8E62' "
                            "WHEN id_club = 'ACB_9' THEN '#FFFFFF' "
                            "WHEN id_club = 'ACB_591' THEN '#F14A49' "
                            "WHEN id_club = 'ACB_657' THEN '#FF5100' "
                            "WHEN id_club = 'ACB_658' THEN '#AB1254' "
                            "END ")
        conexion2.commit()
        conexion2.close()
    print("Colores Equipos ACB Okey")


def coloresTeams2 (): 
    
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        cursor.execute("UPDATE teams "
                            "SET secondary_color  = CASE "
                            "WHEN id_club = 'ACB_22' THEN '#E3D27A' "
                            "WHEN id_club = 'ACB_14' THEN '#614184' "
                            "WHEN id_club = 'ACB_12' THEN '#262A38' "
                            "WHEN id_club = 'ACB_16' THEN '#570D2C' "
                            "WHEN id_club = 'ACB_28' THEN '#292524' "
                            "WHEN id_club = 'ACB_5' THEN '#062761' "
                            "WHEN id_club = 'ACB_592' THEN '#542F8C' "
                            "WHEN id_club = 'ACB_3' THEN '#404562' "
                            "WHEN id_club = 'ACB_13' THEN '#15255D' "
                            "WHEN id_club = 'ACB_10' THEN '#202B4B' "
                            "WHEN id_club = 'ACB_25' THEN '#FF2D30' "
                            "WHEN id_club = 'ACB_2' THEN '#CBEC88' "
                            "WHEN id_club = 'ACB_4' THEN '#DD2427' "
                            "WHEN id_club = 'ACB_8' THEN '#DE7993' "
                            "WHEN id_club = 'ACB_9' THEN '#FDC912' "
                            "WHEN id_club = 'ACB_591' THEN '#B69785' "
                            "WHEN id_club = 'ACB_657' THEN '#002356' "
                            "WHEN id_club = 'ACB_658' THEN '#EA0E20' "
                            "END ")
        conexion.commit()
        conexion.close()
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        cursor2.execute("UPDATE teams "
                            "SET secondary_color  = CASE "
                            "WHEN id_club = 'ACB_22' THEN '#E3D27A' "
                            "WHEN id_club = 'ACB_14' THEN '#614184' "
                            "WHEN id_club = 'ACB_12' THEN '#262A38' "
                            "WHEN id_club = 'ACB_16' THEN '#570D2C' "
                            "WHEN id_club = 'ACB_28' THEN '#292524' "
                            "WHEN id_club = 'ACB_5' THEN '#062761' "
                            "WHEN id_club = 'ACB_592' THEN '#542F8C' "
                            "WHEN id_club = 'ACB_3' THEN '#404562' "
                            "WHEN id_club = 'ACB_13' THEN '#15255D' "
                            "WHEN id_club = 'ACB_10' THEN '#202B4B' "
                            "WHEN id_club = 'ACB_25' THEN '#FF2D30' "
                            "WHEN id_club = 'ACB_2' THEN '#CBEC88' "
                            "WHEN id_club = 'ACB_4' THEN '#DD2427' "
                            "WHEN id_club = 'ACB_8' THEN '#DE7993' "
                            "WHEN id_club = 'ACB_9' THEN '#FDC912' "
                            "WHEN id_club = 'ACB_591' THEN '#B69785' "
                            "WHEN id_club = 'ACB_657' THEN '#002356' "
                            "WHEN id_club = 'ACB_658' THEN '#EA0E20' "
                            "END ")
        conexion2.commit()
        conexion2.close()
    print("Colores Equipos 2 ACB Okey")


def LogosTeams2(): 
    
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        cursor.execute("UPDATE teams "
                            "SET image_2  = CASE "
                            "WHEN id_club = 'ACB_5' THEN 'https://static.acb.com/img/2/58/5b/75611.png' "
                            "END ")
        conexion.commit()
        conexion.close()
    print("Colores Equipos 2 ACB Okey")


def algortimo_obtenerPlayByPlayType(eventIn, Bool):
    if Bool:
        id_playbyplaytype = eventIn['id_playbyplaytype']
    else:
        id_playbyplaytype = eventIn

    if id_playbyplaytype == 599:
        id_playbyplaytypeRegular = 'subsIn'
        description = 'Substitución (in)'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = 'subsIn_started'
            id_globalPBP_typeD= 'Substitución (in) - Cinco Inicial'
            id_principalPBP_typeID = 'subsIn'
            id_principalPBP_typeD = 'Substitución (in)'
            id_secundaryPBP_typeID = 'started'
            id_secundaryPBP_typeD = 'Cinco Inicial'
    elif id_playbyplaytype == 122:
        id_playbyplaytypeRegular = 'startG'
        description = 'Inicio partido'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 121:
        id_playbyplaytypeRegular = 'start'
        description = 'Inicio cuarto'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 178:
        id_playbyplaytypeRegular = 'jumpWin'
        description = 'Salto ganado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 179:
        id_playbyplaytypeRegular = 'jumpLost'
        description = 'Salto perdido'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 97:
        id_playbyplaytypeRegular = 't2out'
        description = 'Tiro 2pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 104:
        id_playbyplaytypeRegular = 'rebD'
        description = 'Rebote Defensivo'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 93:
        id_playbyplaytypeRegular = 't2in'
        description = 'Tiro 2pt anotado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 159:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 110:
        id_playbyplaytypeRegular = 'foulR'
        description = 'Falta recibida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 105:
        id_playbyplaytypeRegular = 'blockAgainst'
        description = 'Tapón Recibido'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 102:
        id_playbyplaytypeRegular = 'block'
        description = 'Tapón'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 94:
        id_playbyplaytypeRegular = 't3in'
        description = 'Tiro 3pt anotado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 108:
        id_playbyplaytypeRegular = 'ast'
        description = 'Asistencia'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 107:
        id_playbyplaytypeRegular = 'ast'
        description = 'Asistencia'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 160:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 92:
        id_playbyplaytypeRegular = 't1in'
        description = 'Tiro 1pt anotado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 100:
        id_playbyplaytypeRegular = 't2in'
        description = 'Tiro 2pt anotado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 130:
        id_playbyplaytypeRegular = 'ca2'
        description = 'Contraataque 2pt'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 98:
        id_playbyplaytypeRegular = 't3out'
        description = 'Tiro 3pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 101:
        id_playbyplaytypeRegular = 'rebO'
        description = 'Rebote Ofensivo'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 106:
        id_playbyplaytypeRegular = 'turn'
        description = 'Pérdida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 103:
        id_playbyplaytypeRegular = 'stl'
        description = 'Recuperación'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 115:
        id_playbyplaytypeRegular = 'subsOut'
        description = 'Substitución (out)'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 112:
        id_playbyplaytypeRegular = 'subsIn'
        description = 'Substitución (in)'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 135:
        id_playbyplaytypeRegular = 'turn'
        description = 'Pérdida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 161:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 96: 
        id_playbyplaytypeRegular = 't1out'
        description = 'Tiro 1pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 116:
        id_playbyplaytypeRegular = 'end'
        description = 'Fin cuarto'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 162:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 118:
        id_playbyplaytypeRegular = 'timeOut'
        description = 'Tiempo Muerto'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 113:
        id_playbyplaytypeRegular = 'timeOut'
        description = 'Tiempo Muerto'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 598:
        id_playbyplaytypeRegular = 'publico'
        description = 'Público'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 166:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 119:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 405:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 109:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 123:
        id_playbyplaytypeRegular = 'endG'
        description = 'Fin partido'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 134:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 131:
        id_playbyplaytypeRegular = 'ca3'
        description = 'Tiro 3pt anotado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 537:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 132:
        id_playbyplaytypeRegular = 't2out'
        description = 'Tiro 2pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 533:
        id_playbyplaytypeRegular = 't2out'
        description = 'Tiro 2pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 544:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 173:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 540:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 133:
        id_playbyplaytypeRegular = 't3out'
        description = 'Tiro 3pt fallado'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 169:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 543:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 165:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 549:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 513:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 522:
        id_playbyplaytypeRegular = 'stl'
        description = 'Recuperación'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 511:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 512:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 517:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 518:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 519:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 516:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 515:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 514:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 417:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 416:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 408:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 409:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 413:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 414:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 411:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 535:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 520:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 407:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 410:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 200:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 406:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 551:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 163:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 412:
        id_playbyplaytypeRegular = 'IR'
        description = 'Instant Replay'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 547:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 168:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 556:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 545:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 526:
        id_playbyplaytypeRegular = 'firma'
        description = 'Firma'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype in [734, 733, 741, 742, 743, 744, 745, 746, 747, 748,749,475]:
        id_playbyplaytypeRegular = 'ajustesEspeciales'
        description = 'ajustesEspeciales'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 171:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 559:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 541:
        id_playbyplaytypeRegular = 'tec'
        description = 'Técnica'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    elif id_playbyplaytype == 167:
        id_playbyplaytypeRegular = 'foul'
        description = 'Falta cometida'
        if Bool:
            normalized_description= eventIn['type']['normalized_description']
            id_globalPBP_typeID = eventIn['id_playbyplaytype']
            id_globalPBP_typeD= eventIn['type']['description']
            id_principalPBP_typeID = eventIn['id_playbyplaytype']
            id_principalPBP_typeD= eventIn['type']['description']
            id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
            id_secundaryPBP_typeD = eventIn['type']['description']
    else:
        print('PBP DESCONICIDA: ')
        print(' - ID: ', id_playbyplaytype)
        print(' - ID: ', eventIn['type']['description'])
        id_playbyplaytypeRegular = str(eventIn['id_playbyplaytype'])
        description = eventIn['type']['description']
        normalized_description= eventIn['type']['normalized_description']
        id_globalPBP_typeID = eventIn['id_playbyplaytype']
        id_globalPBP_typeD= eventIn['type']['description']
        id_principalPBP_typeID = eventIn['id_playbyplaytype']
        id_principalPBP_typeD= eventIn['type']['description']
        id_secundaryPBP_typeID = eventIn['id_playbyplaytype']
        id_secundaryPBP_typeD = eventIn['type']['description']
    
    if Bool:
        out = {
                    'id': id_playbyplaytype,
                    'id_playbyplaytypeRegular': id_playbyplaytypeRegular, 'description': description, 
                    'normalized_description': normalized_description, 'id_globalPBP_typeID': id_globalPBP_typeID, 
                    'id_globalPBP_typeD': id_globalPBP_typeD, 'id_principalPBP_typeID': id_principalPBP_typeID, 
                    'id_principalPBP_typeD': id_principalPBP_typeD, 'id_secundaryPBP_typeID': id_secundaryPBP_typeID, 
                    'id_secundaryPBP_typeD': id_secundaryPBP_typeD
                }
    else:
        out = {'id': id_playbyplaytype,
               'id_playbyplaytypeRegular': id_playbyplaytypeRegular, 'description': description
        }
    
    return out
