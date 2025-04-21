import pandas as pd
import streamlit as st
import google.generativeai as genai



# Configuración de API
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")
    "[Consigue tu API Key de Gemini](https://makersuite.google.com/app/apikey)"
    "[Documentación de Gemini](https://ai.google.dev/)"

if not gemini_api_key:
        st.info("Por favor, ingresa tu clave de API de Gemini.")
        st.stop()

genai.configure(api_key=gemini_api_key)

# Selección de rol y tono

# Configuración inicial
genai.configure(api_key=st.session_state.get("gemini_api_key", ""))

# Diccionario de avatares por rol
role_avatars = {
    "Mentor de Marketing": "📈",
    "Entrenador Personal": "🏋️",
    "Profesor de Literatura Española": "📚"
}

# Sidebar - selección de personalidad
role = st.sidebar.selectbox("Escoge un rol para el chat", [
    "Mentor de Marketing",
    "Entrenador Personal",
    "Profesor de Literatura Española"
])

tono = st.sidebar.selectbox("Escoge un estilo de escritura", [
    "Enfadado",
    "Triste",
    "Neutro",
    "Formal",
    "Motivado"
])

st.title(f"Agente {role} {tono}")


# Detectar si hubo cambio de personalidad
if (
    st.session_state.get("last_role") != role or
    st.session_state.get("last_tono") != tono or
    "chat" not in st.session_state
):
    # Resetear todo si se cambió algo
    st.session_state.messages = []
    st.session_state.last_role = role
    st.session_state.last_tono = tono

    system_prompt = [
        f"Eres un {role}. Respondes con un tono {tono.lower()}. "
        "Mantén tu estilo durante toda la conversación. Sé consistente."
    ]

    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt)
    st.session_state.model = model
    chat = model.start_chat()
    st.session_state.chat = chat
else:
    # Continuar conversación con historial
    model = st.session_state.model
    chat = model.start_chat(history=[
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in st.session_state.get("messages", [])
    ])
    st.session_state.chat = chat

# Mostrar mensajes anteriores
for msg in st.session_state.get("messages", []):
    st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Mostrar y guardar mensaje del usuario
    st.chat_message("user", avatar="🧑").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "🧑"})

    # Obtener respuesta
    response = chat.send_message(user_input)
    reply = response.text

    # Determinar avatar según rol
    bot_avatar = role_avatars.get(role, "🤖")

    # Mostrar y guardar respuesta
    st.chat_message("assistant", avatar=bot_avatar).write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply, "avatar": bot_avatar})


