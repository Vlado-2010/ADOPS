import streamlit as st

def aplicar_estilos_globales():
    st.markdown("""
        <style>
        
        /* Estilo general del sidebar */
        [data-testid="stSidebar"] {
            background-color:#37568b; /* azul claro suave */
            padding: 1rem;
        }
       
        </style>
    """, unsafe_allow_html=True)

def boton_personalizado(label, url, color="#2E86C1", key=None):
    html = f"""
        <a href="{url}" target="_blank" style="text-decoration: none;">
        <button style='background-color:{color}; color:white; padding:10px 20px;
        border:none; border-radius:8px; font-size:16px; cursor:pointer;'>
            {label}
        </button>
        </a>
    """
    st.markdown(html, unsafe_allow_html=True)
   #return st.button(" ", key=key)


def boton_personalizado_con_funcion(label, funcion, color="#fff", key=None):
    st.markdown(f"""
        <style>
        div[data-testid="stButton"] > button[{f'data-testid="{key}"' if key else ""}] {{
            background-color: {color};
            color: white;
            padding: 0.5em 1.2em;
            border: none;
            border-radius: 8px;
            font-size:16px;
            padding:10px 20px;
        }}
        </style>
    """, unsafe_allow_html=True)

    if st.button(label, key=key):
        funcion()
