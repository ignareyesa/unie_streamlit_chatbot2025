import streamlit as st
import pandas as pd
import google.generativeai as genai

#key = "AIzaSyC8i3T8-kptAh_LWLXtt85_LNCjvVCEzco"


# Configuración de API
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")
    "[Consigue tu API Key de Gemini](https://makersuite.google.com/app/apikey)"
    "[Documentación de Gemini](https://ai.google.dev/)"

# Título
st.title("💬 Chatbot con Gemini")
st.caption("🚀 Un chatbot usando Gemini (Google Generative AI)")
#
# Inicializa historial si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

## Mostrar historial
for msg in st.session_state.messages:
    st.chat_message(msg["role"],avatar = msg["avatar"]).write(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    if not gemini_api_key:
        st.info("Por favor, ingresa tu clave de API de Gemini.")
        st.stop()

    # Mostrar y guardar el mensaje del usuario
    st.chat_message("user",avatar = "🦖").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt,"avatar":"🦖"})

    # Configurar Gemini
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Convertir historial a formato válido para Gemini
    history = [
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in st.session_state.messages
    ]
    
    # Iniciar el chat con historial
    chat = model.start_chat(history=history)
    

    # Obtener respuesta
    response = chat.send_message(prompt)
    reply = response.text

    # Mostrar y guardar respuesta
    st.chat_message("assistant", avatar="🧑‍💻").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply,"avatar":"🧑‍💻"})


