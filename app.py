import streamlit as st
st.set_page_config(layout="wide", page_title='Nebula', page_icon='🤖')
import pandas as pd
import utils
from Modelos_clf import Clasificador, model_neg, tokenizer_neg, model_pos, tokenizer_pos
from GEMINI import gemini


# Inicializar session_state si aún no existe
if "carga_comentarios_realizada" not in st.session_state:
    st.session_state.carga_comentarios_realizada = False


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


if st.session_state.carga_comentarios_realizada == True:
        df_positivos = st.session_state.df_positivos
        df_negativos = st.session_state.df_negativos
        df = pd.concat([df_positivos, df_negativos])
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
        
        tab1, tab2 = st.tabs(['Estadisticas', 'Reporte'])
        with tab1:
            utils.graficar_categorias(df[df['tipo']==1], df[df['tipo']==0])
        
        with tab2:
                    st.write('Reporte de comentarios')
                    st.markdown('*El reporte generado sera siempre el mismo por tema de maqueta solamente. La idea es que sea generado en base a los comentarios correspondientes al filtro aplicado*')
                    st.markdown('*Comentar que las sugerencias de mejora, la idea es que vayan solo para los comentarios negativos*')
                    
                    generate = st.button('Generar Reporte')
                    #### AÑADIR FILTROS O INPUTS DE LOS USUARIOS PARA LOS 3 DIFERENTES TIPOS DE REPORTE
                    ### CURSO/SECCION - COORDINACION CURSO (TODAS LAS SECCION DE UN CURSO) - DEPARTAMENTAL (EJ: DEPARTAMENTO DE MATEMATICAS.)

                    if generate:
                        st.markdown("**Reporte a nivel de maqueta solamente. Para hacerse una idea**")
                        st.markdown("**Reporte de comentarios**")
            #             comentarios = "\n".join(
            #               df
            #               .comentario
            #               #.sample(100, random_state=42)
            #               .values
            # )
            #             categoria = "\n".join(
            #                 df
            #                 .topic
            #                 #.sample(100, random_state=42)
            #                 .values)
            #             tabla = tabulate.tabulate(comentarios, tablefmt='grid', headers='keys')
                        prompt = f"Comentario | Categoria\n\n"
                        prompt += "-" * 30 + "\n"  # Línea separadora

                        for idx, row in df.iterrows():
                            prompt += f"{row['comentario']} | {row['topic']}\n"
                            prompt += "-" * 30 + "\n"  # Línea separadora
                        prompt_parts = f"""Genera un reporte de los siguientes comentarios y sus respectivas categorias. El reporte debe ser lo más completo y formal posible. Debe ser en formato informe pensando en que se entregara a quien lo requiera a modo de feedback. Los comentarios son de una encuesta docente. \n\n {prompt}"""
                       # st.text(f"""{prompt_parts}""")
                        response = gemini.generate_content(prompt_parts)
                        reporte = st.markdown(f"""{response.text}""")
                        st.markdown('**El reporte debera ser en formato pdf, por ahora solo es un archivo de texto.**')
                        st.download_button('Descargar reporte', response.text, file_name='reporte.txt')
