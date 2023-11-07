# Importar librerías de Python estándar
import datetime
import requests

# Importar librerías de terceros
import pandas as pd
import streamlit as st

# Importar tus propios módulos 
import pages.Iniciar_Sesion as pis

def mostrarMosaico(listaurl,listanombre):
     count = 0
     # Inicializa la fila HTML
     row_html = "<table><tr>"

     # Muestra los juegos en Streamlit
     for j in range(len(listaurl)) :
            count += 1
                

            # Añade el juego a la fila HTML
            row_html += f"<td style='border: none; width: 100px; height: 200px;text-align: center; vertical-align: top;'><img src='{listaurl[j]}'style='width: 100px; object-fit: contain;'/><br/><div style='width:100px; word-wrap: break-word;'>{listanombre[j]}</div></td>"

            # Si se han añadido tres juegos a la fila, muestra la fila y comienza una nueva
            if count % 5 == 0:
                row_html += "</tr></table>"
                st.write(row_html, unsafe_allow_html=True)
                row_html = "<table><tr>"

    # Si quedan juegos en la última fila, muestra la fila
     if count % 5 != 0:
            row_html += "</tr></table>"
            st.write(row_html, unsafe_allow_html=True)

def mostrarTarjeta(titulo,urlposter,descripcion,fecha):
    st.write(f"""
    <div style ='max-width: 650px; background-color: #E5E5E5; border-radius: 5px; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 43vh; margin: 20px 20px'>
        <div style='flex: 1; padding: 20px'>
            <h3 >{titulo}</h2>
            <p style='font-size: smaller;'> Fecha de lanzamiento: {fecha} </p>
            <p style='font-size: smaller;'> {descripcion} </p>
        </div>
        <img src="{urlposter}" alt="Poster de la película" style='max-width: 200px; height: 43vh; display: block'>
    </div>
    """, unsafe_allow_html=True)




# Se obtienen las rutas de la bases de datos
ruta1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ678ypLCGK-G_2s-9ITKV_RvGhHfDK_0GZLEHHXITjZgHATPSipifh8EsKree2G6FwESWzR-n6NJOK/pub?gid=391645021&single=true&output=csv'

ruta2= 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPPzH9PXbY0LrUs7vtz_Z08ZPNfI9yk9iyP3HFLkoNj2vtEWZ1LPD7nDS5dxq3L2hvSdd9jL4eKq1U/pub?gid=724427749&single=true&output=csv'

df_IMDB2 = pd.read_csv(ruta2)
df_IMDB = pd.read_csv(ruta1)

def obtener_url_poster(titulo):
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['url_poster'].values[0]
    else:
        return None

def obtener_descripcion(titulo):
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['descripcion'].values[0]
    else:
        return None
    
def obtener_fecha(titulo):
    fila = df_IMDB2[df_IMDB2['Title'] == titulo]
    if not fila.empty:
        return fila['fecha'].values[0]
    else:
        return None

# ----------------------------------------------------------------------------------

st.write(df_IMDB)

# Depuracion base de datos de IMDB, se eliminan las filas que tengan columnas vacias
df_IMDB  = df_IMDB .dropna(subset=['Title'])
# df_IMDB  = df_IMDB .dropna(subset=['Director'])
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

# Titulo
st.markdown("# 🎉 Bienvenido a MovieMatch 🎉")
st.sidebar.markdown("# 🎉 MovieMatch 🎉")
st.write("---") 

   


# Sidebar 
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

categorias_Action_Adventure = st.sidebar.selectbox('¿Te emocionan las películas llenas de emoción y situaciones intensas?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Action, Adventure)

categorias_Comedy_Family = st.sidebar.selectbox('¿Prefieres las películas que te hacen reír y pasar un buen rato?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Comedia, Family)

categorias_Crime_Horror_Thriller_Mystery = st.sidebar.selectbox('¿Te emocionan las películas que te hacen saltar de tu asiento?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Mystery, Crime, Thriller, Horror)

categorias_SciFi_Fantasy = st.sidebar.selectbox('¿Te interesan las películas que exploran futuros y mundos alternos?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Sci-Fi, Fantasy) 

categorias_Drama_Romance = st.sidebar.selectbox('¿Te interesan las historias emocionales y conmovedoras?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Romance, drama)

categorias_Animation = st.sidebar.selectbox('¿Te diviertes con películas animadas y llenas de color?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Animation)

categorias_Biography_War_History_FilmNoir = st.sidebar.selectbox('¿Eres fanático de las películas que exploran eventos históricos o de guerra?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(War, History, Biography, Film-Noir)

categorias_Music_Musical = st.sidebar.selectbox('¿Te gustan las peliculas musicales?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Music, Musical)

categorias_Western = st.sidebar.selectbox('¿Eres fanatico de las peliculas del viejo oeste?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Western)

categorias_Sport = st.sidebar.selectbox('¿Te emocionan las películas relacionadas con competencias deportivas y la pasión por el deporte?', \
('Si', 'No') , index=None, placeholder="Seleccione una opcion") #(Sport)


# ----------------------------------------------------------------------------------


# Declarar filtros extras

otros_filtros = st.sidebar.checkbox('Seleccionar filtros')
if otros_filtros:

    #filtro por nombre
    filtro_nombre = st.sidebar.text_input('¿Cual es el nombre de la pelicula que deseas ver?', \
    placeholder="Escriba el nombre de la pelicula")

    #filtro por rating

  # Se obtiene una lista de todos los rating que hay se ordenan de forma descendente
    rating_unicos = df_IMDB['IMDb-Rating'].drop_duplicates()
    rating_unicos = sorted(rating_unicos)

    filtro_rating =  st.sidebar.slider('¿Indica el intervalo del rating para las películas que eliges ver?', \
    min_value=rating_unicos[0], max_value=rating_unicos[-1], \
    value=(rating_unicos[0], rating_unicos[-1]))

  #filtro por aÑos
    año_seleccionado = st.sidebar.selectbox('¿Prefieres ver películas que sean: \n \
    Recientes (lanzadas en los últimos 5 años) \n \
    Moderadamente antiguas (lanzadas hace 5-20 años) \n \
    Clásicas (lanzadas hace más de 20 años)', ('Recientes', 'Moderadamente antiguas', \
    'Clásicas'), index=None, placeholder="Seleccione una opcion") 

    #por duracion
    duracion_seleccionada = st.sidebar.selectbox('¿Cuál es tu preferencia en cuanto a la \
    duración de las películas que te gusta ver? Elige una de las siguientes opciones:', \
    ('Larga', 'Media', 'Corta'), index=None, placeholder="Seleccione una opcion")


# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# # -------------------APLICAR FILTROS CATEGORIAS-----------------------------------
# ----------------------------------------------------------------------------------


# Peliculas filtradas por categoria

# Se extrae en variables diferntes las filas de peliculas que contienen su respectiva categoria

Action= df_IMDB[df_IMDB['Category'].str.contains('Action')]
Adventure = df_IMDB[df_IMDB['Category'].str.contains('Adventure')]
Comedy = df_IMDB[df_IMDB['Category'].str.contains('Comedy')]
Mystery = df_IMDB[df_IMDB['Category'].str.contains('Mystery')]
Thriller = df_IMDB[df_IMDB['Category'].str.contains('Thriller')]
Horror = df_IMDB[df_IMDB['Category'].str.contains('Horror')]
Crime = df_IMDB[df_IMDB['Category'].str.contains('Crime')]
SciFi = df_IMDB[df_IMDB['Category'].str.contains('Sci-Fi')]
Fantasy = df_IMDB[df_IMDB['Category'].str.contains('Fantasy')]
Drama = df_IMDB[df_IMDB['Category'].str.contains('Drama')]
Romance = df_IMDB[df_IMDB['Category'].str.contains('Romance')]
Animation = df_IMDB[df_IMDB['Category'].str.contains('Animation')]
Biography = df_IMDB[df_IMDB['Category'].str.contains('Biography')]
War = df_IMDB[df_IMDB['Category'].str.contains('War')]
History = df_IMDB[df_IMDB['Category'].str.contains('Fantasy')]
FilmNoir = df_IMDB[df_IMDB['Category'].str.contains('Film-Noir')]
Music = df_IMDB[df_IMDB['Category'].str.contains('Music')]
Musical = df_IMDB[df_IMDB['Category'].str.contains('Musical')]
Western = df_IMDB[df_IMDB['Category'].str.contains('Western')]
Sport = df_IMDB[df_IMDB['Category'].str.contains('Sport')]
Family = df_IMDB[df_IMDB['Category'].str.contains('Sport')]


# Variable que almacena la concatenacion de las categorias
dataframe_conc = df_IMDB.copy() #pd.DataFrame(columns=['Title', 'Director','Stars', 'IMDb-Rating', 'Category', 'Duration', 'Censor-board-rating', 'ReleaseYear'])


# Categorias

#Action-Adventure
if(categorias_Action_Adventure):
    if(categorias_Action_Adventure == 'Si'):
        dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Action') | dataframe_conc['Category'].str.contains('Adventure')]


#Comedy, Family
if(categorias_Comedy_Family == 'Si'):
        dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Family') | dataframe_conc['Category'].str.contains('Comedy')]



#Crime-Horror-Thriller-Mystery
if(categorias_Crime_Horror_Thriller_Mystery == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Crime') | dataframe_conc['Category'].str.contains('Horror') | \
                                    dataframe_conc['Category'].str.contains('Thriller') | dataframe_conc['Category'].str.contains('Mystery')]


#Scifi-Fantasy
if(categorias_SciFi_Fantasy == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Sci-Fi') | dataframe_conc['Category'].str.contains('Fantasy')]


#Drama-Romance
if(categorias_Drama_Romance == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Drama') | dataframe_conc['Category'].str.contains('Romance')]

#Animation
if(categorias_Animation == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Animation')]

#Biography_War_History_Film-Noir
if(categorias_Biography_War_History_FilmNoir == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Biography') | dataframe_conc['Category'].str.contains('War') | \
                                    dataframe_conc['Category'].str.contains('History') | dataframe_conc['Category'].str.contains('Film-Noir')]

#Music-Musical
if(categorias_Music_Musical == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Music') | dataframe_conc['Category'].str.contains('Musical')]


#Western
if(categorias_Western == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Western')]

#Sport
if(categorias_Sport == 'Si'):
    dataframe_conc = dataframe_conc[dataframe_conc['Category'].str.contains('Sport')]


# ----------------------------------------------------------------------------------



# Filtros a aplicar por si se decidio excluir algun grupo de categorias


if(dataframe_conc is not None):
    if(categorias_Action_Adventure == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Action')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Adventure')]


    #Comedy, Family
    if(categorias_Comedy_Family == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Family')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Comedy')]


    #Crime, Horror, Thriller, Mystery
    if(categorias_Crime_Horror_Thriller_Mystery == 'No'):  
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Mystery')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Thriller')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Horror')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Crime')]


    #Scifi, Fantasy
    if(categorias_SciFi_Fantasy == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Fantasy')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Sci-Fi')]

    #Drama-Romance
    if(categorias_Drama_Romance == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Romance')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Drama')]

    #Animation
    if(categorias_Animation == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Animation')]


    #Biography_War_History_Film-Noir
    if(categorias_Biography_War_History_FilmNoir == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Film-Noir')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('History')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('War')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Biography')]


    #Music-Musical
    if(categorias_Music_Musical == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Musical')]
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Music')]

    #Western
    if(categorias_Western == 'No'):
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Western')]

    #Sport
    if(categorias_Sport == 'No'): 
      dataframe_conc = dataframe_conc[~dataframe_conc['Category'].str.contains('Sport')]



# ----------------------------------------------------------------------------------


# Si al final no se aplico ninguna clase de filtro, entonces la variable 
# datos_filtrados tendra el valor del datagrame original, en el caso que se aplicara
# al menos un filtro, la variable obtendra los valores de la variable dataframe_conc

if(dataframe_conc is None):
    datos_filtrados = df_IMDB.copy()
else:
    datos_filtrados = dataframe_conc

# ----------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------
# -------------------------APLICAR FILTROS EXTRAS-----------------------------------
# ----------------------------------------------------------------------------------



#Si se decidio aplicar filtros extras, se realizaran las siguientes acciones:

if(otros_filtros):
    #filtro nombre
    if(filtro_nombre):
        datos_filtrados = datos_filtrados[datos_filtrados['Title'].str.contains(filtro_nombre)]

    #filtro rating
    if(filtro_rating):
        datos_filtrados = datos_filtrados[(datos_filtrados['IMDb-Rating'] >= filtro_rating[0]) & (datos_filtrados['IMDb-Rating'] <= filtro_rating[1])]


    #filtro años
    if(año_seleccionado):
        año_actual = datetime.date.today().year
        if(año_seleccionado == 'Recientes'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] >= (año_actual - 5))]
        elif(año_seleccionado == 'Moderadamente antiguas'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] < (año_actual - 5) and datos_filtrados['ReleaseYear'] > (año_actual - 20))]
        elif(año_seleccionado == 'Clásicas'):
            datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] <= (año_actual - 20))]

    #Duracion
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


nombres_peliculas = datos_filtrados.sort_values(by='IMDb-Rating', ascending=False)['Title']
mostrar_tabla = st.sidebar.checkbox("Mostrar Peliculas recomendadas")

# Intentamos cargar un archivo CSV existente o creamos un DataFrame vacío
try:
    df_cuenta_actual = pd.read_csv("cuenta_actual.csv")
except (FileNotFoundError,pd.errors.EmptyDataError):
    df_cuenta_actual = pd.DataFrame(columns=["Correo", "Contraseña","Nombre", "Peliculas Favoritas"])


lista_favoritas = df_cuenta_actual["Peliculas Favoritas"].tolist()
lista_favoritas.append("Once Upon a Time in the West")

st.write(lista_favoritas)

# Verifica si las películas favoritas están en la lista
for pelicula in lista_favoritas:
    esta_presente = pelicula in nombres_peliculas.values

# Elimina las películas favoritas de la lista
nombres_peliculas = nombres_peliculas[~nombres_peliculas.isin(lista_favoritas)]


# Agrega, pero hay que tener cuidado con los indices de peliculas que ya no estan, ej. the godfather
#lista_favoritas.append(nombres_peliculas[2])

# Si el checkbox está desmarcado, mostrar el mosaico de películas
if not mostrar_tabla:
    st.title("Peliculas del momento:")
    # Mostrar la primera columna y las 20 primeras filas
    subset_df = df_IMDB2.iloc[:20, :1]

    # Convertir los datos a una lista
    lista_datos = subset_df.values.tolist()

    # Lista con solo los strings
    nueva_lista = [elemento[0] for elemento in lista_datos]

    url_recomendadas=[]
    nombre_inicio=[]


    for i in range(20):
       urldf=obtener_url_poster(nueva_lista[i])
       url_recomendadas.append(urldf)
       nombre_inicio.append(nueva_lista[i])
       

    mostrarMosaico(url_recomendadas, nombre_inicio)


if(mostrar_tabla):
  nombres_lista = nombres_peliculas.tolist()
  url_lista=[]
  reseña_lista=[]
  fecha_lista=[]

  for j in range(len(nombres_lista)):
       urldf=obtener_url_poster(nombres_lista[j])
       url_lista.append(urldf)
       descripciondf=obtener_descripcion(nombres_lista[j])
       reseña_lista.append(descripciondf)
       fechadf=obtener_fecha(nombres_lista[j])
       fecha_lista.append(fechadf)


  for i in range(len(nombres_lista)):
       mostrarTarjeta(
            titulo=nombres_lista[i],
            urlposter=url_lista[i],
            descripcion=reseña_lista[i],
            fecha=fecha_lista[i]
            )
    

   
try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(
        columns=["Correo", "Primer Nombre", "Primer Apellido", "Contraseña", "Peliculas Favoritas"]
    )

# Verificamos si df_cuentas contiene el mismo correo que df_cuenta_actual
if not df_cuenta_actual.empty:
    
    correo = df_cuenta_actual["Correo"].iloc[0] 
    idx = df_cuentas[df_cuentas["Correo"] == correo].index
    if not idx.empty:
        df_cuentas.at[idx[0], "Peliculas Favoritas"] = lista_favoritas
        
        
df_vacio = pd.DataFrame()
df_vacio.to_csv("cuenta_actual.csv", index=False)
df_cuentas.to_csv("cuentas.csv", index=False)

st.write(df_cuentas)