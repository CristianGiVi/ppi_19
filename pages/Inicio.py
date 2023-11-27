# Importar librerías de Python estándar
import datetime
import requests

# Importar librerías de terceros
import pandas as pd
import streamlit as st
import ast
from st_clickable_images import clickable_images
from streamlit_local_storage import LocalStorage

localS = LocalStorage()

try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(
        columns=["Correo", "Primer Nombre", "Primer Apellido", "Contraseña", "Peliculas Favoritas"]
    )


def getCredentials():
    """ Función para obtener las credenciales del almacenamiento local.
    
    Retorna un diccionario con las credenciales del usuario si no hay problemas, en el caso contrario 
    retorna None
    """

    try:
        localS = LocalStorage()
        info_user = localS.getItem("data")['storage']['value']
        print(info_user) 
        credenciales = ast.literal_eval(info_user)
        return credenciales
    except Exception as e:
        print("error", e)
        return None

cuenta_actual = getCredentials()


def solicitudApi(titulo):
        """Retorna la url del poster de la pelicula, su descripcion, la fecha de lanzamiento y el id en imdb.

        Esta funcion es la que solicita a la api la informacion necesaria de cada pelicula, con unicamente el parametro de su titulo.
        """

        url = f"https://api.themoviedb.org/3/search/movie?query={titulo}&include_adult=false&language=en-US&page=1"

        headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0Nzk3Mjg3MDFkYzExNTRkYWUxOTI4NGU5ZDU3MzhiMyIsInN1YiI6IjY0ZjY4NmIyYWM0MTYxMDBjNDk3YmVkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dKaSrYw9ra42qlml0rZvtZGL9mQ0OO_IjDLXUOrgjBE"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

        primeros_poster_paths = [result["poster_path"] for result in data["results"][:1]]
        descripcion=[result["overview"] for result in data["results"][:1]]
        fecha=[result["release_date"] for result in data ["results"][:1]]
        nombre=[result["original_title"] for result in data["results"][:1]]
        id=[result["id"] for result in data["results"][:1]]

        url_pagina="https://image.tmdb.org/t/p/w500"

        for i in range(len(primeros_poster_paths)):
            primeros_poster_paths[i] = url_pagina+primeros_poster_paths[i]

        return primeros_poster_paths[0],descripcion[0],fecha[0],nombre[0],id[0]

# Se obtienen las rutas de la bases de datos
ruta1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ678ypLCGK-G_2s-9ITKV_RvGhHfDK_0GZLEHHXITjZgHATPSipifh8EsKree2G6FwESWzR-n6NJOK/pub?gid=391645021&single=true&output=csv'

ruta2= 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPPzH9PXbY0LrUs7vtz_Z08ZPNfI9yk9iyP3HFLkoNj2vtEWZ1LPD7nDS5dxq3L2hvSdd9jL4eKq1U/pub?gid=724427749&single=true&output=csv'

df_IMDB2 = pd.read_csv(ruta2)
df_IMDB = pd.read_csv(ruta1)

def obtener_url_poster(titulo):
    """Retonrna la url del poster que esta en el dataframe.

    Esta funcion toma como parametro el titulo de la pelicula, lo busca en el dataframe y devuelve la url del poster.
    """
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['url_poster'].values[0]
    else:
        return None

def obtener_descripcion(titulo):
    """Retorna la descripcion que esta en el dataframe.

    Esta funcion toma como parametro el titulo de la pelicula, lo busca en el dataframe y devuelve la sinopsis.
    """
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['descripcion'].values[0]
    else:
        return None
    
def obtener_fecha(titulo):
    """Retorna la fecha de lanzamiento que esta en el dataframe.

    Esta funcion toma como parametro el titulo de la pelicula, lo busca en el dataframe y devuelve la fecha de lanzamiento de la misma.
    """
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['fecha'].values[0]
    else:
        return None

def consulta2(id):
    """Retorna el tiempo de duracion de la pelicula, una imagen de fondo y el presupuesto de la misma.

    Esta funcion toma como parametro el id previamente encontrado con el titulo en la pasada solicitud,
    con el realizamos nuevamente otra consulta a la api para obtener algunos detalles nuevos.
    """
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0Nzk3Mjg3MDFkYzExNTRkYWUxOTI4NGU5ZDU3MzhiMyIsInN1YiI6IjY0ZjY4NmIyYWM0MTYxMDBjNDk3YmVkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dKaSrYw9ra42qlml0rZvtZGL9mQ0OO_IjDLXUOrgjBE"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
            data = response.json()
    
    runtime = data["runtime"]
    backdrop_path = data["backdrop_path"]
    budget = data["budget"]

    backdrop_path="https://image.tmdb.org/t/p/w500"+backdrop_path

    return runtime,backdrop_path,budget


# ----------------------------------------------------------------------------------

# Depuracion base de datos de IMDB, se eliminan las filas que tengan columnas vacias
df_IMDB  = df_IMDB .dropna(subset=['Title'])
df_IMDB  = df_IMDB .dropna(subset=['Stars'])
df_IMDB  = df_IMDB .dropna(subset=['IMDb-Rating'])
df_IMDB  = df_IMDB .dropna(subset=['Category'])
df_IMDB  = df_IMDB .dropna(subset=['Duration'])
df_IMDB  = df_IMDB .dropna(subset=['Censor-board-rating'])
df_IMDB  = df_IMDB .dropna(subset=['ReleaseYear'])

# Se elimina el sufijo "min" y se convierten los datos de las columnas a enteros
df_IMDB['Duration'] = df_IMDB['Duration'].str.replace('min', '').astype(int)

# Se convierten todos los datos de la columna 'Category' a tipo string
df_IMDB['Category'] = df_IMDB['Category'].astype(str)

# ----------------------------------------------------------------------------------

# Se declara el titulo de la App en la pagina de inicio
st.markdown("# 🎉 Bienvenido a MovieMatch 🎉")
st.sidebar.markdown("# 🎉 MovieMatch 🎉")
st.write("---") 

# Se declaran las indicaciones a seguir para el buen funcionamiento de la APP
st.sidebar.header('Por favor, responde a nuestras preguntas para que podamos recomendarte \
las películas adecuadas siguiendo estas pautas:')

st.sidebar.write('- Si te gusta o deseas verlo, marca "Sí".')
st.sidebar.write('- Si no quieres verlo o no te gusta, marca "No".')
st.sidebar.write('- Si eres indiferente o no tienes preferencias, simplemente no marques nada.')
st.sidebar.write('¡Comencemos!')

# ----------------------------------------------------------------------------------

# filtro por categorias

# se concatenan todos los datos de la columna 'Category' y se separan en una lista 
# usando como separador el caracter ";"
todas_categorias = ';'.join(df_IMDB['Category'])
todas_categorias = todas_categorias.split(';')
# Se convierte la lista en una serie
todas_categorias = pd.Series(todas_categorias)
# Con la lista convertida en serie, se usa la funcion "drop_duplicates()" para poder tener la lista 
# Con todas las categorias de peliculas que hay sin repeticiones
categorias_unicas = todas_categorias.drop_duplicates()

# Se definen los selectbox que estan en el sidebar que contienen los grupos de categorias

# Se declara el selectbox de las categorias (Action, Adventure)

categorias_Action_Adventure = st.sidebar.selectbox('¿Te emocionan las películas llenas de emoción y situaciones intensas?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Comedia, Family)

categorias_Comedy_Family = st.sidebar.selectbox('¿Prefieres las películas que te hacen reír y pasar un buen rato?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Mystery, Crime, Thriller, Horror)

categorias_Crime_Horror_Thriller_Mystery = st.sidebar.selectbox('¿Te emocionan las películas que te hacen saltar de tu asiento?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Sci-Fi, Fantasy) 

categorias_SciFi_Fantasy = st.sidebar.selectbox('¿Te interesan las películas que exploran futuros y mundos alternos?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Romance, drama)

categorias_Drama_Romance = st.sidebar.selectbox('¿Te interesan las historias emocionales y conmovedoras?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Animation)

categorias_Animation = st.sidebar.selectbox('¿Te diviertes con películas animadas y llenas de color?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (War, History, Biography, Film-Noir)

categorias_Biography_War_History_FilmNoir = st.sidebar.selectbox('¿Eres fanático de las películas que exploran eventos históricos o de guerra?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Music, Musical)

categorias_Music_Musical = st.sidebar.selectbox('¿Te gustan las peliculas musicales?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias (Western)

categorias_Western = st.sidebar.selectbox('¿Eres fanatico de las peliculas del viejo oeste?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# Se declara el selectbox de las categorias(Sport)

categorias_Sport = st.sidebar.selectbox('¿Te emocionan las películas relacionadas con competencias deportivas y la pasión por el deporte?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") 

# ----------------------------------------------------------------------------------

# Se declaran los filtros extras que tiene la aplicacion

# Se declara el checkbox que indicara si el usuario desea aplicar filtros extras o no
otros_filtros = st.sidebar.checkbox('Seleccionar filtros')
if otros_filtros:

    # Se aplica el filtro por nombre en donde se le pregunta al usuario por el nombre de la pelicula
    filtro_nombre = st.sidebar.text_input('¿Cual es el nombre de la pelicula que deseas ver?', \
    placeholder="Escriba el nombre de la pelicula")


    # Se obtiene una lista de todos los rating que hay se ordenan de forma descendente
    rating_unicos = df_IMDB['IMDb-Rating'].drop_duplicates()
    rating_unicos = sorted(rating_unicos)

    # Se le pregunta al usuario por el intervalo del rating que desea que tengan las peliculas
    filtro_rating =  st.sidebar.slider('¿Indica el intervalo del rating para las películas que eliges ver?', \
    min_value=rating_unicos[0], max_value=rating_unicos[-1], \
    value=(rating_unicos[0], rating_unicos[-1]))

    # Se le pregunta al usuario por lo antiguedad de las peliculas que desea ver separandolas en tres categorias diferentes
    año_seleccionado = st.sidebar.selectbox('¿Prefieres ver películas que sean: \n \
    Recientes (lanzadas en los últimos 5 años) \n \
    Moderadamente antiguas (lanzadas hace 5-20 años) \n \
    Clásicas (lanzadas hace más de 20 años)', ('Recientes', 'Moderadamente antiguas', \
    'Clásicas'), index=None, placeholder="Seleccione una opcion") 

    # Se le pregunta al usuario por la duracion de la pelicula que desea ver separandola en tres categorias
    duracion_seleccionada = st.sidebar.selectbox('¿Cuál es tu preferencia en cuanto a la \
    duración de las películas que te gusta ver? Elige una de las siguientes opciones:', \
    ('Larga', 'Media', 'Corta'), index=None, placeholder="Seleccione una opcion")

# ----------------------------------------------------------------------------------
# -------------------APLICAR FILTROS CATEGORIAS-----------------------------------
# ----------------------------------------------------------------------------------

# Variable que almacena todas las peliculas
dataframe_conc = df_IMDB.copy() 

# Se aplican los filtros dependiendo de las primeras preguntas que el usuario respondio

# Si el usuario selecciono 'Si' en el selecbox de action y aventura, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan 'Action' o 'Adventure'
if(categorias_Action_Adventure == 'Si'):
    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Action') | dataframe_conc['Category'].str.contains('Adventure'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Comedy, Family
if(categorias_Comedy_Family == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Comedy, Family, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan 'Comedy' o 'Family'
    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Family') | dataframe_conc['Category'].str.contains('Comedy'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Crime-Horror-Thriller-Mystery
if(categorias_Crime_Horror_Thriller_Mystery == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Crime-Horror-Thriller-Mystery, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Crime-Horror-Thriller-Mystery

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Crime') | dataframe_conc['Category'].str.contains('Horror') | 
                                            dataframe_conc['Category'].str.contains('Thriller') | dataframe_conc['Category'].str.contains('Mystery')
                                            )
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Scifi-Fantasy
if(categorias_SciFi_Fantasy == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Scifi-Fantasy, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Scifi-Fantasy

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Sci-Fi') | dataframe_conc['Category'].str.contains('Fantasy'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categorias: Drama-Romance
if(categorias_Drama_Romance == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Drama-Romance, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Drama-Romance

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Drama') | dataframe_conc['Category'].str.contains('Romance'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Animation
if(categorias_Animation == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Animation, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Animation

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Animation'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categorias: Biography_War_History_Film-Noir
if(categorias_Biography_War_History_FilmNoir == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Biography_War_History_Film-Noir, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Biography_War_History_Film-Noir

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Biography') | dataframe_conc['Category'].str.contains('War') | \
                                    dataframe_conc['Category'].str.contains('History') | dataframe_conc['Category'].str.contains('Film-Noir')
                                    )
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Music-Musical
if(categorias_Music_Musical == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Music-Musical, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Music-Musical
    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Music') | dataframe_conc['Category'].str.contains('Musical'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Western
if(categorias_Western == 'Si'):

    # Si el usuario selecciono 'Si' en el selecbox de Western, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Western

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Western'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()

# Filtro por categoria: Sport
if(categorias_Sport == 'Si'):
    # Si el usuario selecciono 'Si' en el selecbox de Sport, se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' tengan las categorias Sport

    condicion_categorias_de_peliculas = (dataframe_conc['Category'].str.contains('Sport'))
    dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
    dataframe_conc = dataframe_conc.dropna()
# ---------------------------------------------------------------------------------------------

# Filtros a aplicar por si se decidio excluir algun grupo de categorias
    
# ---------------------------------------------------------------------------------------------

if(dataframe_conc is not None):

    # Si el usuario selecciono 'No' en el selecbox de 'Action' o 'Adventure', se filtrara la variable dataframe_conc para que solo
    # contenga peliculas que en la columna 'Category' no tengan las categorias 'Action' o 'Adventure'
    if(categorias_Action_Adventure == 'No'):            
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Action') & ~dataframe_conc['Category'].str.contains('Adventure'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()
        
    # Filtros por categoria: Comedy, Family
    if(categorias_Comedy_Family == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Comedy, Family, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Comedy, Family
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Family') & ~dataframe_conc['Category'].str.contains('Comedy'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para las categorias: Crime, Horror, Thriller, Mystery
    if(categorias_Crime_Horror_Thriller_Mystery == 'No'):  

        # Si el usuario selecciono 'No' en el selecbox de Crime-Horror-Thriller-Mystery, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Crime-Horror-Thriller-Mystery
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Mystery') & ~dataframe_conc['Category'].str.contains('Thriller') &
                                                ~dataframe_conc['Category'].str.contains('Horror') & ~dataframe_conc['Category'].str.contains('Crime'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para las categorias: Scifi, Fantasy
    if(categorias_SciFi_Fantasy == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Scifi, Fantasy, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Scifi, Fantasy
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Fantasy') & ~dataframe_conc['Category'].str.contains('Sci-Fi'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para las categorias: Drama-Romance
    if(categorias_Drama_Romance == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Drama-Romance, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Drama-Romance
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Romance') & ~dataframe_conc['Category'].str.contains('Drama'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para la categoria: Animation
    if(categorias_Animation == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Animation, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Animation
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Animation'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para las categorias de: Biography_War_History_Film-Noir
    if(categorias_Biography_War_History_FilmNoir == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de biography_War_History_Film-Noir, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias biography_War_History_Film-Noir

        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Film-Noir') & ~dataframe_conc['Category'].str.contains('History') &
                                                ~dataframe_conc['Category'].str.contains('War') & ~dataframe_conc['Category'].str.contains('Biography'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtros para las categorias de: Music-Musical
    if(categorias_Music_Musical == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Music-Musical, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Music-Musical

        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Musical') & ~dataframe_conc['Category'].str.contains('Music'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtro para la categoria de: Western
    if(categorias_Western == 'No'):

        # Si el usuario selecciono 'No' en el selecbox de Western, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Western
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Western'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

    # Filtro para la categoria de: Sport
    if(categorias_Sport == 'No'): 

        # Si el usuario selecciono 'No' en el selecbox de Sport, se filtrara la variable dataframe_conc para que solo
        # contenga peliculas que en la columna 'Category' no tengan las categorias Sport
        condicion_categorias_de_peliculas = (~dataframe_conc['Category'].str.contains('Sport'))
        dataframe_conc = dataframe_conc.where(condicion_categorias_de_peliculas)
        dataframe_conc = dataframe_conc.dropna()

# ----------------------------------------------------------------------------------

# Si al final no se aplico ninguna clase de filtro, entonces la variable 
# datos_filtrados tendra el valor del datagrame original, en el caso que se aplicara
# al menos un filtro, la variable obtendra los valores de la variable dataframe_conc

if(dataframe_conc is None):
    datos_filtrados = df_IMDB.copy()
else:
    datos_filtrados = dataframe_conc

# ----------------------------------------------------------------------------------
# -------------------------APLICAR FILTROS EXTRAS-----------------------------------
# ----------------------------------------------------------------------------------

#Si se decidio aplicar filtros extras, se realizaran las siguientes acciones:

if(otros_filtros):

    # Se filtraran las peliculas que contengan los valores ingresados en el textInput de buscar por nombre
    if(filtro_nombre):
        datos_filtrados = datos_filtrados[datos_filtrados['Title'].str.contains(filtro_nombre)]

    # Se filtraran las peliculas dependiendo del intervalo del rating que se selecciono
    if(filtro_rating):
        datos_filtrados = datos_filtrados[(datos_filtrados['IMDb-Rating'] >= filtro_rating[0]) & (datos_filtrados['IMDb-Rating'] <= filtro_rating[1])]

    # Se filtraran las peliculas dependiendo de su antiguedad
    if(año_seleccionado):
        año_actual = datetime.date.today().year
        if(año_seleccionado == 'Recientes'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] >= (año_actual - 5))]
        elif(año_seleccionado == 'Moderadamente antiguas'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] < (año_actual - 5) and datos_filtrados['ReleaseYear'] > (año_actual - 20))]
        elif(año_seleccionado == 'Clásicas'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] <= (año_actual - 20))]

    # Se filtran las peliculas dependiendo de su duracion
    if duracion_seleccionada:
        if duracion_seleccionada == 'Larga':
            datos_filtrados = datos_filtrados.loc[datos_filtrados['Duration'] >= 150]
        elif duracion_seleccionada == 'Media':
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['Duration'] < 150) & (datos_filtrados['Duration'] > 90)]
        elif duracion_seleccionada == 'Corta':
            datos_filtrados = datos_filtrados.loc[datos_filtrados['Duration'] <= 90]

# ----------------------------------------------------------------------------------
# ------------------------------MOSTRAR RESULTADOS----------------------------------
# ----------------------------------------------------------------------------------

# Se extraen los nombres de las peliculas filtradas 
nombres_peliculas = datos_filtrados.sort_values(by='IMDb-Rating', ascending=False)['Title']
mostrar_tabla = st.sidebar.checkbox("Mostrar Peliculas recomendadas")


# Se extraen las peliculas favoritas del usuario las cuales estan almacenadas como un string y se convierten a una lista
try:
    lista_favoritas = cuenta_actual["Peliculas Favoritas"][0].split(', ')
    for i in lista_favoritas:
        nombres_peliculas = nombres_peliculas[~nombres_peliculas.isin(lista_favoritas)]
except(TypeError,NameError):
    st.write(
                "<span style='color:red; font-weight:bold;'>Por favor inicie sesion</span>",
                unsafe_allow_html=True,
            )
    
st.write(cuenta_actual)


# Se elimina de la lista de los nombres de las peliculas filtradas, las peliculas que estan dentro de la lista de peliculas favoritas


# Si el checkbox está desmarcado, mostrar el mosaico de películas
if not mostrar_tabla:
    st.title("Peliculas del momento:")
    # Mostrar la primera columna y las 20 primeras filas
    subset_df = df_IMDB2.iloc[:20, :1]

    # Convertir los datos a una lista
    lista_datos = subset_df.values.tolist()

    # Lista con solo los strings
    nueva_lista = [elemento[0] for elemento in lista_datos]

    # Contador para llevar un registro de cuántas peliculas se han mostrado
    count = 0

    query_params = st.experimental_get_query_params().keys()
    if 'page' not in query_params:
        st.experimental_set_query_params(
    
            page = 'main'
        )

    if st.experimental_get_query_params()['page'][0] == 'main':
        image_urls = []
        movie_ids = []
        for i in range(20):
                count += 1
                urldf=obtener_url_poster(nueva_lista[i])
                image_urls.append(urldf)
                movie_ids.append(nueva_lista[i])
                # Incrementa el contador
                count += 1

        # Muestra las imágenes como imágenes clicables
        

        clicked = clickable_images(image_urls,
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "330px", "flex": "0 0 30%"}, key='movies' # Modificado
)


        # Si se hace clic en una imagen, redirige a la página de detalles de la pelicula
        if clicked > -1:
            st.experimental_set_query_params(page='details', movie_id=movie_ids[clicked])

    elif st.experimental_get_query_params()['page'][0] == 'details':
        movie_id = st.experimental_get_query_params()['movie_id'][0]
        

        url,descripcion,fecha,nombre,id=solicitudApi(movie_id)

        # Se realiza una nueva consulta con el id
        runtime,backdrop_path,budget=consulta2(id)

        # Muestra el nombre de la pelicula como título de la página
        st.title(movie_id)

        # Crea dos columnas para mostrar la imagen y la información de la pelicula
        col1, col2 = st.columns(2)

        # Muestra la imagen de la pelicula en la columna de la izquierda
            
        col1.image(url, use_column_width=True)

        # Muestra la información de la pelicula en la columna de la derecha
        col2.markdown(f"**Sinopsis:** {descripcion}")
        col2.markdown(f"**Fecha de lanzamiento** {fecha}")
        col2.markdown(f"**Duracion:** {runtime} min")
        col2.markdown(f"**Presupuesto:** ${budget}")
        
        # Muestra un botón "Volver" que llama a la función 'volver' cuando se hace clic
        if st.button('Volver', key='volver'):
            st.experimental_set_query_params(page='main')

        if st.button('Agregar a favoritos'):
            # Variable que al amacena el nombre de la pelicula seleccionada
            nueva_pelicula = movie_id 

            # validar si la pelicula esta en la lista de favoritos
            if nueva_pelicula in lista_favoritas:
                st.write("La pelicula ya se encuentra entre tus peliculas favoritas")
            else:
                lista_favoritas = cuenta_actual["Peliculas Favoritas"][0].split(', ')
                # Se agrega la pelicula seleccionada junto con el resto de las peliculas favoritas del usuario
                cuenta_actual["Peliculas Favoritas"][0] += ', ' + nueva_pelicula
                
                st.write("La pelicula se ha agregado con exito a tus peliculas favoritas")

                # El primer elemento de la lista es una lista vacia, por ende se borra del listado de peliculas favoritas de la cuenta actual
                if(cuenta_actual["Peliculas Favoritas"][0][:4] == '[], '):
                    #  cuenta_actual["Peliculas Favoritas"][0] = cuenta_actual["Peliculas Favoritas"][0].str[4:]
                    cuenta_actual["Peliculas Favoritas"][0] = cuenta_actual["Peliculas Favoritas"][0][4:]
                
            # Se extrae el listado de las peliculas favoritas del usuario
            st.subheader("Tus peliculas favoritas actuales son: ")
            for pelicula in cuenta_actual["Peliculas Favoritas"][0].split(', '):
                st.write(pelicula)

            localS.setItem("data", str(cuenta_actual))

            actualizar_cuenta = pd.DataFrame(cuenta_actual)

            df_cuentas = df_cuentas[df_cuentas['Correo'] != cuenta_actual["Correo"][0]]
            df_cuentas = pd.concat([df_cuentas, actualizar_cuenta], ignore_index=True)

            # Guardamos el DataFrame actualizado en un archivo CSV
            df_cuentas.to_csv("cuentas.csv", index=False)


if(mostrar_tabla):
    st.title("Peliculas recomendadas:")
    
    nombres_lista = nombres_peliculas.tolist()

    # Contador para llevar un registro de cuántas peliculas se han mostrado
    count = 0

    query_params = st.experimental_get_query_params().keys()
    if 'page' not in query_params:
        st.experimental_set_query_params(
    
            page = 'main'
        )

    if st.experimental_get_query_params()['page'][0] == 'main':
        image_urls = []
        movie_ids = []
        for i in range(len(nombres_lista)):
                count += 1
                urldf=obtener_url_poster(nombres_lista[i])
                image_urls.append(urldf)
                movie_ids.append(nombres_lista[i])
                # Incrementa el contador
                count += 1

        # Muestra las imágenes como imágenes clicables
        

        clicked = clickable_images(image_urls,
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "330px", "flex": "0 0 30%"}, key='movies' # Modificado
)


        # Si se hace clic en una imagen, redirige a la página de detalles de la pelicula
        if clicked > -1:
            st.experimental_set_query_params(page='details', movie_id=movie_ids[clicked])

    elif st.experimental_get_query_params()['page'][0] == 'details':
        movie_id = st.experimental_get_query_params()['movie_id'][0]
        
        # Consulta de la api
        url,descripcion,fecha,nombre,id=solicitudApi(movie_id)

        runtime,backdrop_path,budget=consulta2(id)

        st.title(movie_id)

            # Crea dos columnas para mostrar la imagen y la información de la pelicula
        col1, col2 = st.columns(2)

            # Muestra la imagen de la pelicula en la columna de la izquierda
            
        col1.image(url, use_column_width=True)


        # Muestra la información de la pelicula en la columna de la derecha
        col2.markdown(f"**Sinopsis:** {descripcion}")
        col2.markdown(f"**Fecha de lanzamiento** {fecha}")
        col2.markdown(f"**Duracion:** {runtime} min")
        col2.markdown(f"**Presupuesto:** ${budget}")
        
        # Muestra un botón "Volver" que llama a la función 'volver' cuando se hace clic
        if st.button('Volver', key='volver'):
            st.experimental_set_query_params(page='main')