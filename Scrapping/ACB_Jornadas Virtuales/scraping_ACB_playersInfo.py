import requests
from bs4 import BeautifulSoup
from functions import *
import time
import datetime


def scraping_playersInfo():
    print("Scrapeando players info:")
    obj_posiciones= {
        "Base": "Base",
        "Escolta": "Alero", 
        "Alero": "Alero",
        "Ala-pívot": "Pivot",
        "Pívot": "Pivot"
    }
    obj_posiciones_2 = {
        "Base": "Base",
        "Escolta": "Escolta", 
        "Alero": "Alero",
        "Ala-pívot": "Ala Pivot",
        "Pívot": "Pivot"
    }
    list_clubes = ['22', '14', '12', '16', '28', '5', '592', '3', '13', '10', '25', '2', '4', '8', '9', '591', '657', '658']

    for club in list_clubes:

        # URL de la página de plantilla
        url = "https://www.acb.com/club/plantilla/id/" + club

        # Realizamos la solicitud a la página
        response = requests.get(url)

        # Verificamos que la solicitud fue exitosa
        if response.status_code == 200:
            # Parseamos el HTML con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscamos la tabla o sección que contiene los datos de los jugadores
            players = soup.find_all('article', class_='caja_miembro_plantilla caja_jugador_medio_cuerpo')  # Clase específica para cada jugador
            
            # Iteramos por cada jugador y extraemos el nombre y la edad
            for player in players:              
                time.sleep(0.5)
                link_tag = player.find('a')['href']
                id_player_url = link_tag[(link_tag.index('ver/')+4):(link_tag.index('-'))]
                url_player = "https://www.acb.com/jugador/temporada-a-temporada/id/"+id_player_url

                response_player = requests.get(url_player)

                # Verificamos que la solicitud fue exitosa
                if response_player.status_code == 200:
                    # Parseamos el HTML con BeautifulSoup
                    try:
                        soup_player = BeautifulSoup(response_player.content, 'html.parser')

                        posicion_div = soup_player.find('div', class_='datos_basicos posicion roboto_condensed')
                        posicion_web = posicion_div.span.text
                        posicion = obj_posiciones[posicion_web]
                        posicion_2 = obj_posiciones_2[posicion_web]

                        altura_div = soup_player.find('div', class_='datos_basicos altura roboto_condensed')
                        altura_txt = altura_div.span.text
                        altura = 100*int(altura_txt[:altura_txt.index(',')]) + int(altura_txt[altura_txt.index(',')+1:altura_txt.index(' ')])

                        lugar_nacimiento_div = soup_player.find('div', class_='datos_secundarios lugar_nacimiento roboto_condensed')
                        lugar_nacimiento_span = lugar_nacimiento_div.find('span', class_='roboto_condensed_bold')
                        lugar_nacimiento = lugar_nacimiento_span.text
                        country = lugar_nacimiento[(lugar_nacimiento.index(',')+2):]

                        fecha_nacimiento_div = soup_player.find('div', class_='datos_secundarios fecha_nacimiento roboto_condensed')
                        fecha_nacimiento_span = fecha_nacimiento_div.find('span', class_='roboto_condensed_bold')
                        fecha_nacimiento_txt = fecha_nacimiento_span.text
                        fecha_nacimiento = fecha_nacimiento_txt[:(fecha_nacimiento_txt.index(' ('))]
                        fecha_nacimiento_date = datetime.datetime.strptime(fecha_nacimiento, '%d/%m/%Y')
                        edad = int(fecha_nacimiento_txt[(fecha_nacimiento_txt.index('(')+1):(fecha_nacimiento_txt.index(' años)'))])

                        nacionalid_div = soup_player.find('div', class_='datos_secundarios nacionalidad roboto_condensed')
                        nacionalid_span = nacionalid_div.find('span', class_='roboto_condensed_bold')
                        nacionalid = nacionalid_span.text

                        licencia_div = soup_player.find('div', class_='datos_secundarios licencia roboto_condensed')
                        licencia_span = licencia_div.find('span', class_='roboto_condensed_bold')
                        licencia = licencia_span.text

                        div_datos = soup_player.find('div', class_='datos')
                        image_2 = div_datos.find('div', class_='foto').find("img")["src"]

                        id_person = "ACB_" + id_player_url

                        pass
                        if SQL_NUBE:
                            [conexion, cursor] = conectar_BDD()
                            sql = """
                                    UPDATE p_players
                                    SET position = %(position)s, position_2 = %(position_2)s, lugar_nacimiento = %(lugar_nacimiento)s, country = %(country)s, nacionality = %(nacionality)s, license = %(license)s, birthdate = %(birthdate)s, age = %(age)s, heigth = %(heigth)s, image_2 = %(image_2)s
                                    WHERE id_person = %(id_person)s
                                """
                            datos = {
                                "position": posicion,
                                "position_2": posicion_2,
                                "lugar_nacimiento": lugar_nacimiento,
                                "country": country,
                                "nacionality": nacionalid,
                                "license": licencia,
                                "birthdate": fecha_nacimiento_date,
                                "age": edad,
                                "heigth": altura,
                                "image_2": image_2,
                                "id_person": id_person
                            }
                            cursor.execute(sql, datos)
                            conexion.commit()
                            conexion.close()
                    except:
                        pass
        else:
            print(f"Error al acceder a la página: {response.status_code}")
    print("FIN Scrapeando players info.")