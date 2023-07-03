import streamlit as st
import pandas as pd

def mostra( data ):
#    st.image("../static/img/ciee.jpg")
    st.header("Calendário")
    st.write("- Curso: {{curso}} Turno:{{turno}}")
    st.write("- Carga horária diária: {{chDiaria}} h")
    st.write("- Carga horária teórica: {{chteoricatotal}} h")
    st.write("- Carga horária total: {{chtotal}} h")
    st.write("- Formação Teórica: {{formacaoTeorica}}")
    st.write("- Formação Inicial: {{formacaoInicial}}")
    st.write("- Formação Final: {{formacaoFinal}}")
    st.write("- Férias: {{periodoFerias}}")
    st.write("- Inicio e Térmio do Contrato: {{inicioeTermino}}")
    st.write("")

    # Converter os dados em um DataFrame
    df = pd.DataFrame(data, columns=["Mês", "Ano", "Calendário", "Aulas Teóricas", "Práticas", "CH Mensal"])

    # Exibir o DataFrame usando a função `st.table()`
    #    st.table(df)
    
    st.header("Tabela de Calendário")
    st.write("Legenda:")
    st.write("- [__] = Formação Inicial (i)")
    st.write("- [__] = Aulas Teóricas (t,T) CIEE")
    st.write("- [__] = Formação final (f)")
    st.write("- [__] = Atividades Práticas na Empresa (p)")
    st.write("- [__] = Atividades Práticas na Empresa - Recesso no CIEE (r)")
    st.write("- [__] = Finais de Semanas (x)")
    st.write("- [__] = Feriados (X)")
    st.write("- [__] = Férias")

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
    'Upload do arquivo de feriados e recessos:',
    type='csv')
if arquivo :
    df = pd.read_csv( arquivo )
    # Converter os dados em um DataFrame
    df_data = pd.DataFrame(df, columns=["Mês", "Ano", "Calendário", "Aulas Teóricas", "Práticas", "CH Mensal"])

    # Exibir o DataFrame usando a função `st.table()`
    #    st.table(df)
    
    # df = pd.read_excel( arquivo )
    if st.button('Feriados e Recessos'):
        st.table(df_data)
        st.dataframe( df_data )
        st.text(processa( df_data ))
        
   
    dados = [
    "01;2023;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    "02;2023;01-02-T;02-03-t;03-04-t;04-05-p;05-06-t;06-07-t;07-08-T;08-09-t;09-10-t;10-11-t;11-12-t;12-13-T;13-14-t;14-15-p;15-16-t;16-17-t;17-18-t;18-19-t;19-20-T;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-t;26-27-T;27-28-t;28-01-r;22;06;31",
    "03;2023;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    ]
    mostra( dados )
else:
    st.error(' * Falta realizar UPLoad de arquivo .csv com feriados *')
