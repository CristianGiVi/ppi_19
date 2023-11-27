#Se importan las librerias usadas
import streamlit as st
import pandas as pd
import streamlit as st
from streamlit_local_storage import LocalStorage

localS = LocalStorage()


def iniciarSesion(correo, contra):
    """La funcion recibe dos parametros los cuales son correo y contraseña.

    La funcion se encarga de verificar que correo exista en el csv cuentas y tambien
    se encarga de verificar que la contraseña ingresada sea la misma que la del correo
    ingreado
    """

    if correo == "" or contra == "":
        st.write(
            "<span style='color:red; font-weight:bold;'>Por favor complete todos los campos.</span>",
            unsafe_allow_html=True,
        )
        return False
    if (correo not in df_cuentas["Correo"].values):
        st.write(
            "<span style='color:red; font-weight:bold;'>Credenciales incorrectas. Revise su correo y contraseña.</span>",
            unsafe_allow_html=True,
        )
        return False
    data_user = df_cuentas.loc[df_cuentas["Correo"] == correo, "Contraseña"].values[0]
    if str(contra) != str(data_user):
        st.write(
            "<span style='color:red; font-weight:bold;'>Credenciales incorrectas. Revise su correo y contraseña.</span>",
            unsafe_allow_html=True,
        )
        return False
    return True

# Agregamos un título HTML a la aplicación
st.markdown("<h1>Iniciar Sesión</h1>", unsafe_allow_html=True)
# Intentamos cargar un archivo CSV existente o creamos un DataFrame vacío
try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError,pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(columns=["Correo", "Contraseña"])

# Creamos un formulario de inicio de sesión
formulario_inicio_sesion = st.form
with formulario_inicio_sesion("Formulario de inicio de sesión"):
    # Agregamos un subtítulo al formulario
    st.subheader("Ingrese sus credenciales")

    # Recopilamos la entrada del usuario, incluyendo correo y contraseña
    correo = st.text_input("Correo electrónico")
    contra = st.text_input("Contraseña", type="password")

    # Agregamos un botón de inicio de sesión
    boton_logearse = st.form_submit_button("Iniciar Sesión")
    

    # Realizamos comprobaciones en la entrada del usuario y mostramos mensajes de error si es necesario
    
sesion_iniciada = False    
if boton_logearse:
    if iniciarSesion(correo, contra):
        # Obtenemos el nombre de usuario correspondiente al correo electrónico
        nombre_usuario = df_cuentas.loc[
            df_cuentas["Correo"] == correo, "Primer Nombre"
        ].values[0]
            
        favoritas = df_cuentas.loc[df_cuentas["Correo"] == correo, "Peliculas Favoritas"].values[0]
        apellido = df_cuentas.loc[
            df_cuentas["Correo"] == correo, "Primer Apellido"
        ].values[0]
        data = {
            "Correo": [correo],
            "Contraseña": [contra],
            "Primer Nombre": [nombre_usuario],
            "Primer Apellido" : [apellido],
            "Peliculas Favoritas": [favoritas]
        }
        localS.setItem("data", str(data))
        # Si las credenciales son correctas, mostramos un mensaje de éxito
        st.write("Inicio de sesión exitoso")



st.write("---")

st.title("Acerca de nosotros")
col1, col2, col3 = st.columns(3)
with col1:
    col1.subheader('Alejandro Esteban Muñoz Osorio')
    col1.image('Imagenes/AlejandroPerfil.png', use_column_width = True)
    st.write("[almunozo](https://github.com/almunozo)")

with col2:
    col2.subheader('Cristian Giraldo Villegas')
    col2.image('Imagenes/CristianPerfil.png', use_column_width = True)
    st.write("[CristianGiVi](https://github.com/CristianGiVi)")

with col3:
    col3.subheader('David Ramirez Lara')
    col3.image('Imagenes/DavidPerfil.png', use_column_width = True)
    st.write("[dramirezla](https://github.com/dramirezla)")


# Agregar un enlace para registrarse
st.markdown(
    "¿No tiene una cuenta? [Regístrese aquí](https://moviematch2.streamlit.app/Crear_cuenta)"
)
