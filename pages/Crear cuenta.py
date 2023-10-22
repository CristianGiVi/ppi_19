# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd

# Agregamos un título HTML a la aplicación
st.markdown("<h1>Registro de usuario</h1>", unsafe_allow_html=True)

# Intentamos cargar un archivo CSV existente o creamos un DataFrame vacío
try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(
        columns=["Correo", "Primer Nombre", "Primer Apellido", "Contraseña"]
    )

# Creamos un formulario de registro
formulario_registro = st.form
with formulario_registro("Formulario de registro"):
    # Agregamos un subtítulo al formulario
    st.subheader("Complete todos los campos")

    # Dividimos la interfaz en dos columnas
    col1, col2 = st.columns(2)

    # Recopilamos la entrada del usuario, incluyendo nombre, apellido, correo y contraseñas
    p_nombre = col1.text_input("Primer nombre")
    p_apellido = col2.text_input("Primer apellido")
    correo = st.text_input("Correo electrónico")
    contra = col1.text_input("Contraseña", type="password")
    confcontra = col2.text_input("Confirmar Contraseña", type="password")
    acepta_politicas = st.checkbox(
        "Acepto las políticas de tratamiento de datos personales"
    )

    # Agregamos un botón de envío
    st.form_submit_button("Registrarse")

    # Realizamos comprobaciones en la entrada del usuario y mostramos mensajes de error si es necesario
    if confcontra != contra:
        st.write(
            "<span style='color:red; font-weight:bold;'>Las 2 contraseñas que acaba de ingresar no coinciden.</span>",
            unsafe_allow_html=True,
        )
    elif correo == "" or p_nombre == "" or p_apellido == "" or contra == "":
        st.write(
            "<span style='color:red; font-weight:bold;'>Por favor complete todos los campos.</span>",
            unsafe_allow_html=True,
        )
    elif correo.find("@") == -1:
        st.write(
            "<span style='color:red; font-weight:bold;'>No ingreso una direccion de correo electronico valida</span>",
            unsafe_allow_html=True,
        )
    elif not acepta_politicas:
        st.write(
            "<span style='color:red; font-weight:bold;'>Debes aceptar las politicas de tratamiento de datos personales.</span>",
            unsafe_allow_html=True,
        )
    elif len(contra) < 8:
        st.write(
            "<span style='color:red; font-weight:bold;'>La contraseña debe poseer 8 caracteres o mas.</span>",
            unsafe_allow_html=True,
        )
    elif correo in df_cuentas["Correo"].values:
        st.write(
            "<span style='color:red; font-weight:bold;'>El correo electrónico ya está registrado. Ingrese uno nuevo.</span>",
            unsafe_allow_html=True,
        )
    else:
        # Si todas las comprobaciones pasan, registramos al usuario en el archivo Excel
        nueva_cuenta = pd.DataFrame(
            {
                "Correo": [correo],
                "Primer Nombre": [p_nombre],
                "Primer Apellido": [p_apellido],
                "Contraseña": [contra],
            }
        )
        df_cuentas = pd.concat([df_cuentas, nueva_cuenta], ignore_index=True)

        # Guardamos el DataFrame actualizado en un archivo CSV
        df_cuentas.to_excel("cuentas.csv", index=False)

        # Mostramos el DataFrame actualizado y un mensaje de éxito
        st.write(df_cuentas)
        st.write("Usuario registrado con éxito")
