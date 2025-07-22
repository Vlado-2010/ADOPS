import pandas as pd
import streamlit as st
from config import JSON
import gspread
import glob
import os
from oauth2client.service_account import ServiceAccountCredentials
from backend.data_loader.perfil import show_selection
import datetime
import numpy as np




def Consolidate():
    st.write("Hola")

#-----------------Exeptions-------------------------------------------------------------------------------------------------
def run_data_manipulation_gam(df):
                                try:
                                        with open('./frontend/assets/Exception_gam.py', 'r') as file:
                                                code = file.read()
                                                # Ejecuta el código del archivo manipulate_data.py en el contexto actual
                                                exec(code, {'df_gam': df})

                                        # Mostrar algunos resultados en el ScrolledText
                                        st.success("Exeptions Gam ok..")
                                except Exception as e:
                                        st.error(e)

def run_data_manipulation_Adbook(df):
                                try:
                                        with open('./frontend/assets/Exception_Adbook.py', 'r') as file:
                                                code = file.read()
                                                # Ejecuta el código del archivo manipulate_data.py en el contexto actual
                                                exec(code, {'df_adbook': df})

                                        # Mostrar algunos resultados en el ScrolledText
                                     
                                        st.success("Exeptions Adbook ok..")
                                except Exception as e:
                                        st.error(e)

def run_data_manipulation_ttd(df):
                                try:
                                        with open('./frontend/assets/Exception_ttd.py', 'r') as file:
                                                code = file.read()
                                                # Ejecuta el código del archivo manipulate_data.py en el contexto actual
                                                exec(code, {'df_ttd': df})

                                        # Mostrar algunos resultados en el ScrolledText
                                        st.success("Exeptions TTD ok..")
                                except Exception as e:
                                        st.error(e)
                                        
def run_data_manipulation_dcm(df_join_dcm,df_join_ias,df_join_dv):
                                try:
                                        with open('./frontend/assets/Exception_dcm.py', 'r') as file:
                                                code = file.read()
                                                # Ejecuta el código del archivo manipulate_data.py en el contexto actual
                                                exec(code, {'df_join_dcm': df_join_dcm,'df_join_ias':df_join_ias ,'df_join_dv':df_join_dv})

                                        # Mostrar algunos resultados en el ScrolledText
                                        st.success("Exeptions DCM ok..")
                                        
                                except Exception as e:
                                        st.error(e)                                        
#--------------------------------------------------------------------------------------------------------------------------------


def Run_Consolidated(check_daily,check_monthly,check_package):
        st.write(check_daily)
        st.write(check_monthly)
        st.write(check_package)
        
        #consolidado_web.messages("Ejecutando Funcion Run..")
def conect_sheets():
    from oauth2client.service_account import ServiceAccountCredentials
    scope=['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

    # Cargar desde st.secrets
    creds_dict = st.secrets["gcp_service_account"]
    #local
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON,scope)
    #Streamlit
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_dict,scope)
    client = gspread.authorize(credentials)
    sheet_Date = client.open("Data_Client_Date_2025_1").sheet1
    sheet_Month = client.open("Data_Client_Month_2025_1").sheet1
    sheet_Month_package = client.open("Data_Client_Month_Package").sheet1
    st.success("Google sheets ok...")
    st.markdown("---")
    
def read_paths():
    ias_value = st.session_state.get("path_ias")
    value_ias =show_selection(ias_value) 
    gam_value = st.session_state.get("path_gam")
    value_gam =show_selection(gam_value)
    dcm_value = st.session_state.get("path_dcm")
    value_dcm =show_selection(dcm_value)
    dv_value = st.session_state.get("path_dv")
    value_dv =show_selection(dv_value)
    adbook_value = st.session_state.get("path_adbook")
    value_adbook =show_selection(adbook_value)
    tap_value = st.session_state.get("path_tap")
    value_tap =show_selection(tap_value)
    ttd_value = st.session_state.get("path_ttd")
    value_ttd =show_selection(ttd_value)
    xndr_value = st.session_state.get("path_xandr")
    value_xndr =show_selection(xndr_value)
    
    xlsx_files_ias= glob.glob(value_ias + "*.xlsx")#IAS
    xls_files_gam= value_gam + "Consolidado GAM.xlsx"#GAM
    csv_files_dcm= glob.glob(value_dcm+"*.csv")#DCM
    dv_files= glob.glob(value_dv+"*.csv")#DV
    adbook_files= value_adbook+"Adbook.csv"#Adbook
    tap =value_tap+"tap.csv"#TAP
    ttd = value_ttd+"TTD.xlsx"#TTD
    xandr = value_xndr+"Xandr.xlsx"#Xandr

    
    return xlsx_files_ias, xls_files_gam,csv_files_dcm,dv_files, adbook_files, tap, ttd, xandr
   
        
def ias():
    st.write("Modulo IAS..")
    try:
        path_ias,_,_,_,_,_,_,_ = read_paths()    

        xlsx_list=[]
        for f in path_ias:
                data =  pd.read_excel(f, sheet_name="Performance Report", header=2)
                #print(data)
                nombre = os.path.basename(f)
                data["source_file"] = nombre
                data= data.iloc[:-2 , :]
                #print(data)
                xlsx_list.append(data)

        df_ias= pd.concat(xlsx_list, ignore_index=True)
        df_ias["Partner Cost (USD)"]=0
        df_ias["Date"] = pd.to_datetime(df_ias["Date"])
        df_ias["Date"] = df_ias["Date"].dt.strftime('%Y-%m-%d')
        df_ias.rename({"Ad Server Placement Id":"Placement ID"},axis=1,inplace=True)
        df_data_ias=df_ias[["Partner Cost (USD)","Campaign Id","Campaign","Placement ID","Placement","Date","Eligible Ads For Viewability Measurement","Measured Ads","Viewable Impressions","Eligible Ads For Invalid Traffic Detection","Invalid Traffic","Total Eligible Ads For Brand Safety","Passed Ads","Total Tracked Ads","Failed Ads"]]
        df_ias["Placement ID"].fillna(11111111, inplace= True)
        df_ias["Placement ID"]= df_ias["Placement ID"].astype(int)
        
        st.session_state["df_ias"] = df_ias
        st.session_state["df_data_ias"] = df_data_ias

        #df_data_ias.to_excel("prisa/consolidado/consolidado_IAS.xlsx")
        #df_ias.to_excel("C:/Users/vbautista\OneDrive - Grupo PRISA\Documents\Trafico\Seguimientos diarios\Seguimientos 23\campañas directas/IAS/data/consolidadoIAS.xlsx")
        st.success("IAS ok...")    
    except Exception as e:
             raise Exception(f"Error en IAS: {e}")
def gam():
    st.write("Modulo GAM")
    try:
        _,path_gam,_,_,_,_,_,_ = read_paths()
        df_gam =  pd.read_excel(path_gam,sheet_name="Report data")
                            #print(df_gam)
        df_gam= df_gam.iloc[:-1 , :]
        df_gam["Date"] = pd.to_datetime(df_gam["Date"])
        df_gam["Date"] = df_gam["Date"].dt.strftime('%Y-%m-%d')
        df_gam["Adbook ID"] = (df_gam["Order"]).str.slice(0,6)
        df_gam["Drop ID"] = (df_gam["Line item"]).str.slice(0,8)
        df_gam["Partner Cost (USD)"]=0
        df_gam["server"]="Gam"       
        run_data_manipulation_gam(df_gam)
        st.session_state["df_gam"] = df_gam

    except Exception as e:
        st.error(e)

def xandr():
    st.write("Modulo Xandr")
    try:
        _,_,_,_,_,_,_,path_xandr = read_paths()    
        
        df_xandr =  pd.read_excel(path_xandr,sheet_name="Report Data")
        df_xandr.rename({"day":"Date"},axis=1,inplace=True)
        df_xandr.rename({"advertiser":"Order"},axis=1,inplace=True)
        df_xandr.rename({"imps":"Xandr Imps"},axis=1,inplace=True)
        df_xandr.rename({"clicks":"Xandr Clicks"},axis=1,inplace=True)
        df_xandr.rename({"insertion_order":"Line item"},axis=1,inplace=True) 
        df_xandr.rename({"billing_period.start_date":"Start Date"},axis=1,inplace=True) 
        df_xandr.rename({"billing_period.end_date":"End Date"},axis=1,inplace=True) 
        df_xandr.rename({"total_cost":"Partner Cost (USD)"},axis=1,inplace=True)                        
        df_xandr.rename({"video_starts":"Video Plays"},axis=1,inplace=True)                        
        df_xandr.rename({"video_completions":"Video Completions"},axis=1,inplace=True)                        
        df_xandr.rename({"creative":"Creative"},axis=1,inplace=True)                        

        df_xandr["Adbook ID"] = (df_xandr["Order"]).str.slice(0,6)
        df_xandr["Drop ID"] = (df_xandr["Line item"]).str.slice(0,8)
        df_xandr["server"]="Xandr"                        

        df_xandr["Date"] = pd.to_datetime(df_xandr["Date"])
        df_xandr["Date"] = df_xandr["Date"].dt.strftime('%Y-%m-%d')
        df_xandr["Start Date"] = pd.to_datetime(df_xandr["Start Date"])
        df_xandr["Start Date"] = df_xandr["Start Date"].dt.strftime('%Y-%m-%d')
        df_xandr["End Date"] = pd.to_datetime(df_xandr["End Date"])
        df_xandr["End Date"] = df_xandr["End Date"].dt.strftime('%Y-%m-%d')

        df_xandr = df_xandr[["Date","Order","Line item","Creative","Xandr Imps","Xandr Clicks","Partner Cost (USD)","server","Adbook ID","Drop ID","Video Plays","Video Completions"]]
        st.success("Xandr ok...") 
        #df_xandr.to_excel("C:/Users/vbautista/Documents/Xandr_Prisa.xlsx")
        st.session_state["df_xandr"] = df_xandr

    except Exception as e:
             raise Exception(f"Error en Xandr: {e}")
def tap():
    st.write("Modulo TAP")
    try:
        _,_,_,_,_,path_tap,_,_ = read_paths()    
        
        df_tap = pd.read_csv(path_tap)
        df_tap["Date"] = pd.to_datetime(df_tap["Date"])
        df_tap["Date"] = df_tap["Date"].dt.strftime('%Y-%m-%d')
        df_tap.rename({"Campaign Name":"Order"},axis=1,inplace=True)
        df_tap.rename({"Impressions":"Ad server impressions"},axis=1,inplace=True)
        df_tap.rename({"Flight Name":"Line item"},axis=1,inplace=True)
        df_tap["Adbook ID"] = (df_tap["Order"]).str.slice(0,6)
        df_tap["Drop ID"] = (df_tap["Line item"]).str.slice(0,8)
        df_tap["Creative"] = df_tap["Line item"]
        df_tap["Partner Cost (USD)"]=0                        
        df_tap["server"]="Tap"
        #Elimina campaña de promo
        df_tap = df_tap[df_tap["Order"] !="Lt.Team_Latam_El Pais_Master de Periodismo_Promo_0305_25"]                     
        st.success("Tap ok...")
        st.session_state["df_tap"] = df_tap

    except Exception as e:
             raise Exception(f"Error en Tap: {e}")

def adbook():
    st.write("Modulo Adbook")
    try:
        _,_,_,_,path_adbook,_,_,_ = read_paths()    

        df_adbook = pd.read_csv(path_adbook, encoding='ISO-8859-1')
        df_adbook.rename({"Campaign ID":"Adbook ID"},axis=1,inplace=True)
        df_adbook["Adbook ID"]= df_adbook["Adbook ID"].astype(str)
        df_adbook["Drop ID"]= df_adbook["Drop ID"].astype(str)
        df_adbook["Package Drop ID"] = df_adbook["Package Drop ID"].astype('Int64')
        df_adbook["Package Drop ID"] = df_adbook["Package Drop ID"].astype(str)
        df_adbook["Start Date"] = pd.to_datetime(df_adbook["Start Date"], format = '%m/%d/%Y').dt.strftime('%m/%d/%Y')
        df_adbook["End Date"] = pd.to_datetime(df_adbook["End Date"], format = '%m/%d/%Y')
        df_adbook["Start Date"]= pd.to_datetime(df_adbook["Start Date"], format = '%m/%d/%Y')
        df_adbook["End Date"]= pd.to_datetime(df_adbook["End Date"],format='ISO8601')
        
        #Forzar Sales Person
        run_data_manipulation_Adbook(df_adbook)
        
        #Elimina Duplicados
        df_adbook = df_adbook.drop_duplicates(["Adbook ID", "Drop ID", "Sales Rep","Package Position ID"])
        #asigna Package Adbook
        def assign_drop(row,drop):
                if row =='<NA>':    
                        result = drop
                else:
                        result= row
                return result
        df_adbook['Package ID'] = df_adbook.apply(lambda x: assign_drop(x['Package Drop ID'], x['Drop ID']),axis=1,result_type='expand')#df_adbook[df_adbook['Package Drop ID','Drop ID']].apply(assign_letter)

        def position_name(position, path):
                if position=="VARIOUS TRADITIONAL":
                        result= path
                else:
                        result = position
                return result     
        df_adbook["Position Name"] = df_adbook.apply(lambda x:position_name(x['Position'], x['Path 4']),axis=1, result_type='expand')

        #suma Imps Sold
        data_package = df_adbook.groupby("Package ID").agg(df_adbook=("Impressions Sold", 'sum'))
        df_adbook=pd.merge(df_adbook, data_package, on=('Package ID'), how='outer')
        df_adbook.rename({"df_adbook":"Package Imps Sold"},axis=1,inplace=True)
        
        #hoy
        hoy= datetime.datetime.now()
        hoy = hoy.strftime('%Y-%m-%d')
        df_adbook["Hoy"]= hoy
        print(df_adbook["Hoy"])
        df_adbook["Hoy"] = pd.to_datetime(df_adbook["Hoy"])
        df_adbook['diasHoy'] =  (df_adbook["Hoy"] - df_adbook['Start Date']).dt.days
        df_adbook['dias'] =  (df_adbook['End Date'] - df_adbook['Start Date']).dt.days
        #
        df_adbook['diasx'] =  (df_adbook['End Date'] - df_adbook['Hoy']).dt.days
        df_adbook["End Date"] = df_adbook["End Date"].dt.strftime('%Y-%m-%d')
        df_adbook["Start Date"] = df_adbook["Start Date"].dt.strftime('%Y-%m-%d')
        df_adbook.loc[(df_adbook["diasx"]<0) ,"diasHoy"]=0
        print("****", df_adbook['diasx'])
        
        #df_adbook.to_excel("C:/Users/vbautista/Documents/dataAdbook.xlsx")
        
        df_adbook.loc[(df_adbook["Position Name"]=="DISPLAY O&O") | (df_adbook["Position Name"]=="DISPLAY NETWORK"),"Position Name"]="DISPLAY"
        df_adbook.loc[(df_adbook["Position Name"]=="AUDIO STREAMING AND PODCAST SPOT") ,"Position Name"]="AUDIO"
        df_adbook.loc[(df_adbook["Position Name"]=="CTV/OTT PREROLL VIDEO") ,"Position Name"]="CTV"
        df_adbook.loc[(df_adbook["Position Name"]=="Video") ,"Position Name"]="PREROLL VIDEO"
        
        #elimina
        df_adbook.drop(['Hoy'], axis=1, inplace=True)
        df_adbook.drop(['diasx'], axis=1, inplace=True)
        df_adbook.drop(['*Other Impressions'], axis=1, inplace=True)
        df_adbook.drop(['Position Path'], axis=1, inplace=True)
        df_adbook.drop(['Path 1'], axis=1, inplace=True)
        df_adbook.drop(['Path 2'], axis=1, inplace=True)
        df_adbook.drop(['Path 3'], axis=1, inplace=True)
        df_adbook.drop(['Path 4'], axis=1, inplace=True)
        df_adbook.drop(['Path 5'], axis=1, inplace=True)
        df_adbook.drop(['Package Drop ID'], axis=1, inplace=True)
        #copy dataframe for report beta
        df_adbook_package = df_adbook.copy()
        df_adbook.drop(['Third Party Impressions FTD'], axis=1, inplace=True)
        df_adbook.drop(['Third Party Percent Delivered FTD'], axis=1, inplace=True)
        
        st.session_state["df_adbook"] = df_adbook
        st.session_state["df_adbook_package"] = df_adbook_package


        print(df_adbook.dtypes)
        print(df_adbook_package.dtypes)
    except Exception as e:
             raise Exception(f"Error en Adbook: {e}")

def dcm():
    st.write("Modulo DCM")
    try:
        _,_,path_dcm,_,_,_,_,_ = read_paths()
        csv_list=[]
        for f in path_dcm:
                data =  pd.read_csv(f)#, header=8)
                nombre = os.path.basename(f)
                data["source_file"] = nombre
                data= data.iloc[:-1 , :]
                csv_list.append(data)
        #print(csv_list)

        df_csv= pd.concat(csv_list,ignore_index=True)
        #df_csv.to_excel("C:/Users/vbautista/Documents/consolidadoDCM_test.xlsx")

        df_csv["Date"] = pd.to_datetime(df_csv["Date"])
        df_csv["Date"] = df_csv["Date"].dt.strftime('%Y-%m-%d')
        df_csv.rename({"Impressions":"Impressions DCM"},axis=1,inplace=True)
        df_csv.rename({"Clicks":"Clicks DCM"},axis=1,inplace=True)
        df_csv["Partner Cost (USD)"]=0
        df_csv["Video Plays"].fillna(0, inplace=True)
        df_csv["Video Completions"].fillna(0, inplace=True)
        df_csv.loc[(df_csv["source_file"].str.contains("Innovid")) ,"Video Plays"]=df_csv["Impressions DCM"]
        df_csv.loc[(df_csv["source_file"].str.contains("Innovid")) ,"Video Completions"]=df_csv["video completion 100%"]
        #df_csv.to_excel("C:/Users/vbautista/Documents/dataDCM.xlsx")
        st.session_state["df_dcm"] = df_csv
        st.success("DCM ok...")
    except Exception as e:
             raise Exception(f"Error en DCM: {e}")
    
def dv():
    st.write("Modulo DV")
    try:
        _,_,_,path_dv,_,_,_,_ = read_paths()
        csv_list_dv=[]
        for f in path_dv:
                data =  pd.read_csv(f)
                nombre = os.path.basename(f)
                data["source_file"] = nombre
                data= data.iloc[:-1 , :]
                csv_list_dv.append(data)
        #print(csv_list)

        df_dv= pd.concat(csv_list_dv,ignore_index=True)
        #------------------
        #df_dv = pd.read_csv(dv)
        df_dv.rename({"Campaign Name":"Campaign"},axis=1,inplace=True)
        df_dv.rename({"Placement Name":"Placement"},axis=1,inplace=True)
        df_dv.rename({"Ad Server Placement Code":"Placement ID"},axis=1,inplace=True)
        df_dv["Eligible Ads For Invalid Traffic Detection"] = df_dv["Monitored Ads"]
        df_dv["Total Eligible Ads For Brand Safety"] = df_dv["Monitored Ads"]
        #IVT
        df_dv.rename({"Fraud/SIVT Incidents":"Invalid Traffic"},axis=1,inplace=True)
        #BS
        df_dv.rename({"Brand Suitable Ads":"Passed Ads"},axis=1,inplace=True)
        #VW
        df_dv.rename({"Measured Impressions":"Eligible Ads For Viewability Measurement"},axis=1,inplace=True)


        df_dv["Date"] = pd.to_datetime(df_dv["Date"])
        df_dv["Date"] = df_dv["Date"].dt.strftime('%Y-%m-%d')
        df_dv["Placement ID"].fillna(11111111, inplace= True)
        df_dv["Placement ID"]= df_dv["Placement ID"].astype(int)
        df_dv["Partner Cost (USD)"]=0

        #df_dv.to_excel("Prisa/consolidado_DV.xlsx")
        st.session_state["df_dv"] = df_dv

        st.success("DV ok...")        
        
    except Exception as e:
             raise Exception(f"Error en DV: {e}")

def ttd():
    st.write("Modulo TTD")
    
    try:
        _,_,_,_,_,_,path_ttd,_ = read_paths()
        df_ttd = pd.read_excel(path_ttd, sheet_name="test_data")

        df_ttd.rename({"Impressions":"Impressions TTD"},axis=1,inplace=True)
        df_ttd.rename({"Clicks":"Clicks TTD"},axis=1,inplace=True)

        df_ttd["Date"] = pd.to_datetime(df_ttd["Date"])
        df_ttd["Date"] = df_ttd["Date"].dt.strftime('%Y-%m-%d')
        df_ttd["Creative"].fillna("N/A", inplace= True)
        df_ttd["Adbook ID"] = (df_ttd["Advertiser"]).str.slice(0,6)
        df_ttd["Drop ID"] = (df_ttd["Campaign"]).str.slice(0,8)
        df_ttd["server"]="TTD"                        

        #Forzar Amgen
        run_data_manipulation_ttd(df_ttd)

        #remane
        df_ttd.rename({"Advertiser":"Order"},axis=1,inplace=True)
        df_ttd.rename({"Campaign":"Line item"},axis=1,inplace=True)

        filter_imps = df_ttd["Impressions TTD"]!=0
        df_ttd=df_ttd[filter_imps]
        print(df_ttd)

        #df_ttd.to_excel("C:/Users/vbautista/Documents/dataTTD.xlsx")
        st.session_state["df_ttd"] = df_ttd
        st.success("TTD ok...")  
    except Exception as e:
             raise Exception(f"Error en TTD: {e}")
     
def searh_verificadores():
        try:
                st.write("Modulo  Verificadores")
                #traer dataFrames
                df_ias = st.session_state.get("df_ias")
                df_dv = st.session_state.get("df_dv")
                df_csv = st.session_state.get("df_dcm")
                
                df_gam = st.session_state.get("df_gam")
                df_ttd = st.session_state.get("df_ttd")
                df_tap = st.session_state.get("df_tap")
                df_xandr = st.session_state.get("df_xandr")
                
                df_placement_ID = pd.DataFrame()
                #df_ias["Placement ID"]= df_ias["Placement ID"].astype(str)
                df_placement_ID["Placement ID"] = pd.concat([df_ias["Placement ID"],df_dv["Placement ID"], df_csv["Placement ID"]],  ignore_index=True)

                #df_placement_ID.duplicated(df_placement_ID.columns[~df_placement_ID.columns.isin(['Placement ID'])])

                df_placement_ID["Campaign"] = pd.concat([df_ias["Campaign"], df_dv["Campaign"]],ignore_index=True)
                df_placement_ID["Placement"] = pd.concat([df_ias["Placement"], df_dv["Placement"]],ignore_index=True)
                df_placement_ID= df_placement_ID.drop_duplicates(['Placement ID', 'Campaign','Placement'], keep='first')

                df_gam["Creative"]=df_gam["Creative"].astype(str)
                df_ttd["Creative"]=df_ttd["Creative"].astype(str)
                df_tap["Creative"]=df_tap["Creative"].astype(str)
                df_xandr["Creative"]=df_xandr["Creative"].astype(str)
                
                print(df_placement_ID["Placement ID"])
                df_placement_ID["Placement ID"] = df_placement_ID["Placement ID"].round(0).astype(int)
                df_placement_ID["Placement ID"]= df_placement_ID["Placement ID"].astype(str) #print(df_placement_ID)

                #df_placement_ID.to_excel("C:/Users/vbautista/Documents/PLACEMENT.xlsx")
                data_Gam =[]
                data_TTD =[]
                data_Tap =[]
                data_xandr =[]

                #here

                for i in range(len(df_placement_ID)):
                        row = df_placement_ID.iloc[i]["Placement ID"]
                        rowCampaign = df_placement_ID.iloc[i]["Campaign"]
                        rowPlacement = df_placement_ID.iloc[i]["Placement"]
                        filtro = df_gam[df_gam["Creative"].str.contains(row,case=False)]
                        filtro2 = df_ttd[df_ttd["Creative"].str.contains(row,case=False)]
                        filtro3 = df_tap[df_tap["Creative"].str.contains(row,case=False)]
                        filtro4 = df_xandr[df_xandr["Creative"].str.contains(row,case=False)]
                        filtro["Placement ID"] = row
                        filtro["Campaign"] = rowCampaign
                        filtro["Placement"] = rowPlacement
                        filtro2["Placement ID"] = row
                        filtro2["Campaign"] = rowCampaign
                        filtro2["Placement"] = rowPlacement
                        filtro3["Placement ID"] = row
                        filtro3["Campaign"] = rowCampaign
                        filtro3["Placement"] = rowPlacement
                        filtro4["Placement ID"] = row
                        filtro4["Campaign"] = rowCampaign
                        filtro4["Placement"] = rowPlacement
                        data_Gam.append(filtro)
                        data_TTD.append(filtro2)
                        data_Tap.append(filtro3)
                        data_xandr.append(filtro4)
                df_join_gam= pd.concat(data_Gam, ignore_index=True)
                df_join_ttd= pd.concat(data_TTD, ignore_index=True)
                df_join_tap= pd.concat(data_Tap, ignore_index=True)
                df_join_xandr= pd.concat(data_xandr, ignore_index=True)
                df_join_gam["Placement ID"]= df_join_gam["Placement ID"].astype(str)
                df_join_ttd["Placement ID"]= df_join_ttd["Placement ID"].astype(str)
                df_join_tap["Placement ID"]= df_join_tap["Placement ID"].astype(str)
                df_join_xandr["Placement ID"]= df_join_xandr["Placement ID"].astype(str)
                #df_join_gam.to_excel("prisa/consolidado/consolidado_GAM2024_.xlsx")
                #df_join_xandr.to_excel("C:/Users/vbautista/Documents/xandr_Jojn.xlsx")
                #df_join_ttd.to_excel("C:/Users/vbautista/Documents/tap_Jojn.xlsx")
                st.session_state["df_join_gam"] = df_join_gam
                st.session_state["df_join_ttd"] = df_join_ttd
                st.session_state["df_join_tap"] = df_join_tap
                st.session_state["df_join_xandr"] = df_join_xandr
                st.success("Verificadores OK..")
                print("Search...ok")
        except Exception as e:
                 raise Exception(f"Error en Search Verificadores: {e}")

def joindata():
        
        try:
                st.write("Modulo Join data Frames")
                #Load Dataframes
                df_join_gam = st.session_state.get("df_join_gam")
                df_gam = st.session_state.get("df_gam")
                df_join_ttd = st.session_state.get("df_join_ttd")
                df_ttd = st.session_state.get("df_ttd")
                df_join_tap = st.session_state.get("df_join_tap")
                df_tap = st.session_state.get("df_tap")
                df_join_xandr = st.session_state.get("df_join_xandr")
                df_xandr = st.session_state.get("df_xandr")


                               
                
                join_data_Gam = pd.concat([df_join_gam,df_gam])
                join_data_Gam = join_data_Gam.drop_duplicates(["Order", "Line item", "Creative ID","Date"])
                join_data_ttd = pd.concat([df_join_ttd,df_ttd])
                join_data_ttd = join_data_ttd.drop_duplicates(["Order", "Line item", "Creative", "Date"])
                join_data_tap = pd.concat([df_join_tap,df_tap])
                join_data_tap = join_data_tap.drop_duplicates(["Order", "Line item", "Creative", "Date"])
                #Xandr
                join_data_xandr = pd.concat([df_join_xandr,df_xandr])
                join_data_xandr = join_data_xandr.drop_duplicates(["Order", "Line item", "Creative", "Date"])
                
                st.session_state["join_data_xandr"] = join_data_xandr
                st.session_state["join_data_Gam"] = join_data_Gam
                st.session_state["join_data_ttd"] = join_data_ttd
                st.session_state["join_data_tap"] = join_data_tap


                #join_data_xandr.to_excel("C:/Users/vbautista/Documents/xandr_JoinData.xlsx")
                #join_data_Gam.to_excel("Integration/IAS/dcm/DATA_GAM_Consolidado.xlsx")
                st.success("Join Data OK..")
                
        except Exception as e:
                 raise Exception(f"Error en Join Data: {e}")
         
def search_adbookID():
        
        try:
                st.write("Modulo Search Adbook ID")
                #Load dataframes
                df_join_gam = st.session_state.get("df_join_gam")
                df_join_ttd = st.session_state.get("df_join_ttd")
                df_join_tap = st.session_state.get("df_join_tap")
                join_data_xandr = st.session_state.get("join_data_xandr")



                
                df_placement_DCM = pd.DataFrame()
                #Xandr
                df_placement_DCM["Placement ID"] = pd.concat([df_join_gam["Placement ID"],df_join_ttd["Placement ID"], df_join_tap["Placement ID"], join_data_xandr["Placement ID"]], ignore_index=True)
                df_placement_DCM["Drop ID"] = pd.concat([df_join_gam["Drop ID"], df_join_ttd["Drop ID"], df_join_tap["Drop ID"], join_data_xandr["Drop ID"]],ignore_index=True)
                df_placement_DCM["Adbook ID"] = pd.concat([df_join_gam["Adbook ID"], df_join_ttd["Adbook ID"], df_join_tap["Adbook ID"], join_data_xandr["Adbook ID"]],ignore_index=True)
                #df_placement_DCM["Server"] = pd.concat([df_join_gam["server"],df_join_ttd["server"], df_join_tap["server"]], ignore_index=True)
                #changes
                df_placement_DCM["Date"] = pd.concat([df_join_gam["Date"], df_join_ttd["Date"], df_join_tap["Date"], join_data_xandr["Date"]],ignore_index=True)
                df_placement_DCM["Date"] = df_placement_DCM["Date"]
                df_placement_DCM["Date"] = pd.to_datetime(df_placement_DCM["Date"])
                df_placement_DCM["Date"] = df_placement_DCM["Date"].dt.strftime('%Y-%m-%d')
                #wendys***-----------------------------------------*********---------WENDYS------------------------------***------------------
                new_data = pd.DataFrame({'Drop ID':['13883574','13876943'],'Adbook ID':['777526','777526'],'Placement ID':['4711903','4711904'],'Date':['2025-02-01','2025-02-01']})
                df_placement_DCM = pd.concat([df_placement_DCM,new_data], ignore_index=True)
                
                st.session_state["df_placement_DCM"] = df_placement_DCM

                st.success("Search Adbook ID OK..")
                
        except Exception as e:
                 raise Exception(f"Error en Search Adebook ID: {e}")

def package_function():
        try:
                st.write("Modulo Package")
                #Load dataframes                               
                df_placement_DCM = st.session_state.get("df_placement_DCM")
                df_csv = st.session_state.get("df_dcm")
                df_join_gam = st.session_state.get("df_join_gam")
                df_join_ttd = st.session_state.get("df_join_ttd")
                df_join_tap = st.session_state.get("df_join_tap")
                df_join_xandr = st.session_state.get("df_join_xandr")



                
                
                df_package= df_placement_DCM.copy()
                df_dcm_package = df_csv.copy()
                df_dcm_package["Date"] = pd.to_datetime(df_dcm_package["Date"])
                # Agregar una columna con el mes y año
                df_dcm_package["Mes"] = df_dcm_package["Date"].dt.to_period("M")           
                                                                        
                df_month_dcm_package= df_dcm_package.groupby(["Placement","Placement ID", "Mes", "Date"])[["Impressions DCM","Clicks DCM","Video Plays","Video Completions"]].sum().reset_index()
                df_month_dcm_package["Imps Mensuales"]= df_month_dcm_package.groupby(["Placement","Placement ID", "Mes"])["Impressions DCM"].transform('sum')
                df_month_dcm_package["Partner Cost (USD)"]=0
                
                #df_month_dcm_package.to_excel("C:/Users/vbautista/Documents/month_dcm_package2_02.19.xlsx", index=False)
                
                df_package["Server"] = pd.concat([df_join_gam["server"],df_join_ttd["server"], df_join_tap["server"], df_join_xandr["server"]], ignore_index=True)
                #elimino Server de todos df
                df_join_gam.drop(columns=["server"], inplace=True)
                df_join_ttd.drop(columns=["server"], inplace=True)
                df_join_tap.drop(columns=["server"], inplace=True)
                df_join_xandr.drop(columns=["server"], inplace=True)                       
                
                        
                df_package["Placement ID"]= df_package["Placement ID"].astype(str)
                df_package["Date"] = pd.to_datetime(df_package["Date"])
                # Agregar una columna con el mes y año
                df_package["Mes"] = df_package["Date"].dt.to_period("M")    
                
                
                df_month_dcm_package["Placement ID"]= df_month_dcm_package["Placement ID"].astype(int)
                df_month_dcm_package["Placement ID"]= df_month_dcm_package["Placement ID"].astype(str)
                
                #df_package.to_excel("C:/Users/vbautista/Documents/packeDelete_05.27.xlsx", index=False)

                df_package = df_package.drop_duplicates(['Placement ID','Date','Mes', 'Server'], keep='first')                       
                #df_package.to_excel("C:/Users/vbautista/Documents/packeDelete.xlsx", index=False)
                                        
                df_package_final = df_month_dcm_package.merge(df_package, on=["Placement ID", 'Date',"Mes"], how="outer")
                df_package_final[["Drop ID", "Adbook ID"]] = df_package_final.groupby("Placement ID")[["Drop ID", "Adbook ID"]].ffill()

                #  Convertir "Fecha" a formato datetime
                df_package_final["Date"] = pd.to_datetime(df_package_final["Date"])
                df_package_final["Date"] = df_package_final["Date"].dt.strftime('%Y-%m-%d')
                #df_package_final.to_excel("C:/Users/vbautista/Documents/packeDedf_package_final_Merge_05.27.xlsx", index=False)
                        
                # Función personalizada para rellenar Adbook ID
                def fill_adbook_id(group):
                        # Si Adbook ID es nulo, lo rellenamos con el valor anterior dentro de cada "Placement ID"
                        group['Adbook ID'] = group['Adbook ID'].fillna(method="ffill")
                        group['Drop ID'] = group['Drop ID'].fillna(method="ffill")

                        # Si sigue siendo nulo después del relleno, lo llenamos con el primer valor disponible en el grupo
                        group['Adbook ID'] = group['Adbook ID'].fillna(method="bfill")
                        group['Drop ID'] = group['Drop ID'].fillna(method="bfill")

                        return group

                # Aplicar la función de relleno por grupo de "Mes" y "Placement ID"
                df_package_final = df_package_final.groupby(["Mes", "Placement ID"]).apply(fill_adbook_id)
                #last change, DCM had Duplicate Imps Column Server Xandr vs TTD or GAM
                df_package_final= df_package_final.drop_duplicates(['Placement ID', 'Placement','Date','Mes','Adbook ID','Drop ID'], keep='first')                                   
                #df_package_final.drop(columns=["Mes"], inplace=True)                     
                
                #df_package_final.to_excel("C:/Users/vbautista/Documents/packeDedf_package_final_Merge_06.09_dos.xlsx", index=False)
                #wendys
                df_package_final.loc[(df_package_final["Placement"]=="PC~Value _PM~VM_PD~VAL1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaPreRoll_VAL1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")),"Drop ID"]="13883574"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Hamburger _PM~HAMB_PD~BEEF1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaPreRoll_BEEF1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")),"Drop ID"]="13876966"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Value _PM~VM_PD~VAL1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaCTVOTT_VAL1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")) ,"Drop ID"]="13876943"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Hamburger _PM~HAMB_PD~BEEF1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaCTVOTT_BEEF1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")) ,"Drop ID"]="13876954"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Value _PM~VM_PD~VAL1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaPreRoll_VAL1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")),"Adbook ID"]="777526"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Value _PM~VM_PD~VAL1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaCTVOTT_VAL1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")) ,"Adbook ID"]="777526"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Hamburger _PM~HAMB_PD~BEEF1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaPreRoll_BEEF1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")),"Adbook ID"]="777526"
                df_package_final.loc[(df_package_final["Placement"]=="PC~Hamburger _PM~HAMB_PD~BEEF1_PB~PRISABRN_AS~INNOVIDVAST_AD~AS3PTRCK_IT~OO_DA~NONE_FM~VPRE_DT~CROSS_RT~CPM_VV~VGPMX70DV_TG~CONDEM_AV~RES_PK~VCR_PT~SA_SZ~15S_UN~PrisaCTVOTT_BEEF1_LG~HM_YR~2024") & (df_package_final["Date"].str.contains("2025-02")) ,"Adbook ID"]="777526"
                                        
                # Eliminar filas donde ambas columnas sean nulas o vacías
                df_package_final = df_package_final.dropna(subset=["Adbook ID", "Drop ID"], how="all")
                df_package_final.drop(columns=["Server"], inplace=True)
                
                st.session_state["df_package_final"] = df_package_final

                st.success("Package function OK..")
                       
        except Exception as e:
                raise Exception(f"Error en Package Function: {e}")
                 #raise Exception(f"Error Packages: {e}")              

def add_placement():
        try:
                st.write("Modulo Placement ID")
                #Load dataframes                               
                df_placement_DCM = st.session_state.get("df_placement_DCM")
                df_csv = st.session_state.get("df_dcm")
                df_data_ias = st.session_state.get("df_data_ias")
                df_dv = st.session_state.get("df_dv")

                
                
                df_placement_DCM.drop(['Date'], axis=1, inplace=True)                                               
                df_placement_DCM= df_placement_DCM.drop_duplicates(['Placement ID'], keep='first')
                

                df_csv["Placement ID"]=df_csv["Placement ID"].astype(str)
                df_data_ias["Placement ID"]=df_data_ias["Placement ID"].astype(str)
                df_dv["Placement ID"]=df_dv["Placement ID"].astype(str)
                df_placement_DCM["Placement ID"]= df_placement_DCM["Placement ID"].astype(str)
                #df_placement_DCM.to_excel("C:/Users/vbautista/Documents/DATA_Placement.xlsx", index=False)
                data_Add_Placement =[]
                data_Add_Placement_IAS =[]
                data_Add_Placement_DV =[]                                    
                
                for i in range(len(df_placement_DCM)):
                        row = df_placement_DCM.iloc[i]["Placement ID"]
                        rowCampaign = df_placement_DCM.iloc[i]["Adbook ID"]
                        rowPlacement = df_placement_DCM.iloc[i]["Drop ID"]
                        filtro = df_csv[df_csv["Placement ID"].str.contains(row,case=False)]
                        filtro1 = df_data_ias[df_data_ias["Placement ID"].str.contains(row,case=False)]
                        filtro2 = df_dv[df_dv["Placement ID"].str.contains(row,case=False)]
                        filtro["Placement ID"] = row
                        filtro["Adbook ID"] = rowCampaign
                        filtro["Drop ID"] = rowPlacement
                        filtro1["Placement ID"] = row
                        filtro1["Adbook ID"] = rowCampaign
                        filtro1["Drop ID"] = rowPlacement
                        filtro2["Placement ID"] = row
                        filtro2["Adbook ID"] = rowCampaign
                        filtro2["Drop ID"] = rowPlacement
                        data_Add_Placement.append(filtro)
                        data_Add_Placement_IAS.append(filtro1)
                        data_Add_Placement_DV.append(filtro2)                              
                df_join_dcm= pd.concat(data_Add_Placement, ignore_index=True)
                df_join_ias= pd.concat(data_Add_Placement_IAS, ignore_index=True)
                df_join_dv= pd.concat(data_Add_Placement_DV, ignore_index=True)
                #df_join_dcm.to_excel("C:/Users/vbautista/Documents/data_dcm_placement FEB2025.xlsx")
                #df_join_dcm["Placement ID"]= df_join_dcm["Placement ID"].astype(str)
                df_join_ias["Partner Cost (USD)"]=0
                
                st.session_state["df_join_dcm"] = df_join_dcm
                st.session_state["df_join_ias"] = df_join_ias
                st.session_state["df_join_dv"] = df_join_dv
  
            
                st.success("Add placement Ok..")
                
        except Exception as e:
                 raise Exception(f"Error en Search Adebook ID: {e}")
               
def Exeptions_function():
        
        try:
                st.write("Exeptions DCM")
                #Load Dataframes
                df_join_dcm = st.session_state.get("df_join_dcm")
                df_join_ias = st.session_state.get("df_join_ias")
                df_join_dv = st.session_state.get("df_join_dv")
                
                run_data_manipulation_dcm(df_join_dcm,df_join_ias,df_join_dv)                 
                
        except Exception as e:
                 raise Exception(f"Error en Exeptions DCM: {e}")

def merge_function():        
        try:
                st.write("Merge")
                #Load Dataframes
                df_join_dcm = st.session_state.get("df_join_dcm")
                df_join_ias = st.session_state.get("df_join_ias")
                join_data_Gam = st.session_state.get("join_data_Gam")
                join_data_ttd = st.session_state.get("join_data_ttd")
                join_data_tap = st.session_state.get("join_data_tap")
                df_join_dv = st.session_state.get("df_join_dv")
                join_data_xandr = st.session_state.get("join_data_xandr")
                df_package_final = st.session_state.get("df_package_final")
                df_adbook = st.session_state.get("df_adbook")
                df_adbook_package = st.session_state.get("df_adbook_package")

                
                #Xandr
                join =pd.concat([df_join_dcm,df_join_ias,join_data_Gam,join_data_ttd,join_data_tap, df_join_dv, join_data_xandr])#join_xandr
                join_package =pd.concat([df_package_final,df_join_ias,join_data_Gam,join_data_ttd,join_data_tap, df_join_dv, join_data_xandr])#join_xandr
                #aqui
                join["Completed Impressions"]=0
                join_package["Completed Impressions"]=0

                join_data=join[["Order","Line item","Adbook ID","Drop ID","Campaign","Placement","Placement ID","Date","Impressions DCM","Clicks DCM","Video Plays","Video Completions","Eligible Ads For Viewability Measurement","Measured Ads","Viewable Impressions","Eligible Ads For Invalid Traffic Detection","Invalid Traffic","Total Eligible Ads For Brand Safety","Passed Ads","Total Tracked Ads","Goal quantity","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Monitored Ads","Completed Impressions","Eligible Impressions","Failed Ads","Creative","Partner Cost (USD)","Xandr Imps","Xandr Clicks"]] #"Xandr Imps","Xandr Clicks
                join_data_package=join_package[["Order","Line item","Adbook ID","Drop ID","Campaign","Placement","Placement ID","Date","Impressions DCM","Imps Mensuales","Clicks DCM","Video Plays","Video Completions","Eligible Ads For Viewability Measurement","Measured Ads","Viewable Impressions","Eligible Ads For Invalid Traffic Detection","Invalid Traffic","Total Eligible Ads For Brand Safety","Passed Ads","Total Tracked Ads","Goal quantity","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Monitored Ads","Completed Impressions","Eligible Impressions","Failed Ads","Creative","Partner Cost (USD)","Xandr Imps","Xandr Clicks"]] # "Xandr Imps","Xandr Clicks"
                join_data_package["Month"] = join_data_package["Date"]
                join_data_package["Month"] = pd.to_datetime(join_data_package["Month"])
                join_data_package["Month"] = join_data_package["Month"].dt.strftime('%Y-%m') 
                
                #sumo Imps prisa xandr
                join_data_package["Ad Gam Imps"]= join_data_package.groupby(["Adbook ID","Drop ID", "Month","Placement ID"])["Ad server impressions"].transform('sum')
                join_data_package["Ad TTD Imps"]= join_data_package.groupby(["Adbook ID","Drop ID", "Month","Placement ID"])["Impressions TTD"].transform('sum')
                join_data_package["Ad Xandr Imps"]= join_data_package.groupby(["Adbook ID","Drop ID", "Month","Placement ID"])["Xandr Imps"].transform('sum')
                #join_data_package = join_data_package.drop_duplicates(['Placement ID','Date','Month', 'Adbook ID','Drop ID'], keep='first')                    

                
                
                
                #join_data_package.to_excel("C:/Users/vbautista/Documents/join_data_package_06.05.xlsx", index=False)
                                        
                join_data["Placement ID"]= join["Placement ID"].astype(str)
                join_data["Adbook ID"]= join_data["Adbook ID"].astype(str)
                join_data["Drop ID"]= join_data["Drop ID"].astype(str)
                join_data_package["Placement ID"]= join_data_package["Placement ID"].astype(str)
                join_data_package["Adbook ID"]= join_data_package["Adbook ID"].astype(str)
                join_data_package["Drop ID"]= join_data_package["Drop ID"].astype(str)       
                
                df_final=pd.merge(join_data, df_adbook, on=('Adbook ID', 'Drop ID'), how='outer')
                df_final["Month"] = df_final["Date"]
                df_final["Month"] = pd.to_datetime(df_final["Month"])
                df_final["Month"] = df_final["Month"].dt.strftime('%Y-%m')                      
                
                #join_data_package.to_excel("C:/Users/vbautista/Documents/join_data_FInal.xlsx", index=False)
                
                df_final_package=pd.merge(join_data_package, df_adbook_package, on=('Adbook ID', 'Drop ID'), how='outer')                                           
                                                                                                        
                df_final_package["Imps Prisa"] = df_final_package.groupby(["Adbook ID", "Package ID", "Placement ID","Month"])[["Ad Gam Imps", "Ad TTD Imps","Ad Xandr Imps"]].transform('max').sum(axis=1)#"Ad Xandr Imps
                # Calcular porcentajes en columnas separadas (formato decimal)
                df_final_package['Gam%'] = (df_final_package['Ad Gam Imps'] / df_final_package['Imps Prisa']).round(5)
                df_final_package['TTD%'] = (df_final_package['Ad TTD Imps'] / df_final_package['Imps Prisa']).round(5)
                df_final_package['Xandr%'] = (df_final_package['Ad Xandr Imps'] / df_final_package['Imps Prisa']).round(5)
                #df_final_package.to_excel("C:/Users/vbautista/Documents/df_final_package_FINAL.xlsx", index=False)
                df_final_package['%Parent'] = df_final_package['Gam%'] + df_final_package['TTD%'] + df_final_package['Xandr%']
                #df_final_package.to_excel("C:/Users/vbautista/Documents/df_final_package_FINALBefore.xlsx", index=False)
                                
                df_final_package["Imps DCM Month"]=(df_final_package["%Parent"]*df_final_package["Imps Mensuales"]).round(0)                                               
                df_final_package.rename(columns={'Impressions DCM': 'Impresiones DCM Date', 'Imps DCM Month': 'Impressions DCM'}, inplace=True)
                df_final_package['Impressions DCM'] = np.where(df_final_package['Price Type'] == "Flat Rate", df_final_package['Imps Mensuales'], df_final_package['Impressions DCM'])                      
                #wendys exeption
                df_final_package['Impressions DCM'] = np.where(df_final_package['Adbook ID'] == "777526", df_final_package['Imps Mensuales'], df_final_package['Impressions DCM'])
                df_final_package['Impressions DCM'] = np.where(df_final_package['Adbook ID'] == "777526", df_final_package['Imps Mensuales'], df_final_package['Impressions DCM'])
                df_final_package['Impressions DCM'] = np.where(df_final_package['Imps Prisa'] == 0, df_final_package['Imps Mensuales'], df_final_package['Impressions DCM'])                      

                drops_delete = np.where(df_final_package['Drop ID'] == "13876924")
                df_final_package.drop(index=drops_delete[0], inplace=True)
                #df_final_package.to_excel("C:/Users/vbautista/Documents/df_final_package_FINALDOS.xlsx", index=False)

                #Month year
                date= datetime.datetime.now()
                year_month = date.strftime('%Y-%m')

                filter_month = df_final["Month"]== year_month #"2025-12"
                data_date=df_final[filter_month]
                
                #Xandr
                month= df_final.groupby(["Sales Rep","Price","Partner Cost (USD)","dias","diasHoy","Package ID","Client Name","Month","Adbook ID","Drop ID","Placement ID","Position Name","Start Date","End Date","Impressions Sold","Package Imps Sold"])[["Invalid Traffic","Eligible Ads For Invalid Traffic Detection","Viewable Impressions","Eligible Ads For Viewability Measurement","Passed Ads","Total Eligible Ads For Brand Safety","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Impressions DCM","Clicks DCM","Video Plays","Video Completions","Xandr Imps","Xandr Clicks"]].sum().reset_index()
                data_month = month[["Sales Rep","Price","Partner Cost (USD)","dias","diasHoy","Package ID","Client Name","Month","Adbook ID","Drop ID","Placement ID","Position Name","Start Date","End Date","Impressions Sold","Package Imps Sold","Invalid Traffic","Eligible Ads For Invalid Traffic Detection","Viewable Impressions","Eligible Ads For Viewability Measurement","Passed Ads","Total Eligible Ads For Brand Safety","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Impressions DCM","Clicks DCM","Video Plays","Video Completions","Xandr Imps","Xandr Clicks"]]
                #month_package= df_final_package.groupby(["Sales Rep","Price","Partner Cost (USD)","dias","diasHoy","Package ID","Client Name","Month","Adbook ID","Drop ID","Placement ID","Position Name","Start Date","End Date","Impressions Sold","Package Imps Sold"])[["Invalid Traffic","Eligible Ads For Invalid Traffic Detection","Viewable Impressions","Eligible Ads For Viewability Measurement","Passed Ads","Total Eligible Ads For Brand Safety","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Impressions DCM","Clicks DCM","Video Plays","Video Completions"]].sum().reset_index()
                #data_date.to_excel("C:/Users/vbautista/Documents/data_date.xlsx", index=False)
                #Package Distribution
                month_package= df_final_package.groupby(["Sales Rep","Price","Partner Cost (USD)","dias","diasHoy","Package ID","Client Name","Month","Adbook ID","Drop ID","Placement ID","Position Name","Start Date","End Date","Impressions Sold","Package Imps Sold"]).agg({'Invalid Traffic':'sum',"Eligible Ads For Invalid Traffic Detection":'sum',"Viewable Impressions":'sum',"Eligible Ads For Viewability Measurement":'sum',"Passed Ads":'sum',"Total Eligible Ads For Brand Safety":'sum',"Ad server impressions":'sum',"Ad server clicks":'sum',"Xandr Imps":'sum',"Xandr Clicks":'sum',"Impressions TTD":'sum',"Clicks TTD":'sum',"Impressions DCM":'max',"Clicks DCM":'sum',"Video Plays":'sum',"Video Completions":'sum',"Third Party Impressions FTD":'max',"Third Party Percent Delivered FTD":'max'}).reset_index()                                              
                data_month_package = month_package[["Sales Rep","Price","Partner Cost (USD)","dias","diasHoy","Package ID","Client Name","Month","Adbook ID","Drop ID","Placement ID","Position Name","Start Date","End Date","Impressions Sold","Package Imps Sold","Invalid Traffic","Eligible Ads For Invalid Traffic Detection","Viewable Impressions","Eligible Ads For Viewability Measurement","Passed Ads","Total Eligible Ads For Brand Safety","Ad server impressions","Ad server clicks","Impressions TTD","Clicks TTD","Impressions DCM","Clicks DCM","Video Plays","Video Completions","Third Party Impressions FTD","Third Party Percent Delivered FTD","Xandr Imps","Xandr Clicks"]]
                #data_month_package.to_excel("C:/Users/vbautista/Documents/data_month_package2.xlsx", index=False)
                st.session_state["data_date"] = data_date
                st.session_state["data_month"] = data_month
                st.session_state["data_month_package"] = data_month_package
                st.session_state["df_final"] = df_final
     
                st.success("Merge Ok..")                   
        except Exception as e:
                raise Exception(f"Error en Merge: {e}")

def Cloud_Update(check_daily,check_monthly,check_package):
                
        try:
                st.write("Actualizar en la nube")              
                
                #Load Dataframes            
                data_date = st.session_state.get("data_date")
                data_month = st.session_state.get("data_month")
                data_month_package = st.session_state.get("data_month_package")
                df_final = st.session_state.get("df_final")
                
                
                data_date= data_date.fillna('')
                data_month= data_month.fillna('')
                data_month_package= data_month_package.fillna('')
                df_final=df_final.fillna('')
                #actualiza
                data_date.to_excel("C:/Users/vbautista/Documents/daily_julio.xlsx")
                data_month.to_excel("C:/Users/vbautista/Documents/Montly_julio.xlsx")

                
                def update_package():
                        #Package
                        print("Month_Package")
                        st.write("▶Generando Month Package")
                        #sheet_Month_package.update([data_month_package.columns.values.tolist()]+data_month_package.values.tolist())
                        st.write("Month Package Cargado◀")
                        st.write("✪✪✪-Informe Package Generado con Exito-✪✪✪")
                        
                def update_daily():
                        #Daily
                        print("Date")
                        st.write("▶Generando Date Looker◀")
                        #sheet_Date.update([data_date.columns.values.tolist()]+data_date.values.tolist())
                        st.write("▶Date Cargado◀")
                        st.write("✪✪✪-Informe Date Generado con Exito-✪✪✪")

                        print("Date cargado......")
                
                def update_monthly():
                        #Monthly
                        print("Month")
                        st.write("▶Generando Month Looker◀")
                        #sheet_Month.update([data_month.columns.values.tolist()]+data_month.values.tolist())
                        print("Month cargado.......")
                        st.write("▶Date Cargado◀")
                        st.write("✪✪✪-Informe Monthly Generado con Exito-✪✪✪")
                
                if check_daily==1 and check_monthly==1 and check_package==1:
                        update_daily()
                        update_monthly()
                        update_package()
                        st.info("El Informe de consolidado se ejecuto correctamente...")

                elif check_daily==1 and check_monthly==1:
                        update_daily()
                        update_monthly()
                elif check_daily==1 and check_package==1:
                        update_daily()
                        update_package()
                elif check_monthly==1 and check_package==1:
                        update_monthly()
                        update_package()
                elif check_daily==1:
                        update_daily()
                elif check_monthly==1:
                        update_monthly()
                elif check_package==1:
                        update_package()
                else:
                        st.info("⚠️ Selecciona al menos una opción de informe para actualizar")                                                                                                                                   
                                                                                     
                st.success("Informe Generado en la nube..")                     
        except Exception as e:
                 raise Exception(f"Error en Cloud Update: {e}")
        
                
        