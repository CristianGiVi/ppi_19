from translate import Translator
import requests
import streamlit as st
import pandas as pd

def obtenerPoster(titulo):
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

        url_pagina="https://image.tmdb.org/t/p/w500"

        for i in range(len(primeros_poster_paths)):
               primeros_poster_paths[i] = url_pagina+primeros_poster_paths[i]

        return primeros_poster_paths[0],descripcion[0],fecha[0]

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

def mostrarTarjeta(titulo,ano,descripcion,urlposter):
    print(titulo)
    st.write(f"""
    <div style ='max-width: 650px; background-color: #E5E5E5; border-radius: 5px; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 43vh; margin: 20px 20px'>
        <div style='flex: 1; padding: 20px'>
            <h3 >{titulo}</h2>
            <p style='font-size: smaller;'> Fecha de lanzamiento: {ano}</p>
            <p style='font-size: smaller;'>{descripcion}</p>
        </div>
        <img src="{urlposter}" alt="Poster de la película" style='max-width: 200px; height: 43vh; display: block'>
    </div>
    """, unsafe_allow_html=True)



#Se obtienen las rutas de las bases de datos
ruta1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR2NeukjCnMSMPRo4xRjf8Rl\
KZt6z-EjrNEaBcLEd3JPia27Cf_m1KXFZdxN-bbwwhS-PRaE6jlRR4u/pub?gid=2030210596&sing\
le=true&output=csv'

df_IMDB = pd.read_csv(ruta1)

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
st.markdown("# 🎉 Bienvenido a MovieMatch 🎉")
st.sidebar.markdown("# 🎉 MovieMatch 🎉")
st.write("---") 
st.title("Peliculas recomendadas:")

datos_filtrados = df_IMDB.copy()
mostrar_pelicula = False
mostrar_poster = False

# Sidebar para widgets de filtro
st.sidebar.header('Filtros')

#filtro por nombre
filtro_nombre = st.sidebar.text_input('Escriba el nombre de la pelicula')

#filtro por rating
rating_unicos = datos_filtrados['IMDb-Rating'].drop_duplicates()
rating_unicos = sorted(rating_unicos, reverse=True)
filtro_rating = st.sidebar.selectbox('Elija el rating minimo que debe tener la pelicula', rating_unicos, index=None) 

#filtro por aÑos
años_unicos = datos_filtrados['ReleaseYear'].drop_duplicates()
años_unicos = sorted(años_unicos, reverse=True)
año_seleccionado = st.sidebar.selectbox('Elija el año en el que se estreno la pelicula', años_unicos, index=None) 

#filtro por categoria
#Se convierten todos los datos de la columna 'Category' a tipo string
datos_filtrados['Category'] = datos_filtrados['Category'].astype(str)

#se concatenan todos los datos de la columna 'Category' y se separan en una lista usando como separador
#el caracter ";"

todas_categorias = ';'.join(datos_filtrados['Category'])
todas_categorias = todas_categorias.split(';')

#Se convierte la lista en una serie
todas_categorias = pd.Series(todas_categorias)

#Con la lista convertida en serie, se usa la funcion "drop_duplicates()" para poder tener la lista 
#con todas las categorias de peliculas que hay sin repeticiones
categorias_unicas = todas_categorias.drop_duplicates()
categorias_seleccionadas = st.sidebar.selectbox('Elija la categoria de la pelicula', categorias_unicas, index=None) 


#APLICAR FILTROS


#filtro nombre
if(filtro_nombre):
  datos_filtrados = datos_filtrados[datos_filtrados['Title'].str.contains(filtro_nombre)]
  mostrar_pelicula = True

#filtro rating
if(filtro_rating):
    datos_filtrados = datos_filtrados.loc[(datos_filtrados['IMDb-Rating'] >= filtro_rating)]
    mostrar_pelicula = True

#filtro años
if(año_seleccionado):
    datos_filtrados = datos_filtrados.loc[(datos_filtrados['ReleaseYear'] == año_seleccionado)]
    mostrar_pelicula = True

#categorias
if(categorias_seleccionadas):
    datos_filtrados = datos_filtrados[datos_filtrados['Category'].str.contains(categorias_seleccionadas)]
    mostrar_pelicula = True



#mostrar resultados
if(filtro_nombre or filtro_rating or año_seleccionado or categorias_seleccionadas):
  st.table(datos_filtrados.sort_values(by='IMDb-Rating', ascending=False))


#Se guardan los nombres de las peliculas en la variable "nombres_peliculas" y se muestran en la pantalla
if(mostrar_pelicula):
  nombres_peliculas = datos_filtrados.sort_values(by='IMDb-Rating', ascending=False)['Title']
  st.write("holal mundo")
  st.write(nombres_peliculas)
  #Suponiendo que tienes una Serie llamada nombres_peliculas
  nombres_lista = nombres_peliculas.tolist()
  url_lista=[]
  reseña_lista=[]
  fecha_lista=[]

  for j in range(len(nombres_lista)):
       url,reseña,fechas=obtenerPoster(nombres_lista[j])
       url_lista.append(url)
       reseña_lista.append(reseña)
       fecha_lista.append(fechas)
  
  #mostrarMosaico(url_lista,nombres_lista)
  translator = Translator(to_lang='es')

  for h in range(len(nombres_lista)):
       reseña_lista[h]=translator.translate(reseña_lista[h])

  for i in range(len(nombres_lista)):
       mostrarTarjeta(
            titulo=nombres_lista[i],
            urlposter=url_lista[i],
            descripcion=reseña_lista[i],
            ano=fecha_lista[i]
            )

