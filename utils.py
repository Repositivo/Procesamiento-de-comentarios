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


def graficar_categorias(df_positivos, df_negativos):
    # Configurar el gráfico inicial
    df_negativos = df_negativos[['comentario', 'topic', 'tipo']]
    df_positivos = df_positivos[['comentario', 'topic', 'tipo']]
    df_negativos = df_negativos.dropna()
    df_positivos = df_positivos.dropna()

    # Crear subplots con 2 filas (una para cada tipo)
    fig, axes = plt.subplots(ncols=2, figsize=(15, 10))
    fig.set_facecolor('#121212')  # Establece el fondo a un gris muy oscuro

    # Cambiando de barh a pie
    pie_tipo_1 = axes[0].pie(df_positivos['topic'].value_counts(), 
                                 #labels=df_positivos['topic'].unique(), 
                                 autopct='%1.1f%%',
                                 radius=1,
                                 textprops={'fontsize': 10, 'color': 'black', 'fontweight': 'bold'},
                                 colors=plt.cm.Greens(np.linspace(0, 1, 5)),
                                 wedgeprops={'linewidth': 3, 'edgecolor': '#121212'})
                                 #)
    axes[0].legend(df_positivos['topic'].unique(), 
                      loc='center left', bbox_to_anchor=(1.05, 1), fontsize=15, facecolor='#141414', edgecolor='#121212'
                      , title_fontsize=15, labelcolor='white')
  

    # Segundo subplot para tipo == 0
    pie_tipo_0 = axes[1].pie(df_negativos['topic'].value_counts(), 
                                #labels=df_negativos['topic'].unique(), 
                                autopct='%1.1f%%',
                                radius=1,
                                textprops={'fontsize': 10, 'color': 'black', 'fontweight': 'bold',
                                },
                                colors=plt.cm.Reds(np.linspace(0, 1, 5)),
                                wedgeprops={'linewidth': 3, 'edgecolor': '#121212'})
    axes[1].legend(df_negativos['topic'].unique(), 
                      loc='center left', bbox_to_anchor=(1.05, 1), fontsize=15, facecolor='#141414', edgecolor='#121212',
                      title_fontsize=15, labelcolor='white', 
                      )

    # Ajusta la disposición para evitar solapamiento
    plt.tight_layout()

    # Mostrar la animación
    st.pyplot(fig, use_container_width=True)


  