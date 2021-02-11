import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Preprocesado y modelado
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import multiprocessing

def obtener_media_5ultimos_partidos(lista, p):
    l=len(lista)
    puntos = 0
    pt2ano = 0
    pt2int = 0
    pt3ano = 0
    pt3int = 0
    pt1ano = 0
    pt1int = 0
    defreb = 0
    offreb = 0
    totreb = 0
    ast = 0
    ste = 0
    tur = 0
    mat = 0
    tap_f = 0
    tap_c = 0
    falt_c = 0
    falt_r = 0
    val = 0
    dif = 0
    ca_points = 0
    steal_points = 0
    op2_points = 0
    paint_points = 0
    r_puntos = 0
    r_pt2ano = 0
    r_pt2int = 0
    r_pt3ano = 0
    r_pt3int = 0
    r_pt1ano = 0
    r_pt1int = 0
    r_defreb = 0
    r_offreb = 0
    r_totreb = 0
    r_ast = 0
    r_ste = 0
    r_tur = 0
    r_mat = 0
    r_val = 0
    r_ca_points = 0
    r_steal_points = 0
    r_op2_points = 0
    r_paint_points = 0

    for i in lista:
        puntos = puntos + i['puntos']
        pt2ano = pt2ano + i['pt2ano']
        pt2int = pt2int + i['pt2int']
        pt3ano = pt3ano + i['pt3ano']
        pt3int = pt3int + i['pt3int']
        pt1ano = pt1ano + i['pt1ano']
        pt1int = pt1int + i['pt1int']
        defreb = defreb + i['rdef']
        offreb = offreb + i['roff']
        totreb = totreb + i['rtot']
        ast = ast + i['ast']
        ste = ste + i['ste']
        tur = tur + i['tur']
        mat = mat + i['mat']
        tap_f = tap_f + i['tap_f']
        tap_c = tap_c + i['tap_c']
        falt_c = falt_c + i['falt']
        falt_r = falt_r + i['r_falt']
        val = val + i['val']
        dif = dif + i['dif']
        ca_points = ca_points + i['ca_points']
        steal_points = steal_points + i['steal_points']
        op2_points = op2_points + i['op2_points']
        paint_points = paint_points + i['paint_points']
        r_puntos = r_puntos + i['r_puntos']
        r_pt2ano = r_pt2ano + i['r_pt2ano']
        r_pt2int = r_pt2int + i['r_pt2int']
        r_pt3ano = r_pt3ano + i['r_pt3ano']
        r_pt3int = r_pt3int + i['r_pt3int']
        r_pt1ano = r_pt1ano + i['r_pt1ano']
        r_pt1int = r_pt1int + i['r_pt1int']
        r_defreb = r_defreb + i['r_rdef']
        r_offreb = r_offreb + i['r_roff']
        r_totreb = r_totreb + i['r_rtot']
        r_ast = r_ast + i['r_ast']
        r_ste = r_ste + i['r_ste']
        r_tur = r_tur + i['r_tur']
        r_mat = r_mat + i['r_mat']
        r_val = r_val + i['r_val']
        r_ca_points = r_ca_points + i['r_ca_points']
        r_steal_points = r_steal_points + i['r_steal_points']
        r_op2_points = r_op2_points + i['r_op2_points']
        r_paint_points = r_paint_points + i['r_paint_points']

    media={'partido': p, 'T1_puntos': puntos/l, 'T1_pt2ano': pt2ano/l, 'T1_pt2int': pt2int/l, 'T1_pt3ano': pt3ano/l, 'T1_pt3int': pt3int/l, 'T1_pt1ano': pt1ano/l,
           'T1_pt1int': pt1int/l,'T1_defreb': defreb/l, 'T1_offreb': offreb/l, 'T1_totreb': totreb/l, 'T1_ast': ast/l, 'T1_ste': ste/l,
           'T1_tur': tur/l,'T1_mat': mat/l, 'T1_tap_f': tap_f/l, 'T1_tap_c': tap_c/l, 'T1_falt_c': falt_c/l, 'T1_falt_r': falt_r/l, 'T1_val': val/l,'T1_dif': dif/l,
           'T1_ca_points': ca_points/l,'T1_steal_points': steal_points/l, 'T1_op2_points': op2_points/l, 'T1_paint_points': paint_points/l,
           'T1_r_puntos': r_puntos/l, 'T1_r_pt2ano': r_pt2ano/l, 'T1_r_pt2int': r_pt2int/l, 'T1_r_pt3ano': r_pt3ano/l, 'T1_r_pt3int': r_pt3int/l, 'T1_r_pt1ano': r_pt1ano/l,
           'T1_r_pt1int': r_pt1int/l, 'T1_r_defreb': r_defreb/l, 'T1_r_offreb': r_offreb/l, 'T1_r_totreb': r_totreb/l, 'T1_r_ast': r_ast/l, 'T1_r_ste': r_ste/l,
           'T1_r_tur': r_tur/l, 'T1_r_mat': r_mat/l, 'T1_r_val': r_val/l,
           'T1_r_ca_points': r_ca_points/l, 'T1_r_steal_points': r_steal_points/l, 'T1_r_op2_points': r_op2_points/l, 'T1_r_paint_points': r_paint_points/l}
    return media



conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select j_teamstats.id_match as partido, m.start_date as fecha, t.abrev_name as equipo, "
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
                        "inner join j_matches m on m.id_match=j_teamstats.id_match "
                        "where period =0 "
                        "order by fecha")
rows = cursor.fetchall()

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]
conexion.commit()
conexion.close()


df = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df.columns = ['partido', 'fecha', 'equipo', 'puntos', 'pt2ano', 'pt2int', 'pt2por', 'pt3ano', 'pt3int', 'pt3por',
              'pt1ano', 'pt1int', 'pt1por', 'rdef', 'roff', 'rtot',
              'ast', 'ste', 'tur', 'mat', 'tap_f', 'tap_c', 'falt', 'r_falt', 'val',
              'r_puntos', 'r_pt2ano', 'r_pt2int', 'r_pt2por', 'r_pt3ano', 'r_pt3int', 'r_pt3por',
              'r_pt1ano', 'r_pt1int', 'r_pt1por', 'r_rdef', 'r_roff', 'r_rtot',
              'r_ast', 'r_ste', 'r_tur', 'r_mat', 'r_val',
              'dif', 'banq_points', 'ca_points', 'steal_points', 'op2_points', 'paint_points',
              'r_ca_points', 'r_steal_points', 'r_op2_points', 'r_paint_points', 'res']


equipos_test=['Zaragoza', 'Unicaja', 'Valencia', 'Obradoiro', 'Murcia', 'Manresa',
         'Madrid', 'Joventut', 'Bilbao', 'Fuenlabrada', 'Estudiantes', 'Gran Canaria',
         'Tenerife', 'Burgos', 'Betis', 'Baskonia', 'Barsa', 'Andorra', 'Acunsa']

stats=[]
for team in equipos_test:
    partidos_previos=[]
    for index, row in df.iterrows():
        if row['equipo']==team:
            if len(partidos_previos)==5:
                media=obtener_media_5ultimos_partidos(partidos_previos, row['partido'])
                media['resultado_puntosAnotados'] = row['puntos']
                media['resultado_puntosRecibidos'] = row['r_puntos']
                media['resultado'] = row['res']
                partidos_previos.pop(0)
                partidos_previos.append(row)
                stats.append(media)
            else:
                partidos_previos.append(row)


games_remove=[]
for i in range(len(stats)):
    valido = False
    for game2 in stats:
        if stats[i]['partido'] == game2['partido'] and stats[i]['T1_puntos'] != game2['T1_puntos']:
           stats[i]['T2_puntos'] = game2['T1_puntos']
           stats[i]['T2_pt2ano'] = game2['T1_pt2ano']
           stats[i]['T2_pt2int'] = game2['T1_pt2int']
           stats[i]['T2_pt3ano'] = game2['T1_pt3ano']
           stats[i]['T2_pt3int'] = game2['T1_pt3int']
           stats[i]['T2_pt1ano'] = game2['T1_pt1ano']
           stats[i]['T2_pt1int'] = game2['T1_pt1int']
           stats[i]['T2_defreb'] = game2['T1_defreb']
           stats[i]['T2_offreb'] = game2['T1_offreb']
           stats[i]['T2_totreb'] = game2['T1_totreb']
           stats[i]['T2_ast'] = game2['T1_ast']
           stats[i]['T2_ste'] = game2['T1_ste']
           stats[i]['T2_tur'] = game2['T1_tur']
           stats[i]['T2_mat'] = game2['T1_mat']
           stats[i]['T2_tap_f'] = game2['T1_tap_f']
           stats[i]['T2_tap_c'] = game2['T1_tap_c']
           stats[i]['T2_falt_c'] = game2['T1_falt_c']
           stats[i]['T2_falt_r'] = game2['T1_falt_r']
           stats[i]['T2_val'] = game2['T1_val']
           stats[i]['T2_dif'] = game2['T1_dif']
           stats[i]['T2_ca_points'] = game2['T1_ca_points']
           stats[i]['T2_steal_points'] = game2['T1_steal_points']
           stats[i]['T2_op2_points'] = game2['T1_op2_points']
           stats[i]['T2_paint_points'] = game2['T1_paint_points']
           stats[i]['T2_r_puntos'] = game2['T1_r_puntos']
           stats[i]['T2_r_pt2ano'] = game2['T1_r_pt2ano']
           stats[i]['T2_r_pt2int'] = game2['T1_r_pt2int']
           stats[i]['T2_r_pt3ano'] = game2['T1_r_pt3ano']
           stats[i]['T2_r_pt3int'] = game2['T1_r_pt3int']
           stats[i]['T2_r_pt1ano'] = game2['T1_r_pt1ano']
           stats[i]['T2_r_pt1int'] = game2['T1_r_pt1int']
           stats[i]['T2_r_defreb'] = game2['T1_r_defreb']
           stats[i]['T2_r_offreb'] = game2['T1_r_offreb']
           stats[i]['T2_r_totreb'] = game2['T1_r_totreb']
           stats[i]['T2_r_ast'] = game2['T1_r_ast']
           stats[i]['T2_r_ste'] = game2['T1_r_ste']
           stats[i]['T2_r_tur'] = game2['T1_r_tur']
           stats[i]['T2_r_mat'] = game2['T1_r_mat']
           stats[i]['T2_r_val'] = game2['T1_r_val']
           stats[i]['T2_r_ca_points'] = game2['T1_r_ca_points']
           stats[i]['T2_r_steal_points'] = game2['T1_r_steal_points']
           stats[i]['T2_r_op2_points'] = game2['T1_r_op2_points']
           stats[i]['T2_r_paint_points'] = game2['T1_r_paint_points']
           valido = True
           break
    if valido == False:
        games_remove.insert(0, i)

for game in games_remove:
    stats.pop(game)

df_stats=pd.DataFrame(stats)

df_stats = df_stats.drop(['partido'], axis=1)

df_resultado = df_stats.drop(['resultado_puntosAnotados', 'resultado_puntosRecibidos'], axis=1).copy()
df_puntosAnotados = df_stats.drop(['resultado', 'resultado_puntosRecibidos'], axis=1).copy()
df_puntosRecibidos = df_stats.drop(['resultado_puntosAnotados', 'resultado'], axis=1).copy()









## 1. Cross Validation:
## Separación del dataset en 2: training y test:
X_train, X_test, y_train, y_test = train_test_split(
                                        df_resultado.drop(columns = 'resultado'),
                                        df_resultado['resultado'],
                                        test_size=0.2,
                                        random_state = 2
                                    )
'''
# Grid de hiperparámetros evaluados
# ==============================================================================
param_grid = {'n_estimators': [500, 1000], # numero de árboles a calcular
              'max_features': [10,20,30,40,50,60,70,80], # número de features a contemplar
              'max_depth': [None], # profundidad máxima del árbol
              'criterion': ['gini']
             }

# Búsqueda por grid search con validación cruzada
# ==============================================================================
grid = GridSearchCV(
        estimator=RandomForestClassifier(random_state = 123),
        param_grid=param_grid,

        scoring='accuracy',
        n_jobs=multiprocessing.cpu_count() - 1,
        cv=RepeatedKFold(n_splits=5, n_repeats=3, random_state=123),
        refit=True,
        verbose=0,
        return_train_score=True
       )

grid.fit(X=X_train, y=y_train)

# Resultados
# ==============================================================================
resultados = pd.DataFrame(grid.cv_results_)
print(resultados.filter(regex = '(param*|mean_t|std_t)') \
    .drop(columns = 'params') \
    .sort_values('mean_test_score', ascending = False) \
    .head(10))

# Mejores hiperparámetros por validación cruzada
# ==============================================================================
print("----------------------------------------")
print("Mejores hiperparámetros encontrados (cv)")
print("----------------------------------------")
print(grid.best_params_, ":", grid.best_score_, grid.scoring)

# Asignación de los hiperparámetros al modelo final
modelo_final = grid.best_estimator_

plot_confusion_matrix(modelo_final, X_test, y_test)
plt.show()

predicciones = modelo_final.predict(X = X_test)

print(
    classification_report(
        y_true = y_test,
        y_pred = predicciones
    )
)
'''


clf1 = RandomForestClassifier(max_depth=None, n_estimators=1000, max_features=20)
clf1.fit(X_train, y_train)


plot_confusion_matrix(clf1, X_test, y_test)
plt.show()

predicciones = clf1.predict(X = X_test)

print(
    classification_report(
        y_true = y_test,
        y_pred = predicciones
    )
)

importancia_predictores = pd.DataFrame(
                            {'predictor': X_train.columns,
                             'importancia': clf1.feature_importances_}
                            )
print("Importancia de los predictores en el modelo")
print("-------------------------------------------")
print(importancia_predictores.sort_values('importancia', ascending=False))











X_train, X_test, y_train, y_test = train_test_split(
                                        df_puntosAnotados.drop(columns = 'resultado_puntosAnotados'),
                                        df_puntosAnotados['resultado_puntosAnotados'],
                                        test_size=0.2,
                                        random_state = 123)

'''
# Grid de hiperparámetros evaluados
# ==============================================================================
param_grid = {'n_estimators': [250, 500, 1000],
              'max_features': [10,20,30,40,50,60,70,80],
              'max_depth'   : [None, 10, 20, 50]
             }

# Búsqueda por grid search con validación cruzada
# ==============================================================================
grid = GridSearchCV(
        estimator  = RandomForestRegressor(random_state = 123),
        param_grid = param_grid,
        scoring    = 'neg_root_mean_squared_error',
        n_jobs     = multiprocessing.cpu_count() - 1,
        cv         = RepeatedKFold(n_splits=5, n_repeats=3, random_state=123),
        refit      = True,
        verbose    = 0,
        return_train_score = True
       )

grid.fit(X = X_train, y = y_train)

# Resultados
# ==============================================================================
resultados = pd.DataFrame(grid.cv_results_)
print(resultados.filter(regex = '(param.*|mean_t|std_t)') \
    .drop(columns = 'params') \
    .sort_values('mean_test_score', ascending = False) \
    .head(4))

# Mejores hiperparámetros por validación cruzada
# ==============================================================================
print("----------------------------------------")
print("Mejores hiperparámetros encontrados (cv)")
print("----------------------------------------")
print(grid.best_params_, ":", grid.best_score_, grid.scoring)
'''

clf2 = RandomForestRegressor(max_depth=10, n_estimators=500, max_features=10)
clf2.fit(X_train, y_train)


# Error de test del modelo final
# ==============================================================================
predicciones = clf2.predict(X = X_test)
rmse = mean_squared_error(
        y_true  = y_test,
        y_pred  = predicciones,
        squared = False
       )
print(f"El error (rmse) de test es: {rmse}")

importancia_predictores = pd.DataFrame(
                            {'predictor': df_puntosAnotados.drop(columns = "resultado_puntosAnotados").columns,
                             'importancia': clf2.feature_importances_}
                            )
print("Importancia de los predictores en el modelo")
print("-------------------------------------------")
print(importancia_predictores.sort_values('importancia', ascending=False))






X_train, X_test, y_train, y_test = train_test_split(
                                        df_puntosRecibidos.drop(columns = 'resultado_puntosRecibidos'),
                                        df_puntosRecibidos['resultado_puntosRecibidos'],
                                        test_size=1,
                                        random_state = None)

'''
# Grid de hiperparámetros evaluados
# ==============================================================================
param_grid = {'n_estimators': [250, 500, 1000],
              'max_features': [10,20,30,40,50,60,70,80],
              'max_depth'   : [None, 10, 20, 50]
             }

# Búsqueda por grid search con validación cruzada
# ==============================================================================
grid = GridSearchCV(
        estimator  = RandomForestRegressor(random_state = 123),
        param_grid = param_grid,
        scoring    = 'neg_root_mean_squared_error',
        n_jobs     = multiprocessing.cpu_count() - 1,
        cv         = RepeatedKFold(n_splits=5, n_repeats=3, random_state=123),
        refit      = True,
        verbose    = 0,
        return_train_score = True
       )

grid.fit(X = X_train, y = y_train)

# Resultados
# ==============================================================================
resultados = pd.DataFrame(grid.cv_results_)
print(resultados.filter(regex = '(param.*|mean_t|std_t)') \
    .drop(columns = 'params') \
    .sort_values('mean_test_score', ascending = False) \
    .head(4))

# Mejores hiperparámetros por validación cruzada
# ==============================================================================
print("----------------------------------------")
print("Mejores hiperparámetros encontrados (cv)")
print("----------------------------------------")
print(grid.best_params_, ":", grid.best_score_, grid.scoring)
'''

clf3 = RandomForestRegressor(max_depth=20, n_estimators=1000, max_features=20)
clf3.fit(X_train, y_train)


# Error de test del modelo final
# ==============================================================================
predicciones = clf3.predict(X = X_test)
rmse = mean_squared_error(
        y_true  = y_test,
        y_pred  = predicciones,
        squared = False
       )
print(f"El error (rmse) de test es: {rmse}")

importancia_predictores = pd.DataFrame(
                            {'predictor': df_puntosRecibidos.drop(columns = "resultado_puntosRecibidos").columns,
                             'importancia': clf3.feature_importances_}
                            )
print("Importancia de los predictores en el modelo")
print("-------------------------------------------")
print(importancia_predictores.sort_values('importancia', ascending=False))







conexion = sqlite3.connect('../../ACB_Jornadas Virtuales/ACB_BDD/ACB.db')
cursor = conexion.cursor()
table = cursor.execute("select j_teamstats.id_match as partido, m.start_date as fecha, t.abrev_name as equipo, "
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
                        "inner join j_matches m on m.id_match=j_teamstats.id_match "
                        "where period =0 "
                        "order by fecha desc")
rows = cursor.fetchall()

table = {}
for n in range(len(rows)):
    table[str(n)] = rows[n]
conexion.commit()
conexion.close()


df_actual = pd.DataFrame(table, columns = [str(n) for n in range(len(table))]).T

df_actual.columns = ['partido', 'fecha', 'equipo', 'puntos', 'pt2ano', 'pt2int', 'pt2por', 'pt3ano', 'pt3int', 'pt3por',
              'pt1ano', 'pt1int', 'pt1por', 'rdef', 'roff', 'rtot',
              'ast', 'ste', 'tur', 'mat', 'tap_f', 'tap_c', 'falt', 'r_falt', 'val',
              'r_puntos', 'r_pt2ano', 'r_pt2int', 'r_pt2por', 'r_pt3ano', 'r_pt3int', 'r_pt3por',
              'r_pt1ano', 'r_pt1int', 'r_pt1por', 'r_rdef', 'r_roff', 'r_rtot',
              'r_ast', 'r_ste', 'r_tur', 'r_mat', 'r_val',
              'dif', 'banq_points', 'ca_points', 'steal_points', 'op2_points', 'paint_points',
              'r_ca_points', 'r_steal_points', 'r_op2_points', 'r_paint_points', 'res']

stats_actual=[]
for team in equipos_test:
    partidos_previos=[]
    for index, row in df_actual.iterrows():
        if row['equipo']==team:
            if len(partidos_previos)==5:
                media=obtener_media_5ultimos_partidos(partidos_previos, row['partido'])
                media['equipo']= team
                stats_actual.append(media)
                break
            else:
                partidos_previos.append(row)

df_stats_actual=pd.DataFrame(stats_actual)
pred1='Barsa'
for index, row in df_stats_actual.iterrows():
    if pred1==row['equipo']:
        a = row.tolist()
        a.pop(0)
        a.pop(-1)
pred2='Barsa'
for index, row in df_stats_actual.iterrows():
    if pred2==row['equipo']:
        b = row.tolist()
        b.pop(0)
        b.pop(-1)

partido =a+b
partido = pd.DataFrame(partido).T

prediccion = clf1.predict(X = partido)
probabilidad = clf1.predict_proba(X = partido)

print('Prediccion: ', prediccion)
print('Probabilidad: ', probabilidad)

anotacionLocal = clf2.predict(X = partido)
anotacionLocal =round(anotacionLocal[0], 0)

print('Anotacion Local: ', anotacionLocal)

anotacionVisitante = clf3.predict(X = partido)
anotacionVisitante =round(anotacionVisitante[0], 0)

print('Anotacion Visitante: ', anotacionVisitante)





















