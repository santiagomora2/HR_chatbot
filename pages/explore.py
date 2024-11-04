import functions_utils as fn
import streamlit as st
import pandas as pd

df = pd.read_csv('fake_data.csv')
options_entities = list(df['Entidad'].unique())

def main():
    st.set_page_config(
        page_title="Explora"
    )

    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.header('Explora los datos de los candidatos!')

    # Variables de la sesión
    if 'entidad_sel' not in st.session_state:
        st.session_state.entidad_sel = "México"

    ############ Sidebar ############
    with st.sidebar:
        # Actualizar opciones de entidades
        options_entities.remove(st.session_state.entidad_sel)
        options_entities.insert(0, st.session_state.entidad_sel)
        
        # Seleccionar Entidad
        st.session_state.entidad_sel = st.selectbox(
            "Entidad Federativa:",
            options_entities
        )

        # Obtener opciones de ciudades según la entidad seleccionada
        options_cities = fn.obtain_cities(st.session_state.entidad_sel, df)
        
        # Seleccionar Ciudad
        cities = st.multiselect(
            'Ciudad/Municipio',
            options_cities,
            default=options_cities  # Seleccionar ciudades válidas o la primera opción
        )

        st.page_link("pages/ask.py", label="Pregunta a la IA", icon="🤖")
        st.page_link("app.py", label="Regresar a Inicio", icon="🏠")

    try:
        data, _ = fn.obtain_candidates(cities, df)
        data = data.drop(columns = 'index')

        ############## Información sobre candidatos (General) ###############

        # ingresar index de candidato
        indexx = st.text_input("Índice (index) de Candidato")
        if indexx:
            try:
            # try, except para si el índice no existe
                try:
                    # Extraer informacion del candidato
                    info_cand = fn.informacion_candidato(indexx, data)

                    # Mostrar informacion en dos columnas 
                    col1, col2 = st.columns(2)
                    keys = list(info_cand.keys())
                    num_keys = len(keys)

                    # Calcular el punto medio
                    half = (num_keys // 2) + 2

                    # Mostrar la primera mitad en la primera columna
                    with col1:
                        for key in keys[:half]:
                            st.write(f"{key}: {info_cand[key][0]}")

                    # Mostrar la segunda mitad en la segunda columna
                    with col2:
                        for key in keys[half:]:
                            st.write(f"{key}: {info_cand[key][0]}")
                except ValueError:
                    st.error('''Favor de ingresar un número de ```index``` válido''', icon="🚨")
            except KeyError:
                st.error('''El Índice (index) de Candidato no se encontró en los candidatos de las ciudades seleccionadas. 
                         Favor de ingresar un Índice correcto que se encuentre en la columna ```index``` de la base de datos siguiente.''', icon="🚨")
        st.markdown('**Base de datos con todos los candidatos en las ciudades seleccionadas.**')
        st.dataframe(data)

    except IndexError:
        st.error('Por favor selecciona una ciudad/municipio', icon="🚨")


if __name__ == '__main__':
    main()