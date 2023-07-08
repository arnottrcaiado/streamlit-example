import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

diasSemana ={"0":"segunda-feira", "1":"terça-feira", "2":"quarta-feira", "3":"quinta-feira", "4":"sexta-feira"}
DIAFIMSEMANA = 5


def mostra( data, curso, turno, municipio, data_inicio_curso, data_inicio_ferias, data_final_ferias, ch_total, ch_teorica, ch_inicial, horas_semana, dia_semana, semana_complementar, dia_complementar ):
#    st.image("../static/img/ciee.jpg")
    st.header("Calendário")
    st.write("- Curso:",curso,"Turno:",turno)
    st.write("- Carga horária diária:",horas_semana,"h")
    st.write("- Carga horária teórica:",ch_teorica,"h")
    st.write("- Carga horária total:",ch_total,"h")
    st.write("- Formação Teórica:",data_inicio_curso)
    st.write("- Formação Inicial:",data_inicio_curso)
    st.write("- Formação Final:",ch_total)
    st.write("- Férias:",data_inicio_ferias," a ",data_final_ferias)
    st.write("- Inicio e Térmio do Contrato:",data_inicio_curso)
    st.write("")

    # Dividir cada string em uma lista de elementos
    dados_divididos = [d.split(';') for d in data]

    st.table(dados_divididos)
    
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

def inicia ( df ):
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

# ------------------------------------------------------------------------------------------------------
def gerar_calendario_completo(data_inicial, dia_semana_teorica, carga_horaria_total, carga_teorica_total,
                            horas_teoricas_semana, feriados, ferias, recessos, periodoContinuo,aulasComp, diaSemanaComp, ordemSemanaComp ):

    # Converter as datas iniciais e finais para objetos de data
    data_inicial = datetime.strptime(data_inicial, '%d-%m-%Y')
#    data_inicial = data_inicial
    calendario = []
    aulaTeoricaPendente= False
    teoricaSemana = False
    data_atual = data_inicial

    while carga_horaria_total > 0 or carga_teorica_total >0:
        ano_data = data_atual.year
        mes_data = data_atual.month
        dia_data = data_atual.day
        dia_semana = data_atual.weekday()
        data_str = datetime.strftime(data_atual, '%d-%m-%Y')

        teoricaSemana = False # controle de aula teorica na semana

        if not ehferias( data_atual, ferias ) and not ehrecesso( data_str, recessos ) :
          if dia_semana < DIAFIMSEMANA  : # segunda a sexta ?
            if ehferiado( data_str, feriados ) :
                tipo_aula = 'feriado'
            else :
                tipo_aula = ''
            # Verificar se o dia atual é um dia de aula teorica
            if ((dia_semana == dia_semana_teorica) or (dia_semana_teorica ==-1)) and (tipo_aula != 'feriado') :
                if (carga_teorica_total > 0) and (dia_semana < DIAFIMSEMANA) :
                    if not teoricaSemana and not aulaTeoricaPendente :
                        tipo_aula = 't'
                        teoricaSemana = True
                        aulaTeoricaPendente = False
                        carga_teorica_total -= horas_teoricas_semana
                elif dia_semana < DIAFIMSEMANA :
                    tipo_aula = 'p'
                    carga_horaria_total -= horas_teoricas_semana
                    #calendario.append({
                    #    'ano': ano_data,
                    #    'mes': str(mes_data),
                    #    'dia': dia_data,
                    #    'data': data_str,
                    #    'tipo_aula': tipo_aula,
                    #    'dia_semana': str(dia_semana)
                    #    })


                if periodoContinuo :
                    tipo_aula ='i'
            elif (dia_semana < DIAFIMSEMANA ) and (tipo_aula != 'feriado') and (tipo_aula != 't') :
                if carga_horaria_total > 0 :
                    if aulaTeoricaPendente and not teoricaSemana:
                        tipo_aula = 'T'
                        carga_teorica_total -= horas_teoricas_semana
                        aulaTeoricaPendente = False
                        teoricaSemana = True
                    else :
                        tipo_aula = 'p'
                        carga_horaria_total -= horas_teoricas_semana
                elif carga_teorica_total > 0 : # carga horarioa total ja concluiu. Mas ainda não as teoricas
                    tipo_aula = 'f'
                    carga_teorica_total -= horas_teoricas_semana

            if tipo_aula != 'feriado' :
                calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                  })

            if ((dia_semana==dia_semana_teorica or dia_semana_teorica ==-1)) and (tipo_aula == 'feriado' and not periodoContinuo) :
                # anteceder um dia a aula teorica
                if ( dia_semana <= 2 ) : # se for uma segunda, terca ou quarta com feriado, marcar pendencia
                    if not teoricaSemana :
                        aulaTeoricaPendente = True
                elif ( carga_teorica_total > 0 ) :
                    if not teoricaSemana and not aulaTeoricaPendente : # se nao tem nenhuma hora teorica na semana
                        for i in range(len(calendario)-1, -1, -1):
                            if int(calendario[i]['dia_semana']) >= DIAFIMSEMANA : # se estiver voltando semana, interrompe
                                aulaTeoricaPendente = True
                                break;
                            if calendario[i]['tipo_aula'] == 'p' :
                                aulaTeoricaPendente = False
                                teoricaSemana = True
                                calendario[i]['tipo_aula'] ='T';
                                carga_teorica_total -= horas_teoricas_semana
                                carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                                break;

            if tipo_aula == 'feriado' :
                tipo_aula = 'X'
                calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })
          else : #final de semana
            tipo_aula ='x'
            teoricaSemana = False
            calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })

        else : # se eh ferias ou recesso
            if ehferias( data_atual, ferias ):
                    tipo_aula = 'F'
                    calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                  })
            elif ehrecesso( data_str, recessos ) :
                if dia_semana < DIAFIMSEMANA :
                    if ( dia_semana <= 2 and (dia_semana == dia_semana_teorica)) : # se for uma segunda com recesso, marcar pendencia
                        if not teoricaSemana :
                            aulaTeoricaPendente = True
                    if ((dia_semana==dia_semana_teorica)  and not periodoContinuo) :
                        # anteceder um dia a aula teorica
                        if ( carga_teorica_total > 0 and not aulaTeoricaPendente and not teoricaSemana ) :
                            for i in range(len(calendario)-1, -1, -1):
                                if int(calendario[i]['dia_semana']) >= DIAFIMSEMANA : # se estiver voltando na semana anterior, interromper
                                    aulaTeoricaPendente = True
                                    break;
                                if calendario[i]['tipo_aula'] == 'p' :
                                    aulaTeoricaPendente = False
                                    teoricaSemana = True
                                    calendario[i]['tipo_aula'] ='T';
                                    carga_teorica_total -= horas_teoricas_semana
                                    carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                                    break;
                    if carga_horaria_total > 0 :
                        tipo_aula = 'r' # recesso - dia de atividade pratica
                        carga_horaria_total -= horas_teoricas_semana
                        calendario.append({
                          'ano': ano_data,
                          'mes': str(mes_data),
                          'dia': dia_data,
                          'data': data_str,
                          'tipo_aula': tipo_aula,
                          'dia_semana': str(dia_semana)
                        })

                    elif periodoContinuo :
                        tipo_aula = 'X'
                        calendario.append({
                              'ano': ano_data,
                              'mes': str(mes_data),
                              'dia': dia_data,
                              'data': data_str,
                              'tipo_aula': tipo_aula,
                              'dia_semana': str(dia_semana)
                            })
                    else : # nao eh periodo continuo mas eh recesso e aulas totais ja terminaram
                        # carga_teorica_total -= horas_teoricas_semana
                        tipo_aula = 'r' # recesso - dia de atividade pratica
                        # carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                        calendario.append({
                            'ano': ano_data,
                            'mes': str(mes_data),
                            'dia': dia_data,
                            'data': data_str,
                            'tipo_aula': tipo_aula,
                            'dia_semana': str(dia_semana)
                            })

                else : # final de semana
                    tipo_aula ='x'
                    calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })

        # Avançar para o próximo dia
        data_atual += timedelta(days=1)
      #  data_atual = datetime.strptime(data_atual, '%d-%m-%Y')


    data_final = data_atual - timedelta(days=1)
    return calendario, data_final
# -----------------------------------------------------------------------------------
def mostrar_calendario(calendario, chdia):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
        ]

    dia_semanaExtenso=['seg','ter','qua','qui','sex','sab','dom']
    dias = len(calendario)
    posicao = 0
    totalTeoricas = 0
    totalPraticas = 0
    resultados = []

    while posicao < dias:
        data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
        mes_atual = data_atual.month
        mudames = False
        teoricas, praticas = 0, 0
        resultado = f"{meses[mes_atual-1]};{data_atual.year};"

        while mudames == False and posicao < dias:
            data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
            dia_semana = dia_semanaExtenso[int(calendario[posicao]['dia_semana'])]
            tipo_aula = calendario[posicao]['tipo_aula']

            if posicao >= dias or data_atual.month != mes_atual:
                mudames = True
                break

            if tipo_aula == 't':
                teoricas += 1
                tipo_aula = 't'
            else:
                praticas += 1
                tipo_aula = 'p'

            resultado += f"{str(data_atual.day)}-{str(dia_semana)}-{str(tipo_aula)};"

            posicao += 1

        #resultado += f"Teoricas {meses[mes_atual-1]};{str(teoricas)};Praticas {meses[mes_atual-1]};{str(praticas)};Total;{(teoricas+praticas)*chdia}"
        resultado += f"{(teoricas+praticas)*chdia}"

        resultados.append(resultado)

        totalTeoricas += teoricas * chdia
        totalPraticas += praticas * chdia

    return totalTeoricas, totalPraticas, resultados
# -----------------------------------------------------------------------------------
def mostrar_calendarioCompleto(calendario, chdia):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
        ]

    dia_semanaExtenso=['2ª','3ª','4ª','5ª','6ª','s','d']
    dias = len(calendario)
    posicao = 0
    totalTeoricas = 0
    totalPraticas = 0
    resultados = []

    while posicao < dias:
        data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
        mes_atual = data_atual.month
        mudames = False
        teoricas, praticas = 0, 0
        resultado = f"{meses[mes_atual-1]};{data_atual.year};"

        while mudames == False and posicao < dias:
            data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
            dia_semana = dia_semanaExtenso[int(calendario[posicao]['dia_semana'])]
            tipo_aula = calendario[posicao]['tipo_aula']

            if posicao >= dias or data_atual.month != mes_atual:
                mudames = True
                break

            if tipo_aula == 't':    # aulas teoricas
                teoricas += 1
            if tipo_aula == 'T' :   # aulas de reposicao praticas
                teoricas += 1
            if tipo_aula == 'i' :   # aulas teoricas iniciais
                teoricas += 1
            if tipo_aula == 'f' :   # aulas teoricas finais
                teoricas += 1
            if tipo_aula == 'p':    # aulas praticas na empresa
                praticas += 1
            if tipo_aula == 'r' :   # recesso
                praticas += 1

            resultado += f"{str(data_atual.day)}-{str(dia_semana)}-{str(tipo_aula)};"

            posicao += 1

        resultado += f"{str(teoricas)};{str(praticas)};{(teoricas+praticas)*chdia}"
        # resultado += f"{(teoricas+praticas)*chdia}"

        resultados.append(resultado)

        totalTeoricas += teoricas * chdia
        totalPraticas += praticas * chdia

    return totalTeoricas, totalPraticas, resultados
# ------------------------------------------------------------
def listaFeriados( df,  nacional, estadual, municipal):
  df_nacional=df.loc[df['local'] == nacional ].reset_index()
  df_estadual=df.loc[df['local'] == estadual ].reset_index()
  df_municipal=df.loc[df['local'] == municipal ].reset_index()

  feriados =[]
  for i in range( len(df_nacional)) :
    feriados.extend( df_nacional['feriados'][i].split(','))
  for i in range( len(df_estadual)) :
    feriados.extend( df_estadual['feriados'][i].split(','))
  for i in range( len(df_municipal)) :
    feriados.extend( df_municipal['feriados'][i].split(','))
  return feriados
# ------------------------------------------------------------
def listaRecessos( df,  recesso):
  df_recesso=df.loc[df['local'] == recesso ].reset_index()
  recessos =[]
  for i in range( len(df_recesso)) :
    recessos.extend( df_recesso['feriados'][i].split(','))
  return recessos
# ------------------------------------
def ehferias ( data, ferias):
  if len(ferias[0]) == 0 :
      return False
  if data >= datetime.strptime(ferias[0], '%d-%m-%Y') and data <= datetime.strptime(ferias[1], '%d-%m-%Y'):
      return True
  else :
      return False
# ----------------------------------
def ehferiado( data, feriados ):
  for i in range( len(feriados)):
 #   if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(feriados[i],"%d-%m-%Y") :
    if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(feriados[i],"%d-%m-%Y") :
      return True
  return False

def ehrecesso ( data, recesso):
  for i in range(len(recesso)) :
#    if datetime.strptime(data, "%d-%m-%Y") == datetime.strptime(recesso[i],"%d-%m-%Y") :
    if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(recesso[i],"%d-%m-%Y") :
      return True
  return False

def ehcomplementar( data, complementar, semana, dia ) :
    if not complementar :
        return False
    else :
        return True


# -------------------------------------------
st.title( 'Calendário - Tela Inicial')
arquivo = st.file_uploader( 
    'Upload do arquivo de feriados e recessos:',
    type='csv')
if arquivo :
    df = pd.read_csv( arquivo )
    # df = pd.read_excel( arquivo )
    if st.button('Feriados e Recessos') :
        df1=df
        st.table(df1)
    if st.button('Ocultar tabela')  :
        df1=pd.DataFrame()
        st.table(df1)
        # st.dataframe( df )
    # st.text(curso, turno, municipio, data_inicio_curso, data_inicio_ferias, data_final_ferias, ch_total, ch_teorica, ch_inicial, horas_semana, dia_semana, semana_complementar, dia_complementar=processa( df ))
    curso, turno, municipio, data_inicio_curso, data_inicio_ferias, data_final_ferias, ch_total, ch_teorica, ch_inicial, horas_semana, dia_semana, semana_complementar, dia_complementar=inicia( df )

    
    dados = [
    "01;2023;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    "02;2024;01-02-T;02-03-t;03-04-t;04-05-p;05-06-t;06-07-t;07-08-T;08-09-t;09-10-t;10-11-t;11-12-t;12-13-T;13-14-t;14-15-p;15-16-t;16-17-t;17-18-t;18-19-t;19-20-T;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-t;26-27-T;27-28-t;28-01-r;22;06;31",
    "03;2025;01-02-t;02-03-p;03-04-t;04-05-x;05-06-T;06-07-t;07-08-p;08-09-t;09-10-t;10-11-t;11-12-T;12-13-t;13-14-p;14-15-t;15-16-t;16-17-T;17-18-t;18-19-x;19-20-t;20-21-t;21-22-p;22-23-t;23-24-t;24-25-t;25-26-T;26-27-t;27-28-p;28-29-t;29-30-t;30-31-t;31-01-r;26;05;31",
    ]
    mostra( dados, curso, turno, municipio, data_inicio_curso, data_inicio_ferias, data_final_ferias, ch_total, ch_teorica, ch_inicial, horas_semana, dia_semana, semana_complementar, dia_complementar )
else:
    st.error(' * Falta realizar UPLoad de arquivo .csv com feriados *')
