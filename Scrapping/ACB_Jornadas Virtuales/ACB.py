# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:48:46 2020

@author: jonbe
"""

import requests
import json

from generar_registros import *
from agregar_BDD import *

from variables import *
from scraping_ACB_playersInfo import *



Token = 'H4sIAAAAAAAAA32Ry3aqMBSG36iLi7qOw4oFk9PEQyohZEYilkCirIMF5OkbOmiVQUdZ+/bv798pbrAUkVR7BUEyAhcr0IIzWcoArEDdMBrA9VNxg5BPiQqp1wDGnEGTp/009MIZD4sd0dIsSxFMw7ATUaL2ulWxN7jZGV2poTegehuvrzKiTp7iRniL7zxhoZuzTZl5uhPKTTkD055Q+qTkkR6Pka4y9qNDTDjyu/hg6zxdVnkajq+UazmZ0Bstz7gT5j5HGhmtx4MPa9s/34dyxvUj41LL22OdMOxkqdXxSZN5d9r10BwNDS2v5Vh/zPg8ntD6W9OhwzHVvfDnPU033ZFHL495uinlmTTcsv/q5Yshmc+2GdNB8fXWs32wK3a4Ej7UMx8JT13LBy3LvUdsNXDDjf2P2X3YW6+EgQZUlwEf6gXeIgdvk4W9my52z2pfAReNcY8q1KPte4+CXtn/cub9p/jJef7j/Xvf/j150Sag6C1ctS41qVe3p6Fml5U4gf/xdecli8sn/TA0Eb8CAAA='


for i in range(220):

    p = i+104050 #104050
    id_match = ACB_PRE + str(p)
    repetido = comprobarExistPartido(id_match)

    if (repetido == 0 or REPETIR_REPETIDO):#== 0:

        url_match = 'https://api2.acb.com/api/v1/openapilive/Matches/matchlite?idMatch=' + str(p)
        url_playerStats = 'https://api2.acb.com/api/v1/openapilive/Boxscore/playermatchstatistics?idMatch=' + str(p)
        url_teamStats = 'https://api2.acb.com/api/v1/openapilive/Boxscore/teammatchstatistics?idMatch=' + str(p)
        url_events = 'https://api2.acb.com/api/v1/openapilive/PlayByPlay/matchevents?idMatch=' + str(p)

        try:
            r_info = requests.get(url_match, headers={'Authorization': Token})
            info = json.loads(r_info.content)
            info['id_competition']
            r_players = requests.get(url_playerStats, headers={'Authorization': Token})
            playersInfo = json.loads(r_players.content)
            r_teamStats = requests.get(url_teamStats, headers={'Authorization': Token})
            teamStatsInfo = json.loads(r_teamStats.content)
            r_events = requests.get(url_events, headers={'Authorization': Token})
            eventsInfo = json.loads(r_events.content)
            valido = True
        except:
            valido = False

        if valido:
            if info['id_competition']==1 and info['id_edition']==ID_EDICION and info['status']=='FINALIZED':
                
                print('Partido', id_match, ': ')
                startDate = datetime.datetime.fromtimestamp(info['start_date'])#.strftime('%d-%m-%Y - %H:%M')

                '''crear competiciones si no existen'''
                competition = gen_competicion(info)
                agregar_competicion(competition)


                '''crear arenas si no existen'''
                arena = gen_arena(info)
                agregar_arenas(arena)


                '''crear equipos si no existen'''
                team1 = gen_equipo(info['team1'], competition)
                agregar_equipo(team1)

                team2 = gen_equipo(info['team2'], competition)
                agregar_equipo(team2)


                #crear arbitros si no existen
                list_referees = gen_referee(info['referee'])
                for ref in list_referees:
                    agregar_referee(ref)
                    

                #crear coaches si no existen
                list_coaches1 = gen_coach(info['team1']['coaches'], team1, competition)
                for coach in list_coaches1:
                    agregar_coach(coach)
                    
                list_coaches2 = gen_coach(info['team2']['coaches'], team2, competition)
                for coach in list_coaches2:
                    agregar_coach(coach)
                    

                '''crear j_matches si no existen'''
                jmatch = gen_jmatch(info, team1, team2, list_referees, competition, id_match, startDate, arena)
                agregar_jmatch(jmatch)


                '''crear jugadores si no existen y relaciones jugador-equipo'''
                list_players = gen_player(playersInfo, competition)
                for player in list_players:
                    agregar_player(player)
                    

                
                #crear j_matchevents si no existen y tipos de playbyplay
                [jmatchevents, playbyplaytypes]= gen_jmatchevents(eventsInfo, competition, id_match, startDate)
                agregarMany_jmatchevents(jmatchevents)
                #for play in range(len(jmatchevents)):
                #    agregar_jmatchevents(jmatchevents[play])
                for tplay in range(len(playbyplaytypes)):
                    agregar_typesplaybyplay(playbyplaytypes[tplay])
                    

                    
                #crear j_minutesDistributionPlayer si no existen
                for player in list_players:
                        jminutesPlayer = gen_jminutesPlayer(player, jmatchevents, id_match, competition, startDate, team1, info)
                        agregarMany_jminutesPlayer(jminutesPlayer)
                        #for minute in range(len(jminutesPlayer)):
                         #   agregar_jminutesPlayer(jminutesPlayer[minute])


                #crear j_minutesDistributionPlayer si no existen
                jassistPlayer = gen_jassistPlayer(jmatchevents, id_match, competition, startDate, team1, info)            
                agregarMany_jassistsPlayer(jassistPlayer)
                #for assistPlayer in jassistPlayer:
                #    agregar_jassistsPlayer(assistPlayer)


                
                #crear j_shoots si no existen y tipos de shoots
                url_shoots = 'https://api2.acb.com/api/v1/openapilive/PlayByPlay/shotsbreakdown?idMatch=' + str(p)
                try:
                    r_shoots = requests.get(url_shoots, headers={'Authorization': Token})
                    shootsInfo = json.loads(r_shoots.content)
                    
                    jshoots = gen_jshoots(shootsInfo, competition, id_match, startDate, team1, info)
                    agregarMany_jshoots(jshoots)
                    #for shoot in range(len(jshoots)):
                    #    agregar_jshoots(jshoots[shoot])
                except:
                    print(' - Fallo en los tiros')



        
                #crear j_teamStats si no existen
                if (ACB_PRE + str(teamStatsInfo[0]['id_team'])) == team1['id_team']:
                    teamStatsInfo1 = teamStatsInfo[0]
                    teamStatsInfo2 = teamStatsInfo[1]
                else:
                    teamStatsInfo1 = teamStatsInfo[1]
                    teamStatsInfo2 = teamStatsInfo[0]
                jteamStatsA = gen_jteamStats(teamStatsInfo1, teamStatsInfo2, team1, team2, competition, id_match, startDate, info, jmatchevents, jassistPlayer, 0)
                agregar_jteamStats(jteamStatsA)
                jteamStatsB = gen_jteamStats(teamStatsInfo2, teamStatsInfo1, team2, team1, competition, id_match, startDate, info, jmatchevents, jassistPlayer, 0)
                agregar_jteamStats(jteamStatsB)
                for CUARTO in range(info['period']):
                    PD = CUARTO + 1
                    url_teamStatsP = 'https://api2.acb.com/api/v1/openapilive/Boxscore/teammatchstatistics?idMatch=' + str(p) + '&period=' + str(PD)
                    try:
                        r_teamStatsP = requests.get(url_teamStatsP, headers={'Authorization': Token})
                        teamStatsInfoP = json.loads(r_teamStatsP.content)
                        if (ACB_PRE + str(teamStatsInfoP[0]['id_team'])) == team1['id_team']:
                            teamStatsInfoP1 = teamStatsInfoP[0]
                            teamStatsInfoP2 = teamStatsInfoP[1]
                        else:
                            teamStatsInfoP1 = teamStatsInfoP[1]
                            teamStatsInfoP2 = teamStatsInfoP[0]
                        jteamStatsAP = gen_jteamStats(teamStatsInfoP1, teamStatsInfoP1, team1, team2, competition, id_match, startDate, info, jmatchevents, jassistPlayer, PD)
                        agregar_jteamStats(jteamStatsAP)
                        jteamStatsBP = gen_jteamStats(teamStatsInfoP2, teamStatsInfoP2, team2, team1, competition, id_match, startDate, info, jmatchevents, jassistPlayer, PD)
                        agregar_jteamStats(jteamStatsBP)
                    except:
                        print(' - Fallo en las estadisticas de equipo cuarto ' + str(PD))


                #crear j_playerStats si no existen
                jplayerStatsA = gen_jplayerStats(playersInfo, competition, id_match, startDate, info, team1, jmatchevents, jassistPlayer, jshoots, 0)
                agregarMany_jplayerStats(jplayerStatsA)
                #for player in range(len(jplayerStatsA)):
                #    agregar_jplayerStats(jplayerStatsA[player])
                for CUARTO in range(info['period']):
                    PD = CUARTO + 1
                    url_playerStatsP = 'https://api2.acb.com/api/v1/openapilive/Boxscore/playermatchstatistics?idMatch=' + str(p) + '&period=' + str(PD)
                    try:
                        r_playerStatsP = requests.get(url_playerStatsP, headers={'Authorization': Token})
                        playerStatsInfoP = json.loads(r_playerStatsP.content)
                        jplayerStatsAP = gen_jplayerStats(playerStatsInfoP, competition, id_match, startDate, info, team1, jmatchevents, jassistPlayer, jshoots, PD)
                        agregarMany_jplayerStats(jplayerStatsAP)
                        #for playerP in range(len(jplayerStatsAP)):
                        #    agregar_jplayerStats(jplayerStatsAP[playerP])
                    except:
                        print(' - Fallo en las estadisticas de jugador cuarto ' + str(PD))

                
                #crear j_markerbreakdown si no existen
                url_markerbreakdown = 'https://api2.acb.com/api/v1/openapilive/PlayByPlay/markerbreakdown?idMatch=' + str(p)
                try:
                    r_markerbreakdown = requests.get(url_markerbreakdown, headers={'Authorization': Token})
                    markerbreakdownInfo = json.loads(r_markerbreakdown.content)
                    [jmarkerbreakdownLocal, jmarkerbreakdownVisitor]= gen_jmarkerbreakdown(markerbreakdownInfo, id_match, competition, startDate, info, team1, team2, jmatchevents)
                    agregarMany_jmarkerbreakdown(jmarkerbreakdownLocal)
                    #for minuteMarker in jmarkerbreakdownLocal:
                    #    agregar_jmarkerbreakdown(minuteMarker)
                    agregarMany_jmarkerbreakdown(jmarkerbreakdownVisitor)
                    #for minuteMarker in jmarkerbreakdownVisitor:
                    #    agregar_jmarkerbreakdown(minuteMarker)
                except:
                    print(' - Fallo en los markerbreakdown')
                
                
                
                #crear j_fives, j_fours, j_threes, j_twos si no existen (j_matchevents agrupados por quintetos)
                [jplaybyplayFiveLocal, jplaybyplayFiveVisitor, jplaybyplayFiveLocalAWS, jplaybyplayFiveVisitorAWS] = gen_jmatcheventsFive(jmatchevents, id_match, competition, startDate, team1, team2, list_players, info, jshoots)
                
                jplaybyplayFourLocal = gen_jmatcheventsFour(jplaybyplayFiveLocal)
                jplaybyplayThreeLocal = gen_jmatcheventsThree(jplaybyplayFiveLocal)
                jplaybyplayTwoLocal = gen_jmatcheventsTwo(jplaybyplayFiveLocal)
                
                if len(jplaybyplayFiveLocal) > 1:
                    agregarMany_jfives(jplaybyplayFiveLocal)
                    #for play5 in range(len(jplaybyplayFiveLocal)):
                    #    agregar_jfives(jplaybyplayFiveLocal[play5])
                    
                    agregarMany_jfours(jplaybyplayFourLocal)
                    #for play4 in range(len(jplaybyplayFourLocal)):
                    #    agregar_jfours(jplaybyplayFourLocal[play4])

                    agregarMany_jthrees(jplaybyplayThreeLocal)
                    #for play3 in range(len(jplaybyplayThreeLocal)):
                    #    agregar_jthrees(jplaybyplayThreeLocal[play3])

                    agregarMany_jtwos(jplaybyplayTwoLocal)
                    #for play2 in range(len(jplaybyplayTwoLocal)):
                    #    agregar_jtwos(jplaybyplayTwoLocal[play2])
                    

                jplaybyplayFourVisitor = gen_jmatcheventsFour(jplaybyplayFiveVisitor)
                jplaybyplayThreeVisitor = gen_jmatcheventsThree(jplaybyplayFiveVisitor)
                jplaybyplayTwoVisitor = gen_jmatcheventsTwo(jplaybyplayFiveVisitor)
                
                if len(jplaybyplayFiveVisitor) > 1:
                    agregarMany_jfives(jplaybyplayFiveVisitor)
                    #for play5 in range(len(jplaybyplayFiveVisitor)):
                    #    agregar_jfives(jplaybyplayFiveVisitor[play5])
                    
                    agregarMany_jfours(jplaybyplayFourVisitor)
                    #for play4 in range(len(jplaybyplayFourVisitor)):
                    #    agregar_jfours(jplaybyplayFourVisitor[play4])

                    agregarMany_jthrees(jplaybyplayThreeVisitor)
                    #for play3 in range(len(jplaybyplayThreeVisitor)):
                    #    agregar_jthrees(jplaybyplayThreeVisitor[play3])

                    agregarMany_jtwos(jplaybyplayTwoVisitor)
                    #for play2 in range(len(jplaybyplayTwoVisitor)):
                    #    agregar_jtwos(jplaybyplayTwoVisitor[play2])
                 
                

coloresTeams()
coloresTeams2()
scraping_playersInfo()