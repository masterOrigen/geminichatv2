import streamlit as st
from PIL import Image
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import geminai

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API de Gemini IA del archivo .env
GEMINIAI_API_KEY = os.getenv('GEMINIAI_API_KEY')

# Función para hacer preguntas a Gemini IA
def hacer_pregunta(texto):
    respuesta = geminai.ask(texto)
    return respuesta

# Configurar el título de la aplicación
st.title('App de Preguntas con Gemini IA')

# Configurar la barra lateral
st.sidebar.title('Subir Archivos')
archivo = st.sidebar.file_uploader('Subir Archivo', type=['jpg', 'jpeg', 'png', 'mp4', 'csv', 'txt'])

# Mostrar el archivo subido
if archivo is not None:
    st.sidebar.write('Archivo subido exitosamente!')
    st.sidebar.write(f'Tipo de archivo: {archivo.type}')
    st.sidebar.write(f'Tamaño del archivo: {len(archivo.getvalue())} bytes')

    # Mostrar la imagen si es una imagen
    if archivo.type.startswith('image'):
        imagen = Image.open(archivo)
        st.image(imagen, caption='Archivo subido', use_column_width=True)
    # Mostrar el video si es un video
    elif archivo.type.startswith('video'):
        st.video(archivo)
    # Leer el archivo CSV si es un archivo CSV
    elif archivo.type == 'text/csv':
        datos = pd.read_csv(archivo)
        st.write(datos)
    # Leer el texto si es un archivo de texto
    elif archivo.type == 'text/plain':
        texto = str(archivo.read(), 'utf-8')
        st.write(texto)
    # Si es una URL de YouTube, hacer una pregunta sobre el video
    elif archivo.type == 'application/octet-stream':
        url = str(archivo.read(), 'utf-8')
        st.write(f'URL de YouTube: {url}')
        respuesta = hacer_pregunta(f'Análisis de {url}')
        st.write('Respuesta de Gemini IA:')
        st.write(respuesta)
    else:
        st.write('Formato de archivo no compatible')

# Área de texto para hacer preguntas
pregunta = st.text_input('Haz una pregunta sobre el archivo subido')

# Hacer una pregunta si se ha ingresado texto
if st.button('Enviar pregunta'):
    if pregunta:
        respuesta = hacer_pregunta(pregunta)
        st.write('Respuesta de Gemini IA:')
        st.write(respuesta)
    else:
        st.write('Por favor, ingresa una pregunta')
