import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def preprocesamiento_comments(df):
  '''
   Función que preprocesa los comentarios, eliminando comentarios demasiado cortos y separando el dataframe en comentarios
   positivos y negativos.

   dataframe -> dataframe (+), dataframe (-)
  '''
  df = df[df['comentario'].apply(lambda x: len(str(x).split()) > 3)]
  df_positivos = df[df['tipo']==1]
  df_negativos = df[df['tipo']==0]
  return df_positivos, df_negativos, df

def graficar_barras_apiladas_departamento(df):
    # Agrupar y contar el número de observaciones para cada combinación de 'topico' y 'tipo'
    grouped_df = df.groupby(['Departamento', 'topico']).size().unstack()
    #ordenar por total
    grouped_df = grouped_df.sort_values(by=['Atención y Disposición Docente'], ascending=True)
    # Crear el gráfico de barras horizontales apiladas
    fig, ax = plt.subplots(figsize=(12, 8))
    grouped_df.plot(kind='barh', stacked=True, colormap='RdYlGn', edgecolor='black', ax=ax, ecolor='white',)
    ax.set_facecolor('#121212')  # Cambié el color del fondo del gráfico
    fig.set_facecolor('#121212')  # Cambié el color del fondo de la figura
    ax.tick_params(colors='white')  # Cambié el color de las marcas de los ejes


    # Personalizar el gráfico
    plt.title('Cantidad de comentarios en cada categoria según departamento', color='white')
    plt.xlabel('Cantidad', color='white')
    plt.ylabel('')
    legend = plt.legend(title='Categoria', bbox_to_anchor=(1, 1), edgecolor='white', labelcolor='white', facecolor='#121212', title_fontsize='12', loc = 'best')
    legend.get_title().set_color('white')
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)

def graficar_barras_apiladas_categoria(df):
    # Agrupar y contar el número de observaciones para cada combinación de 'topico' y 'tipo'
    grouped_df = df.groupby(['topico', 'tipo']).size().unstack()
    #ordenar por total
    grouped_df = grouped_df.sort_values(by=0, ascending=True)
    # Crear el gráfico de barras horizontales apiladas
    fig, ax = plt.subplots(figsize=(12, 8))
    grouped_df.plot(kind='barh', stacked=True, colormap='RdYlGn', edgecolor='black', ax=ax, ecolor='white',)
    ax.set_facecolor('#121212')  # Cambié el color del fondo del gráfico
    fig.set_facecolor('#121212')  # Cambié el color del fondo de la figura
    ax.tick_params(colors='white')  # Cambié el color de las marcas de los ejes


    # Personalizar el gráfico
    plt.title('Cantidad de comentarios en cada categoria según aspecto del comentario', color='white')
    plt.xlabel('Cantidad', color='white')
    plt.ylabel('')
    legend = plt.legend(title='Aspecto', bbox_to_anchor=(1, 1), edgecolor='white', labelcolor='white', facecolor='#121212', title_fontsize='12', loc = 'best')
    legend.get_title().set_color('white')
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)

def graficar_barras_apiladas_seccion(df):
    # Agrupar y contar el número de observaciones para cada combinación de 'topico' y 'tipo'
    grouped_df = df.groupby(['seccion', 'topico']).size().unstack()
    #ordenar por total
    grouped_df = grouped_df.sort_values(by=['seccion'], ascending=False)
    # Crear el gráfico de barras horizontales apiladas
    fig, ax = plt.subplots(figsize=(12, 8))
    grouped_df.plot(kind='barh', stacked=True, colormap='RdYlGn', edgecolor='black', ax=ax, ecolor='white',)
    ax.set_facecolor('#121212')  # Cambié el color del fondo del gráfico
    fig.set_facecolor('#121212')  # Cambié el color del fondo de la figura
    ax.tick_params(colors='white')  # Cambié el color de las marcas de los ejes


    # Personalizar el gráfico
    plt.title('Cantidad de comentarios en cada categoria según seccion', color='white')
    plt.xlabel('Cantidad', color='white')
    plt.ylabel('')
    legend = plt.legend(title='Categoria', bbox_to_anchor=(1, 1), edgecolor='white', labelcolor='white', facecolor='#121212', title_fontsize='12', loc = 'best')
    legend.get_title().set_color('white')
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)

def graficar_barras_apiladas_curso(df):
    # Agrupar y contar el número de observaciones para cada combinación de 'topico' y 'tipo'
    grouped_df = df.groupby(['nombre_curso', 'topico']).size().unstack()
    #ordenar por total
    grouped_df['total'] = grouped_df.sum(axis=1)
    grouped_df = grouped_df.sort_values(by=['total'], ascending=True)
    grouped_df = grouped_df.drop(['total'], axis=1)
    # Crear el gráfico de barras horizontales apiladas
    fig, ax = plt.subplots(figsize=(12, 8))
    grouped_df.plot(kind='barh', stacked=True, colormap='RdYlGn', edgecolor='black', ax=ax, ecolor='white',)
    ax.set_facecolor('#121212')  # Cambié el color del fondo del gráfico
    fig.set_facecolor('#121212')  # Cambié el color del fondo de la figura
    ax.tick_params(colors='white')  # Cambié el color de las marcas de los ejes


    # Personalizar el gráfico
    plt.title('Cantidad de comentarios en cada categoria según curso', color='white')
    plt.xlabel('Cantidad', color='white')
    plt.ylabel('')
    legend = plt.legend(title='Categoria', bbox_to_anchor=(1, 1), edgecolor='white', labelcolor='white', facecolor='#121212', title_fontsize='12', loc = 'best')
    legend.get_title().set_color('white')
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)

def graficar_categorias(df_positivos, df_negativos):
    # Configurar el gráfico inicial
    df_negativos = df_negativos[['comentario', 'topico', 'tipo']]
    df_positivos = df_positivos[['comentario', 'topico', 'tipo']]
    df_negativos = df_negativos.dropna()
    df_positivos = df_positivos.dropna()

    # Crear subplots con 2 filas (una para cada tipo)
    fig, axes = plt.subplots(ncols=2, figsize=(15, 10))
    fig.set_facecolor('#121212')  # Establece el fondo a un gris muy oscuro
    # Cambiando de barh a pie
    pie_tipo_1 = axes[0].pie(df_positivos['topico'].value_counts(), 
                                 #labels=df_positivos['topic'].unique(), 
                                 autopct='%1.1f%%',
                                 radius=1,
                                 textprops={'fontsize': 9, 'color': 'white', 'fontweight': 'bold'},
                                 colors=plt.cm.Greens(np.linspace(0, 1, 5)),
                                 wedgeprops={'linewidth': 3, 'edgecolor': '#121212'},
                                 pctdistance=1.2)
                                 #)
    axes[0].legend(df_positivos['topico'].unique(), 
                      loc='best', bbox_to_anchor=(1.05, 1), fontsize=15, facecolor='#141414', edgecolor='#121212'
                      , title_fontsize=15, labelcolor='white')
  

    # Segundo subplot para tipo == 0
    pie_tipo_0 = axes[1].pie(df_negativos['topico'].value_counts(), 
                                #labels=df_negativos['topic'].unique(), 
                                autopct='%1.1f%%',
                                radius=1,
                                textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'bold',
                                },
                                colors=plt.cm.Reds(np.linspace(0, 1, 5)),
                                wedgeprops={'linewidth': 3, 'edgecolor': '#121212'},
                                pctdistance=1.2)
    axes[1].legend(df_negativos['topico'].unique(), 
                      loc='best', bbox_to_anchor=(1.05, 1), fontsize=15, facecolor='#141414', edgecolor='#121212',
                      title_fontsize=15, labelcolor='white', 
                      )
    # Ajusta la disposición para evitar solapamiento
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)


  