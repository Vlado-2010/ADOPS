from config import DATAFRAME_PATHS
import os
import pandas as pd
import streamlit as st

df = DATAFRAME_PATHS()
'''url_looker=show_selection(df_value_looker)
file_pas=show_selection(df_value_Pas)
file_pds=show_selection(df_value_Pds)
file_table=show_selection(df_value_Table) '''
          
def load_saved_value():
    
        if os.path.exists('./frontend/assets/perfil.xlsx'):
            saved_df = pd.read_excel('./frontend/assets/perfil.xlsx')
            #st.write("Contenido del perfil.xlsx:", saved_df)  # 👈 Agregado para ver qué trae
        if not saved_df.empty:
            try:
                saved_value_perfil = saved_df['Perfil'].iloc[0]
                st.session_state['profile'] = saved_value_perfil
                
                saved_value = saved_df['Valor Looker'].iloc[0]
                saved_value_Pas = saved_df['Valor Read Pas'].iloc[0]
                saved_value_Pds = saved_df['Valor Read Pds'].iloc[0]
                saved_value_table = saved_df['Valor Table PMPs'].iloc[0]
                saved_value_export_ctr = saved_df['Valor Export CTR'].iloc[0]
                saved_value_export_vw = saved_df['Valor Export VW'].iloc[0]
                saved_value_export_cr = saved_df['Valor Export CR'].iloc[0]
                saved_value_file_ias = saved_df['Path IAS'].iloc[0]
                st.session_state['path_ias'] = saved_value_file_ias
                
                
                saved_value_file_gam = saved_df['Path GAM'].iloc[0]
                saved_value_file_dcm = saved_df['Path DCM'].iloc[0]
                saved_value_file_dv = saved_df['Path DV'].iloc[0]
                saved_value_file_abk = saved_df['Path ABK'].iloc[0]
                saved_value_file_ttd = saved_df['Path TTD'].iloc[0]
                saved_value_file_tap = saved_df['Path TAP'].iloc[0]
                saved_value_looker = saved_df['Valor Looker Consolidado'].iloc[0]
                saved_value_OneDrive_Direct = saved_df['Path OneDrive Directas'].iloc[0]
                saved_value_file_xandr = saved_df['Xandr Path'].iloc[0]
                
                st.session_state['looker_pds'] = saved_value
                st.session_state['file_pas'] = saved_value_Pas
                st.session_state['file_pds'] = saved_value_Pds
                st.session_state['file_table_pds'] = saved_value_table
                st.session_state['file_export_ctr'] = saved_value_export_ctr
                st.session_state['file_export_vw'] = saved_value_export_vw
                st.session_state['file_export_cr'] = saved_value_export_cr
                
                st.session_state['path_gam'] = saved_value_file_gam
                st.session_state['path_dcm'] = saved_value_file_dcm
                st.session_state['path_dv'] = saved_value_file_dv
                st.session_state['path_adbook'] = saved_value_file_abk
                st.session_state['path_ttd'] = saved_value_file_ttd
                st.session_state['path_tap'] = saved_value_file_tap
                st.session_state['path_one_drive'] = saved_value_OneDrive_Direct
                st.session_state['path_xandr'] = saved_value_file_xandr
                st.session_state['looker_consolidado'] = saved_value_looker 
                
                
                st.write("✅ Perfil cargado:")
            except Exception as e:
                st.error(f"❌ Error al cargar perfil: {e}")
                             
        '''if os.path.exists('./frontend/assets/perfil.xlsx'):
            saved_df = pd.read_excel('./frontend/assets/perfil.xlsx')
            if not saved_df.empty:
                saved_value_perfil = saved_df['Perfil'].iloc[0]
                saved_value = saved_df['Valor Looker'].iloc[0]
                saved_value_Pas = saved_df['Valor Read Pas'].iloc[0]
                saved_value_Pds = saved_df['Valor Read Pds'].iloc[0]
                saved_value_table = saved_df['Valor Table PMPs'].iloc[0]
                saved_value_export_ctr = saved_df['Valor Export CTR'].iloc[0]
                saved_value_export_vw = saved_df['Valor Export VW'].iloc[0]
                saved_value_export_cr = saved_df['Valor Export CR'].iloc[0]
                saved_value_file_ias = saved_df['Path IAS'].iloc[0]
                saved_value_file_gam = saved_df['Path GAM'].iloc[0]
                saved_value_file_dcm = saved_df['Path DCM'].iloc[0]
                saved_value_file_dv = saved_df['Path DV'].iloc[0]
                saved_value_file_abk = saved_df['Path ABK'].iloc[0]
                saved_value_file_ttd = saved_df['Path TTD'].iloc[0]
                saved_value_file_tap = saved_df['Path TAP'].iloc[0]
                saved_value_looker = saved_df['Valor Looker Consolidado'].iloc[0]
                saved_value_OneDrive_Direct = saved_df['Path OneDrive Directas'].iloc[0]
                saved_value_file_xandr = saved_df['Xandr Path'].iloc[0]
                
                #Values
                st.session_state['profile'] = saved_value_perfil
                st.session_state['looker_pds'] = saved_value
                st.session_state['file_pas'] = saved_value_Pas
                st.session_state['file_pds'] = saved_value_Pds
                st.session_state['file_table_pds'] = saved_value_table
                st.session_state['file_export_ctr'] = saved_value_export_ctr
                st.session_state['file_export_vw'] = saved_value_export_vw
                st.session_state['file_export_cr'] = saved_value_export_cr
                st.session_state['path_ias'] = saved_value_file_ias
                st.session_state['path_gam'] = saved_value_file_gam
                st.session_state['path_dcm'] = saved_value_file_dcm
                st.session_state['path_dv'] = saved_value_file_dv
                st.session_state['path_adbook'] = saved_value_file_abk
                st.session_state['path_ttd'] = saved_value_file_ttd
                st.session_state['path_tap'] = saved_value_file_tap
                st.session_state['path_one_drive'] = saved_value_OneDrive_Direct
                st.session_state['path_xandr'] = saved_value_file_xandr
                st.session_state['looker_consolidado'] = saved_value_looker '''              
                
                #show_selection()        

def show_selection(df_value):
        # Obtener el valor seleccionado del Combobox
        selected_value = df_value
        if selected_value:
            # Obtener la fila correspondiente al valor seleccionado
            selected_row = df[df['Path_Name'] == selected_value]
            if not selected_row.empty:
            # Mostrar el valor seleccionado en el label
                return selected_row.iloc[0, 1]

load_saved_value()
