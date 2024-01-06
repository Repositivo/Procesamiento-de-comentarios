from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import streamlit as st
import tensorflow as tf

#path_model_neg = "./Artifacts/Modelos/negative_model-20231231T214220Z-001/negative_model/"
#path_model_pos = "./Artifacts/Modelos/positivo_model-20231231T214212Z-001/positivo_model/"

try:
    # funcion para cargar modelos
    @st.cache_resource(show_spinner='Cargando modelos...')
    def cargar_modelos():
        """
        Esta función permite cargar los modelos y los tokenizadores

        """
        model_neg = TFAutoModelForSequenceClassification.from_pretrained('crisU8/negative_model')
        tokenizer_neg = AutoTokenizer.from_pretrained('crisU8/negative_model')

        model_pos = TFAutoModelForSequenceClassification.from_pretrained('crisU8/positivo_model')
        tokenizer_pos = AutoTokenizer.from_pretrained('crisU8/positivo_model')

        return model_neg, tokenizer_neg, model_pos, tokenizer_pos
    
    ## llama a la función para cargar los modelos

    model_neg, tokenizer_neg, model_pos, tokenizer_pos = cargar_modelos()
    print("Modelos cargados correctamente")

except:
    ## Error en la carga de modelos
    st.error("Error en la carga de modelos")


## Funciones de clasificación

st.cache(show_spinner=False)
def Clasificador(model, tokenizer, text, max_length=512):
    """
    Esta función permite clasificar un texto o una lista de textos

    Args:
    - model: El modelo de clasificación
    - tokenizer: El tokenizer asociado al modelo
    - max_length: La longitud máxima de los textos
    - text: El texto o la lista de textos a clasificar

    Returns:
    - preds: Lista de predicciones para cada texto
    """
    if isinstance(text, str):
        text = [text]

    inputs = tokenizer(text, padding=True, truncation=True, max_length=max_length, return_tensors="tf")
    outputs = model.predict([inputs['input_ids'], inputs['attention_mask'], inputs['token_type_ids']], batch_size=100)
    probs = tf.nn.softmax(outputs.logits, axis=-1)
    preds = tf.math.argmax(probs, axis=-1)
    preds = [model.config.id2label[pred] for pred in preds.numpy()]

    return preds
            