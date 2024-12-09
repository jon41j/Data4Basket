from functions import *
import datetime
import pandas as pd
import numpy as np

from variables import *


def gen_competicion(info):
    key_competition = str(info['id_competition']) + '_' + str(info['id_edition'])
    competition = {'key_competition': key_competition,
                   'id_competition': str(info['id_competition']), 'name': info['competition']['official_name'].strip(),
                    'id_edition': str(info['id_edition']),  'year': YEAR_EDICION,
                    'id_phase': str(info['phase']['id']), 'phase_name': info['phase']['description'].strip(),
                    'category': 1, 'country': 'Spain',
                    'gender': 'Male',
                    'image': info['competition']['url_image'].strip(), 'image_2': info['competition']['url_image_negative'].strip()}
    return (competition)


def gen_arena(info):
    arena = {'id_arena': info['id_arena'], 'name': info['arena']['name'].strip().replace("'", ""),
             'town': info['arena']['town'].strip(), 'country': 'Spain',
             'image1': info['team1']['club']['media'][0]['url']}
    return (arena)


def gen_equipo(infoTeam, competition):
    imageLogoTrans = get_image(infoTeam['club']['media'], "logo_negativo")
    imageLogo = get_image(infoTeam['club']['media'], "logo")
    team = {'id_club': 'ACB_'+str(infoTeam['id_club']), 'id_team': ACB_PRE+str(infoTeam['id']), 'year': YEAR_EDICION,
            'short_team_name': infoTeam['team_actual_short_name'], 'abrev_name': infoTeam['team_abbrev_name'], 'team_name': infoTeam['team_actual_name'],
            'gender': 'Male', 'country': 'Spain',
            'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'],
            'key_competition': competition['key_competition'],
            'image': imageLogoTrans, 'image_2': imageLogo}
    return (team)



def gen_referee(list_infoReferees):
    list_referees_out = []
    for ref in list_infoReferees:
        list_referees_out.append(
            {
                'id_referee': 'ACB_'+ str(ref['license']['id_person']), 'id_person': str(ref['license']['id_person']),
                'name': str(ref['license']['licenseStr15']), 'name_nick': str(ref['license']['licenseNick']),
                'nacionality': 'Spain', 'gender': 'Male',
                'license': ref['license_policy']
            }
        )   
    return (list_referees_out)


def gen_coach(list_infoCoaches, team, competition):
    list_coaches_out = []
    for coach in list_infoCoaches:
        if coach['id_License_subtype'] == 8:
            coachtype = 'Principal'
        else:
            coachtype = 'Ayudante'
        list_coaches_out.append(
            {
                'id_coach': team['id_team'] + '_'+ str(coach['license']['id_person']), 'id_person': 'ACB_' + str(coach['license']['id_person']),
                'name': str(coach['license']['licenseStr15']), 'name_nick': str(coach['license']['licenseNick']),
                'coachtype': coachtype, 'id_team': team['id_team'], 'id_competition': competition['id_competition'],
                'id_edition': competition['id_edition']
            }
        )   
    return (list_coaches_out)


def gen_jmatch(info, team1, team2, list_referees, competition, id_match, statDate, arena):
    jmatch = {'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 
              'id_match': id_match, 'num_match': info['id'],
              'matchWeek': info['matchweek_number'], 'matchWeek_description': info['matchweek_descriptor'],
              'start_date': statDate, 
              'id_arena': arena['id_arena'],'crowd': info['crowd'],
              'id_localteam': team1['id_team'], 'local_points': info['local_points'],
              'id_visitorteam': team2['id_team'], 'visitor_points': info['visitor_points'],
              'id_referee1': list_referees[0]['id_referee'], 'id_referee2': list_referees[1]['id_referee'], 'id_referee3': list_referees[2]['id_referee']}
    return (jmatch)


def gen_player(listPlayers, competition):
    list_players_out=[]
    for player in listPlayers:
        id_team = ACB_PRE+str(player['id_team'])
        if player['license'] != None:
            id_player = id_team + '_' + str(player['license']['id'])

            imageCuerpo = get_image(player['license']['media'], "foto_cuerpo")
            imageCara = get_image(player['license']['media'], "foto_de_cara")

            list_players_out.append({
                'id_player': id_player, 'id_person': 'ACB_' + str(player['license']['id']),
                'name': str(player['license']['licenseStr15']), 'name_nick': str(player['license']['licenseNick']),
                'gender': 'Male', 'dorsal': player['pno'],
                'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'],
            'key_competition': competition['key_competition'],
                'id_team': id_team,
                'image': imageCuerpo, 'image_2': imageCara
            })
    return (list_players_out)


def gen_jteamStats(teamStats, visitorStats, team, visitor, competition, id_match, startDate, info, jmatchevents, jassistPlayer, period):
    lado = 'Local' if teamStats['is_local'] else 'Visitante'
    if period == 0:
        periodD = '0 - Todos'
    elif period == 1:     
        periodD = '1º Cuarto'
    elif period == 2:     
        periodD = '2º Cuarto'
    elif period == 3:     
        periodD = '3º Cuarto'
    elif period == 4:     
        periodD = '4º Cuarto'
    elif period == 5:     
        periodD = 'Prórroga'
    elif period == 6:     
        periodD = 'Prórroga'
    elif period == 7:     
        periodD = 'Prórroga'
    elif period == 8:     
        periodD = 'Prórroga'
    elif period == 9:     
        periodD = 'Prórroga'       
    else:     
        periodD = 'Prórroga'

    if lado== 'Local':
        difference = info['local_points'] - info['visitor_points']
    else:
        difference = info['visitor_points'] - info['local_points']

    if difference > 0:
        result = 1
        resultD = 'Victoria'
    else:
        result = 0
        resultD = 'Derrota'

    differencePeriod = teamStats['points'] - visitorStats['points']
    if differencePeriod > 0:
        resultPeriod = 1
        resultPeriodD = 'Victoria'
    else:
        resultPeriod = 0
        resultPeriodD = 'Derrota'

    if teamStats['2pt_tried'] == 0:
        pt2_percentage = 0
    else:
        pt2_percentage = round(teamStats['2pt_success'] / teamStats['2pt_tried'], 2)
    if teamStats['3pt_tried'] == 0:
        pt3_percentage = 0
    else:
        pt3_percentage = round(teamStats['3pt_success'] / teamStats['3pt_tried'], 2)
    if teamStats['1pt_tried'] == 0:
        pt1_percentage = 0
    else:
        pt1_percentage = round(teamStats['1pt_success'] / teamStats['1pt_tried'], 2)

    
    if visitorStats['2pt_tried'] == 0:
        rival_pt2_percentage = 0
    else:
        rival_pt2_percentage = round(visitorStats['2pt_success'] / visitorStats['2pt_tried'], 2)
    if visitorStats['3pt_tried'] == 0:
        rival_pt3_percentage = 0
    else:
        rival_pt3_percentage = round(visitorStats['3pt_success'] / visitorStats['3pt_tried'], 2)
    if visitorStats['1pt_tried'] == 0:
        rival_pt1_percentage = 0
    else:
        rival_pt1_percentage = round(visitorStats['1pt_success'] / visitorStats['1pt_tried'], 2)

    [substitutions, rivalSubstitutions] = obtenerSubstitutionsTeam(team, jmatchevents, period)
    [points_afterassist, points_afterassist_against] = obtenerPointsAfterAssistsTeam(team, jassistPlayer, period)

    jteamStats = {'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                  'id_match': id_match, 'id_team': team['id_team'], 'start_date': startDate, 
                  'rival_id_team': visitor['id_team'], 'rival_team_name': visitor['short_team_name'], 
                  'crowd': info['crowd'], 'period': period, 'periodD': periodD, 'lado': lado, 'time_played': teamStats['time_played'],
                  'points': teamStats['points'], 'rival_points': visitorStats['points'], 'difference': difference,
                  'differencePeriod': differencePeriod, 
                  'pt2_success': teamStats['2pt_success'], 'pt2_tried': teamStats['2pt_tried'], 'pt2_percentage': pt2_percentage,
                  'pt3_success': teamStats['3pt_success'], 'pt3_tried': teamStats['3pt_tried'], 'pt3_percentage': pt3_percentage,
                  'pt1_success': teamStats['1pt_success'], 'pt1_tried': teamStats['1pt_tried'], 'pt1_percentage': pt1_percentage,
                  'deffensive_rebound': teamStats['defensive_rebound'], 'offensive_rebound': teamStats['offensive_rebound'], 
                  'total_rebound': teamStats['total_rebound'], 'assists': teamStats['asis'],
                  'steals': teamStats['steals'], 'turnovers': teamStats['turnovers'],
                  'dunks': teamStats['dunks'], 'blocks': teamStats['blocks'],
                  'received_blocks': teamStats['received_blocks'], 'personal_fouls': teamStats['personal_fouls'],
                  'received_fouls': teamStats['received_fouls'], 'val': teamStats['val'],
                  'timeouts': teamStats['timeouts'],'substitutions': substitutions,
                  'max_difference': teamStats['maximun_difference'], 'minute_max_difference': np.nan, 	
                  'max_difference_against': visitorStats['time_played'], 'minute_max_difference_against': np.nan, 
                  'leader_changes': teamStats['leader_changes'], 'time_as_leader': teamStats['time_as_leader'], 
                  'time_losing': visitorStats['time_as_leader'], 'best_streak': teamStats['best_streak'], 
                  'best_streak_against': visitorStats['best_streak'], 'bench_points': teamStats['bench_points'],
                  'starters_points': teamStats['points']-teamStats['bench_points'], 'points_fastbreak': teamStats['counter_attack'], 
                  'points_fastbreak_against': visitorStats['counter_attack'], 'points_aftersteal': teamStats['points_after_steal'],
                  'points_aftersteal_against': visitorStats['points_after_steal'], 'points_afterassist': points_afterassist,
                  'points_afterassist_against': points_afterassist_against, 'points_secondchance': teamStats['second_opportinity_points'],
                  'points_secondchance_against': visitorStats['second_opportinity_points'], 'points_in_the_paint': teamStats['points_in_the_paint'], 
                  'points_in_the_paint_against': visitorStats['points_in_the_paint'], 'bench_assists': np.nan,
                  'starters_assists': np.nan, 'bench_steals': np.nan,
                  'starters_steals': np.nan, 'bench_turnovers': np.nan,
                  'starters_turnovers': np.nan,
                  'bench_assists_against': np.nan, 'starters_assists_against': np.nan,
                  'bench_steals_against': np.nan, 'starters_steals_against': np.nan,
                  'bench_turnovers_against': np.nan, 'starters_turnovers_against': np.nan,
                  'rival_2pt_success': visitorStats['2pt_success'], 'rival_2pt_tried': visitorStats['2pt_tried'], 'rival_2pt_percentage': rival_pt2_percentage,
                  'rival_3pt_success': visitorStats['3pt_success'], 'rival_3pt_tried': visitorStats['3pt_tried'], 'rival_3pt_percentage': rival_pt3_percentage,
                  'rival_1pt_success': visitorStats['1pt_success'], 'rival_1pt_tried': visitorStats['1pt_tried'], 'rival_1pt_percentage': rival_pt1_percentage,
                  'rival_deffensive_rebound': visitorStats['defensive_rebound'],  'rival_offensive_rebound': visitorStats['offensive_rebound'],
                  'rival_total_rebound': visitorStats['total_rebound'], 'rival_assists': visitorStats['asis'],
                  'rival_steals': visitorStats['steals'], 'rival_turnovers': visitorStats['turnovers'],
                  'rival_dunks': visitorStats['dunks'], 'rival_val': visitorStats['val'],
                  'rival_timeouts': visitorStats['timeouts'], 'rival_substitutions': rivalSubstitutions,
                  'rival_bench_points': visitorStats['bench_points'], 'rival_starters_points': visitorStats['points']-visitorStats['bench_points'],
                  'overtime': info['period']-4, 'result': result,
                  'resultD': resultD, 'resultPeriod': resultPeriod, 'resultPeriodD': resultPeriodD}
    return (jteamStats)

                    	
def gen_jplayerStats(playersStats, competition, id_match, startDate, info, team1, jmatchevents, jassistPlayer, jshoots, period):
    if period == 0:
        periodD = '0 - Todos'
    elif period == 1:     
        periodD = '1º Cuarto'
    elif period == 2:     
        periodD = '2º Cuarto'
    elif period == 3:     
        periodD = '3º Cuarto'
    elif period == 4:     
        periodD = '4º Cuarto'
    elif period == 5:     
        periodD = 'Prórroga'
    elif period == 6:     
        periodD = 'Prórroga'
    elif period == 7:     
        periodD = 'Prórroga'
    elif period == 8:     
        periodD = 'Prórroga'
    elif period == 9:     
        periodD = 'Prórroga'       
    else:     
        periodD = 'Prórroga'

    jplayerStats=[]
    for playerStats in playersStats:
        id_team = ACB_PRE+ str(playerStats['id_team'])
        id_player = id_team + '_' + str(playerStats['id_license'])

        if id_team == team1['id_team']:
            lado = 'Local'
            difference = info['local_points'] - info['visitor_points']      
            rival_team_name = info['team2']['team_actual_name']
        else:
            lado = 'Visitante'
            difference = info['visitor_points'] - info['local_points']
            rival_team_name = info['team1']['team_actual_name']
        
        if difference > 0:
            resultPeriod = 1
            resultPeriodD = 'Victoria'
        else:
            resultPeriod = 0
            resultPeriodD = 'Derrota'

        if playerStats['2pt_tried'] == 0:
            pt2_percentage = 0
        else:
            pt2_percentage = round(playerStats['2pt_success'] / playerStats['2pt_tried'], 2)
        if playerStats['3pt_tried'] == 0:
            pt3_percentage = 0
        else:
            pt3_percentage = round(playerStats['3pt_success'] / playerStats['3pt_tried'], 2)
        if playerStats['1pt_tried'] == 0:
            pt1_percentage = 0
        else:
            pt1_percentage = round(playerStats['1pt_success'] / playerStats['1pt_tried'], 2)

        
        puntosPintura = obtenerPuntosPinturaPlayer(id_player, jshoots, period)
        puntos2Oportunidad = obtenerPuntosSegundaOportunidadPlayer(id_player, jmatchevents, period)
        puntosTrasRobo = obtenerPuntosTrasRoboPlayer(id_player, jmatchevents, period)
        puntosCA = obtenerPuntosCAPlayer(id_player, jmatchevents, period)
        puntosTrasAsistencia = obtenerPuntosTrasAsistenciaPlayer(id_player, jassistPlayer, period)

        key_playerstat = id_player + '_' + id_match + '_p' + str(period)

        jplayerStats.append({})
        jplayerStats[-1] = {'key_playerstat': key_playerstat,
                            'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
            'key_competition': competition['key_competition'],
                       	'id_match': id_match,
                       	'id_team': id_team,
                       	'id_player': id_player,
                        'start_date': startDate,
                       	'period': period,
                        'periodD': periodD,
                        'lado': lado,
                       	'sstarting': playerStats['starting'],
                       	'finishing': playerStats['playing'],
                       	'time_played': playerStats['time_played'],
                       	'points': playerStats['points'],
                       	'pt2_success': playerStats['2pt_success'],
                       	'pt2_tried': playerStats['2pt_tried'],
                       	'pt2_percentage': pt2_percentage,
                       	'pt3_success': playerStats['3pt_success'],
                       	'pt3_tried': playerStats['3pt_tried'],
                       	'pt3_percentage': pt3_percentage,
                       	'pt1_success': playerStats['1pt_success'],
                       	'pt1_tried': playerStats['1pt_tried'],
                       	'pt1_percentage': pt1_percentage,
                       	'deffensive_rebound': playerStats['defensive_rebound'],
                       	'offensive_rebound': playerStats['offensive_rebound'],
                       	'total_rebound': playerStats['total_rebound'],
                       	'assists': playerStats['asis'],
                       	'steals': playerStats['steals'],
                       	'turnovers': playerStats['turnovers'],
                       	'dunks': playerStats['dunks'],
                       	'counter_attacks': playerStats['counter_attack'],
                       	'blocks': playerStats['blocks'],
                       	'received_blocks': playerStats['received_blocks'],
                       	'personal_fouls': playerStats['personal_fouls'],
                       	'received_fouls': playerStats['received_fouls'],
                       	'disqualified': playerStats['disqualified'],
                       	'difference': difference,
                        'differencePlayer': playerStats['differential'],
                       	'val': playerStats['val'],
                        'points_fast_break': puntosCA,
                       	'points_in_the_paint': puntosPintura,
                        'points_second_chance': puntos2Oportunidad,
                        'points_aftersteal': puntosTrasRobo,
                        'points_afterassist': puntosTrasAsistencia,
                        'rival_team_name': rival_team_name,
                    	'result': resultPeriod,
                        'resultD': resultPeriodD}
    return (jplayerStats)


def gen_jmarkerbreakdown(markerbreakdownInfo, idMatch, competition, startDate, info, team1, team2, jmatchevents):
    jmarkerbreakdownLocal=[]
    jmarkerbreakdownVisitor = []

    jmatchevents = pd.DataFrame(jmatchevents)

    difference = info['local_points'] - info['visitor_points'] 

    if difference > 0:
        resultPeriodLocal = 1
        resultPeriodDLocal = 'Victoria'
        resultPeriodVisitor = 0
        resultPeriodDVisitor = 'Derrota'
    else:
        resultPeriodLocal = 0
        resultPeriodDLocal = 'Derrota'
        resultPeriodVisitor = 1
        resultPeriodDVisitor = 'Victoria'

    for m in markerbreakdownInfo:
        jmarkerbreakdownLocal.append({})
        jmarkerbreakdownVisitor.append({})

        period = m['period']

        if period == 0:
            periodD = '0 - Todos'
        elif period == 1:     
            periodD = '1º Cuarto'
        elif period == 2:     
            periodD = '2º Cuarto'
        elif period == 3:     
            periodD = '3º Cuarto'
        elif period == 4:     
            periodD = '4º Cuarto'
        elif period == 5:     
            periodD = 'Prórroga'
        elif period == 6:     
            periodD = 'Prórroga'
        elif period == 7:     
            periodD = 'Prórroga'
        elif period == 8:     
            periodD = 'Prórroga'
        elif period == 9:     
            periodD = 'Prórroga'       
        else:     
            periodD = 'Prórroga'
    
        localTeam = team1['id_team']
        visitorTeam = team2['id_team']

        posesionLocal = 0
        posesionVisitor = 0

        jmatcheventsMinute = jmatchevents[(jmatchevents['period'] == period) & (jmatchevents['minute'] == (m['minute']-1))].reset_index()

        for me in range(len(jmatcheventsMinute)):
            if jmatcheventsMinute['id_playbyplaytype'][me] in ['t2in', 't2out', 't3in', 't3out', 'turn']:
                if jmatcheventsMinute['id_team'][me] == localTeam:
                    posesionLocal = posesionLocal + 1
                elif jmatcheventsMinute['id_team'][me] == visitorTeam:
                    posesionVisitor = posesionVisitor + 1
            elif jmatcheventsMinute['id_playbyplaytype'][me] == 'rebO':
                if jmatcheventsMinute['id_team'][me] == localTeam:
                    posesionLocal = posesionLocal - 1
                elif jmatcheventsMinute['id_team'][me] == visitorTeam:
                    posesionVisitor = posesionVisitor - 1
            elif jmatcheventsMinute['id_playbyplaytype'][me] in ['t1in', 't1out', 't1'] and jmatcheventsMinute['id_playbyplaytype'][me-1] not in ['t1in', 't1out', 't1']:
                try:
                    if jmatcheventsMinute['id_playbyplaytype'][me+1] in ['t1in', 't1out', 't1']:
                        if jmatcheventsMinute['id_team'][me] == localTeam:
                            posesionLocal = posesionLocal + 1
                        elif jmatcheventsMinute['id_team'][me] == visitorTeam:
                            posesionVisitor = posesionVisitor + 1
                except:
                    True

        minute = 10*period - m['minute']

        jmarkerbreakdownLocal[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                                   'id_match': idMatch, 'id_team': localTeam, 'period': period, 'periodD': periodD,'lado': 'Local',
                                    'result': resultPeriodLocal, 'resultD': resultPeriodDLocal, 'startDate': startDate, 'minute':minute, 'second': 0,
                                    'scoreTeam': m['scoreLocal'], 'scoreRivalTeam': m['scoreVisitor'],
                                    'score_differential':  m['scoreLocal'] -  m['scoreVisitor'],
                                    'posesions': posesionLocal}
    

        jmarkerbreakdownVisitor[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                                   'id_match': idMatch, 'id_team': visitorTeam, 'period': period, 'periodD': periodD,'lado': 'Visitante',
                                    'result': resultPeriodVisitor, 'resultD': resultPeriodDVisitor, 'startDate': startDate, 'minute':minute, 'second': 0,
                                    'scoreTeam': m['scoreVisitor'], 'scoreRivalTeam': m['scoreLocal'],
                                    'score_differential':  m['scoreVisitor'] -  m['scoreLocal'],
                                    'posesions': posesionVisitor}

    return([jmarkerbreakdownLocal, jmarkerbreakdownVisitor])



def gen_jshoots(shootsInfo, competition, id_match, startDate, team1, info):

    jshoots = []
    Nshot = 0
    for shoot in shootsInfo:
        TL = False
        Nshot = Nshot + 1
        if (shoot['id_playbyplaytype'] == 92) or (shoot['id_playbyplaytype'] == 96):
            TL = True #TL
        elif shoot['id_playbyplaytype'] == 100:
            # Mate
            posX = 50
            posY = 1
        else:
            posX = round(shoot['posY']/1000*50/7.5, 1) + 50
            posY = round(shoot['posX']/1000*50/10.75, 1)
            if posX > 100:
                posX = 100
            elif posX < 0:
                posX = 0
            if posY > 49.5:
                posY = 49.5
            elif posY < 0:
                posY = 0
        
        period = shoot['period']
        if period == 0:
            periodD = '0 - Todos'
        elif period == 1:     
            periodD = '1º Cuarto'
        elif period == 2:     
            periodD = '2º Cuarto'
        elif period == 3:     
            periodD = '3º Cuarto'
        elif period == 4:     
            periodD = '4º Cuarto'
        elif period == 5:     
            periodD = 'Prórroga'
        elif period == 6:     
            periodD = 'Prórroga'
        elif period == 7:     
            periodD = 'Prórroga'
        elif period == 8:     
            periodD = 'Prórroga'
        elif period == 9:     
            periodD = 'Prórroga'       
        else:     
            periodD = 'Prórroga'

        out_id_action = algortimo_obtenerPlayByPlayType(shoot['id_playbyplaytype'], False)
        id_action = out_id_action['id_playbyplaytypeRegular']
        action = out_id_action['description']

        if 'in' in id_action:
            result = 1
        else:
            result = 0

        id_team = ACB_PRE+ str(shoot['id_team'])
        difference = info['local_points'] - info['visitor_points'] 
        if id_team == team1['id_team']:
            lado = 'Local'
            if difference > 0:
                resultD = 'Victoria'
                resultPartido = 1
            else:
                resultD = 'Derrota'
                resultPartido = 0
        else:
            lado = 'Visitante'
            if difference > 0:
                resultD = 'Derrota'
                resultPartido = 0
            else:
                resultD = 'Victoria'
                resultPartido = 1

        if not TL:
            id_shoot = str(id_match) + '_S' + str(Nshot)
            id_player = id_team + '_' + str(shoot['license']['id'])
            key_shoot = id_player + id_shoot + '_p' + str(period)
            jshoots.append({})
            jshoots[-1] = {'key_shoot': key_shoot,
                           'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'],
            'key_competition': competition['key_competition'], 'id_phase': competition['id_phase'],
                            'id_match': id_match, 'id_shoot': id_shoot, 'id_team': id_team,
                            'id_player': id_player, 'start_date': startDate, 'lado': lado,
                            'period': period, 'periodD': periodD, 'minute': 0, 'second': 0,
                            'score_local': 0, 'score_visitor': 0, 'id_action': id_action, 'action': action,
                            'result': result, 'posX': posX, 'posY': posY,
                            'fastbreak': 0, 'aftersteal': 0, 'secondchance': 0, 'zone': 0,
                            'resultD': resultD}
    return(jshoots)



def gen_jmatchevents(eventsInfo, competition, id_match, startDate):
    jplaybyplay = []
    playbyplaytypes = []
    id_playbyplaytypes = []
    previous_action = 'firstAction'
    for eventNum in range(len(eventsInfo)):
        eventIn = eventsInfo[eventNum]
        out_algortimo = algortimo_obtenerPlayByPlayType(eventIn, True)
        id_playbyplaytypeRegular = out_algortimo['id_playbyplaytypeRegular']
        description = out_algortimo['description']
        normalized_description = out_algortimo['normalized_description']
        id_globalPBP_typeID = out_algortimo['id_globalPBP_typeID']
        id_globalPBP_typeD = out_algortimo['id_globalPBP_typeD']
        id_principalPBP_typeID = out_algortimo['id_principalPBP_typeID']
        id_principalPBP_typeD = out_algortimo['id_principalPBP_typeD']
        id_secundaryPBP_typeID = out_algortimo['id_secundaryPBP_typeID']
        id_secundaryPBP_typeD = out_algortimo['id_secundaryPBP_typeD']

        try:
            name_player = eventIn['license']['licenseNick']
        except:
            name_player = ''

        jplaybyplay.append({})
        jplaybyplay[-1] = {'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                           'id_match': id_match, 'start_date': startDate, 'id_event': eventNum+1, 'period': eventIn['period'], 'minute': eventIn['minute'],
                    	   'second': eventIn['second'], 'score_local': eventIn['score_local'], 'score_visitor': eventIn['score_visitor'], 
                           'id_team': ACB_PRE+str(eventIn['id_team']), 'id_player': ACB_PRE+str(eventIn['id_team']) + '_' + str(eventIn['id_license']),
                           'name_player': name_player,
                    	   'id_playbyplaytype': id_playbyplaytypeRegular, 'id_globalPBP_typeID': id_globalPBP_typeID, 'id_principalPBP_typeID': id_principalPBP_typeID,
                           'id_secundaryPBP_typeID': id_secundaryPBP_typeID, 'wall_clock': 0, 'previous_action': previous_action}
        previous_action = id_playbyplaytypeRegular

        if id_playbyplaytypeRegular not in id_playbyplaytypes:
            id_playbyplaytypes.append(id_playbyplaytypeRegular)
            playbyplaytypes.append({})
            playbyplaytypes[-1] = {'id_playbyplaytype': id_playbyplaytypeRegular, 'description': description, 'normalized_description': normalized_description, 
                                   'id_globalPBP_typeID': id_globalPBP_typeID, 'id_globalPBP_typeD': id_globalPBP_typeD, 'id_principalPBP_typeID': id_principalPBP_typeID, 
                                   'id_principalPBP_typeD': id_principalPBP_typeD, 'id_secundaryPBP_typeID': id_secundaryPBP_typeID, 
                                   'id_secundaryPBP_typeD': id_secundaryPBP_typeD}

    return(jplaybyplay, playbyplaytypes)



def gen_jminutesPlayer(player, jmatchevents, id_match, competition, startDate, team1, info):

    if len(jmatchevents) > 0:

        id_team = player['id_team']
        difference = info['local_points'] - info['visitor_points'] 
        if id_team == team1['id_team']:
            lado = 'Local'
            if difference > 0:
                resultD = 'Victoria'
                result = 1
            else:
                resultD = 'Derrota'
                result = 0
        else:
            lado = 'Visitante'
            if difference > 0:
                resultD = 'Derrota'
                result = 0
            else:
                resultD = 'Victoria'
                result = 1


        jminutesPlayer = []

        cuarto1Minuto = 9
        cuarto2Minuto = 9
        cuarto3Minuto = 9
        cuarto4Minuto = 9
        cuarto5Minuto = 4
        
        iDplayer = player['id_player']
        nameplayer = player['name']
        playerIn = 0
        playerTemp = 0
        for me in range(len(jmatchevents)):
            if jmatchevents[me]['id_player'] == iDplayer: 
                if jmatchevents[me]['id_playbyplaytype'] == 'subsIn':
                    playerTemp = 1
                    if jmatchevents[me]['minute'] == 10:
                        playerIn = 1
                    else:
                        playerIn = 0.5
                elif jmatchevents[me]['id_playbyplaytype'] == 'subsOut':
                    playerTemp = 2
                    if jmatchevents[me]['minute'] == 10:
                        playerIn = 0
                    else:
                        playerIn = 0.5

            if jmatchevents[me]['period'] == 1:
                if jmatchevents[me]['minute'] == cuarto1Minuto and cuarto1Minuto > -1:
                    minute = 9 - cuarto1Minuto
                    cuarto1Minuto = cuarto1Minuto -1
                    jminutesPlayer.append({})
                    jminutesPlayer[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player': iDplayer, 'name_player': nameplayer, 'period': 1, 'periodD': '1º Cuarto',
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute':minute, 'second': 0,
                                        'playIn': playerIn}
                    if playerTemp == 1:
                        playerTemp = 0
                        playerIn = 1
                    elif playerTemp == 2:
                        playerTemp = 0
                        playerIn = 0

            if jmatchevents[me]['period'] == 2:
                if jmatchevents[me]['minute']  == cuarto2Minuto and cuarto2Minuto > -1:
                    minute = 19 - cuarto2Minuto
                    cuarto2Minuto = cuarto2Minuto -1
                    jminutesPlayer.append({})
                    jminutesPlayer[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player': iDplayer, 'name_player': nameplayer, 'period': 2, 'periodD': '2º Cuarto',
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute':minute, 'second': 0,
                                        'playIn': playerIn}
                    if playerTemp == 1:
                        playerTemp = 0
                        playerIn = 1
                    elif playerTemp == 2:
                        playerTemp = 0
                        playerIn = 0

            if jmatchevents[me]['period'] == 3:
                if jmatchevents[me]['minute'] == cuarto3Minuto and cuarto3Minuto > -1:
                    minute = 29 - cuarto3Minuto
                    cuarto3Minuto = cuarto3Minuto -1
                    jminutesPlayer.append({})
                    jminutesPlayer[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player': iDplayer, 'name_player': nameplayer, 'period': 3, 'periodD': '3º Cuarto',
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute':minute, 'second': 0,
                                        'playIn': playerIn}
                    if playerTemp == 1:
                        playerTemp = 0
                        playerIn = 1
                    elif playerTemp == 2:
                        playerTemp = 0
                        playerIn = 0

            if jmatchevents[me]['period'] == 4:
                if jmatchevents[me]['minute']  == cuarto4Minuto and cuarto4Minuto > -1:
                    minute = 39 - cuarto4Minuto
                    cuarto4Minuto = cuarto4Minuto -1
                    jminutesPlayer.append({})
                    jminutesPlayer[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player': iDplayer, 'name_player': nameplayer, 'period': 4, 'periodD': '4º Cuarto',
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute':minute, 'second': 0,
                                        'playIn': playerIn}
                    if playerTemp == 1:
                        playerTemp = 0
                        playerIn = 1
                    elif playerTemp == 2:
                        playerTemp = 0
                        playerIn = 0

            if jmatchevents[me]['period'] > 4:
                if jmatchevents[me]['minute']  == cuarto5Minuto and cuarto5Minuto > -1:
                    minute = 44 - cuarto5Minuto
                    cuarto5Minuto = cuarto5Minuto -1
                    jminutesPlayer.append({})
                    jminutesPlayer[-1]={'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player': iDplayer, 'name_player': nameplayer, 'period': 5, 'periodD': 'Prórroga',
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute':minute, 'second': 0,
                                        'playIn': playerIn}
                    if playerTemp == 1:
                        playerTemp = 0
                        playerIn = 1
                    elif playerTemp == 2:
                        playerTemp = 0
                        playerIn = 0
        
    return(jminutesPlayer)


def gen_jassistPlayer(jmatchevents, id_match, competition, startDate, team1, info):

    jassistaPlayer = []
    
    if len(jmatchevents) > 0:

        for me in range(len(jmatchevents)):
            if jmatchevents[me]['id_playbyplaytype'] == 'ast':
                id_player_assist = jmatchevents[me]['id_player']
                name_player_assist = jmatchevents[me]['name_player']
                id_player_shot = jmatchevents[me-1]['id_player']
                name_player_shot = jmatchevents[me-1]['name_player']
                id_team = jmatchevents[me]['id_team']

                difference = info['local_points'] - info['visitor_points'] 
                if id_team == team1['id_team']:
                    lado = 'Local'
                    if difference > 0:
                        resultD = 'Victoria'
                        result = 1
                    else:
                        resultD = 'Derrota'
                        result = 0
                else:
                    lado = 'Visitante'
                    if difference > 0:
                        resultD = 'Derrota'
                        result = 0
                    else:
                        resultD = 'Victoria'
                        result = 1

                period = jmatchevents[me]['period']
                if period == 0:
                    periodD = '0 - Todos'
                elif period == 1:     
                    periodD = '1º Cuarto'
                elif period == 2:     
                    periodD = '2º Cuarto'
                elif period == 3:     
                    periodD = '3º Cuarto'
                elif period == 4:     
                    periodD = '4º Cuarto'
                elif period == 5:     
                    periodD = 'Prórroga'
                elif period == 6:     
                    periodD = 'Prórroga'
                elif period == 7:     
                    periodD = 'Prórroga'
                elif period == 8:     
                    periodD = 'Prórroga'
                elif period == 9:     
                    periodD = 'Prórroga'       
                else:     
                    periodD = 'Prórroga'

                # Ponemos la canasta para saber si 2 puntos o 1:
                id_playbyplaytype = jmatchevents[me-1]['id_playbyplaytype']
                if id_playbyplaytype == 't2in':
                    description = 'Tiro 2pt anotado'
                elif id_playbyplaytype == 't3in':
                    description = 'Triple anotado'
                else:
                    description = ''

                minute = jmatchevents[me]['minute']
                second = jmatchevents[me]['second']
                key_assistsDistributionPlayer = id_match + '_' + id_player_assist + '_' + str(period) + '_' + str(minute) + '_' + str(second)

                jassistaPlayer.append({})
                jassistaPlayer[-1]={'key_assistsDistributionPlayer': key_assistsDistributionPlayer, 'key_competition': competition['key_competition'],'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'], 'id_match': id_match, 'id_team': id_team, 'id_player_assist': id_player_assist, 'name_player_assist': name_player_assist, 'id_player_shot': id_player_shot, 'name_player_shot': name_player_shot, 'period': period, 'periodD': periodD,
                                        'lado': lado, 'result': result, 'resultD': resultD, 'startDate': startDate, 'minute': minute, 'second': second,
                                        'id_playbyplaytype': id_playbyplaytype, 'description': description}
    return jassistaPlayer


def gen_jmatcheventsFive(jmatchevents, id_match, competition, startDate, team1, team2, list_players, info, jshoots):

    jshoots = pd.DataFrame(jshoots)
    list_total_shoots = [False] * jshoots.shape[0]
    jshoots['repetido'] = list_total_shoots
        
    playersLocal = []
    playersLocalName = []
    playersVisitor = []
    playersVisitorName = []
    jplaybyplayFiveLocal = []
    jplaybyplayFiveVisitor = []
    obj_playersLocal = {}
    obj_playersVisitor = {}
    jplaybyplayFiveLocalAWS = []
    jplaybyplayFiveVisitorAWS = []

    list_fiveStart = []
    list_fiveEnd = []

    difference = info['local_points'] - info['visitor_points'] 

    if difference > 0:
        resultLocal = 1
        resultDLocal = 'Victoria'
        resultVisitor = 0
        resultDVisitor = 'Derrota'
    else:
        resultLocal = 0
        resultDLocal = 'Derrota'
        resultVisitor = 1
        resultDVisitor = 'Victoria'

    NUM_EVENT = 0
    for event in range(len(jmatchevents)):
        if jmatchevents[event]['id_playbyplaytype'] == 'subsIn':
            if jmatchevents[event]['id_team'] == team1['id_team']:
                event_idPlayerLocal = jmatchevents[event]['id_player']
                playersLocal.append(event_idPlayerLocal)
                playersLocal.sort()
                event_namePlayerLocal = jmatchevents[event]['name_player']
                playersLocalName.append(event_namePlayerLocal)
                playersLocalName.sort()
                obj_playersLocal[event_idPlayerLocal] = event_namePlayerLocal
            else:
                event_idPlayerVisitor = jmatchevents[event]['id_player']
                playersVisitor.append(event_idPlayerVisitor)
                playersVisitor.sort()
                event_namePlayerVisitor = jmatchevents[event]['name_player']
                playersVisitorName.append(event_namePlayerVisitor)
                playersVisitorName.sort()
                obj_playersVisitor[event_idPlayerVisitor] = event_namePlayerVisitor

        try:
            playerLocal1 = playersLocal[0]
        except:
            playerLocal1 = ''
        try:
            playerLocal2 = playersLocal[1]
        except:
            playerLocal2 = ''
        try:
            playerLocal3 = playersLocal[2]
        except:
            playerLocal3 = ''
        try:
            playerLocal4 = playersLocal[3]
        except:
            playerLocal4 = ''
        try:
            playerLocal5 = playersLocal[4]
        except:
            playerLocal5 = ''
        try:
            playerVisitor1 = playersVisitor[0]
        except:
            playerVisitor1 = ''
        try:
            playerVisitor2 = playersVisitor[1]
        except:
            playerVisitor2 = ''
        try:
            playerVisitor3 = playersVisitor[2]
        except:
            playerVisitor3 = ''
        try:
            playerVisitor4 = playersVisitor[3]
        except:
            playerVisitor4 = ''
        try:
            playerVisitor5 = playersVisitor[4]
        except:
            playerVisitor5 = ''
        
        try:
            playerLocal1Name = playersLocalName[0]
        except:
            playerLocal1Name = ''
        try:
            playerLocal2Name = playersLocalName[1]
        except:
            playerLocal2Name = ''
        try:
            playerLocal3Name = playersLocalName[2]
        except:
            playerLocal3Name = ''
        try:
            playerLocal4Name = playersLocalName[3]
        except:
            playerLocal4Name = ''
        try:
            playerLocal5Name = playersLocalName[4]
        except:
            playerLocal5Name = ''
        try:
            playerVisitor1Name = playersVisitorName[0]
        except:
            playerVisitor1Name = ''
        try:
            playerVisitor2Name = playersVisitorName[1]
        except:
            playerVisitor2Name = ''
        try:
            playerVisitor3Name = playersVisitorName[2]
        except:
            playerVisitor3Name = ''
        try:
            playerVisitor4Name = playersVisitorName[3]
        except:
            playerVisitor4Name = ''
        try:
            playerVisitor5Name = playersVisitorName[4]
        except:
            playerVisitor5Name = ''

        period = jmatchevents[event]['period']
        if period == 0:
            periodD = '0 - Todos'
        elif period == 1:     
            periodD = '1º Cuarto'
        elif period == 2:     
            periodD = '2º Cuarto'
        elif period == 3:     
            periodD = '3º Cuarto'
        elif period == 4:     
            periodD = '4º Cuarto'
        elif period == 5:     
            periodD = 'Prórroga'
        elif period == 6:     
            periodD = 'Prórroga'
        elif period == 7:     
            periodD = 'Prórroga'
        elif period == 8:     
            periodD = 'Prórroga'
        elif period == 9:     
            periodD = 'Prórroga'       
        else:     
            periodD = 'Prórroga'

        if (jmatchevents[event]['id_team'] == team1['id_team']) or (jmatchevents[event]['id_playbyplaytype'] in ['start', 'startG', 'end', 'endG']):
            id_playbyplaytypeLocal = jmatchevents[event]['id_playbyplaytype']
        else:
            id_playbyplaytypeLocal = 'r_' + jmatchevents[event]['id_playbyplaytype']

        if (jmatchevents[event]['id_team'] == team2['id_team']) or (jmatchevents[event]['id_playbyplaytype'] in ['start', 'startG', 'end', 'endG']):
            id_playbyplaytypeVisitor = jmatchevents[event]['id_playbyplaytype']
        else:
            id_playbyplaytypeVisitor = 'r_' + jmatchevents[event]['id_playbyplaytype']

        scoreTeam_Local = jmatchevents[event]['score_local']
        id_rivalTeam_Local = team2['id_team']      
        name_Team_Local = team1['short_team_name']    
        name_rivalTeam_Local = team2['short_team_name']
        scoreRivalTeam_Local = jmatchevents[event]['score_visitor']

        scoreTeam_Visitor = jmatchevents[event]['score_visitor']
        id_rivalTeam_Visitor = team1['id_team']    
        name_Team_Visitor = team2['short_team_name']          
        name_rivalTeam_Visitor = team1['short_team_name']
        scoreRivalTeam_Visitor = jmatchevents[event]['score_local']

        playersLocal.sort()
        id_localFive = " - ".join(playersLocal)

        playersVisitor.sort()
        id_visitorFive = " - ".join(playersVisitor)

        playersLocalName.sort()
        name_localFive = " - ".join(playersLocalName)

        playersVisitorName.sort()
        name_visitorFive = " - ".join(playersVisitorName)

        num_playersLocal = len(playersLocal)
        num_playersVisitor = len(playersVisitor)

        minute = jmatchevents[event]['minute']
        second = jmatchevents[event]['second']
        try:
            if period > 4:
                second_game = ( ( 40* 60 ) + (period - 5) * 5 * 60 ) + ( ((10 - minute) * 60) - (second) )
            else:
                second_game = ((period - 1) * 10 * 60) + ( ((10 - minute) * 60) - (second) )
        except:
            second_game = 0


        isInCombinationSubLocal = 0
        isInCombinationSubVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['subsIn', 'subsOut']:
            if jmatchevents[event]['id_player'] in id_localFive:
                isInCombinationSubLocal = 1
            elif jmatchevents[event]['id_player'] in id_visitorFive:
                isInCombinationSubVisitor = 1
        
        second_gameInLocal = 0
        second_gameInVisitor = 0
        second_gameOutLocal = 0
        second_gameOutVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['start', 'startG']:
            second_gameInLocal = second_game
            second_gameInVisitor = second_game
        elif jmatchevents[event]['id_playbyplaytype'] in ['end']:
            second_gameOutLocal = second_game
            second_gameOutVisitor = second_game     
        if isInCombinationSubLocal == 1:
            if jmatchevents[event]['id_playbyplaytype'] == 'subsIn':
                second_gameInLocal = second_game
            elif jmatchevents[event]['id_playbyplaytype'] == 'subsOut':
                second_gameOutLocal = second_game
        elif isInCombinationSubVisitor == 1:
            if jmatchevents[event]['id_playbyplaytype'] == 'subsIn':
                second_gameInVisitor = second_game
            elif jmatchevents[event]['id_playbyplaytype'] == 'subsOut':
                second_gameOutVisitor = second_game


        puntosPinturaLocal = 0
        puntosPinturaVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['t2in']:
            if jmatchevents[event]['id_player'] in id_localFive:
                [puntosPinturaLocal, jshoots] = obtenerPuntosPinturaFive(jshoots, jmatchevents[event]['id_player'], period, minute, second)
            elif jmatchevents[event]['id_player'] in id_visitorFive:
                [puntosPinturaVisitor, jshoots] = obtenerPuntosPinturaFive(jshoots, jmatchevents[event]['id_player'], period, minute, second)
        points_in_the_paint_againstLocal = puntosPinturaVisitor
        points_in_the_paint_againstVisitor = puntosPinturaLocal

        puntosCaLocal = 0
        puntosCaVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['t2in', 't3in']:
            if jmatchevents[event]['id_team'] == team1['id_team']:
                if jmatchevents[event+1]['id_playbyplaytype'] == 'ca2':
                    puntosCaLocal = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 'ca3':
                    puntosCaLocal = 3
            else:
                if jmatchevents[event+1]['id_playbyplaytype'] == 'ca2':
                    puntosCaVisitor = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 'ca3':
                    puntosCaVisitor = 3
        puntosCA_againstLocal = puntosCaVisitor
        puntosCA_againstVisitor = puntosCaLocal

        puntos2OportunidadLocal = 0
        puntos2OportunidadVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['rebO']:
            if jmatchevents[event]['id_player'] in id_localFive:
                if jmatchevents[event+1]['id_playbyplaytype'] == 't2in':
                    puntos2OportunidadLocal = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 't3in':
                    puntos2OportunidadLocal = 3
            elif jmatchevents[event]['id_player'] in id_visitorFive:
                if jmatchevents[event+1]['id_playbyplaytype'] == 't2in':
                    puntos2OportunidadVisitor = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 't3in':
                    puntos2OportunidadVisitor = 3
        points_secondchance_againstLocal = puntos2OportunidadVisitor
        points_secondchance_againstVisitor = puntos2OportunidadLocal

        puntosTrasRoboLocal = 0
        puntosTrasRoboVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['stl']:
            if jmatchevents[event]['id_player'] in id_localFive:
                if jmatchevents[event+1]['id_playbyplaytype'] == 't2in':
                    puntosTrasRoboLocal = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 't3in':
                    puntosTrasRoboLocal = 3
            elif jmatchevents[event]['id_player'] in id_visitorFive:
                if jmatchevents[event+1]['id_playbyplaytype'] == 't2in':
                    puntosTrasRoboVisitor = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 't3in':
                    puntosTrasRoboVisitor = 3
        points_aftersteal_againstLocal = puntosTrasRoboVisitor
        points_aftersteal_againstVisitor = puntosTrasRoboLocal

        puntosTrasAsistenciaLocal = 0
        puntosTrasAsistenciaVisitor = 0
        if jmatchevents[event]['id_playbyplaytype'] in ['ast']:
            if jmatchevents[event]['id_player'] in id_localFive:
                if jmatchevents[event-1]['id_playbyplaytype'] == 't2in':
                    puntosTrasAsistenciaLocal = 2
                elif jmatchevents[event-1]['id_playbyplaytype'] == 't3in':
                    puntosTrasAsistenciaLocal = 3
            elif jmatchevents[event]['id_player'] in id_visitorFive:
                if jmatchevents[event+1]['id_playbyplaytype'] == 't2in':
                    puntosTrasAsistenciaVisitor = 2
                elif jmatchevents[event+1]['id_playbyplaytype'] == 't3in':
                    puntosTrasAsistenciaVisitor = 3
        points_afterassist_againstLocal = puntosTrasAsistenciaVisitor
        points_afterassist_againstVisitor = puntosTrasAsistenciaLocal

        if id_playbyplaytypeLocal == 'startG':
            list_fiveStart.append(id_localFive)
            list_fiveStart.append(id_visitorFive)
        if id_playbyplaytypeLocal == 'endG':
            list_fiveEnd.append(id_localFive)
            list_fiveEnd.append(id_visitorFive)

        if id_localFive in list_fiveStart:
            startingLocal = 1
        else: 
            startingLocal = 0
        if id_visitorFive in list_fiveStart:
            startingVisitor = 1
        else: 
            startingVisitor = 0

        if id_localFive in list_fiveEnd:
            finishingLocal = 1
        else: 
            finishingLocal = 0
        if id_visitorFive in list_fiveEnd:
            finishingVisitor = 1
        else: 
            finishingVisitor = 0
            
        #key_five_local = str(id_match) + '_' + str(id_localFive) + '_E' + str(jmatchevents[event]['id_event'])
        #key_five_visitor = str(id_match) + '_' + str(id_visitorFive) + '_E' + str(jmatchevents[event]['id_event'])
        key_five_local = str(id_match) + '_' + str(team1['id_team']) + '_E' + str(NUM_EVENT)
        key_five_visitor = str(id_match) + '_' + str(team2['id_team']) + str(NUM_EVENT)

        if jmatchevents[event]['id_playbyplaytype'] in ['t2in', 't2out', 't3in', 't3out', 't1in', 't1out', 'ast', 'stl', 'turn','rebD','rebO','block','blockAgainst','foul','foulR','subsIn', 'subsOut', 'end', 'start']:
            jplaybyplayFiveLocal.append({})
            jplaybyplayFiveLocal[-1] = {'key_five': key_five_local, 'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                'key_competition': competition['key_competition'],
                        'id_match': id_match, 'id_event': str(id_match) + '_E' + str(jmatchevents[event]['id_event']), 'start_date': startDate, 'id_team': team1['id_team'],
                        'scoreTeam': scoreTeam_Local, 'id_rivalTeam': id_rivalTeam_Local, 'scoreRivalTeam': scoreRivalTeam_Local, 'id_five': id_localFive, 'name_five': name_localFive,
                        'num_players': num_playersLocal, 'lado': 'Local', 'period': period, 'periodD': periodD,
                        'minute': minute, 'second': second, 'second_gameIn': second_gameInLocal, 'isInCombinationSub': isInCombinationSubLocal, 'second_gameOut': second_gameOutLocal,
                        'id_player1': playerLocal1, 'id_player2': playerLocal2, 'id_player3': playerLocal3,
                        'id_player4': playerLocal4, 'id_player5': playerLocal5, 'name_player1': playerLocal1Name, 'name_player2': playerLocal2Name,
                        'name_player3': playerLocal3Name, 'name_player4': playerLocal4Name, 'name_player5': playerLocal5Name,
                        'id_teamEjecutor': jmatchevents[event]['id_team'], 'id_playerEjecutor': jmatchevents[event]['id_player'], 'id_playbyplaytype': id_playbyplaytypeLocal,
                        'result' : resultLocal, 'resultD': resultDLocal, 'team_name': name_Team_Local, 'rival_team_name': name_rivalTeam_Local,
                        'difference': difference, 'sstarting': startingLocal, 'finishing' : finishingLocal,
                        'points_fastbreak': puntosCaLocal, 'points_aftersteal': puntosTrasRoboLocal, 'points_afterassist': puntosTrasAsistenciaLocal, 
                        'points_secondchance': puntos2OportunidadLocal,
                        'points_in_the_paint': puntosPinturaLocal, 'points_fastbreak_against': puntosCA_againstLocal, 'points_aftersteal_against': points_aftersteal_againstLocal, 
                        'points_afterassist_against': points_afterassist_againstLocal,
                        'points_secondchance_against': points_secondchance_againstLocal, 'points_in_the_paint_against': points_in_the_paint_againstLocal,
                        'obj_players': obj_playersLocal.copy()
                                }
            jplaybyplayFiveLocalAWS.append({})
            jplaybyplayFiveLocalAWS[-1] = {'key_five': key_five_local,
                'key_competition': competition['key_competition'],
                        'id_match': id_match, 'start_date': startDate, 'id_team': team1['id_team'], 'id_five': id_localFive, 'name_five': name_localFive,
                        'num_players': num_playersLocal, 'lado': 'Local', 'period': period,'second_gameIn': second_gameInLocal, 'second_gameOut': second_gameOutLocal, 'name_player1': playerLocal1Name, 'name_player2': playerLocal2Name,
                        'name_player3': playerLocal3Name, 'name_player4': playerLocal4Name, 'name_player5': playerLocal5Name,
                        'id_teamEjecutor': jmatchevents[event]['id_team'], 'id_playerEjecutor': jmatchevents[event]['id_player'], 'id_playbyplaytype': id_playbyplaytypeLocal,
                        'result' : resultLocal, 'team_name': name_Team_Local, 'rival_team_name': name_rivalTeam_Local,
                        'difference': difference, 'points_aftersteal': puntosTrasRoboLocal, 'points_afterassist': puntosTrasAsistenciaLocal, 
                        'points_secondchance': puntos2OportunidadLocal,
                        'points_in_the_paint': puntosPinturaLocal, 'points_aftersteal_against': points_aftersteal_againstLocal, 
                        'points_afterassist_against': points_afterassist_againstLocal,
                        'points_secondchance_against': points_secondchance_againstLocal, 'points_in_the_paint_against': points_in_the_paint_againstLocal
                                }
            
            jplaybyplayFiveVisitor.append({})
            jplaybyplayFiveVisitor[-1] = {'key_five': key_five_visitor, 'id_competition': competition['id_competition'], 'id_edition': competition['id_edition'], 'id_phase': competition['id_phase'],
                'key_competition': competition['key_competition'],
                        'id_match': id_match, 'id_event': str(id_match) + '_E' + str(jmatchevents[event]['id_event']), 'start_date': startDate, 'id_team': team2['id_team'],
                        'scoreTeam': scoreTeam_Visitor, 'id_rivalTeam': id_rivalTeam_Visitor, 'scoreRivalTeam': scoreRivalTeam_Visitor, 'id_five': id_visitorFive, 'name_five': name_visitorFive,
                        'num_players': num_playersVisitor, 'lado': 'Visitante', 'period': period, 'periodD': periodD,
                        'minute': minute, 'second': second, 'second_gameIn': second_gameInVisitor, 'isInCombinationSub': isInCombinationSubVisitor, 'second_gameOut': second_gameOutVisitor,
                        'id_player1': playerVisitor1, 'id_player2': playerVisitor2, 'id_player3': playerVisitor3,
                        'id_player4': playerVisitor4, 'id_player5': playerVisitor5, 'name_player1': playerVisitor1Name, 'name_player2': playerVisitor2Name,
                        'name_player3': playerVisitor3Name, 'name_player4': playerVisitor4Name, 'name_player5': playerVisitor5Name,
                        'id_teamEjecutor': jmatchevents[event]['id_team'], 'id_playerEjecutor': jmatchevents[event]['id_player'], 'id_playbyplaytype': id_playbyplaytypeVisitor,
                        'result' : resultVisitor, 'resultD': resultDVisitor, 'team_name': name_Team_Visitor, 'rival_team_name': name_rivalTeam_Visitor,
                        'difference': -difference, 'sstarting': startingVisitor, 'finishing' : finishingVisitor,
                        'points_fastbreak': puntosCaVisitor, 'points_aftersteal': puntosTrasRoboVisitor, 'points_afterassist': puntosTrasAsistenciaVisitor,
                        'points_secondchance': puntos2OportunidadVisitor,
                        'points_in_the_paint': puntosPinturaVisitor, 'points_fastbreak_against': puntosCA_againstVisitor, 'points_aftersteal_against': points_aftersteal_againstVisitor, 
                        'points_afterassist_against': points_afterassist_againstVisitor,
                        'points_secondchance_against': points_secondchance_againstVisitor, 'points_in_the_paint_against': points_in_the_paint_againstVisitor,
                        'obj_players': obj_playersVisitor.copy()
                                }
            jplaybyplayFiveVisitorAWS.append({})
            jplaybyplayFiveVisitorAWS[-1] = {'key_five': key_five_visitor,
                'key_competition': competition['key_competition'],
                        'id_match': id_match, 'start_date': startDate, 'id_team': team2['id_team'], 'id_five': id_visitorFive, 'name_five': name_visitorFive,
                        'num_players': num_playersVisitor, 'lado': 'Visitante', 'period': period,'second_gameIn': second_gameInVisitor, 'second_gameOut': second_gameOutVisitor, 'name_player1': playerVisitor1Name, 'name_player2': playerVisitor2Name,
                        'name_player3': playerVisitor3Name, 'name_player4': playerVisitor4Name, 'name_player5': playerVisitor5Name,
                        'id_teamEjecutor': jmatchevents[event]['id_team'], 'id_playerEjecutor': jmatchevents[event]['id_player'], 'id_playbyplaytype': id_playbyplaytypeVisitor,
                        'result' : resultVisitor, 'team_name': name_Team_Visitor, 'rival_team_name': name_rivalTeam_Visitor,
                        'difference': difference, 'points_aftersteal': puntosTrasRoboVisitor, 'points_afterassist': puntosTrasAsistenciaVisitor, 
                        'points_secondchance': puntos2OportunidadVisitor,
                        'points_in_the_paint': puntosPinturaVisitor, 'points_aftersteal_against': points_aftersteal_againstVisitor, 
                        'points_afterassist_against': points_afterassist_againstVisitor,
                        'points_secondchance_against': points_secondchance_againstVisitor, 'points_in_the_paint_against': points_in_the_paint_againstVisitor
                                }
        
        if jmatchevents[event]['id_playbyplaytype']== 'subsOut':
            if jmatchevents[event]['id_team'] == team1['id_team']:
                try:
                    playersLocal.remove(jmatchevents[event]['id_player'])
                    playersLocal.sort()
                    playersLocalName.remove(jmatchevents[event]['name_player'])
                    playersLocalName.sort()
                    del obj_playersLocal[jmatchevents[event]['id_player']]
                except:
                    print('ERROR SUBSOUT QUINTETOS')
                    pass
            else:
                try:
                    playersVisitor.remove(jmatchevents[event]['id_player'])
                    playersVisitor.sort()
                    playersVisitorName.remove(jmatchevents[event]['name_player'])
                    playersVisitorName.sort()
                    del obj_playersVisitor[jmatchevents[event]['id_player']]
                except:
                    pass
        
        NUM_EVENT = NUM_EVENT +1

                    
    return([jplaybyplayFiveLocal, jplaybyplayFiveVisitor, jplaybyplayFiveLocalAWS, jplaybyplayFiveVisitorAWS])


def gen_jmatcheventsFour(jplaybyplayFive):

    id_competition = jplaybyplayFive[0]['id_competition'] 
    id_edition = jplaybyplayFive[0]['id_edition'] 
    id_phase = jplaybyplayFive[0]['id_phase'] 
    id_match = jplaybyplayFive[0]['id_match'] 
    startDate = jplaybyplayFive[0]['start_date'] 
    id_team = jplaybyplayFive[0]['id_team'] 
    scoreTeam = jplaybyplayFive[0]['scoreTeam'] 
    id_rivalTeam = jplaybyplayFive[0]['id_rivalTeam'] 
    scoreRivalTeam = jplaybyplayFive[0]['scoreRivalTeam'] 
    result = jplaybyplayFive[0]['result'] 
    resultD = jplaybyplayFive[0]['resultD'] 
    teamName = jplaybyplayFive[0]['team_name'] 
    rivalTeamName = jplaybyplayFive[0]['rival_team_name'] 
    difference = jplaybyplayFive[0]['difference']

    jplaybyplayFour = []
    for j4 in jplaybyplayFive:
        event_id = j4['id_event'] 
        lado = j4['lado'] 
        period = j4['period'] 
        periodD = j4['periodD'] 
        minute = j4['minute'] 
        second = j4['second']  
        second_gameIn_total = j4['second_gameIn']
        second_gameOut_total = j4['second_gameOut']
        id_teamEjecutor = j4['id_teamEjecutor'] 
        id_playerEjecutor = j4['id_playerEjecutor'] 
        id_playbyplaytype = j4['id_playbyplaytype'] 
        points_in_the_paint = j4['points_in_the_paint']
        points_secondchance = j4['points_secondchance']
        points_aftersteal = j4['points_aftersteal']
        points_afterassist = j4['points_afterassist']
        points_in_the_paint_against = j4['points_in_the_paint_against']
        points_secondchance_against = j4['points_secondchance_against']
        points_aftersteal_against = j4['points_aftersteal_against']
        points_afterassist_against = j4['points_afterassist_against']
        sstarting = j4['sstarting'] 
        finishing = j4['finishing']
        points_fastbreak = j4['points_fastbreak']
        points_fastbreak_against = j4['points_fastbreak_against']
        obj_players = j4['obj_players']
    
        if j4['num_players'] == 4:
            player1 = j4['id_player1']
            player2 = j4['id_player2']
            player3 = j4['id_player3']
            player4 = j4['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total


            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
        elif j4['num_players'] > 4:
            player1 = j4['id_player1']
            player2 = j4['id_player2']
            player3 = j4['id_player3']
            player4 = j4['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }

            player1 = j4['id_player1']
            player2 = j4['id_player2']
            player3 = j4['id_player3']
            player4 = j4['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }        

            player1 = j4['id_player1']
            player2 = j4['id_player2']
            player3 = j4['id_player4']
            player4 = j4['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }

            player1 = j4['id_player1']
            player2 = j4['id_player3']
            player3 = j4['id_player4']
            player4 = j4['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }                                        
 
            player1 = j4['id_player2']
            player2 = j4['id_player3']
            player3 = j4['id_player4']
            player4 = j4['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            name_player4 = obj_players[player4]
            players = [player1, player2, player3, player4]
            players.sort()
            id_four = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3, name_player4]
            playersName.sort()
            name_four = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_four:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayFour.append({})
            jplaybyplayFour[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_four': id_four, 'name_four': name_four, 'num_players': 4,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3, 'id_player4': player4,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3, 'name_player4': name_player4,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }          

    return(jplaybyplayFour)


def gen_jmatcheventsThree(jplaybyplayFive):

    id_competition = jplaybyplayFive[0]['id_competition'] 
    id_edition = jplaybyplayFive[0]['id_edition'] 
    id_phase = jplaybyplayFive[0]['id_phase']
    id_match = jplaybyplayFive[0]['id_match'] 
    startDate = jplaybyplayFive[0]['start_date'] 
    id_team = jplaybyplayFive[0]['id_team'] 
    scoreTeam = jplaybyplayFive[0]['scoreTeam'] 
    id_rivalTeam = jplaybyplayFive[0]['id_rivalTeam'] 
    scoreRivalTeam = jplaybyplayFive[0]['scoreRivalTeam']  
    result = jplaybyplayFive[0]['result'] 
    resultD = jplaybyplayFive[0]['resultD']
    teamName = jplaybyplayFive[0]['team_name'] 
    rivalTeamName = jplaybyplayFive[0]['rival_team_name'] 
    difference = jplaybyplayFive[0]['difference'] 

    jplaybyplayThree = []
    for j3 in jplaybyplayFive:
        event_id = j3['id_event'] 
        lado = j3['lado'] 
        period = j3['period']  
        periodD = j3['periodD'] 
        minute = j3['minute'] 
        second = j3['second']  
        second_gameIn_total = j3['second_gameIn']
        second_gameOut_total = j3['second_gameOut']
        id_teamEjecutor = j3['id_teamEjecutor'] 
        id_playerEjecutor = j3['id_playerEjecutor'] 
        id_playbyplaytype = j3['id_playbyplaytype'] 
        points_in_the_paint = j3['points_in_the_paint']
        points_secondchance = j3['points_secondchance']
        points_aftersteal = j3['points_aftersteal']
        points_afterassist = j3['points_afterassist']
        points_in_the_paint_against = j3['points_in_the_paint_against']
        points_secondchance_against = j3['points_secondchance_against']
        points_aftersteal_against = j3['points_aftersteal_against']
        points_afterassist_against = j3['points_afterassist_against']
        sstarting = j3['sstarting']
        finishing = j3['finishing'] 
        points_fastbreak = j3['points_fastbreak']
        points_fastbreak_against = j3['points_fastbreak_against']
        obj_players = j3['obj_players']
    
        if j3['num_players'] == 3:
            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
        elif j3['num_players'] == 4:
            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
                            
            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
                                                        
            player1 = j3['id_player1']
            player2 = j3['id_player3']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
                                                        
            player1 = j3['id_player2']
            player2 = j3['id_player3']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
        elif j3['num_players'] > 4:
            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }

            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            } 

            player1 = j3['id_player1']
            player2 = j3['id_player2']
            player3 = j3['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player1']
            player2 = j3['id_player3']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player1']
            player2 = j3['id_player3']
            player3 = j3['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player1']
            player2 = j3['id_player4']
            player3 = j3['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player2']
            player2 = j3['id_player3']
            player3 = j3['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player2']
            player2 = j3['id_player4']
            player3 = j3['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

            player1 = j3['id_player3']
            player2 = j3['id_player4']
            player3 = j3['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            name_player3 = obj_players[player3]
            players = [player1, player2, player3]
            players.sort()
            id_three = " - ".join(players)
            playersName = [name_player1, name_player2, name_player3]
            playersName.sort()
            name_three = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_three:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayThree.append({})
            jplaybyplayThree[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_three': id_three, 'name_three': name_three, 'num_players': 3,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'id_player3': player3,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'name_player3': name_player3,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }   

    return(jplaybyplayThree)    



def gen_jmatcheventsTwo(jplaybyplayFive):

    id_competition = jplaybyplayFive[0]['id_competition'] 
    id_edition = jplaybyplayFive[0]['id_edition'] 
    id_phase = jplaybyplayFive[0]['id_phase']
    id_match = jplaybyplayFive[0]['id_match'] 
    startDate = jplaybyplayFive[0]['start_date'] 
    id_team = jplaybyplayFive[0]['id_team'] 
    scoreTeam = jplaybyplayFive[0]['scoreTeam'] 
    id_rivalTeam = jplaybyplayFive[0]['id_rivalTeam'] 
    scoreRivalTeam = jplaybyplayFive[0]['scoreRivalTeam'] 
    result = jplaybyplayFive[0]['result'] 
    resultD = jplaybyplayFive[0]['resultD'] 
    teamName = jplaybyplayFive[0]['team_name'] 
    rivalTeamName = jplaybyplayFive[0]['rival_team_name'] 
    difference = jplaybyplayFive[0]['difference']  

    jplaybyplayTwo = []
    for j2 in jplaybyplayFive:
        event_id = j2['id_event'] 
        lado = j2['lado'] 
        period = j2['period'] 
        periodD = j2['periodD']  
        minute = j2['minute'] 
        second = j2['second'] 
        second_gameIn_total = j2['second_gameIn']
        second_gameOut_total = j2['second_gameOut']
        id_teamEjecutor = j2['id_teamEjecutor'] 
        id_playerEjecutor = j2['id_playerEjecutor'] 
        id_playbyplaytype = j2['id_playbyplaytype']  
        points_in_the_paint = j2['points_in_the_paint']
        points_secondchance = j2['points_secondchance']
        points_aftersteal = j2['points_aftersteal']
        points_afterassist = j2['points_afterassist']
        points_in_the_paint_against = j2['points_in_the_paint_against']
        points_secondchance_against = j2['points_secondchance_against']
        points_aftersteal_against = j2['points_aftersteal_against']
        points_afterassist_against = j2['points_afterassist_against']
        sstarting = j2['sstarting'] 
        finishing = j2['finishing'] 
        points_fastbreak = j2['points_fastbreak']
        points_fastbreak_against = j2['points_fastbreak_against']
        obj_players = j2['obj_players']
    
        if j2['num_players'] == 2:
            player1 = j2['id_player1']
            player2 = j2['id_player2']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
        elif j2['num_players'] == 3:
            player1 = j2['id_player1']
            player2 = j2['id_player2']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
                            
            player1 = j2['id_player1']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
                                                        
            player1 = j2['id_player2']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }
        elif j2['num_players'] == 4:
            player1 = j2['id_player1']
            player2 = j2['id_player2']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            } 

            player1 = j2['id_player1']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }    
                            
            player1 = j2['id_player1']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }    
                            
            player1 = j2['id_player2']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }    
                            
            player1 = j2['id_player2']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }    
                            
            player1 = j2['id_player3']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }  
        elif j2['num_players'] > 4:
            player1 = j2['id_player1']
            player2 = j2['id_player2']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            } 

            player1 = j2['id_player1']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }    

            player1 = j2['id_player1']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player1']
            player2 = j2['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player2']
            player2 = j2['id_player3']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player2']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player2']
            player2 = j2['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player3']
            player2 = j2['id_player4']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player3']
            player2 = j2['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }     

            player1 = j2['id_player4']
            player2 = j2['id_player5']
            name_player1 = obj_players[player1]
            name_player2 = obj_players[player2]
            players = [player1, player2]
            players.sort()
            id_two = " - ".join(players)
            playersName = [name_player1, name_player2]
            playersName.sort()
            name_two = " - ".join(playersName)
            isInCombinationSub = 0
            second_gameIn = 0
            second_gameOut = 0
            if id_playerEjecutor in id_two:
                if id_playbyplaytype == 'subsIn':               
                    isInCombinationSub = 1 
                    second_gameIn = second_gameIn_total              
                elif id_playbyplaytype == 'subsOut':            
                    isInCombinationSub = 1    
                    second_gameOut = second_gameOut_total
            if id_playbyplaytype == 'start':
                second_gameIn = second_gameIn_total 
            elif id_playbyplaytype == 'end':
                second_gameOut = second_gameOut_total

            jplaybyplayTwo.append({})
            jplaybyplayTwo[-1] = {'id_competition': id_competition, 'id_edition': id_edition, 'id_phase': id_phase, 'id_match': id_match, 'id_event': event_id, 
                            'start_date': startDate, 'id_team': id_team, 'scoreTeam': scoreTeam,
                            'id_rivalTeam': id_rivalTeam, 'scoreRivalTeam': scoreRivalTeam,
                            'id_two': id_two, 'name_two': name_two, 'num_players': 2,
                            'period': period, 'periodD': periodD, 'minute': minute, 'second': second,
                            'second_gameIn': second_gameIn, 'isInCombinationSub': isInCombinationSub, 'second_gameOut': second_gameOut,
                            'id_player1': player1, 'id_player2': player2,
                            'name_player1': name_player1, 'name_player2': name_player2,
                            'id_teamEjecutor': id_teamEjecutor,
                            'id_playerEjecutor': id_playerEjecutor, 'id_playbyplaytype': id_playbyplaytype,
                            'result': result, 'resultD': resultD, 'team_name': teamName, 'rival_team_name': rivalTeamName, 'difference': difference, 
                            'sstarting': sstarting, 'finishing': finishing, 'lado': lado,
                            'points_in_the_paint': points_in_the_paint, 'points_secondchance': points_secondchance, 'points_aftersteal': points_aftersteal,
                            'points_in_the_paint_against': points_in_the_paint_against, 'points_secondchance_against': points_secondchance_against, 'points_aftersteal_against': points_aftersteal_against,
                            'points_afterassist': points_afterassist, 'points_afterassist_against': points_afterassist_against, 'points_fastbreak': points_fastbreak, 'points_fastbreak_against': points_fastbreak_against
                            }              

    return(jplaybyplayTwo)    