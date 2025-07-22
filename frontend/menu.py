import streamlit as st
from streamlit_option_menu import option_menu
from backend.data_loader.perfil import  show_selection



def mostrar_menu():
    with st.sidebar:
        profile= st.session_state.get("profile")
        value_profile = show_selection(profile)        
        st.sidebar.image("frontend/assets/Img/logo.png", use_container_width=True)
        
        seleccion = option_menu(
            menu_title=f"{value_profile}",  # Título opcional
            options=["Consolidado", "PMPs", "Tools", "Settings"],
            icons=["bar-chart", "file-earmark-text", "tools", "gear"],  # Íconos de Bootstrap
            menu_icon="cast",  # Ícono general del menú
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#000000"},
                "icon": {"color": "#1f77b4", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#27ae60",
                },
                "nav-link-selected": {
                    "background-color": "#1f77b4",
                    "color": "white",
                },
            }
        )
    return seleccion
