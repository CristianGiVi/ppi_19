#import streamlit as st

#st.set_page_config(
#    page_title="Multipage App",
#    page_icon="👋",
#)

#st.title("MovieMatch")
#st.sidebar.success("Seleccione la pagina que desea visitar.")

#if "my_input" not in st.session_state:
#    st.session_state["my_input"] = ""

#my_input = st.text_input("Buscar peliculas", st.session_state["my_input"])

#submit = st.button("Buscar")

#if submit:
#    st.session_state["my_input"] = my_input
#    st.write("You have entered: ", my_input)

import requests
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from PIL import Image

#Se obtienen las rutas de las bases de datos
ruta1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR2NeukjCnMSMPRo4xRjf8Rl\
KZt6z-EjrNEaBcLEd3JPia27Cf_m1KXFZdxN-bbwwhS-PRaE6jlRR4u/pub?gid=2030210596&sing\
le=true&output=csv'

ruta2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQvpkLNNlf1vBNA0JX_ICl28\
zRiFsd6gl3s01msP7WuBmLU2NZ0XMuqNVvP8Z1wQHsanWVRnjLIv2ye/pub?gid=38863328&single=true&output=csv'

df_IMDB = pd.read_csv(ruta1)
df_Netflix = pd.read_csv(ruta2)

#Depuracion base de datos de IMDB, se eliminan las filas que tengan columnas vacias
df_IMDB  = df_IMDB .dropna(subset=['Title'])
df_IMDB  = df_IMDB .dropna(subset=['Director'])
df_IMDB  = df_IMDB .dropna(subset=['Stars'])
df_IMDB  = df_IMDB .dropna(subset=['IMDb-Rating'])
df_IMDB  = df_IMDB .dropna(subset=['Category'])
df_IMDB  = df_IMDB .dropna(subset=['Duration'])
df_IMDB  = df_IMDB .dropna(subset=['Censor-board-rating'])
df_IMDB  = df_IMDB .dropna(subset=['ReleaseYear'])



#titulo - decoracion
st.markdown("# Page 1 🎉")
st.sidebar.markdown("# Page 1 🎉")
st.write("---") 
st.title("Que filtro deseas aplicar?")


#Variable que se va a usar para almacenar los titulos de las peliculas que fueron filtradas
datos_filtrados = None


#Seccion de filtrado

#lista desplegable de los diferentes filtros que se pueden aplicar
option = st.selectbox(
    'Que filtro deseas aplicar?',
    ('Busqueda fija', 'Rating', 'Categoria', 'Año'))


#Diferentes opciones de filtros:

#Filtro de busqueda por nombre en la columna de titulo
if(option == 'Busqueda fija'):
  pelicula = st.text_input('Escriba el nombre de la pelicula')

  #Filtrado de la base de datos, el filtro se realiza con la funcion "str.contains" que busca en
  #la columna de la base de datos "Tittle" si contiene el string que se almacena en la variable "pelicula"
  datos_filtrados = df_IMDB[df_IMDB['Title'].str.contains(pelicula)]

  #se muestra la tabla en la pagina, la misma se muestra en orden descendente dependiendo de los datos
  #en la columna 'IMDb-Rating'
  st.table(datos_filtrados.sort_values(by='IMDb-Rating', ascending=False))




#Filtro por rating
elif(option == 'Rating'):

  #Esta variable almacena todos los datos que tiene la columna 'IMDb-Rating' y con la funcion
  #.drop_duplicates() se eliminan los datos repetidos.
  elementos_unicos = df_IMDB['IMDb-Rating'].drop_duplicates()

  #la variable se ordena de forma descendente
  elementos_unicos = sorted(elementos_unicos, reverse=True)

  option = st.selectbox('Elija el rating minimo que debe tener la pelicula', elementos_unicos) 
  datos_filtrados = df_IMDB.loc[(df_IMDB['IMDb-Rating'] >= option)]
  st.table(datos_filtrados)



elif(option == 'Año'):
  #practicamente lo mismo que sucede con la variable "elementos_unicos" de arriba
  elementos_unicos = df_IMDB['ReleaseYear'].drop_duplicates()
  elementos_unicos = sorted(elementos_unicos, reverse=True)
  option = st.selectbox('Elija el año en el que se estreno la pelicula', elementos_unicos) 
  datos_filtrados = df_IMDB.loc[(df_IMDB['ReleaseYear'] == option)]
  st.table(datos_filtrados) 



elif(option == 'Categoria'):

  #Se convierten todos los datos de la columna 'Category' a tipo string
  df_IMDB['Category'] = df_IMDB['Category'].astype(str)

  #se concatenan todos los datos de la columna 'Category' y se separan en una lista usando como separador
  #el caracter ";"

  todas_categorias = ';'.join(df_IMDB['Category'])
  todas_categorias = todas_categorias.split(';')

  #Se convierte la lista en una serie
  todas_categorias = pd.Series(todas_categorias)

  #Con la lista convertida en serie, se usa la funcion "drop_duplicates()" para poder tener la lista 
  #con todas las categorias de peliculas que hay sin repeticiones
  elementos_unicos = todas_categorias.drop_duplicates()

  options = st.multiselect('Elija el rating minimo que debe tener la pelicula', elementos_unicos) 


  if(len(options) > 0):
    #datos_filtrados = df_IMDB.copy()
    for categoria in options:
      datos_filtrados = df_IMDB[df_IMDB['Category'].str.contains(categoria)]
      #datos_filtrados = datos_filtrados[df_IMDB['Category'].str.contains(categoria)]
      st.table(datos_filtrados)

 

#Se guardan los nombres de las peliculas en la variable "nombres_p" y se muestran en la pantalla
if(datos_filtrados is not None):
  nombres_p = datos_filtrados['Title']
  st.write(nombres_p)

