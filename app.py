import streamlit as st
import pandas as pd


body = st.container()
with st.sidebar:
    st.header('Procesamiento de comentarios', divider =  'grey')

    with st.expander('Carga de comentarios'):
        df = st.file_uploader("Elige un archivo CSV", type='csv')
    
    if df is not None:
        df = pd.read_csv(df)
        st.header('Filtros', divider =  'grey')

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
        st.markdown('**Estadisticas de ejemplo**')
        st.markdown('Aqui se deberia ver un grafico similar que cuente, por ejemplo, que categoria es más comun en un cierto FILTRO')
        st.markdown('** <--- Se actuliza en tiempo real segun el filtro**')
        st.markdown('**Cantidad de comentarios asignados a cada categoria(El grafico de abajo es solo un ejemplo, ya que muestra la cantidad de comentarios positivos y negativos por el filtro aplicado)**')
        st.bar_chart(df['tipo'].value_counts())
        st.markdown('**Otro tipo de información. Quizas añadir la precision con la que fueron clasificados los comentarios en su respectiva categoria, ya que un modelo no será nunca totalmente preciso**')
        st.markdown('*[Inserte mas informacion util para visualizar por filtro]*')


    with tab2:
        st.write('Reporte de comentarios')
        st.markdown('*El reporte generado sera siempre el mismo por tema de maqueta solamente. La idea es que sea generado en base a los comentarios correspondientes al filtro aplicado*')
        st.markdown('*Comentar que las sugerencias de mejora, la idea es que vayan solo para los comentarios negativos*')
        
        generate = st.button('Generar Reporte')

        if generate:
            st.markdown("**Reporte de comentarios**")
            reporte_texto = """**Reporte de Evaluación y Sugerencias de Mejora para Categorías de Comentarios Positivos**

---

### Categoría 1: Curso y Docente
**Fortalezas:**
- Los comentarios destacan la calidad del curso y la labor del docente.
- La mención de "mejor" y "gracias" sugiere una apreciación general.

**Sugerencias de Mejora:**
- Fomentar la retroalimentación específica sobre aspectos que los estudiantes consideran "mejores" para mantener y fortalecer esos puntos fuertes.
- Explorar oportunidades para destacar aún más la labor del equipo docente para crear un ambiente de aprendizaje positivo.

---

### Categoría 2: Actitud del Profesor y Disposición
**Fortalezas:**
- Se destaca la actitud positiva del profesor y su disposición para abordar dudas.
- Menciones positivas sobre la relación con los estudiantes.

**Sugerencias de Mejora:**
- Fomentar una comunicación abierta para conocer más detalles sobre la disposición del profesor y cómo puede ser mejorada.
- Implementar actividades que promuevan una interacción más estrecha entre el profesor y los estudiantes para fortalecer la conexión positiva.

---

### Categoría 3: Contenido de las Clases y Comprensión
**Fortalezas:**
- Se menciona la calidad de las clases, la materia y la comprensión de los contenidos.
- Los términos "bien" y "entender" indican una experiencia positiva de aprendizaje.

**Sugerencias de Mejora:**
- Realizar encuestas específicas sobre los métodos de enseñanza y la comprensión de los contenidos para obtener más detalles sobre lo que los estudiantes encuentran efectivo.
- Explorar posibles ajustes en la presentación de los ejercicios para mejorar aún más la comprensión y aplicabilidad de la materia.

---

### Observaciones Generales:
- Las categorías de comentarios positivos reflejan una experiencia generalmente favorable.
- La incorporación de actividades interactivas o dinámicas en las clases podría fortalecer aún más la participación y el interés de los estudiantes.
- Se recomienda establecer canales de retroalimentación abiertos para que los estudiantes expresen sus ideas de manera más detallada.

Este informe ofrece una visión general de las fortalezas y sugerencias de mejora basadas en las categorías extraídas de los comentarios positivos. La implementación de estas sugerencias puede contribuir a una experiencia educativa más enriquecedora y satisfactoria para los estudiantes."""
            reporte = st.markdown(f"""{reporte_texto}""")

            st.markdown('**Elss reporte debera ser en formato pdf, por ahora solo es un archivo de texto.**')
            st.download_button('Descargar reporte', reporte_texto)
    
    








