import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("MovieMatch")
st.sidebar.success("Seleccione la pagina que desea visitar.")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Buscar peliculas", st.session_state["my_input"])

submit = st.button("Buscar")

if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)



