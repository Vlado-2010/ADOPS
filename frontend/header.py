import streamlit as st

def mostrar_titulo_dinamico(opcion_menu):
    titulos = {
        "Consolidado": "📊 Report Consolidado ",
        "PMPs": "📄PMPs",
        "Tools": "🧰 Herramientas del Sistema",
        "Settings": "⚙️ Configuración"
    }

    titulo = titulos.get(opcion_menu, "Dashboard Prisa")

    st.markdown(f"""
        <h1 style='text-align: center; color: #1f77b4; font-size: 38px; margin-bottom: 20px;'>
            {titulo}
        </h1>
    """, unsafe_allow_html=True)
