import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
# from transformers import pipeline

# clf_p = pipeline("text-classification",model="crisU8/positivo_model", from_tf=True)

# clf_p = pipeline("text-classification",model="crisU8/negative_model", from_tf=True)
# load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set up the model
generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

body = st.container()
with st.sidebar:
    st.header('Procesamiento de comentarios', divider =  'grey')

    with st.expander('Carga de comentarios'):
        df = st.file_uploader("Elige un archivo CSV", type='csv')
    
    if df is not None:
        df = pd.read_csv(df)
        st.header('Filtros', divider =  'grey')
        st.text('Los filtros finales seran en base a la base de datos con los comentarios de la encuesta docente')

        filter_container = st.container()
        with filter_container:
            filtro_general = st.multiselect('Por columna', df.columns.tolist())
            st.divider()
            for column in filtro_general:
                input = st.multiselect(column, df[column].unique().tolist())
                df = df[df[column].isin(input)]
            body.header('Visualización de comentarios', divider =  'grey')  
            body.dataframe(df, use_container_width=True, hide_index=True, height=200)


if df is not None:
    
    tab1, tab2 = st.tabs(['Estadisticas', 'Reporte'])
    with tab1:
        # df_p = df[df['tipo'] == 1]
        # df_n = df[df['tipo'] == 0]
        # comments_p = df_p['comentario'].sample(100).tolist()
        # comments_n = df_n['comentario'].sample(100).tolist()
        # clasificacion_p = clf_p(comments_p)
        # clasificacion_n = clf_p(comments_n)
        # list_cat_p = [clasificacion_p[i]['label'] for i in range(len(comments_p))]
        # list_cat_n = [clasificacion_n[i]['label'] for i in range(len(comments_n))]
        # df_prueba_p = pd.DataFrame({
        #     'comentario': comments_p,
        #     'clasificacion': list_cat_p
        # })
        # df_prueba_n = pd.DataFrame({
        #     'comentario': comments_n,
        #     'clasificacion': list_cat_n
        # })
        # st.bar_chart(df_prueba_p['clasificacion'].value_counts())
        st.bar_chart(df['tipo'].value_counts())


    with tab2:
        st.write('Reporte de comentarios')
        st.markdown('*El reporte generado sera siempre el mismo por tema de maqueta solamente. La idea es que sea generado en base a los comentarios correspondientes al filtro aplicado*')
        st.markdown('*Comentar que las sugerencias de mejora, la idea es que vayan solo para los comentarios negativos*')
        
        generate = st.button('Generar Reporte')
        #### AÑADIR FILTROS O INPUTS DE LOS USUARIOS PARA LOS 3 DIFERENTES TIPOS DE REPORTE
        ### CURSO/SECCION - COORDINACION CURSO (TODAS LAS SECCION DE UN CURSO) - DEPARTAMENTAL (EJ: DEPARTAMENTO DE MATEMATICAS.)

        if generate:
            st.markdown("**Reporte de comentarios**")
            comentarios = "\n".join(
               df
               .comentario
               .sample(100, random_state=42)
               .values
)
            categoria = "\n".join(
                df
                .nombre_curso
                .sample(100, random_state=42)
                .values)
            prompt_parts = [
  f"Genera un reporte de los siguientes comentarios. El reporte debe ser lo más completo y formal posible. Debe ser en formato informe pensando en que se entregara a quien lo requiera a modo de feedback. Los comentarios son de una encuesta docente. \n Comentarios{comentarios}",
]
            st.markdown(f"""{comentarios}""")
            response = model.generate_content(prompt_parts)
            reporte = st.markdown(f"""{response.text}""")
#             #reporte_texto = """**Reporte de Evaluación y Sugerencias de Mejora para Categorías de Comentarios Positivos**

# ---

# ### Categoría 1: Curso y Docente
# **Fortalezas:**
# - Los comentarios destacan la calidad del curso y la labor del docente.
# - La mención de "mejor" y "gracias" sugiere una apreciación general.

# **Sugerencias de Mejora:**
# - Fomentar la retroalimentación específica sobre aspectos que los estudiantes consideran "mejores" para mantener y fortalecer esos puntos fuertes.
# - Explorar oportunidades para destacar aún más la labor del equipo docente para crear un ambiente de aprendizaje positivo.

# ---

# ### Categoría 2: Actitud del Profesor y Disposición
# **Fortalezas:**
# - Se destaca la actitud positiva del profesor y su disposición para abordar dudas.
# - Menciones positivas sobre la relación con los estudiantes.

# **Sugerencias de Mejora:**
# - Fomentar una comunicación abierta para conocer más detalles sobre la disposición del profesor y cómo puede ser mejorada.
# - Implementar actividades que promuevan una interacción más estrecha entre el profesor y los estudiantes para fortalecer la conexión positiva.

# ---

# ### Categoría 3: Contenido de las Clases y Comprensión
# **Fortalezas:**
# - Se menciona la calidad de las clases, la materia y la comprensión de los contenidos.
# - Los términos "bien" y "entender" indican una experiencia positiva de aprendizaje.

# **Sugerencias de Mejora:**
# - Realizar encuestas específicas sobre los métodos de enseñanza y la comprensión de los contenidos para obtener más detalles sobre lo que los estudiantes encuentran efectivo.
# - Explorar posibles ajustes en la presentación de los ejercicios para mejorar aún más la comprensión y aplicabilidad de la materia.

# ---

# ### Observaciones Generales:
# - Las categorías de comentarios positivos reflejan una experiencia generalmente favorable.
# - La incorporación de actividades interactivas o dinámicas en las clases podría fortalecer aún más la participación y el interés de los estudiantes.
# - Se recomienda establecer canales de retroalimentación abiertos para que los estudiantes expresen sus ideas de manera más detallada.

# Este informe ofrece una visión general de las fortalezas y sugerencias de mejora basadas en las categorías extraídas de los comentarios positivos. La implementación de estas sugerencias puede contribuir a una experiencia educativa más enriquecedora y satisfactoria para los estudiantes."""
#             #reporte = st.markdown(f"""{reporte_texto}""")

            st.markdown('**El reporte debera ser en formato pdf, por ahora solo es un archivo de texto.**')
            st.download_button('Descargar reporte', response.text, file_name='reporte.txt')
    
    








