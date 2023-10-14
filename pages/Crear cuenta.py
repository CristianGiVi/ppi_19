import streamlit as st
import openpyxl
import pandas as pd
st.markdown("<h1>Registro usuario</h1>",unsafe_allow_html=True)

try:
    df_cuentas = pd.read_excel('cuentas.xlsx')
except FileNotFoundError:
    df_cuentas = pd.DataFrame(columns=["Correo", "Primer Nombre", "Primer Apellido", "Contraseña"])

formulario_registro = st.form
with formulario_registro("Formulario de registro"):
    st.subheader("Complete todos los campos")
    col1,col2=st.columns(2)
    p_nombre = col1.text_input("Primer nombre")
    p_apellido = col2.text_input("Primer apellido")
    correo = st.text_input("Correo electronico")
    contra = col1.text_input("Contraseña", type = "password")
    confcontra = col2.text_input("Confirmar Contraseña", type = "password")
    acepta_politicas = st.checkbox("Acepto las políticas de tratamiento de datos personales")
    st.form_submit_button("Submit")
    if confcontra != contra:
        st.write("Las 2 contraseñas que acabo de digitar no coinciden")
    elif (correo == "" or p_nombre == "" or p_apellido == "" or contra == ""):
        st.write("Porfavor llene todos los campos")
    elif (correo.find("@") == -1):
        st.write("No escribio una dirreccion de correo electronico válida")
    elif (not acepta_politicas):
        st.write("Debes aceptar las politicas de tratamiento de datos para crear una cuenta")
    elif (len(contra)<8):
        st.write("La contraseña debe tener como minimo 8 caracteres")
    else:
        # Registrar el usuario en el archivo Excel
        nueva_cuenta = pd.DataFrame({
            "Correo": [correo],
            "Primer Nombre": [p_nombre],
            "Primer Apellido": [p_apellido],
            "Contraseña": [contra]
        })
        df_cuentas = pd.concat([df_cuentas, nueva_cuenta], ignore_index=True)
        df_cuentas.to_excel('cuentas.xlsx', index=False)
        
        st.write("Usuario registrado con éxito")

        #a="meter los datos en un base de datos y poner al correo como identificador unico de los usuarios"
#formulario_registro.clear             