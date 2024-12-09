from functions import *
import math
import time


def agregar_competicion(competition):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO competition (id_competition, name, id_edition, year, id_phase, phase_name, category, country, gender, image, image_2) VALUES ('{}','{}','{}','{}', '{}','{}','{}','{}','{}','{}','{}')".format(competition['id_competition'], competition['name'], competition['id_edition'], competition['year'], competition['id_phase'], competition['phase_name'], competition['category'], competition['country'],competition['gender'], competition['image'], competition['image_2']) )
        except :
            #print("La competición id '{}', edición '{}', fase '{}' ya existe.".format(competition['id_competition'], competition['id_edition'], competition['id_phase']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO competition (id_competition, name, id_edition, year, id_phase, phase_name, category, country, gender, image, image_2) VALUES ('{}','{}','{}','{}', '{}','{}','{}','{}','{}','{}','{}')".format(competition['id_competition'], competition['name'], competition['id_edition'], competition['year'], competition['id_phase'], competition['phase_name'], competition['category'], competition['country'],competition['gender'], competition['image'], competition['image_2']) )
        except :
            #print("La competición id '{}', edición '{}', fase '{}' ya existe.".format(competition['id_competition'], competition['id_edition'], competition['id_phase']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_arenas(arena):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO arenas (id_arena, name, town, country, image) VALUES ('{}','{}','{}','{}','{}')".format(arena['id_arena'], arena['name'],arena['town'], arena['country'], arena['image1']) )
        except :
            #print("El arena id '{}', nombre '{}' ya existe.".format(arena['id_arena'], arena['name']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO arenas (id_arena, name, town, country, image) VALUES ('{}','{}','{}','{}','{}')".format(arena['id_arena'], arena['name'],arena['town'], arena['country'], arena['image1']) )
        except :
            #print("El arena id '{}', nombre '{}' ya existe.".format(arena['id_arena'], arena['name']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_equipo(equipo):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO teams(id_club,id_team, year,short_team_name,abrev_name, team_name, gender, country, id_competition, id_edition, image, image_2) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                equipo['id_club'], equipo['id_team'], equipo['year'],equipo['short_team_name'], equipo['abrev_name'], equipo['team_name'],equipo['gender'],equipo['country'], equipo['id_competition'], equipo['id_edition'], equipo['image'], equipo['image_2']))
        except :
            #print("El equipo id '{}' ya existe.".format(equipo['id_team']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO teams(id_club,id_team, year,short_team_name,abrev_name, team_name, gender, country, id_competition, id_edition, image, image_2) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                equipo['id_club'], equipo['id_team'], equipo['year'],equipo['short_team_name'], equipo['abrev_name'], equipo['team_name'],equipo['gender'],equipo['country'], equipo['id_competition'], equipo['id_edition'], equipo['image'], equipo['image_2']))
        except :
            #print("El equipo id '{}' ya existe.".format(equipo['id_team']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_referee(referee):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO p_referees (id_referee, id_person, name, name_nick, nacionality, gender, license) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(
                referee['id_referee'], referee['id_person'], referee['name'], referee['name_nick'],  referee['nacionality'], referee['gender'], referee['license']))
        except :
            #print("El engominado id '{}' ya existe.".format(referee['id_referee']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO p_referees (id_referee, id_person, name, name_nick, nacionality, gender, license) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(
                referee['id_referee'], referee['id_person'], referee['name'], referee['name_nick'],  referee['nacionality'], referee['gender'], referee['license']))
        except :
            #print("El engominado id '{}' ya existe.".format(referee['id_referee']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_coach(coach):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO p_coaches (id_coach, id_person, name, name_nick, coachtype, id_team, id_competition, id_edition) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                coach['id_coach'], coach['id_person'], coach['name'], coach['name_nick'], coach['coachtype'], coach['id_team'], coach['id_competition'], coach['id_edition']))
        except :
            #print("El coach id '{}' ya existe.".format(coach['id_coach']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO p_coaches (id_coach, id_person, name, name_nick, coachtype, id_team, id_competition, id_edition) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                coach['id_coach'], coach['id_person'], coach['name'], coach['name_nick'], coach['coachtype'], coach['id_team'], coach['id_competition'], coach['id_edition']))
        except :
            #print("El coach id '{}' ya existe.".format(coach['id_coach']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_jmatch(jmatch):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute("INSERT INTO j_matches (id_competition, id_edition, id_phase, id_match, num_match, matchWeek, matchWeek_description, start_date, id_localteam, local_points, id_visitorteam, visitor_points, id_arena, crowd, id_referee1, id_referee2, id_referee3) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                jmatch['id_competition'], jmatch['id_edition'], jmatch['id_phase'], jmatch['id_match'], jmatch['num_match'],
                jmatch['matchWeek'], jmatch['matchWeek_description'], jmatch['start_date'],
                jmatch['id_localteam'], jmatch['local_points'], jmatch['id_visitorteam'], jmatch['visitor_points'], jmatch['id_arena'], jmatch['crowd'],
                jmatch['id_referee1'], jmatch['id_referee2'], jmatch['id_referee3']))
        except :
            print("Partido id '{}' ya existe.".format(jmatch['id_match']))
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        #try:
        cursor2.execute("INSERT INTO j_matches (id_competition, id_edition, id_phase, id_match, num_match, matchWeek, matchWeek_description, start_date, id_localteam, local_points, id_visitorteam, visitor_points, id_arena, crowd, id_referee1, id_referee2, id_referee3) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            jmatch['id_competition'], jmatch['id_edition'], jmatch['id_phase'], jmatch['id_match'], jmatch['num_match'],
            jmatch['matchWeek'], jmatch['matchWeek_description'], jmatch['start_date'], jmatch['id_arena'], jmatch['crowd'],
            jmatch['id_localteam'], jmatch['local_points'], jmatch['id_visitorteam'], jmatch['visitor_points'],
            jmatch['id_referee1'], jmatch['id_referee2'], jmatch['id_referee3']))
        #except :
        #    print("Partido id '{}' ya existe.".format(jmatch['id_match']))
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregar_player(player):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute(
                "INSERT INTO p_players (id_player, id_person, name, name_nick, gender, dorsal, id_competition, id_edition, id_team, image, image_2) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    player['id_player'], player['id_person'], player['name'], player['name_nick'],player['gender'], player['dorsal'], player['id_competition'], player['id_edition'],player['id_team'], player['image'], player['image_2']))
        except :
            #print("El player id '{}' ya existe.".format(player['id_player']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute(
                "INSERT INTO p_players (id_player, id_person, name, name_nick, gender, dorsal, id_competition, id_edition, id_team, image, image_2) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    player['id_player'], player['id_person'], player['name'], player['name_nick'],player['gender'], player['dorsal'], player['id_competition'], player['id_edition'],player['id_team'], player['image'], player['image_2']))
        except :
            #print("El player id '{}' ya existe.".format(player['id_player']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)
    

def agregar_jteamStats (jteamStats) :
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        list_value_integers = ['time_played','points','rival_points','difference','differencePeriod','pt2_success','pt2_tried','pt2_percentage',
                            'pt3_success','pt3_tried','pt3_percentage','pt1_success','pt1_tried','pt1_percentage'	,'deffensive_rebound',
                            'offensive_rebound','total_rebound','assists','turnovers','dunks',
                            'blocks','received_blocks','personal_fouls','received_fouls',
                            'val','timeouts','substitutions','max_difference','minute_max_difference','max_difference_against','minute_max_difference_against',
                            'leader_changes','time_as_leader', 'time_losing','best_streak','best_streak_against','bench_points','starters_points',
                            'rival_bench_points','rival_starters_points','points_fastbreak','points_fastbreak_against',
                            'points_aftersteal','points_aftersteal_against','points_afterassist','points_afterassist_against',
                            'points_secondchance','points_secondchance_against','points_in_the_paint','points_in_the_paint_against',
                            'bench_assists','starters_assists',
                            'bench_steals','starters_steals','bench_turnovers','starters_turnovers','bench_assists_against','starters_assists_against',
                            'bench_steals_against','starters_steals_against','bench_turnovers_against','starters_turnovers_against','rival_2pt_success',
                            'rival_2pt_tried','rival_2pt_percentage','rival_3pt_success','rival_3pt_tried','rival_3pt_percentage','rival_1pt_success',
                            'rival_1pt_tried','rival_1pt_percentage','rival_deffensive_rebound','rival_offensive_rebound','rival_total_rebound','rival_assists',
                            'rival_steals','rival_turnovers','rival_dunks','rival_val','rival_timeouts','rival_substitutions','rival_bench_points','rival_starters_points']
        for value in list_value_integers:
            jteamStats[value] = 0 if math.isnan(jteamStats[value]) else jteamStats[value]
        try:
            cursor.execute("INSERT INTO j_teamstats(id_competition, id_edition, id_phase, id_match, id_team, start_date, rival_id_team, rival_team_name, crowd, period, periodD, lado, time_played, points, rival_points, difference, differencePeriod, pt2_success, pt2_tried, pt2_percentage, pt3_success, pt3_tried, pt3_percentage, pt1_success, pt1_tried, pt1_percentage, deffensive_rebound, offensive_rebound, total_rebound, assists, steals, turnovers, dunks, blocks, received_blocks, personal_fouls, received_fouls, val, timeouts, substitutions, max_difference, minute_max_difference, max_difference_against, minute_max_difference_against, leader_changes, time_as_leader, time_losing, best_streak, best_streak_against, bench_points, starters_points, points_fastbreak, points_fastbreak_against, points_aftersteal, points_aftersteal_against, points_afterassist, points_afterassist_against, points_secondchance,points_secondchance_against, points_in_the_paint, points_in_the_paint_against, bench_assists, starters_assists, bench_steals, starters_steals, bench_turnovers,starters_turnovers, bench_assists_against, starters_assists_against, bench_steals_against, starters_steals_against, bench_turnovers_against, starters_turnovers_against, rival_2pt_success, rival_2pt_tried, rival_2pt_percentage, rival_3pt_success, rival_3pt_tried, rival_3pt_percentage, rival_1pt_success, rival_1pt_tried, rival_1pt_percentage, rival_deffensive_rebound, rival_offensive_rebound, rival_total_rebound, rival_assists, rival_steals, rival_turnovers, rival_dunks, rival_val, rival_timeouts, rival_substitutions, rival_bench_points, rival_starters_points, overtime, result, resultD, resultPeriod, resultPeriodD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jteamStats['id_competition'], jteamStats['id_edition'], jteamStats['id_phase'], jteamStats['id_match'], jteamStats['id_team'], jteamStats['start_date'], jteamStats['rival_id_team'], jteamStats['rival_team_name'], jteamStats['crowd'], jteamStats['period'], jteamStats['periodD'], jteamStats['lado'], jteamStats['time_played'], jteamStats['points'], jteamStats['rival_points'], jteamStats['difference'], jteamStats['differencePeriod'], jteamStats['pt2_success'], jteamStats['pt2_tried'], jteamStats['pt2_percentage'], jteamStats['pt3_success'], jteamStats['pt3_tried'], jteamStats['pt3_percentage'], jteamStats['pt1_success'], jteamStats['pt1_tried'], jteamStats['pt1_percentage'], jteamStats['deffensive_rebound'], jteamStats['offensive_rebound'], jteamStats['total_rebound'], jteamStats['assists'], jteamStats['steals'], jteamStats['turnovers'], jteamStats['dunks'], jteamStats['blocks'], jteamStats['received_blocks'], jteamStats['personal_fouls'], jteamStats['received_fouls'], jteamStats['val'], jteamStats['timeouts'], jteamStats['substitutions'], jteamStats['max_difference'], jteamStats['minute_max_difference'], jteamStats['max_difference_against'], jteamStats['minute_max_difference_against'], jteamStats['leader_changes'], jteamStats['time_as_leader'], jteamStats['time_losing'], jteamStats['best_streak'], jteamStats['best_streak_against'], jteamStats['bench_points'], jteamStats['starters_points'], jteamStats['points_fastbreak'], jteamStats['points_fastbreak_against'], jteamStats['points_aftersteal'], jteamStats['points_aftersteal_against'], jteamStats['points_afterassist'], jteamStats['points_afterassist_against'], jteamStats['points_secondchance'], jteamStats['points_secondchance_against'], jteamStats['points_in_the_paint'], jteamStats['points_in_the_paint_against'], jteamStats['bench_assists'], jteamStats['starters_assists'], jteamStats['bench_steals'], jteamStats['starters_steals'], jteamStats['bench_turnovers'], jteamStats['starters_turnovers'], jteamStats['bench_assists_against'], jteamStats['starters_assists_against'], jteamStats['bench_steals_against'], jteamStats['starters_steals_against'], jteamStats['bench_turnovers_against'], jteamStats['starters_turnovers_against'], jteamStats['rival_2pt_success'], jteamStats['rival_2pt_tried'], jteamStats['rival_2pt_percentage'], jteamStats['rival_3pt_success'], jteamStats['rival_3pt_tried'], jteamStats['rival_3pt_percentage'], jteamStats['rival_1pt_success'], jteamStats['rival_1pt_tried'], jteamStats['rival_1pt_percentage'], jteamStats['rival_deffensive_rebound'], jteamStats['rival_offensive_rebound'], jteamStats['rival_total_rebound'], jteamStats['rival_assists'], jteamStats['rival_steals'], jteamStats['rival_turnovers'], jteamStats['rival_dunks'], jteamStats['rival_val'], jteamStats['rival_timeouts'], jteamStats['rival_substitutions'], jteamStats['rival_bench_points'], jteamStats['rival_starters_points'], jteamStats['overtime'], jteamStats['result'], jteamStats['resultD'], jteamStats['resultPeriod'], jteamStats['resultPeriodD']))
        except :
            print("La estadisticas del partido id '{}' del equipo'{}' ya existen.".format(jteamStats['id_match'], jteamStats['id_team']))
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute("INSERT INTO j_teamstats(id_competition, id_edition, id_phase, id_match, id_team, start_date, rival_id_team, rival_team_name, crowd, period, periodD, lado, time_played, points, rival_points, difference, differencePeriod, pt2_success, pt2_tried, pt2_percentage, pt3_success, pt3_tried, pt3_percentage, pt1_success, pt1_tried, pt1_percentage, deffensive_rebound, offensive_rebound, total_rebound, assists, steals, turnovers, dunks, blocks, received_blocks, personal_fouls, received_fouls, val, timeouts, substitutions, max_difference, minute_max_difference, max_difference_against, minute_max_difference_against, leader_changes, time_as_leader, time_losing, best_streak, best_streak_against, bench_points, starters_points, points_fastbreak, points_fastbreak_against, points_aftersteal, points_aftersteal_against, points_afterassist, points_afterassist_against, points_secondchance,points_secondchance_against, points_in_the_paint, points_in_the_paint_against, bench_assists, starters_assists, bench_steals, starters_steals, bench_turnovers,starters_turnovers, bench_assists_against, starters_assists_against, bench_steals_against, starters_steals_against, bench_turnovers_against, starters_turnovers_against, rival_2pt_success, rival_2pt_tried, rival_2pt_percentage, rival_3pt_success, rival_3pt_tried, rival_3pt_percentage, rival_1pt_success, rival_1pt_tried, rival_1pt_percentage, rival_deffensive_rebound, rival_offensive_rebound, rival_total_rebound, rival_assists, rival_steals, rival_turnovers, rival_dunks, rival_val, rival_timeouts, rival_substitutions, rival_bench_points, rival_starters_points, overtime, result, resultD, resultPeriod, resultPeriodD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jteamStats['id_competition'], jteamStats['id_edition'], jteamStats['id_phase'], jteamStats['id_match'], jteamStats['id_team'], jteamStats['start_date'], jteamStats['rival_id_team'], jteamStats['rival_team_name'], jteamStats['crowd'], jteamStats['period'], jteamStats['periodD'], jteamStats['lado'], jteamStats['time_played'], jteamStats['points'], jteamStats['rival_points'], jteamStats['difference'], jteamStats['differencePeriod'], jteamStats['pt2_success'], jteamStats['pt2_tried'], jteamStats['pt2_percentage'], jteamStats['pt3_success'], jteamStats['pt3_tried'], jteamStats['pt3_percentage'], jteamStats['pt1_success'], jteamStats['pt1_tried'], jteamStats['pt1_percentage'], jteamStats['deffensive_rebound'], jteamStats['offensive_rebound'], jteamStats['total_rebound'], jteamStats['assists'], jteamStats['steals'], jteamStats['turnovers'], jteamStats['dunks'], jteamStats['blocks'], jteamStats['received_blocks'], jteamStats['personal_fouls'], jteamStats['received_fouls'], jteamStats['val'], jteamStats['timeouts'], jteamStats['substitutions'], jteamStats['max_difference'], jteamStats['minute_max_difference'], jteamStats['max_difference_against'], jteamStats['minute_max_difference_against'], jteamStats['leader_changes'], jteamStats['time_as_leader'], jteamStats['time_losing'], jteamStats['best_streak'], jteamStats['best_streak_against'], jteamStats['bench_points'], jteamStats['starters_points'], jteamStats['points_fastbreak'], jteamStats['points_fastbreak_against'], jteamStats['points_aftersteal'], jteamStats['points_aftersteal_against'], jteamStats['points_afterassist'], jteamStats['points_afterassist_against'], jteamStats['points_secondchance'], jteamStats['points_secondchance_against'], jteamStats['points_in_the_paint'], jteamStats['points_in_the_paint_against'], jteamStats['bench_assists'], jteamStats['starters_assists'], jteamStats['bench_steals'], jteamStats['starters_steals'], jteamStats['bench_turnovers'], jteamStats['starters_turnovers'], jteamStats['bench_assists_against'], jteamStats['starters_assists_against'], jteamStats['bench_steals_against'], jteamStats['starters_steals_against'], jteamStats['bench_turnovers_against'], jteamStats['starters_turnovers_against'], jteamStats['rival_2pt_success'], jteamStats['rival_2pt_tried'], jteamStats['rival_2pt_percentage'], jteamStats['rival_3pt_success'], jteamStats['rival_3pt_tried'], jteamStats['rival_3pt_percentage'], jteamStats['rival_1pt_success'], jteamStats['rival_1pt_tried'], jteamStats['rival_1pt_percentage'], jteamStats['rival_deffensive_rebound'], jteamStats['rival_offensive_rebound'], jteamStats['rival_total_rebound'], jteamStats['rival_assists'], jteamStats['rival_steals'], jteamStats['rival_turnovers'], jteamStats['rival_dunks'], jteamStats['rival_val'], jteamStats['rival_timeouts'], jteamStats['rival_substitutions'], jteamStats['rival_bench_points'], jteamStats['rival_starters_points'], jteamStats['overtime'], jteamStats['result'], jteamStats['resultD'], jteamStats['resultPeriod'], jteamStats['resultPeriodD']))
        except :
            print("La estadisticas del partido id '{}' del equipo'{}' ya existen.".format(jteamStats['id_match'], jteamStats['id_team']))
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)



def agregarMany_jplayerStats (jplayerStats) :
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jplayerStats) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase', 'id_match', 'id_team', 'id_player', 'start_date', 'period', 'periodD', 'lado', 'sstarting', 'finishing', 'time_played', 'points', 'pt2_success', 'pt2_tried', 'pt2_percentage', 'pt3_success', 'pt3_tried', 'pt3_percentage', 'pt1_success', 'pt1_tried', 'pt1_percentage', 'deffensive_rebound', 'offensive_rebound', 'total_rebound', 'assists', 'steals', 'turnovers', 'dunks', 'counter_attacks', 'blocks', 'received_blocks', 'personal_fouls', 'received_fouls', 'disqualified', 'difference', 'differencePlayer', 'val', 'points_fast_break', 'points_in_the_paint', 'points_second_chance', 'points_aftersteal', 'points_afterassist', 'rival_team_name', 'result', 'resultD']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jplayerStats, listOfKeys)
    insert_st = 'INSERT INTO j_playerstats (id_competition, id_edition, id_phase, id_match, id_team, id_player, start_date, period, periodD, lado, sstarting, finishing, time_played, points, pt2_success, pt2_tried, pt2_percentage, pt3_success, pt3_tried, pt3_percentage, pt1_success, pt1_tried, pt1_percentage, deffensive_rebound, offensive_rebound, total_rebound, assists, steals, turnovers, dunks, counter_attacks, blocks, received_blocks, personal_fouls, received_fouls, disqualified, difference, differencePlayer, val, points_fast_break, points_in_the_paint, points_second_chance, points_aftersteal, points_afterassist, rival_team_name, result, resultD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
        #    print('Error al agregar a BBDD el jplayerStats ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_playerstats (id_competition, id_edition, id_phase, id_match, id_team, id_player, start_date, period, periodD, lado, sstarting, finishing, time_played, points, pt2_success, pt2_tried, pt2_percentage, pt3_success, pt3_tried, pt3_percentage, pt1_success, pt1_tried, pt1_percentage, deffensive_rebound, offensive_rebound, total_rebound, assists, steals, turnovers, dunks, counter_attacks, blocks, received_blocks, personal_fouls, received_fouls, disqualified, difference, differencePlayer, val, points_fast_break, points_in_the_paint, points_second_chance, points_aftersteal, points_afterassist, rival_team_name, result, resultD) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)



'''
def agregar_jplayerStats (jplayerStats) :
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute("INSERT INTO j_playerstats(id_competition, id_edition, id_phase, id_match, id_team, id_player, start_date, period, periodD, lado, sstarting, finishing, time_played, points, pt2_success, pt2_tried, pt2_percentage, pt3_success, pt3_tried, pt3_percentage, pt1_success, pt1_tried, pt1_percentage, deffensive_rebound, offensive_rebound, total_rebound, assists, steals, turnovers, dunks, counter_attacks, blocks, received_blocks, personal_fouls, received_fouls, disqualified, difference, differencePlayer, val, points_fast_break, points_in_the_paint, points_second_chance, points_aftersteal, points_afterassist, rival_team_name, result, resultD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jplayerStats['id_competition'], jplayerStats['id_edition'], jplayerStats['id_phase'], jplayerStats['id_match'], jplayerStats['id_team'], jplayerStats['id_player'], jplayerStats['start_date'], jplayerStats['period'], jplayerStats['periodD'], jplayerStats['lado'], jplayerStats['sstarting'], jplayerStats['finishing'], jplayerStats['time_played'], jplayerStats['points'], jplayerStats['pt2_success'], jplayerStats['pt2_tried'], jplayerStats['pt2_percentage'], jplayerStats['pt3_success'], jplayerStats['pt3_tried'], jplayerStats['pt3_percentage'], jplayerStats['pt1_success'], jplayerStats['pt1_tried'], jplayerStats['pt1_percentage'], jplayerStats['deffensive_rebound'], jplayerStats['offensive_rebound'], jplayerStats['total_rebound'], jplayerStats['assists'], jplayerStats['steals'], jplayerStats['turnovers'], jplayerStats['dunks'], jplayerStats['counter_attacks'], jplayerStats['blocks'], jplayerStats['received_blocks'], jplayerStats['personal_fouls'], jplayerStats['received_fouls'], jplayerStats['disqualified'], jplayerStats['difference'], jplayerStats['differencePlayer'], jplayerStats['val'], jplayerStats['points_fast_break'], jplayerStats['points_in_the_paint'], jplayerStats['points_second_chance'], jplayerStats['points_aftersteal'], jplayerStats['points_afterassist'], jplayerStats['rival_team_name'], jplayerStats['result'], jplayerStats['resultD']))
    except :
        print("La estadisticas del partido id '{}' del jugador '{}' ya existen.".format(
            jplayerStats['id_match'], jplayerStats['id_player']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''


def agregarMany_jmarkerbreakdown(jmarkerbreakdown):
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jmarkerbreakdown) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase','id_match', 'id_team', 'period', 'periodD', 'lado', 'result', 'resultD', 'startDate', 'minute', 'second', 'scoreTeam', 'scoreRivalTeam', 'score_differential', 'posesions']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jmarkerbreakdown, listOfKeys)
    insert_st = 'INSERT INTO j_markerbreakdown (id_competition, id_edition, id_phase,id_match, id_team, period, periodD, lado, result, resultD, start_date, minute, second, score_team, score_rivalTeam, score_differential, posesions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:    #try:
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
        #    print('Error al agregar a BBDD el jmarkerbreakdown ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        #except :
        #    print('Error al agregar a BBDD el jmarkerbreakdown ')
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_markerbreakdown (id_competition, id_edition, id_phase,id_match, id_team, period, periodD, lado, result, resultD, start_date, minute, second, score_team, score_rivalTeam, score_differential, posesions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


'''
def agregar_jmarkerbreakdown(jmarkerbreakdown):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute(
            "INSERT INTO j_markerbreakdown (id_competition, id_edition, id_phase,id_match, id_team, period, periodD, lado, result, resultD, start_date, minute, second, score_team, score_rivalTeam, score_differential, posesions) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    jmarkerbreakdown['id_competition'], jmarkerbreakdown['id_edition'], jmarkerbreakdown['id_phase'],jmarkerbreakdown['id_match'], jmarkerbreakdown['id_team'], jmarkerbreakdown['period'], jmarkerbreakdown['periodD'],
                    jmarkerbreakdown['lado'], jmarkerbreakdown['result'], jmarkerbreakdown['resultD'], jmarkerbreakdown['startDate'], jmarkerbreakdown['minute'],
                    jmarkerbreakdown['second'], jmarkerbreakdown['scoreTeam'], jmarkerbreakdown['scoreRivalTeam'], jmarkerbreakdown['score_differential'], jmarkerbreakdown['posesions']))
        
        except :
            print("El markerbreakdowndel partido id '{}' minuto '{}' ya existe.".format(jmarkerbreakdown['id_match'], jmarkerbreakdown['minute']))
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
'''
'''
def agregar_jminutesPlayer(jminutesPlayer):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute(
            "INSERT INTO j_minutesDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player, name_player, period, periodD, lado, result, resultD, start_date, minute, second, playIn) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                jminutesPlayer['id_competition'], jminutesPlayer['id_edition'], jminutesPlayer['id_phase'], jminutesPlayer['id_match'], jminutesPlayer['id_team'], jminutesPlayer['id_player'], jminutesPlayer['name_player'], jminutesPlayer['period'], jminutesPlayer['periodD'],
                jminutesPlayer['lado'], jminutesPlayer['result'], jminutesPlayer['resultD'], jminutesPlayer['startDate'], jminutesPlayer['minute'],
                jminutesPlayer['second'], jminutesPlayer['playIn']))
    except :
        print("El minuteDistributionPlayer partido id '{}' minuto '{}' ya existe.".format(jminutesPlayer['id_match'], jminutesPlayer['minute']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''
def agregarMany_jminutesPlayer(jminutesPlayer):
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jminutesPlayer) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase', 'id_match', 'id_team', 'id_player', 'name_player', 'period', 'periodD', 'lado', 'result', 'resultD', 'startDate', 'minute', 'second', 'playIn']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jminutesPlayer, listOfKeys)
    insert_st = 'INSERT INTO j_minutesDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player, name_player, period, periodD, lado, result, resultD, start_date, minute, second, playIn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
        try:
            cursor.executemany(insert_st, listOfTuples_out)
        except :
            print('Error al agregar a BBDD el minuteDistributionPlayer ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_minutesDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player, name_player, period, periodD, lado, result, resultD, start_date, minute, second, playIn) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


def agregarMany_jassistsPlayer(jminutesPlayer):
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jminutesPlayer) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase', 'id_match', 'id_team', 'id_player_assist', 'name_player_assist', 'id_player_shot', 'name_player_shot', 'period', 'periodD', 'lado', 'result', 'resultD', 'startDate', 'minute', 'second', 'id_playbyplaytype', 'description']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jminutesPlayer, listOfKeys)
    insert_st = 'INSERT INTO j_assistsDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player_assist, name_player_assist, id_player_shot, name_player_shot, period, periodD, lado, result, resultD, start_date, minute, second, id_playbyplaytype, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
        #    print('Error al agregar a BBDD el j_assistsDistributionPlayer ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2() 
        insert_st2 = 'INSERT INTO j_assistsDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player_assist, name_player_assist, id_player_shot, name_player_shot, period, periodD, lado, result, resultD, start_date, minute, second, id_playbyplaytype, description) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' 
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jassistsPlayer(jminutesPlayer):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute(
            "INSERT INTO j_assistsDistributionPlayer (id_competition, id_edition, id_phase, id_match, id_team, id_player_assist, name_player_assist, id_player_shot, name_player_shot, period, periodD, lado, result, resultD, start_date, minute, second, id_playbyplaytype, description) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                jminutesPlayer['id_competition'], jminutesPlayer['id_edition'], jminutesPlayer['id_phase'], jminutesPlayer['id_match'], jminutesPlayer['id_team'], jminutesPlayer['id_player_assist'], jminutesPlayer['name_player_assist'], jminutesPlayer['id_player_shot'], jminutesPlayer['name_player_shot'], jminutesPlayer['period'], jminutesPlayer['periodD'],
                jminutesPlayer['lado'], jminutesPlayer['result'], jminutesPlayer['resultD'], jminutesPlayer['startDate'], jminutesPlayer['minute'],
                jminutesPlayer['second'], jminutesPlayer['id_playbyplaytype'], jminutesPlayer['description']))
    except :
        print("El assistDistributionPlayer partido id '{}' minuto '{}' ya existe.".format(jminutesPlayer['id_match'], jminutesPlayer['minute']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''

def agregarMany_jmatchevents(jmatchevents):
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jmatchevents) 
    listOfKeys = ['id_competition','id_edition','id_phase', 'start_date','id_match', 'id_event', 'period', 'minute', 'second', 'score_local', 'score_visitor', 'id_team', 'id_player', 'name_player', 'id_playbyplaytype', 'id_globalPBP_typeID', 'id_principalPBP_typeID', 'id_secundaryPBP_typeID', 'wall_clock', 'previous_action']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jmatchevents, listOfKeys)
    insert_st = 'INSERT INTO j_matchevents (id_competition,id_edition,id_phase, start_date,id_match, id_event, period, minute, second, score_local, score_visitor, id_team, id_player, name_player, id_playbyplaytype, id_globalPBP_typeID, id_principalPBP_typeID, id_secundaryPBP_typeID, wall_clock, previous_action) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
        #print('Error al agregar a BBDD el j_matchevents ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_matchevents (id_competition,id_edition,id_phase, start_date,id_match, id_event, period, minute, second, score_local, score_visitor, id_team, id_player, name_player, id_playbyplaytype, id_globalPBP_typeID, id_principalPBP_typeID, id_secundaryPBP_typeID, wall_clock, previous_action) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jmatchevents(jmatchevents):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute(
            "INSERT INTO j_matchevents (id_competition,id_edition,id_phase, start_date,id_match, id_event, period, minute, second, score_local, score_visitor, id_team, id_player, name_player, id_playbyplaytype, id_globalPBP_typeID, id_principalPBP_typeID, id_secundaryPBP_typeID, wall_clock, previous_action) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                jmatchevents['id_competition'], jmatchevents['id_edition'], jmatchevents['id_phase'],
                jmatchevents['start_date'], jmatchevents['id_match'], jmatchevents['id_event'],
                jmatchevents['period'], jmatchevents['minute'], jmatchevents['second'], jmatchevents['score_local'], jmatchevents['score_visitor'], jmatchevents['id_team'], jmatchevents['id_player'], jmatchevents['name_player'], jmatchevents['id_playbyplaytype'], jmatchevents['id_globalPBP_typeID'], jmatchevents['id_principalPBP_typeID'], jmatchevents['id_secundaryPBP_typeID'], jmatchevents['wall_clock'], jmatchevents['previous_action']))
    except :
        print("El evento id '{}' del partido '{}' ya existe.".format(jmatchevents['id_event'], jmatchevents['id_match']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''


def agregar_typesplaybyplay(playbyplaytypes):
    if SQL_NUBE:
        [conexion, cursor] = conectar_BDD()
        try:
            cursor.execute(
                "INSERT INTO t_playbyplay (id, id_playbyplaytype, description, normalized_description, id_globalPBP_typeID, id_globalPBP_typeD, id_principalPBP_typeID, id_principalPBP_typeD, id_secundaryPBP_typeID, id_secundaryPBP_typeD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    playbyplaytypes['id'],playbyplaytypes['id_playbyplaytype'], playbyplaytypes['description'],playbyplaytypes['normalized_description'], playbyplaytypes['id_globalPBP_typeID'], playbyplaytypes['id_globalPBP_typeD'],playbyplaytypes['id_principalPBP_typeID'], playbyplaytypes['id_principalPBP_typeD'], playbyplaytypes['id_secundaryPBP_typeID'],playbyplaytypes['id_secundaryPBP_typeD']))
        except :
            #print("La accion de playbyplay id '{}' ya existe.".format(playbyplaytypes['id_playbyplaytype']))
            True
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()
        try:
            cursor2.execute(
                "INSERT INTO t_playbyplay (id, id_playbyplaytype, description, normalized_description, id_globalPBP_typeID, id_globalPBP_typeD, id_principalPBP_typeID, id_principalPBP_typeD, id_secundaryPBP_typeID, id_secundaryPBP_typeD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    playbyplaytypes['id'],playbyplaytypes['id_playbyplaytype'], playbyplaytypes['description'],playbyplaytypes['normalized_description'], playbyplaytypes['id_globalPBP_typeID'], playbyplaytypes['id_globalPBP_typeD'],playbyplaytypes['id_principalPBP_typeID'], playbyplaytypes['id_principalPBP_typeD'], playbyplaytypes['id_secundaryPBP_typeID'],playbyplaytypes['id_secundaryPBP_typeD']))
        except :
            #print("La accion de playbyplay id '{}' ya existe.".format(playbyplaytypes['id_playbyplaytype']))
            True
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)
    


def agregarMany_jshoots(jshoots):
    [conexion, cursor] = conectar_BDD()
    df = pd.DataFrame(jshoots) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase', 'id_match', 'id_shoot', 'id_team', 'id_player', 'start_date', 'lado', 'period', 'periodD', 'minute', 'second', 'score_local', 'score_visitor', 'id_action', 'action', 'result', 'posX', 'posY', 'fastbreak', 'aftersteal', 'secondchance', 'zone', 'resultD']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jshoots, listOfKeys)
    insert_st = 'INSERT INTO j_shoots (id_competition, id_edition, id_phase, id_match, id_shoot, id_team, id_player, start_date, lado, period, periodD, minute, second, score_local, score_visitor, id_action, action, result, posX, posY, fastbreak, aftersteal, secondchance, zone, resultD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
        #print('Error al agregar a BBDD el jshoots ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_shoots (id_competition, id_edition, id_phase, id_match, id_shoot, id_team, id_player, start_date, lado, period, periodD, minute, second, score_local, score_visitor, id_action, action, result, posX, posY, fastbreak, aftersteal, secondchance, zone, resultD) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)


'''
def agregar_jshoots(jshoots):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute(
            "INSERT INTO j_shoots (id_competition, id_edition, id_phase, id_match, id_shoot, id_team, id_player, start_date, lado, period, periodD, minute, second, score_local, score_visitor, id_action, action, result, posX, posY, fastbreak, aftersteal, secondchance, zone, resultD) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jshoots['id_competition'],jshoots['id_edition'],jshoots['id_phase'],jshoots['id_match'],jshoots['id_shoot'],jshoots['id_team'],jshoots['id_player'],jshoots['start_date'],jshoots['lado'],jshoots['period'],jshoots['periodD'],jshoots['minute'], jshoots['second'], jshoots['score_local'], jshoots['score_visitor'], jshoots['id_action'], jshoots['action'], jshoots['result'],jshoots['posX'],jshoots['posY'],jshoots['fastbreak'],jshoots['aftersteal'],jshoots['secondchance'],jshoots['zone'],jshoots['resultD']))
    except :
        print("El tiro idjshoots['{}' del partidojshoots['{}' ya existe.".format(jshoots['id_shoot'], jshoots['id_match']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''

   
'''    
def agregar_typesshoot(shoottypes):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute(
            "INSERT INTO t_shoots (id_shoottype, description, normalized_description) VALUES ('{}','{}','{}')".format(
                shoottypes['id_shoottype'], shoottypes['description'], shoottypes['normalized_description']))
    except :
        print("El tipo de tiro idjshoots['{}' ya existe.".format(shoottypes['id_shoottype']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''

def agregarMany_jfives(jplaybyplayFive):
    df = pd.DataFrame(jplaybyplayFive) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase','id_match', 'id_event', 'start_date', 'id_team', 'scoreTeam', 'id_rivalTeam', 'scoreRivalTeam', 'id_five', 'name_five', 'num_players', 'lado', 'period', 'periodD', 'minute', 'second', 'second_gameIn', 'isInCombinationSub', 'second_gameOut', 'id_player1', 'id_player2', 'id_player3', 'id_player4', 'id_player5', 'name_player1', 'name_player2', 'name_player3', 'name_player4', 'name_player5', 'id_teamEjecutor', 'id_playerEjecutor', 'id_playbyplaytype', 'result', 'resultD', 'team_name', 'rival_team_name', 'difference', 'sstarting', 'finishing' , 'points_fastbreak', 'points_aftersteal', 'points_afterassist', 'points_secondchance', 'points_in_the_paint', 'points_fastbreak_against', 'points_aftersteal_against', 'points_afterassist_against', 'points_secondchance_against', 'points_in_the_paint_against']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jplaybyplayFive, listOfKeys)
    insert_st = 'INSERT INTO j_fives (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_five, name_five, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, id_player5, name_player1, name_player2, name_player3, name_player4, name_player5, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        [conexion, cursor] = conectar_BDD()
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
            #print('Error al agregar a BBDD el jplaybyplayFive ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_fives (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_five, name_five, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, id_player5, name_player1, name_player2, name_player3, name_player4, name_player5, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jfives(jplaybyplayFive):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute("INSERT INTO j_fives(id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_five, name_five, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, id_player5, name_player1, name_player2, name_player3, name_player4, name_player5, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jplaybyplayFive['id_competition'], jplaybyplayFive['id_edition'], jplaybyplayFive['id_phase'],jplaybyplayFive['id_match'], jplaybyplayFive['id_event'], jplaybyplayFive['start_date'], jplaybyplayFive['id_team'], jplaybyplayFive['scoreTeam'], jplaybyplayFive['id_rivalTeam'], jplaybyplayFive['scoreRivalTeam'], jplaybyplayFive['id_five'], jplaybyplayFive['name_five'], jplaybyplayFive['num_players'], jplaybyplayFive['lado'], jplaybyplayFive['period'], jplaybyplayFive['periodD'], jplaybyplayFive['minute'], jplaybyplayFive['second'], jplaybyplayFive['second_gameIn'], jplaybyplayFive['isInCombinationSub'], jplaybyplayFive['second_gameOut'], jplaybyplayFive['id_player1'], jplaybyplayFive['id_player2'], jplaybyplayFive['id_player3'], jplaybyplayFive['id_player4'], jplaybyplayFive['id_player5'], jplaybyplayFive['name_player1'], jplaybyplayFive['name_player2'], jplaybyplayFive['name_player3'], jplaybyplayFive['name_player4'], jplaybyplayFive['name_player5'], jplaybyplayFive['id_teamEjecutor'], jplaybyplayFive['id_playerEjecutor'], jplaybyplayFive['id_playbyplaytype'], jplaybyplayFive['result'], jplaybyplayFive['resultD'], jplaybyplayFive['team_name'], jplaybyplayFive['rival_team_name'], jplaybyplayFive['difference'], jplaybyplayFive['sstarting'], jplaybyplayFive['finishing'], jplaybyplayFive['points_fastbreak'], jplaybyplayFive['points_aftersteal'], jplaybyplayFive['points_afterassist'], jplaybyplayFive['points_secondchance'], jplaybyplayFive['points_in_the_paint'], jplaybyplayFive['points_fastbreak_against'], jplaybyplayFive['points_aftersteal_against'], jplaybyplayFive['points_afterassist_against'], jplaybyplayFive['points_secondchance_against'], jplaybyplayFive['points_in_the_paint_against']))
    except :
        print("La acción del partido id '{}' número'{}' ya existe en quintetos.".format(
            jplaybyplayFive['id_match'], jplaybyplayFive['id_event']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''


def agregarMany_jfours(jplaybyplayFour):
    df = pd.DataFrame(jplaybyplayFour) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase','id_match', 'id_event', 'start_date', 'id_team', 'scoreTeam', 'id_rivalTeam', 'scoreRivalTeam', 'id_four', 'name_four', 'num_players', 'lado', 'period', 'periodD', 'minute', 'second', 'second_gameIn', 'isInCombinationSub', 'second_gameOut', 'id_player1', 'id_player2', 'id_player3', 'id_player4', 'name_player1', 'name_player2', 'name_player3', 'name_player4', 'id_teamEjecutor', 'id_playerEjecutor', 'id_playbyplaytype', 'result', 'resultD', 'team_name', 'rival_team_name', 'difference', 'sstarting', 'finishing' , 'points_fastbreak', 'points_aftersteal', 'points_afterassist', 'points_secondchance', 'points_in_the_paint', 'points_fastbreak_against', 'points_aftersteal_against', 'points_afterassist_against', 'points_secondchance_against', 'points_in_the_paint_against']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jplaybyplayFour, listOfKeys)
    insert_st = 'INSERT INTO j_fours (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_four, name_four, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, name_player1, name_player2, name_player3, name_player4, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        ''' 
        [conexion, cursor] = conectar_BDD()
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
            #print('Error al agregar a BBDD el jplaybyplayFour ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
        ''' 
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_fours (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_four, name_four, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, name_player1, name_player2, name_player3, name_player4, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jfours(jplaybyplayFour):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute("INSERT INTO j_fours(id_competition, id_edition, id_phase,id_match, id_event, startDate, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_four, name_four, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, id_player4, name_player1, name_player2, name_player3, name_player4, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jplaybyplayFour['id_competition'], jplaybyplayFour['id_edition'], jplaybyplayFour['id_phase'],jplaybyplayFour['id_match'], jplaybyplayFour['id_event'], jplaybyplayFour['start_date'], jplaybyplayFour['id_team'], jplaybyplayFour['scoreTeam'], jplaybyplayFour['id_rivalTeam'], jplaybyplayFour['scoreRivalTeam'], jplaybyplayFour['id_four'], jplaybyplayFour['name_four'], jplaybyplayFour['num_players'], jplaybyplayFour['lado'], jplaybyplayFour['period'], jplaybyplayFour['periodD'], jplaybyplayFour['minute'], jplaybyplayFour['second'], jplaybyplayFour['second_gameIn'], jplaybyplayFour['isInCombinationSub'], jplaybyplayFour['second_gameOut'], jplaybyplayFour['id_player1'], jplaybyplayFour['id_player2'], jplaybyplayFour['id_player3'], jplaybyplayFour['id_player4'], jplaybyplayFour['name_player1'], jplaybyplayFour['name_player2'], jplaybyplayFour['name_player3'], jplaybyplayFour['name_player4'], jplaybyplayFour['id_teamEjecutor'], jplaybyplayFour['id_playerEjecutor'], jplaybyplayFour['id_playbyplaytype'], jplaybyplayFour['result'], jplaybyplayFour['resultD'], jplaybyplayFour['team_name'], jplaybyplayFour['rival_team_name'], jplaybyplayFour['difference'], jplaybyplayFour['sstarting'], jplaybyplayFour['finishing'], jplaybyplayFour['points_fastbreak'], jplaybyplayFour['points_aftersteal'], jplaybyplayFour['points_afterassist'], jplaybyplayFour['points_secondchance'], jplaybyplayFour['points_in_the_paint'], jplaybyplayFour['points_fastbreak_against'], jplaybyplayFour['points_aftersteal_against'], jplaybyplayFour['points_afterassist_against'], jplaybyplayFour['points_secondchance_against'], jplaybyplayFour['points_in_the_paint_against']))
    except :
        print("La acción del partido id '{}' número'{}' ya existe en cuartetos.".format(
            jplaybyplayFour['id_match'], jplaybyplayFour['id_event']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''

def agregarMany_jthrees(jplaybyplayThree):
    df = pd.DataFrame(jplaybyplayThree) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase','id_match', 'id_event', 'start_date', 'id_team', 'scoreTeam', 'id_rivalTeam', 'scoreRivalTeam', 'id_three', 'name_three', 'num_players', 'lado', 'period', 'periodD', 'minute', 'second', 'second_gameIn', 'isInCombinationSub', 'second_gameOut', 'id_player1', 'id_player2', 'id_player3', 'name_player1', 'name_player2', 'name_player3', 'id_teamEjecutor', 'id_playerEjecutor', 'id_playbyplaytype', 'result', 'resultD', 'team_name', 'rival_team_name', 'difference', 'sstarting', 'finishing' , 'points_fastbreak', 'points_aftersteal', 'points_afterassist', 'points_secondchance', 'points_in_the_paint', 'points_fastbreak_against', 'points_aftersteal_against', 'points_afterassist_against', 'points_secondchance_against', 'points_in_the_paint_against']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jplaybyplayThree, listOfKeys)
    insert_st = 'INSERT INTO j_threes (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_three, name_three, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, name_player1, name_player2, name_player3, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        ''' 
        [conexion, cursor] = conectar_BDD()
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
            #print('Error al agregar a BBDD el jplaybyplayThree ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
        ''' 
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_threes (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_three, name_three, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, name_player1, name_player2, name_player3, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jthrees(jplaybyplayThree):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute("INSERT INTO j_threes(id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_three, name_three, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, id_player3, name_player1, name_player2, name_player3, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jplaybyplayThree['id_competition'], jplaybyplayThree['id_edition'], jplaybyplayThree['id_phase'],jplaybyplayThree['id_match'], jplaybyplayThree['id_event'], jplaybyplayThree['start_date'], jplaybyplayThree['id_team'], jplaybyplayThree['scoreTeam'], jplaybyplayThree['id_rivalTeam'], jplaybyplayThree['scoreRivalTeam'], jplaybyplayThree['id_three'], jplaybyplayThree['name_three'], jplaybyplayThree['num_players'], jplaybyplayThree['lado'], jplaybyplayThree['period'], jplaybyplayThree['periodD'], jplaybyplayThree['minute'], jplaybyplayThree['second'], jplaybyplayThree['second_gameIn'], jplaybyplayThree['isInCombinationSub'], jplaybyplayThree['second_gameOut'], jplaybyplayThree['id_player1'], jplaybyplayThree['id_player2'], jplaybyplayThree['id_player3'], jplaybyplayThree['name_player1'], jplaybyplayThree['name_player2'], jplaybyplayThree['name_player3'], jplaybyplayThree['id_teamEjecutor'], jplaybyplayThree['id_playerEjecutor'], jplaybyplayThree['id_playbyplaytype'], jplaybyplayThree['result'], jplaybyplayThree['resultD'], jplaybyplayThree['team_name'], jplaybyplayThree['rival_team_name'], jplaybyplayThree['difference'], jplaybyplayThree['sstarting'], jplaybyplayThree['finishing'], jplaybyplayThree['points_fastbreak'], jplaybyplayThree['points_aftersteal'], jplaybyplayThree['points_afterassist'], jplaybyplayThree['points_secondchance'], jplaybyplayThree['points_in_the_paint'], jplaybyplayThree['points_fastbreak_against'], jplaybyplayThree['points_aftersteal_against'], jplaybyplayThree['points_afterassist_against'], jplaybyplayThree['points_secondchance_against'], jplaybyplayThree['points_in_the_paint_against']))
    except :
        print("La acción del partido id '{}' número'{}' ya existe en trios.".format(
            jplaybyplayThree['id_match'], jplaybyplayThree['id_event']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''

def agregarMany_jtwos(jplaybyplayTwo):
    df = pd.DataFrame(jplaybyplayTwo) 
    listOfKeys = ['id_competition', 'id_edition', 'id_phase','id_match', 'id_event', 'start_date', 'id_team', 'scoreTeam', 'id_rivalTeam', 'scoreRivalTeam', 'id_two', 'name_two', 'num_players', 'lado', 'period', 'periodD', 'minute', 'second', 'second_gameIn', 'isInCombinationSub', 'second_gameOut', 'id_player1', 'id_player2', 'name_player1', 'name_player2', 'id_teamEjecutor', 'id_playerEjecutor', 'id_playbyplaytype', 'result', 'resultD', 'team_name', 'rival_team_name', 'difference', 'sstarting', 'finishing' , 'points_fastbreak', 'points_aftersteal', 'points_afterassist', 'points_secondchance', 'points_in_the_paint', 'points_fastbreak_against', 'points_aftersteal_against', 'points_afterassist_against', 'points_secondchance_against', 'points_in_the_paint_against']
    listOfTuples_out = generarListOfTuples_from_ListOfDicts(jplaybyplayTwo, listOfKeys)
    insert_st = 'INSERT INTO j_twos (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_two, name_two, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, name_player1, name_player2, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    if SQL_NUBE:
            #try:
        '''  
        [conexion, cursor] = conectar_BDD()
        cursor.executemany(insert_st, listOfTuples_out)
        #except :
            #print('Error al agregar a BBDD el jplaybyplayTwo ')
        conexion.commit()
        conexion.close()
        time.sleep(0.5)
        '''
    if SQL_LOCAL:
        [conexion2, cursor2] = conectar_BDD_2()  
        insert_st2 = 'INSERT INTO j_twos (id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_two, name_two, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, name_player1, name_player2, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor2.executemany(insert_st2, listOfTuples_out)
        conexion2.commit()
        conexion2.close()
        time.sleep(0.5)

'''
def agregar_jtwos(jplaybyplayTwo):
    [conexion, cursor] = conectar_BDD()
    try:
        cursor.execute("INSERT INTO j_twos(id_competition, id_edition, id_phase,id_match, id_event, start_date, id_team, scoreTeam, id_rivalTeam, scoreRivalTeam, id_two, name_two, num_players, lado, period, periodD, minute, second, second_gameIn, isInCombinationSub, second_gameOut, id_player1, id_player2, name_player1, name_player2, id_teamEjecutor, id_playerEjecutor, id_playbyplaytype, result, resultD, team_name, rival_team_name, difference, sstarting, finishing , points_fastbreak, points_aftersteal, points_afterassist, points_secondchance, points_in_the_paint, points_fastbreak_against, points_aftersteal_against, points_afterassist_against, points_secondchance_against, points_in_the_paint_against) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(jplaybyplayTwo['id_competition'], jplaybyplayTwo['id_edition'], jplaybyplayTwo['id_phase'],jplaybyplayTwo['id_match'], jplaybyplayTwo['id_event'], jplaybyplayTwo['start_date'], jplaybyplayTwo['id_team'], jplaybyplayTwo['scoreTeam'], jplaybyplayTwo['id_rivalTeam'], jplaybyplayTwo['scoreRivalTeam'], jplaybyplayTwo['id_two'], jplaybyplayTwo['name_two'], jplaybyplayTwo['num_players'], jplaybyplayTwo['lado'], jplaybyplayTwo['period'], jplaybyplayTwo['periodD'], jplaybyplayTwo['minute'], jplaybyplayTwo['second'], jplaybyplayTwo['second_gameIn'], jplaybyplayTwo['isInCombinationSub'], jplaybyplayTwo['second_gameOut'], jplaybyplayTwo['id_player1'], jplaybyplayTwo['id_player2'], jplaybyplayTwo['name_player1'], jplaybyplayTwo['name_player2'], jplaybyplayTwo['id_teamEjecutor'], jplaybyplayTwo['id_playerEjecutor'], jplaybyplayTwo['id_playbyplaytype'], jplaybyplayTwo['result'], jplaybyplayTwo['resultD'], jplaybyplayTwo['team_name'], jplaybyplayTwo['rival_team_name'], jplaybyplayTwo['difference'], jplaybyplayTwo['sstarting'], jplaybyplayTwo['finishing'], jplaybyplayTwo['points_fastbreak'], jplaybyplayTwo['points_aftersteal'], jplaybyplayTwo['points_afterassist'], jplaybyplayTwo['points_secondchance'], jplaybyplayTwo['points_in_the_paint'], jplaybyplayTwo['points_fastbreak_against'], jplaybyplayTwo['points_aftersteal_against'], jplaybyplayTwo['points_afterassist_against'], jplaybyplayTwo['points_secondchance_against'], jplaybyplayTwo['points_in_the_paint_against']))
    except :
        print("La acción del partido id '{}' número'{}' ya existe en parejas.".format(
            jplaybyplayTwo['id_match'], jplaybyplayTwo['id_event']))
    conexion.commit()
    conexion.close()
    time.sleep(0.5)
'''