import pandas as pd

# Obtener las ciudades dentro de una entidad federativa, en forma de lista
def obtain_cities(entity:str, data:pd.DataFrame):
    # Recibe -- entidad (string)
    # Regresa -- ciudades (lista)
    return list(data[data['Entidad'] == entity]['Ciudad'].unique())

# Obtener los candidatos que pertenecen a alguna ciudad dentro de una lista de ciudades
def obtain_candidates(cities:list, data:pd.DataFrame):
    # Recibe -- ciudades (lista)
    # Regresa -- Información de Candidatos (DataFrame)
    #         -- Información de candidatos sin información sensible (DataFrame)
    
    df_t = data[data['Ciudad'] == cities[0]]
    if len(cities) > 0:
        for i in range(1, len(cities)):
            df_t = pd.concat([df_t, data[data['Ciudad'] == cities[i]]])
    df_t = df_t.reset_index()

    df_t_public = df_t.drop(columns = ['Nombre', 'Apellido',
       'Fecha de nacimiento', 'Género', 'Teléfono',
       'E-mail', 'Ciudad', 'Entidad'])
    
    return df_t, df_t_public

# Función para obtener información de un candidato en específico
def informacion_candidato(indexx:int, data:pd.DataFrame):
    # Recibe -- Índice (int)
    #        -- data (Dataframe): de los candidatos en las ciudades seleccionadas
    # Regresa -- diccionario con la información del candidato
    return data[data['ID'] == int(indexx)].reset_index().drop(columns = 'index').to_dict()
    
# función para convertir base de datos de candidatos a formato json para preguntar a IA
def data_to_text(data_public:pd.DataFrame):
    # Recibe -- dataFrame con candidatos
    # Regresa -- texto en formato Json con la información

    # Convertir los datos a un formato adecuado para el modelo
    candidatos = data_public.to_dict(orient='records')

    # Formatear como texto para pasarlo a la API
    texto_candidatos = "\n".join([f"Candidato: {candidato}" for _, candidato in enumerate(candidatos)])

    return texto_candidatos

