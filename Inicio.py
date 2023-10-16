import streamlit as st
import pandas as pd

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

