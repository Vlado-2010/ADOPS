JSON="./frontend/assets/prisa.json"
import pandas as pd
import streamlit as st
#lee Assets
def READ_PATH():    
    
    df_path = pd.read_excel("./frontend/assets/Paths.xlsx")
    path = df_path.iloc[0]['Path_Route']    
    
    return path

def READ_PATH_LOCAL():  
      
    df_path = pd.read_excel("./frontend/assets/Paths.xlsx")
    path_local = df_path.iloc[1]['Path_Route']
    
    return path_local

def READ_PATH_OPTI_REPORTS():    
    df_path = pd.read_excel("./frontend/assets/Paths.xlsx")
    path_local_report = df_path.iloc[2]['Path_Route']
    
    return path_local_report

def DATAFRAME_PATHS():
    df = pd.read_excel("./frontend/assets/Paths.xlsx")
    return df