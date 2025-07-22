import streamlit as st
from frontend.menu import mostrar_menu
from frontend.header import mostrar_titulo_dinamico
from frontend import web_forms_consolidado
from backend.data_loader.perfil import load_saved_value, show_selection


st.set_page_config(page_title="Dashboard Prisa", layout="wide")
# Mostrar título con estilos
# Mostrar el menú lateral
load_saved_value()
opcion = mostrar_menu()
# Mostrar el título dinámico según la opción
mostrar_titulo_dinamico(opcion)

 #Cargar la vista correspondiente
if opcion == "Consolidado":
    web_forms_consolidado.consolidado_web()
elif opcion == "Reports Directas":
    reports.mostrar()
elif opcion == "Tools":
    tools.mostrar()
elif opcion == "Settings":
    settings.mostrar()
else:
    st.warning("Opción no reconocida.")