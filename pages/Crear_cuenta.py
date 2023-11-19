# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
# Agregamos un título HTML a la aplicación

# Intentamos cargar un archivo CSV existente o creamos un DataFrame vacío
try:
    df_cuenta_actual = pd.read_csv("cuenta_actual.csv")
except (FileNotFoundError,pd.errors.EmptyDataError):
    df_cuenta_actual = pd.DataFrame(columns=["Correo", "Contraseña","Primer Nombre", "Peliculas Favoritas"])   
try:
    df_cuentas = pd.read_csv("cuentas.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    df_cuentas = pd.DataFrame(
        columns=["Correo", "Primer Nombre", "Primer Apellido", "Contraseña", "Peliculas Favoritas"]
    )
if len(df_cuenta_actual) == 0:
    st.markdown("<h1>Registro de usuario</h1>", unsafe_allow_html=True)
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
                "Peliculas Favoritas": []
            }
        )
            df_cuentas = pd.concat([df_cuentas, nueva_cuenta], ignore_index=True)

        # Guardamos el DataFrame actualizado en un archivo CSV
            df_cuentas.to_csv("cuentas.csv", index=False)

        # Mostramos el DataFrame actualizado y un mensaje de éxito
            st.write("Usuario registrado con éxito")
        
# Texto de la política de tratamiento de datos personales
    politica_text = """
# Política de Tratamiento de Datos Personales

## 1. Introducción

Esta Política de Tratamiento de Datos Personales describe cómo Moviematch recopila, utiliza, almacena y protege la información personal que proporcionas a través de nuestra aplicación. Esta Política se aplica a todos los usuarios de la Aplicación.

## 2. Información Personal que Recopilamos

Recopilamos información personal que tú proporcionas voluntariamente cuando utilizas la Aplicación. Esta información puede incluir, entre otros:

- Nombre y apellidos.
- Dirección de correo electrónico.
- Preferencias de género para recomendaciones de películas.
- Historial de visualización y calificaciones de películas.
- Información de la cuenta, como nombre de usuario y contraseña.

## 3. Uso de la Información Personal

Utilizamos la información personal que recopilamos para los siguientes propósitos:

- Proporcionar recomendaciones personalizadas de películas.
- Mejorar la experiencia del usuario en la Aplicación.
- Proteger la seguridad de la Aplicación y de nuestros usuarios.
- Cumplir con las leyes y regulaciones aplicables.

## 4. Consentimiento

Al utilizar la Aplicación, aceptas y consientes el tratamiento de tu información personal de acuerdo con esta Política.

## 5. Compartir Información Personal

No compartimos tu información personal con terceros sin tu consentimiento, excepto en los siguientes casos:

- Proveedores de servicios: Podemos compartir tu información con terceros que nos brindan servicios, como el alojamiento de datos, análisis y soporte técnico.
- Cumplimiento legal: Podemos divulgar tu información personal si estamos obligados por ley o si creemos de buena fe que dicha divulgación es necesaria para cumplir con una obligación legal, proteger nuestros derechos, resolver disputas o garantizar la seguridad de nuestros usuarios.

## 6. Seguridad de Datos

Tomamos medidas razonables para proteger tu información personal contra pérdida, acceso no autorizado, divulgación, alteración o destrucción. Sin embargo, ten en cuenta que ninguna transmisión de datos en Internet o sistema de almacenamiento es completamente seguro.

## 7. Derechos del Titular de los Datos

Tienes derechos sobre tus datos personales, que incluyen:

- Acceder a tus datos personales.
- Corregir tus datos personales.

## 8. Cambios en la Política

Nos reservamos el derecho de actualizar o modificar esta Política en cualquier momento. Te notificaremos sobre los cambios a través de la Aplicación o por otros medios. El uso continuado de la Aplicación después de dichas modificaciones constituye tu aceptación de la Política revisada.

## 9. Contacto

Si tienes preguntas, inquietudes o solicitudes relacionadas con esta Política, contáctanos a través de dramirezla@unal.edu.co.

Fecha de entrada en vigor: Octubre 28 del 2023
"""

# Mostrar la política de tratamiento de datos personales en Markdown
    with st.expander("Ver Política de Tratamiento de Datos Personales"):
        st.markdown(politica_text)

else:
    titulo = "Bienvenido a tu perfil "+ df_cuenta_actual["Primer Nombre"] + "!"
    st.title(titulo[0])
    st.write("Estos son tus datos: ")
    st.write(df_cuenta_actual)

    seleccion = st.selectbox("Selecciona el campo de tus datos que deseas editar",["Cambiar contraseña","Cambiar Nombre","Borrar pelicula favorita"])
    correo = df_cuenta_actual["Correo"][0]
    boton_aplicar = st.button("Aplicar")
    boton_cerrar = st.button("Cerrar Sesion")

    if boton_cerrar:
        df_vacio = pd.DataFrame(columns=["Correo","Contraseña","Primer Nombre","Peliculas Favoritas"])
        df_vacio.to_csv("cuenta_actual.csv", index=False)


    if seleccion == "Cambiar contraseña":
        nueva_cont = st.text_input("Digite una nueva contraseña",type="password")
        conf_cont = st.text_input("Digite de nuevo la contraseña",type="password")

        if boton_aplicar:
            if (nueva_cont != conf_cont):
                st.write(
            "<span style='color:red; font-weight:bold;'>Las contraseñas no coinciden</span>",
            unsafe_allow_html=True,
        )
            elif(len(nueva_cont) < 8):
                st.write(
            "<span style='color:red; font-weight:bold;'>Su contraseña debe poseer 8 caracteres o mas</span>",
            unsafe_allow_html=True,
        )
            else:
                df_cuenta_actual["Contraseña"] = nueva_cont
                if correo in df_cuentas['Correo'].values:
                    df_cuentas.loc[df_cuentas['Correo'] == correo, 'Contraseña'] = nueva_cont
                st.write(
            "<span style='color:red; font-weight:bold;'>La contraseña se ha cambiado con exito</span>",
            unsafe_allow_html=True,
        )
                df_cuenta_actual.to_csv("cuenta_actual.csv", index=False)
                df_cuentas.to_csv("cuentas.csv", index = False)
    
    if seleccion == "Cambiar Nombre" :
        nuevo_nombre = st.text_input("Digite su nuevo nombre")
        if boton_aplicar:
            if nuevo_nombre == "":
                st.write(
            "<span style='color:red; font-weight:bold;'>Su nuevo nombre no puede estar vacio</span>",
            unsafe_allow_html=True,
        )
            else:
                df_cuenta_actual["Primer Nombre"] = nuevo_nombre
                if correo in df_cuentas['Correo'].values:
                    df_cuentas.loc[df_cuentas['Correo'] == correo, 'Primer Nombre'] = nuevo_nombre
                st.write(
            "<span style='color:red; font-weight:bold;'>El Nombre se ha cambiado con exito</span>",
            unsafe_allow_html=True,
        )
                df_cuenta_actual.to_csv("cuenta_actual.csv", index=False)
                df_cuentas.to_csv("cuentas.csv", index = False)
    if seleccion == "Borrar pelicula favorita" :
        listado_peliculas = df_cuenta_actual["Peliculas Favoritas"].str.split(', ').explode().unique()
        pelicula_a_borrar = st.selectbox("Indique que pelicula desea borrar",listado_peliculas)
        if boton_aplicar:
        # Borrar la película seleccionada
            listado_peliculas = listado_peliculas[listado_peliculas != pelicula_a_borrar]
            df_cuenta_actual['Peliculas Favoritas'] = df_cuenta_actual['Peliculas Favoritas'].apply(lambda x: [pelicula for pelicula in x.split(', ') if pelicula != pelicula_a_borrar])
        # Actualizar el DataFrame o realizar cualquier otra acción necesaria
        # Puedes imprimir un mensaje para confirmar que la película se ha borrado
            st.write(f"La película '{pelicula_a_borrar}' ha sido borrada de las favoritas.")
            st.write(df_cuenta_actual)
            st.write(listado_peliculas)
            df_cuentas.loc[df_cuentas['Correo'] == correo, 'Peliculas Favoritas'] = df_cuenta_actual
            st.write(
            "<span style='color:red; font-weight:bold;'>Las peliculas favoritas han sido cambiadas con exito</span>",
            unsafe_allow_html=True,
        )
            df_cuenta_actual.to_csv("cuenta_actual.csv", index=False)
            df_cuentas.to_csv("cuentas.csv", index = False)
        

