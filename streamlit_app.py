import streamlit as st
import pandas as pd

def processa ( df ):
    curso = st.text_input('Nome do curso e/ou turma:')

    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = True

    turno = st.radio(
        "Turno",
        ["Manha","Tarde","Manha/Tarde"],
        key="Manha",
        label_visibility = st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal)
    
    municipio = st.text_input("Municipio:")
    data_inicio_curso = st.date_input("Data de inicio do curso:")
    data_inicio_ferias = st.date_input("Férias - data de inicio:")
    data_final_ferias = st.date_input("Férias - data final:")
    ch_total = st.text_input("Carga horária:", max_chars=4)
    ch_teorica = st.text_input("Carga horária teórica:", max_chars=3)
    ch_inicial = st.text_input("Formacao inicial(CH):", max_chars=2)
    horas_semana = st.text_input("Horas Teoricas por semana:", max_chars=1)

    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = True

    dia_semana = st.radio(
        "Aulas fixas",
        ["seg","ter","qua", "qui", "sex"],
        key="seg",
        label_visibility = st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal)

    semana_complementar = st.radio(
        "Aulas complementares - semana",
        ["nenhum","primeira","segunda","terceira","quarta"],
        key="nenhuma",
        label_visibility = st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal)

    dia_complementar = st.radio(
        "Dia para aulas complementares",
        ["nenhum","seg","ter","qua","qui","sex"],
        key="nenhum",
        label_visibility = st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal)

    return curso, turno, municipio, data_inicio_curso, data_inicio_ferias, data_final_ferias, ch_total, ch_teorica, ch_inicial, horas_semana, dia_semana, semana_complementar, dia_complementar

st.title( 'Calendário - Tela Inicial')
            
arquivo = st.file_uploader( 
    'Upload do arquivo de feriados e recessos:', type='xlsx'
    # type='csv')
if arquivo :
    # df = pd.read_csv( arquivo )
    df = pd.read_excel( arquivo )
    st.dataframe( df )
    st.text(processa( df ))
else:
    st.error(' * Falta realizar UPLoad de arquivo .csv com feriados *')
