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
import pandas as pd


# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################


# def sjoin(x):
#     """..."""
#     return ';'.join(x[x.notnull()].astype(str))


def convert_df(df):
    """..."""
    return df.to_csv(sep=';').encode('latin1')


# #######################################################################################################################
#                                              # === PROCESS NEW EXPORTS === #
# #######################################################################################################################
st.title("OPALE - fusion des exports")
st.markdown("""---""")



uploaded_files = st.file_uploader("Selectionner les fichiers CSV", accept_multiple_files=True, type="csv")

if uploaded_files:
    concat_df = None

    ##########
    # Choix premier bloc
    ##########
    names = []
    for iFile in uploaded_files:
        names.append(iFile.name)

    st.markdown("---")
    first = st.radio(label='Choix du bloc de référence',
                     options=names)

    final_up_list = []
    for iCpt, iFile in enumerate(uploaded_files):
        if iFile.name == first:
            final_up_list.append(iFile)
    for iCpt, iFile in enumerate(uploaded_files):
        if iFile.name != first:
            final_up_list.append(iFile)


    ##########
    # Affichage
    ##########

    st.markdown("---")
    l = []
    for iCpt, uploaded_file in enumerate(final_up_list):

            df = pd.read_csv(uploaded_file,
                             sep=';',
                             encoding='latin-1')
            df.set_index('initiales_nom')
            df = df.add_prefix(str(iCpt+1)+'_')

            with st.expander(str(uploaded_file.name)):
                df_display = df.astype(str)
                st.dataframe(df_display)
                st.markdown('Le document contient **'+str(df_display.shape[0])+' lignes** et **'+str(df_display.shape[1])+' colonnes**.')

            globals()['df%s' % iCpt] = df
            l.append(globals()['df%s' % iCpt])

    button = st.button("Initier le processus de fusion")
    if button:
        concat_df = pd.concat(l, axis=1)
        # concat_df = pd.concat([concat_df, df], axis=1)


        st.markdown("---")
        st.markdown("Document fusionné")
        st.dataframe(concat_df)
        st.markdown('Le document contient **'+str(concat_df.shape[0])+' lignes** et **'+str(concat_df.shape[1])+' colonnes**.')


        merged_file_name = st.text_input(label="Entrer le nom du fichier incluant le .csv",
                                  value="merged_file.csv")

        csv = convert_df(concat_df)

        st.download_button(
            label="Télécharger le fichier sous format CSV",
            data=csv,
            file_name=merged_file_name,
            mime='text/csv')


#########################################################################################################################
#########################################################################################################################

#                                              # === END OF FILE === #

#########################################################################################################################
# #######################################################################################################################
