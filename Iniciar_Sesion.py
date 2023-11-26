import streamlit as st
import pandas as pd


# Agregamos un título HTML a la aplicación
st.markdown("<h1>Iniciar Sesión</h1>", unsafe_allow_html=True)

# Intentamos cargar un archivo CSV existente o creamos un DataFrame vacío

nueva_cuenta = pd.DataFrame({})

try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError,pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(columns=["Correo", "Contraseña"])

try:
    df_cuenta_actual = pd.read_csv("cuenta_actual.csv")
except (FileNotFoundError,pd.errors.EmptyDataError):
    df_cuenta_actual = pd.DataFrame(columns=["Correo", "Contraseña","Primer Nombre","Peliculas Favoritas"])

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
        
    if correo == "" or contra == "":
        st.write(
            "<span style='color:red; font-weight:bold;'>Por favor complete todos los campos.</span>",
            unsafe_allow_html=True,
        )
    elif (
        correo not in df_cuentas["Correo"].values
        or contra
        != df_cuentas.loc[df_cuentas["Correo"] == correo, "Contraseña"].values[0]
    ):
        st.write(
            "<span style='color:red; font-weight:bold;'>Credenciales incorrectas. Revise su correo y contraseña.</span>",
            unsafe_allow_html=True,
        )
    else:
        # Si las credenciales son correctas, mostramos un mensaje de éxito
        st.write("Inicio de sesión exitoso")
        sesion_iniciada = True
        # Obtenemos el nombre de usuario correspondiente al correo electrónico
        nombre_usuario = df_cuentas.loc[
            df_cuentas["Correo"] == correo, "Primer Nombre"
        ].values[0]
        
        favoritas = df_cuentas.loc[df_cuentas["Correo"] == correo, "Peliculas Favoritas"].values[0]
        nueva_cuenta = pd.DataFrame(
            {
                "Correo": [correo],
                "Contraseña": [contra],
                "Primer Nombre": [nombre_usuario],
                "Peliculas Favoritas": [favoritas]
            }
        )
        if len(df_cuenta_actual) < 1:
            df_cuenta_actual = pd.concat([df_cuenta_actual, nueva_cuenta], ignore_index=True)
            df_cuenta_actual.to_csv("cuenta_actual.csv", index=False)
        # Guardamos el DataFrame actualizado en un archivo

# Agregar un enlace para registrarse
st.markdown(
    "¿No tiene una cuenta? [Regístrese aquí](https://moviematch1.streamlit.app/Crear_cuenta)"
)

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