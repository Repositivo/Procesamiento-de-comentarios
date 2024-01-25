import streamlit as st
st.set_page_config(layout="wide", page_title='Nebula', page_icon='🤖')
import pandas as pd
import utils
from Modelos_clf import Clasificador, model_neg, tokenizer_neg, model_pos, tokenizer_pos
from GEMINI import gemini



# Inicializar session_state si aún no existe
if "carga_comentarios_realizada" not in st.session_state:
    st.session_state.carga_comentarios_realizada = True


# Verificar si la carga de comentarios ya se ha realizado
if not st.session_state.carga_comentarios_realizada:
        st.header('Procesamiento de comentarios', divider =  'grey')
        df = st.file_uploader("Elige un archivo CSV", type='csv')
        if df is not None:
            df = pd.read_csv(df)
            df = df.sample(100, random_state=22)
            df_positivos, df_negativos, df = utils.preprocesamiento_comments(df)
            
            with st.spinner('Procesando comentarios...'):
                df_positivos['topic'] = Clasificador(model_pos, tokenizer_pos, text=df_positivos['comentario'].tolist())
                df_negativos['topic'] = Clasificador(model_neg, tokenizer_neg, text=df_negativos['comentario'].tolist())
                st.success('Comentarios procesados correctamente',icon='🤖')
                st.session_state.df_positivos = df_positivos
                st.session_state.df_negativos = df_negativos
                st.session_state.df = df
            st.session_state.carga_comentarios_realizada = True
            st.rerun()


if st.session_state.carga_comentarios_realizada == True:

        # df_positivos = st.session_state.df_positivos
        # df_negativos = st.session_state.df_negativos
        # df = pd.concat([df_positivos, df_negativos])
        df = pd.read_csv('./Datos/PlanComun2023-otono-labeled.csv')
        body = st.container()
        with st.sidebar:
            st.header('Filtros', divider =  'grey')
            filtro_general = st.multiselect('¿Qué columnas quieres filtrar?', df.columns.tolist())
            st.divider()
            for column in filtro_general:
                input = st.multiselect(column, df[column].unique().tolist())
                df = df[df[column].isin(input)]
            body.header('Visualización de comentarios', divider =  'grey') 
            body.dataframe(df, use_container_width=True, hide_index=True, height=150)
        # comentario contiene una palabra clave
            lista = ['humillante', 'humillación', 'humillado', 'humillada', 'humillar', 'humillan', 'humillamos', 'humillabamos', 'humillaban', 'humillaba', 'humilló',
                     'machista', 'machismo', 'machista', 'machistas', 'machismos', 'machistamente', 'machistico', 'machistos', 'machistamente', 'machistico', 'machistos',
                     'discriminación', 'discriminado', 'discriminada', 'discriminados', 'discriminadas', 'discriminamos', 'discriminabamos', 'discriminaban', 'discriminaba', 'discriminó',
                     'racista', 'racismo', 'racistas', 'racismos', 'racistamente', 'racistico', 'racistos', 'racistamente', 'racistico', 'racistos',
                     ]
         
           
           
        tab1, tab2, tab3, tab4 = st.tabs(['Análisis','Detalle categorías', 'Generar reporte', '⚠️Alerta!'])
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('## Dashboard')
            with col2:
                st.metric(label='Total comentarios', value=df.shape[0])
            with col3:
                st.metric(label='Total comentarios positivos', value=df[df['tipo']==1].shape[0])
            with col4:
                st.metric(label='Total comentarios negativos', value=df[df['tipo']==0].shape[0]) 
            with st.container(border=True):
                st.markdown('## Porcentaje de comentarios por categoría')

                utils.graficar_categorias(df[df['tipo']==1], df[df['tipo']==0])
                col1, col2 = st.columns(2)
 
                with col1:
                    utils.graficar_barras_apiladas_departamento(df)
                    utils.graficar_barras_apiladas_curso(df)
                with col2:
                    
                    utils.graficar_barras_apiladas_categoria(df)
                    utils.graficar_barras_apiladas_seccion(df)

              
            
        
        with tab2:

                selected = st.selectbox('Selecciona una categoría', df['topico'].unique().tolist())

                categories_mapping = {
    "Experiencia Educativa": 0,
    "Atención y Disposición Docente": 1,
    "Calidad de la Enseñanza": 2,
    "Gestión de Actividades y Evaluaciones": 3,
    "Estilo de Enseñanza y Dinámica de Clases": 4,
    "Experiencia y Organización del Curso": 5,
    "Reconocimiento a Profesores y Auxiliares": 6,
    "Evaluaciones y Controles": 7,
    "Otros": 99
}

                if selected in categories_mapping:
                    st.header('Descripcion de la categoría', divider='grey')
                    category_id = categories_mapping[selected]
                    
                    


                    descriptions = {
                        0: '''
                        Este tópico aborda las opiniones y evaluaciones de estudiantes sobre la calidad de la enseñanza proporcionada por el equipo docente y los auxiliares en un curso académico. Se discuten aspectos como la disposición, el entusiasmo, la claridad en la explicación, la participación, el compromiso y otros elementos que impactan la experiencia de aprendizaje. Los comentarios reflejan tanto aspectos positivos como áreas de mejora, proporcionando una visión completa de la dinámica educativa en el curso.
                        ''',
                        1: '''
                        Este tópico se centra en la interacción entre profesores y estudiantes, especialmente en cuanto a la disposición para resolver dudas. Los comentarios reflejan la dedicación, claridad y participación del profesor en el proceso educativo. Se abordan aspectos positivos como la preocupación por el aprendizaje, la comunicación efectiva, y la disposición para escuchar a los alumnos. También se mencionan áreas de mejora, como la necesidad de una mayor atención a correos electrónicos y una comunicación más dinámica en clase. La retroalimentación proporciona una visión completa de la experiencia educativa desde la perspectiva de la interacción profesor-estudiante.
                        ''',
                        2: '''
                        Este tópico se centra en la evaluación de la calidad de la enseñanza, abordando la forma en que se presentan y explican los contenidos. Los comentarios reflejan opiniones sobre la comprensión de la materia, la claridad de las explicaciones, la efectividad de los ejemplos proporcionados y la percepción general sobre la enseñanza de los contenidos del curso. Se destaca tanto aspectos positivos, como la dinámica y la empatía de los profesores, como áreas de mejora, incluyendo la necesidad de una explicación más clara de los ejercicios y una mayor coherencia en la presentación de materiales.
                        ''',
                        3: '''
                        Este tópico aborda la organización y gestión de actividades y evaluaciones en el curso. Los comentarios reflejan la percepción de los estudiantes sobre la disposición del profesor y auxiliares para responder dudas, la claridad en las instrucciones y el tiempo de entrega de notas. Se destacan tanto aspectos positivos, como la utilidad de las guías y el material de preparación, como áreas de mejora, incluyendo la necesidad de una mayor retroalimentación y claridad en las actividades. La retroalimentación proporciona una visión detallada de la experiencia de los estudiantes en cuanto a la planificación y ejecución de las tareas y evaluaciones.
                        ''',
                        4: '''
                        Este tópico aborda la dinámica de las clases, el estilo de enseñanza del profesor y la participación de los estudiantes. Los comentarios reflejan percepciones sobre la motivación, la claridad en la explicación, la interactividad en clase y la relación entre el contenido y la materia. Se destacan tanto aspectos positivos, como la participación activa y la disponibilidad del profesor, como áreas de mejora, incluyendo la necesidad de mayor motivación y claridad en la enseñanza. La retroalimentación proporciona una visión detallada de la experiencia de aprendizaje en términos de dinámica de clases y enfoque del profesor.
                        ''',
                        5: '''
                        Este tópico se centra en la evaluación general del curso por parte de los estudiantes. Los comentarios reflejan aspectos positivos y áreas de mejora, abordando la estructura y organización del curso, la relación con los docentes, el nivel de compromiso y la utilidad percibida. Se destacan elementos como la empatía de los profesores, la organización del curso y la efectividad de la estructura de evaluación. La retroalimentación proporciona una visión general de la experiencia del curso, permitiendo identificar aspectos apreciados y posibles oportunidades de mejora.
                        ''',
                        6: '''
                        Este tópico se centra en expresiones de agradecimiento, reconocimiento y valoración positiva hacia profesores y auxiliares. Los comentarios reflejan aprecio por la labor docente, destacando la calidad de enseñanza, empatía, y el impacto positivo en la experiencia de aprendizaje. También se menciona la importancia de algunos profesores y auxiliares en la percepción del curso y se expresan opiniones sobre su efectividad y capacidad para generar un ambiente propicio para el aprendizaje.
                        ''',
                        7: '''
                        Este tópico se enfoca en las evaluaciones y controles del curso, abordando aspectos como la dificultad de las preguntas, la metodología utilizada en los exámenes, y la experiencia general durante estas instancias de evaluación. Los comentarios reflejan opiniones sobre la preparación proporcionada, la claridad en las pautas, así como sugerencias y críticas constructivas sobre la dificultad y el tiempo asignado para los controles. Se mencionan aspectos específicos de las tareas y se proponen mejoras en la comunicación de los enunciados. Además, se destaca la importancia de los materiales proporcionados con anticipación para el estudio.
                        ''',
                        99: '''
                        Este tópico representa comentarios que no se agrupan directamente en ninguna de las categorías principales. Contiene comentarios monosilabos, sin sentido, o que no aportan información relevante para el análisis. También incluye comentarios que no se pueden clasificar debido a la falta de contexto o información.
                        '''
                    }
                    
                    
                    st.markdown(descriptions[category_id])
                    st.markdown('## Comentarios de la categoría')
                    st.dataframe(df[df['topico']==selected]['comentario'], use_container_width=True, hide_index=True, height=150, width=600)
                else:
                    st.warning("Categoría no encontrada.")
            
        with tab3:
                    reporte = ''
                    st.markdown('## Reporte de comentarios')                    
                    with st.container(border=True):
                         fecha = st.date_input('Fecha de entrega')
                         destinatario = st.text_input('Destinatario')
                         cargo = st.selectbox('Cargo', ['Director de carrera', 'Coordinador de curso', 'Coordinador de carrera', 'Coordinador de departamento', 'Docente'])
                         remitente = st.text_input('Remitente') 
                         tipo = st.selectbox('Tipo de reporte', ['Curso/sección', 'Coordinación de curso', 'Departamental'])
                         generar = st.button(label='Generar Reporte')
                         
                    if generar:
                        with st.spinner('Generando reporte...'):
                            prompt = f"Comentario | Categoria\n\n"
                            prompt += "-" * 30 + "\n"  # Línea separadora

                            for idx, row in df.sample(100).iterrows():
                                prompt += f"{row['comentario']} | {row['topico']}\n"
                                prompt += "-" * 30 + "\n"  # Línea separadora
                            prompt_parts = f"""
                           Genera un informe exhaustivo de los comentarios recabados en la encuesta docente, clasificándolos según sus respectivas categorías. El informe se estructura a nivel {tipo} y está dirigido a {destinatario}, quien ocupa el cargo de {cargo}. El remitente del informe es {remitente}, y su fecha de emisión es {fecha}.

Este documento adoptará la formalidad de un informe completo diseñado para su presentación a la entidad solicitante. Incluye la cantidad de los comentarios de la siguiente manera: {df[df['tipo']==1].shape[0]} comentarios positivos y {df[df['tipo']==0].shape[0]} comentarios negativos. Evita la inclusión de porcentajes, ya que los comentarios proporcionados son una muestra representativa del total.

{prompt}"""
                        
                            response = gemini.generate_content(prompt_parts)

                            with st.container(border=True):
                                with st.chat_message('ai',):
                                        reporte = st.markdown(f"""{response.text}""")
                                        #Button para copiar el texto
                            
   

        with tab4:
             if df[df['comentario'].str.contains('|'.join(lista))].shape[0] > 0:
                    st.warning('Se han encontrado comentarios con palabras fuertes')
                    st.dataframe(df[df['comentario'].str.contains('|'.join(lista))], use_container_width=False, hide_index=True, height=150, width=600)
             else:
                    st.success('No se han encontrado comentarios con palabras fuertes')
                    