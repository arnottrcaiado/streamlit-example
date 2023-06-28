import streamlit as st
import pandas as pd

def mostra( dados ):
    st.title("Calendário de Aulas")
    st.image("../static/img/ciee.jpg")

    st.header("Calendário")
    st.markdown(
        """
        <ul>
            <li><span </span>Curso: {{curso}} Turno:{{turno}}</li>
            <li><span </span>Carga horária diária: {{chDiaria}} h</li>
            <li><span </span>Carga horária teórica: {{chteoricatotal}} h</li>
            <li><span </span>Carga horária total: {{chtotal}} h</li>
            <li><span </span>Formação Teórica: {{formacaoTeorica}}</li>
            <li><span </span>Formação Inicial: {{formacaoInicial}}</li>
            <li><span </span>Formação Final: {{formacaoFinal}}</li>
            <li><span </span>Férias: {{periodoFerias}}</li>
            <li><span </span>Inicio e Térmio do Contrato: {{inicioeTermino}}</li>
        </ul>
        """
    )

    st.write("")

    data = [
        # Dados para preencher a tabela
    ]

    table_html = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            text-align: center;
            padding: 10px;
            border-bottom: 1px solid #ccc;
        }
        .inicio {
            background-color: #ADD8E6 ;
            color : white;
        }
        .reposicao {
            background-color: #1E90FF ;
            color : white;
        }
        .teorica_final {
            background-color: #0000FF ;
            color : white;
        }
        .teorico {
            background-color: #00BFFF ;
            color : white;
        }
        .pratico {
            background-color: #0000CD;
            color: white;
        }
        .recesso {
            background-color: #836FFF ;
            color: white ;
        }
        .fds {
            background-color: #B0C4DE ;
            color: white ;
        }
        .ferias {
            background-color: #A9A9A9 ;
            color: white ;
        }
        .feriado {
            background-color: #C0C0C0 ;
            color: white ;
        }
        .total {
            font-weight: bold;
        }
    </style>

    <table>
        <tr>
            <th>Ano</th>
            <th>Mês</th>
            <th>Calendário</th>
            <th>Aulas Teoricas</th>
            <th>Práticas</th>
            <th>CH Mensal</th>
        </tr>
        {% for entry in data %}
            {% set month = entry.split(';')[0] %}
            {% set year = entry.split(';')[1] %}
            {% set teoricas_praticas = entry.split(';')[2:-1] %}
            {% set teoricas = entry.split(';')[-3] %}
            {% set praticas = entry.split(';')[-2] %}
            {% set total = entry.split(';')[-1] %}
            <tr>
                <td>{{ year }}</td>
                <td>{{ month }}</td>
                <td>
                    <div style="display">

                    {% set coluna = 1 %}
                    {% for day in teoricas_praticas %}
                        {% set day_completo = day %}
                        {% set aula_type = day.split('-')[2] %}
                        {% set day_number = day.split('-')[0] ~ '-' ~ day.split('-')[1] %}
                        {% if aula_type == 'i' %}
                            <span class="inicio">{{ day_number }}</span>
                        {% elif aula_type == 't' %}
                            <span class="teorico">{{ day_number }}</span>
                        {% elif aula_type == 'T' %}
                            <span class="teorico">{{ day_number }}</span>
                        {% elif aula_type == 'p' %}
                            <span class="pratico">{{ day_number }}</span>
                        {% elif aula_type == 'x' %}
                            <span class="fds">{{ day_number }}</span>
                        {% elif aula_type == 'X' %}
                            <span class="feriado">{{ day_number }}</span>
                        {% elif aula_type == 'r' %}
                            <span class="recesso">{{ day_number }}</span>
                        {% elif aula_type == 'F' %}
                            <span class="ferias">{{ day_number }}</span>
                        {% elif aula_type == 'f' %}
                            <span class="teorica_final">{{ day_number }}</span>
                        {% endif %}
                        {% set coluna = coluna + 1 %}
                        {%if coluna == 10 %}
                            {% set coluna = 1 %}
                        {% endif %}
                    {% endfor %}
                    </div>

                </td>
                <td>{{ teoricas }}</td>
                <td>{{ praticas }}</td>
                <td>{{ total }}</td>
            </tr>
        {% endfor %}
    </table>

    <h3>Legenda</h3>
    <ul>
        <li><span class="inicio">[__]</span> = Formação Inicial (i)</li>
        <li><span class="teorico">[__]</span> = Aulas Teóricas (t,T) CIEE</li>
        <li><span class="teorica_final">[__]</span> = Formação final (f)</li>
        <li><span class="pratico">[__]</span> = Atividades Práticas na Empresa (p)</li>
        <li><span class="recesso">[__]</span> = Atividades Práticas na Empresa - Recesso no CIEE (r)</li>
        <li><span class="fds">[__]</span> = Finais de Semanas (x)</li>
        <li><span class="feriado">[__]</span> = Feriados (X)</li>
        <li><span class="ferias">[__]</span> = Férias</li>
    </ul>
    """

    # Renderiza o código HTML
    st.components.v1.html(table_html)



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
    # df = pd.read_excel( arquivo )
    st.dataframe( df )
    st.text(processa( df ))
    dados = [
    "01;2023;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    "02;2023;01-02-T;02-03-t;03-04-t;04-05-p;05-06-t;06-07-t;07-08-T;08-09-t;09-10-t;10-11-t;11-12-t;12-13-T;13-14-t;14-15-p;15-16-t;16-17-t;17-18-t;18-19-t;19-20-T;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-t;26-27-T;27-28-t;28-01-r;22;06;31",
    "03;2023;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    ]
    st.text( mostra( dados ))
else:
    st.error(' * Falta realizar UPLoad de arquivo .csv com feriados *')
