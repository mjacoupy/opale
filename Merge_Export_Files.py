#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:28:35 2022

@author: maximejacoupy
"""


# #######################################################################################################################
#                                              # === LIBRAIRIES === #
# #######################################################################################################################
import streamlit as st
from PIL import Image
import pandas as pd


# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################


def sjoin(x): 
    return ';'.join(x[x.notnull()].astype(str))


# #######################################################################################################################
#                                              # === PROCESS NEW FILE === #
# #######################################################################################################################
st.title("OPALE - fusion des exports")
st.markdown("""---""")


    
uploaded_files = st.file_uploader("Selectionner les fichiers CSV", accept_multiple_files=True, type="csv")

if uploaded_files:
    dfc = None
    
    st.markdown("---")
    for iCpt, uploaded_file in enumerate(uploaded_files):
        df = pd.read_csv(uploaded_file, sep=';', index_col="ID")
        with st.expander("See CSV file - "+str(uploaded_file.name)):

            st.dataframe(df)
        dfc = pd.concat([dfc, df], axis=1)
        
   
    df_tmp = dfc.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))

    df_final = df_tmp.applymap(lambda x: x.split(';')[0]).reset_index()   
    
    st.markdown("---")
    st.markdown("Document fusionné")
    st.dataframe(df_final)
    
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(df_final)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='merge_file.csv',
        mime='text/csv')
    
        
