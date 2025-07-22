import streamlit as st
import time
from frontend.estilos import aplicar_estilos_globales, boton_personalizado, boton_personalizado_con_funcion
from backend.data_loader.perfil import load_saved_value, show_selection
from config import DATAFRAME_PATHS
import os
import logging
import pandas as pd
from backend.script_consolidado import Run_Consolidated,conect_sheets,read_paths, ias, gam, xandr, tap, adbook, dcm, dv, ttd, searh_verificadores, joindata, search_adbookID, package_function, add_placement, Exeptions_function, merge_function, Cloud_Update


def consolidado_web():
     # --- estilos y variables ---
    aplicar_estilos_globales() 
    df = DATAFRAME_PATHS()
    looker_value = st.session_state.get("looker_consolidado")
    value_url_looker=show_selection(looker_value) 
    
    # Contenedor para mensajes y barra de progreso
    msg_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    def messages(mensaje, paso, total_pasos):
        msg_placeholder.info(f"🔄 {mensaje}")
        progreso = int((paso / total_pasos) * 100)
        progress_bar.progress(progreso)
        
    def ejecutar_paso(nombre, paso, total_pasos, funcion):
        try:
            messages(f"{nombre}", paso, total_pasos)
            funcion()
            time.sleep(1)
        except Exception as e:
            raise Exception(f"❌ Error en {nombre}: {e}")        
    
            
    def funcion_main():
        total_pasos = 20
        try:
            messages("Iniciando proceso...", 1, total_pasos)
            time.sleep(1)

            ejecutar_paso("Conectando Google Sheets...", 2, total_pasos, conect_sheets)
            messages("Cargando Files...", 3, total_pasos)
            time.sleep(1)

            ejecutar_paso("⏳Cargando IAS...", 4, total_pasos, ias)
            ejecutar_paso("⏳Cargando Gam...", 5, total_pasos, gam)
            ejecutar_paso("⏳Cargando Xandr...", 6, total_pasos, xandr)
            ejecutar_paso("⏳Cargando Tap...", 7, total_pasos, tap)
            ejecutar_paso("⏳Cargando Adbook...", 8, total_pasos, adbook)
            ejecutar_paso("⏳Cargando DCM...", 9, total_pasos, dcm)
            ejecutar_paso("⏳Cargando DV...", 10, total_pasos, dv)
            ejecutar_paso("⏳Cargando TTD...", 11, total_pasos, ttd)
            ejecutar_paso("🔍 Ejecutando Search Verificadores...", 12, total_pasos, searh_verificadores)
            ejecutar_paso("🔗 Join Dataframes...", 13, total_pasos, joindata)
            ejecutar_paso("🔍 Seach AdbookID...", 14, total_pasos, search_adbookID)
            ejecutar_paso("📦 Packages...", 15, total_pasos, package_function)
            ejecutar_paso("🧩 Function Placement...", 16, total_pasos, add_placement)
            ejecutar_paso("💥 Exeptions DCM...", 17, total_pasos, Exeptions_function)
            ejecutar_paso("🔗 Merge...", 18, total_pasos, merge_function)
            ejecutar_paso("☁️ Actualizando informes en la nube...", 19, total_pasos, lambda: Cloud_Update(c_daily, c_monthly, c_package))

            messages("Finalizando...", 20, total_pasos)
            time.sleep(1)

            msg_placeholder.success("✅ ¡Proceso completado!")
            progress_bar.progress(100)

        except Exception as e:
            msg_placeholder.error(f"❌ Se produjo un error: {str(e)}")
            progress_bar.empty()        
        
    
        
    col1, col2, col3 = st.columns(3)
    with col1:
        c_daily = st.checkbox("🔁 Daily" , value=True)
    with col2:
        c_monthly = st.checkbox("✅ Monthly", value=True)
    with col3:
        c_package = st.checkbox("🎨 Package", value=True)

    st.markdown("---")

    # --- Botones usando la función personalizada ---
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        boton_procesar = boton_personalizado_con_funcion("🟢 Ejecutar", funcion_main, "#2E86C1", key="btn2")
    with col_btn2:
        boton_detener = boton_personalizado("🛑 Detenar", "#ff022a", key="btn3")
    with col_btn3:        
        btn_looker = boton_personalizado("📥 Ir a looker", f"{value_url_looker}", "#2E86C1", key="btn1")


    st.markdown("---")
   
    
