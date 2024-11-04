import functions_utils as fn
import streamlit as st
from openai import OpenAI
import pandas as pd
import time

##################### API KEY Google ##################
OPENAI_API_KEY = st.secrets['API_KEY']

# API key para OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

initial_prompt = """
Actúa como si fueras un reclutador experto en recursos humanos. Se te proporcionará un diccionario con información
de candidatos, actúa como si el elemento 'index' de cada candidato fuera su nombre. Se te hará una pregunta sobre el 
posible reclutamiento de los candidatos, a lo que tu debes contestar qué candidatos (MENcIONANDO SU 'index') crees  serían más aptos para la posición
y por qué crees esto. Trata de no hablar sobre cosas que no tienen nada que ver o responder preguntas que no tienen que ver con tu rol como experto en recursos humanos.
"""

df = pd.read_excel('fake_data.xlsx')
options_entities = list(df['Entidad'].unique())

def main():
    st.set_page_config(
        page_title="IA",
    )

    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.header('Pregunta a la IA!')

    # Inicializar variables de sesión
    if 'respuesta' not in st.session_state:
        st.session_state.respuesta = ""
    if 'prev_question' not in st.session_state:
        st.session_state.prev_question = ""
    if 'entidad_sel' not in st.session_state:
        st.session_state.entidad_sel = "Ciudad de México"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar la respuesta guardada en sesión al regresar

    st.write(st.session_state.respuesta)

    # Información de Protección de Datos
    st.info('''IMPORTANTE: Por protección de datos, la IA te dirá a qué ```index``` de candidato se refiere en vez de su nombre.''', icon="ℹ️")

    ############ Sidebar ############
    with st.sidebar:
        # Actualizar opciones de entidades
        options_entities.remove(st.session_state.entidad_sel)
        options_entities.insert(0, st.session_state.entidad_sel)

        # Seleccionar Entidad
        st.session_state.entidad_sel = st.selectbox(
            "Entidad Federativa:",
            options_entities,
            index=0
        )

        # Obtener opciones de ciudades según la entidad seleccionada
        options_cities = fn.obtain_cities(st.session_state.entidad_sel, df)
        
        # Selección de Ciudad con multiselect
        cities = st.multiselect(
            'Ciudad/Municipio',
            options=options_cities,
            default=options_cities  # Seleccionar ciudades válidas o la primera opción
        )

        st.page_link("pages/explore.py", label="Explorar candidatos", icon="👤")
        st.page_link("app.py", label="Regresar a Inicio", icon="🏠")

    ############ página principal ############
    # try, except es para si no se selecciona ninguna ciudad
    try:
        # obtener datos privados y públicos
        _, data_public = fn.obtain_candidates(cities, df)

        data_public = data_public.drop(columns='index')

        ############## pregunta ia sobre candidato ###############

        data_text_for_ai = fn.data_to_text(data_public)

        question = st.chat_input('Pregunta a la IA sobre los candidatos')

        # Solo enviar la pregunta a la IA si es diferente a la anterior
        if question and question != st.session_state.prev_question:
            prompt = f"""
            CANDIDATOS:
            {data_text_for_ai}

            PREGUNTA:
            {question}
            """
            st.session_state.prev_question = question  # Actualizar pregunta anterior
            
            # Respuesta de OpenAI como stream
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # Asegúrate de usar el modelo correcto
                messages=[
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            st.write_stream(stream)

            # Mostrar la respuesta en un stream
            for chunk in stream:
                st.session_state.respuesta += chunk  # Actualizar valor en sesión


    except IndexError:
        st.error('Por favor selecciona una ciudad/municipio', icon="🚨")


if __name__ == '__main__':
    main()
