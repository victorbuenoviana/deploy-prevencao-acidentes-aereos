import pandas as pd
import plotly.express as px
import streamlit as st
import unidecode
import re
import plotly.express as px


# Configurando pagina
st.set_page_config(
   page_title="Ocorrências Aeronáuticas",
   page_icon= r"\img\logo_cenipa.png",
   layout="wide",
   initial_sidebar_state="expanded",
)

with open(r"styles.css") as estilo:
    st.markdown(
        f"<style>{estilo.read()}</style>",
        unsafe_allow_html=True,
        )

# importando dataset
df_ocorr = pd.read_csv(r'df_ocorrencias_aeronauticas_tratado.csv')

# definindo os tipos de dados de cada coluna
def normalizar_string(string):

    string_normalizada = string.strip() # remove espaços em branco no início e no final da string
    string_normalizada = string_normalizada.lower() # transforma todas as letras em minúsculas
    string_normalizada = unidecode.unidecode(string_normalizada)
    string_normalizada = re.sub(r'[^\w\s-]', '', string_normalizada)

    return string_normalizada

def tratar_tipos_dados():
    df_ocorr["ocorrencia_latitude"] = df_ocorr["ocorrencia_latitude"].apply(lambda x: ".".join(str(x).split(".")[0:2]).replace("°","")).astype(float)        
    df_ocorr["ocorrencia_longitude"] = df_ocorr["ocorrencia_longitude"].apply(lambda x: ".".join(str(x).split(".")[0:2]).replace("°","")).astype(float)  
    df_ocorr["ocorrencia_classificacao"] = df_ocorr["ocorrencia_classificacao"].apply(normalizar_string).astype("category")              
    df_ocorr["ocorrencia_cidade"] = df_ocorr["ocorrencia_cidade"].apply(normalizar_string).astype("category")        
    df_ocorr["ocorrencia_uf"] = df_ocorr["ocorrencia_uf"].apply(normalizar_string).astype("category")                        
    df_ocorr["ocorrencia_aerodromo"] = df_ocorr["ocorrencia_aerodromo"].apply(lambda x: x.strip().lower()).astype("category")           
    df_ocorr["total_recomendacoes"] = df_ocorr["total_recomendacoes"].astype(int)            
    df_ocorr["total_aeronaves_envolvidas"] = df_ocorr["total_aeronaves_envolvidas"].astype(int)     
    df_ocorr["ocorrencia_saida_pista"] = df_ocorr["ocorrencia_saida_pista"].apply(lambda x: x.strip().lower()).astype("category")         
    df_ocorr["ocorrencia_tipo"] = df_ocorr["ocorrencia_tipo"].apply(normalizar_string).astype("category")            
    df_ocorr["ocorrencia_tipo_categoria"] = df_ocorr["ocorrencia_tipo_categoria"].apply(normalizar_string).astype("category")      
    df_ocorr["taxonomia_tipo_icao"] = df_ocorr["taxonomia_tipo_icao"].apply(lambda x: x.strip()).astype("category")        
    df_ocorr["recomendacao_status"] = df_ocorr["recomendacao_status"].apply(lambda x: x.strip().lower()).astype("category")            
    df_ocorr["recomendacao_destinatario"] = df_ocorr["recomendacao_destinatario"].apply(lambda x: x.strip().lower()).astype("category")                
    df_ocorr["aeronave_tipo_veiculo"] = df_ocorr["aeronave_tipo_veiculo"].apply(normalizar_string).astype("category")          
    df_ocorr["aeronave_fabricante"] = df_ocorr["aeronave_fabricante"].apply(normalizar_string).astype("category")            
    df_ocorr["aeronave_modelo"] = df_ocorr["aeronave_modelo"].apply(lambda x: x.strip().lower()).astype("category")                        
    df_ocorr["aeronave_motor_tipo"] = df_ocorr["aeronave_motor_tipo"].apply(normalizar_string).astype("category")            
    df_ocorr["aeronave_motor_quantidade"] = df_ocorr["aeronave_motor_quantidade"].apply(normalizar_string).astype("category")       
    df_ocorr["aeronave_voo_origem"] = df_ocorr["aeronave_voo_origem"].apply(lambda x: x.strip().lower()).astype(str).astype("category")             
    df_ocorr["aeronave_voo_destino"] = df_ocorr["aeronave_voo_destino"].apply(lambda x: x.strip().lower()).astype(str).astype("category")            
    df_ocorr["aeronave_fase_operacao"] = df_ocorr["aeronave_fase_operacao"].apply(normalizar_string).astype("category")         
    df_ocorr["aeronave_tipo_operacao"] = df_ocorr["aeronave_tipo_operacao"].apply(normalizar_string).astype("category")         
    df_ocorr["aeronave_nivel_dano"] = df_ocorr["aeronave_nivel_dano"].apply(normalizar_string).astype("category")            
    df_ocorr["aeronave_fatalidades_total"] = df_ocorr["aeronave_fatalidades_total"].astype(int)      
    df_ocorr["fator_nome"] = df_ocorr["fator_nome"].apply(normalizar_string).astype("category")                    
    df_ocorr["fator_aspecto"] = df_ocorr["fator_aspecto"].apply(normalizar_string).astype("category")                  
    df_ocorr["fator_condicionante"] = df_ocorr["fator_condicionante"].apply(normalizar_string).astype("category")            
    df_ocorr["fator_area"] = df_ocorr["fator_area"].apply(normalizar_string).astype("category")
    df_ocorr["ocorrencia_data_hora"] = pd.to_datetime(df_ocorr["ocorrencia_data_hora"])

tratar_tipos_dados()

# Configurando Layout da pagina
with st.container():

    # st.title("Ocorrências por Período")

    ocorr_hora, ocorr_dia_semana, ocorr_dia_mes, ocorr_mes, ocorr_ano = st.tabs(["Ocorrências x Hora", "Ocorrências x Dia da Semana", "Ocorrências x Dia do Mês", "Ocorrências x Mês", "Ocorrências x Ano"])

    with ocorr_hora:
        
        df_ocorr["ocorrencia_hora"] = df_ocorr["ocorrencia_data_hora"].dt.hour
        df_ocorr_ocorr_hora = df_ocorr["ocorrencia_hora"].value_counts().sort_index()
        df_ocorr_ocorr_hora = pd.DataFrame(df_ocorr_ocorr_hora)
        df_ocorr_ocorr_hora.reset_index(inplace=True)
        
        grf_ocorr_hora = px.line(
            data_frame=df_ocorr_ocorr_hora,
            x=df_ocorr_ocorr_hora["ocorrencia_hora"].apply(lambda x : f"{x}h"),
            y=(df_ocorr_ocorr_hora["count"]/df_ocorr_ocorr_hora["count"].sum())*100,
            title=f"Ocorrências x Hora",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_hora.update_layout(
            title_x = 0.5,
            title_y = 0.9,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            # yaxis_showgrid=False,  # Remover linhas de grade do eixo y
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=20,  # margem esquerda
                r=20,  # margem direita
                b=20,  # margem inferior
                t=0,  # margem superior
                pad=0  # preenchimento
            ),
        )
        grf_ocorr_hora.update_traces(
            hovertemplate='%{x} : %{y}% ocorrências',
            fill='tozeroy', 
            # text=(df_ocorr_ocorr_hora["count"] / df_ocorr_ocorr_hora["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            # mode='lines+text', 
            # textposition='top center',
            )
        grf_ocorr_hora.update_xaxes(title = "")
        grf_ocorr_hora.update_yaxes(title = "Ocorrências [%]")
        
        grf_ocorr_hora = px.line(
            data_frame=df_ocorr_ocorr_hora,
            x=df_ocorr_ocorr_hora["ocorrencia_hora"].apply(lambda x : f"{x}h"),
            y=(df_ocorr_ocorr_hora["count"]/df_ocorr_ocorr_hora["count"].sum())*100,
            title=f"Ocorrências x Hora",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_hora.update_layout(
            title_x = 0.5,
            title_y = 0.96,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            # yaxis_showgrid=False,  # Remover linhas de grade do eixo y
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=20,  # margem esquerda
                r=20,  # margem direita
                b=20,  # margem inferior
                t=0,  # margem superior
                pad=0  # preenchimento
            ),
        )
        grf_ocorr_hora.update_traces(
            hovertemplate='%{x} : %{y}% ocorrências',
            fill='tozeroy', 
            text=(df_ocorr_ocorr_hora["count"] / df_ocorr_ocorr_hora["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            mode='lines+text', 
            textposition='top center',
            )
        grf_ocorr_hora.update_xaxes(title = "")
        grf_ocorr_hora.update_yaxes(visible=False)

        st.plotly_chart(grf_ocorr_hora, use_container_width=True)

    with ocorr_dia_semana:  

        # Percentural de Ocorrências x Dia[semana]
        df_ocorr["ocorrencia_dia_semana"] = df_ocorr["ocorrencia_data_hora"].dt.day_of_week

        def converter_numero_dia_semana(num_dia:int) -> str:
            match num_dia:
                case 0:return "domingo"
                case 1:return "segunda"
                case 2:return "terça"
                case 3:return "quarta"
                case 4:return "quinta"
                case 5:return "sexta"
                case 6:return "sabado"

        df_ocorr_ocorr_dia_semana = df_ocorr["ocorrencia_dia_semana"].value_counts().sort_index()
        df_ocorr_ocorr_dia_semana = pd.DataFrame(df_ocorr_ocorr_dia_semana)
        df_ocorr_ocorr_dia_semana.reset_index(inplace=True)
        df_ocorr_ocorr_dia_semana["ocorrencia_dia_semana"] = df_ocorr_ocorr_dia_semana["ocorrencia_dia_semana"].map(converter_numero_dia_semana)

        grf_ocorr_dia_semana = px.line(
            data_frame=df_ocorr_ocorr_dia_semana,
            x=df_ocorr_ocorr_dia_semana["ocorrencia_dia_semana"],
            y=(df_ocorr_ocorr_dia_semana["count"]/df_ocorr_ocorr_dia_semana["count"].sum())*100,
            title=f"Ocorrências x Dia[semana]",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_dia_semana.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=20,  # margem esquerda
                r=20,  # margem direita
                b=20,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
        )
        grf_ocorr_dia_semana.update_traces(
            hovertemplate='%{x} : %{y}% ocorrências',
            fill='tozeroy', 
            text=(df_ocorr_ocorr_dia_semana["count"] / df_ocorr_ocorr_dia_semana["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            mode='lines+text', 
            textposition='top center',
            )
        grf_ocorr_dia_semana.update_xaxes(title = "")
        grf_ocorr_dia_semana.update_yaxes(visible=False)

        st.plotly_chart(grf_ocorr_dia_semana, use_container_width=True)
        
    with ocorr_dia_mes:

        # Percentural de Ocorrências x Dia[mês]
        df_ocorr["ocorrencia_dia_mes"] = df_ocorr["ocorrencia_data_hora"].dt.day
        df_ocorr_ocorr_dia_mes = df_ocorr["ocorrencia_dia_mes"].value_counts().sort_index()
        df_ocorr_ocorr_dia_mes = pd.DataFrame(df_ocorr_ocorr_dia_mes)
        df_ocorr_ocorr_dia_mes.reset_index(inplace=True)

        grf_ocorr_dia_mes = px.line(
            data_frame=df_ocorr_ocorr_dia_mes,
            x=df_ocorr_ocorr_dia_mes["ocorrencia_dia_mes"],
            y=(df_ocorr_ocorr_dia_mes["count"]/df_ocorr_ocorr_dia_mes["count"].sum())*100,
            title=f"Ocorrências x Dia[mês]",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_dia_mes.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=20,  # margem esquerda
                r=20,  # margem direita
                b=20,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
        )
        grf_ocorr_dia_mes.update_traces(
            hovertemplate='Dia %{x} : %{y} ocorrências',
            fill='tozeroy', 
            text=(df_ocorr_ocorr_dia_mes["count"] / df_ocorr_ocorr_dia_mes["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            mode='lines+text', 
            textposition='top center',
            )
        grf_ocorr_dia_mes.update_xaxes(title = "")
        grf_ocorr_dia_mes.update_yaxes(visible=False)

        st.plotly_chart(grf_ocorr_dia_mes, use_container_width=True)

    with ocorr_mes:

        # Percentural de Ocorrências x Mês
        df_ocorr["ocorrencia_mes"] = df_ocorr["ocorrencia_data_hora"].dt.month

        def converter_numero_nome_mes(num_mes:int) -> str:
            match num_mes:
                case 1:return "janeiro"
                case 2:return "fevereiro"
                case 3:return "marco"
                case 4:return "abril"
                case 5:return "maio"
                case 6:return "junho"
                case 7:return "julho"
                case 8:return "agosto"
                case 9:return "setembro"
                case 10:return "outubro"
                case 11:return "novembro"
                case 12:return "dezembro"

        df_ocorr_ocorr_mes = df_ocorr["ocorrencia_mes"].value_counts().sort_index()
        df_ocorr_ocorr_mes = pd.DataFrame(df_ocorr_ocorr_mes)
        df_ocorr_ocorr_mes.reset_index(inplace=True)
        df_ocorr_ocorr_mes["ocorrencia_mes"] = df_ocorr_ocorr_mes["ocorrencia_mes"].map(converter_numero_nome_mes)

        grf_ocorr_mes = px.line(
            data_frame=df_ocorr_ocorr_mes,
            x=df_ocorr_ocorr_mes["ocorrencia_mes"],
            y=(df_ocorr_ocorr_mes["count"]/df_ocorr_ocorr_mes["count"].sum())*100,
            title=f"Ocorrências[%] x Mês",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_mes.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=10,  # margem esquerda
                r=25,  # margem direita
                b=0,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
            # xaxis_range=['janeiro','dezembro'],
        )
        grf_ocorr_mes.update_traces(
            hovertemplate='%{x} : %{y}% ocorrências',
            fill='tozeroy', 
            text=(df_ocorr_ocorr_mes["count"] / df_ocorr_ocorr_mes["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            mode='lines+text', 
            textposition='top center',
            )
        grf_ocorr_mes.update_xaxes(title = "", tickangle=45)
        grf_ocorr_mes.update_yaxes(visible=False)

        st.plotly_chart(grf_ocorr_mes, use_container_width=True)

    with ocorr_ano:

        # Percentural de Ocorrências x Ano
        df_ocorr["ocorrencia_ano"] = df_ocorr["ocorrencia_data_hora"].dt.year
        df_ocorr_ocorr_ano = df_ocorr["ocorrencia_ano"].value_counts().sort_index()
        df_ocorr_ocorr_ano = pd.DataFrame(df_ocorr_ocorr_ano)
        df_ocorr_ocorr_ano.reset_index(inplace=True)

        grf_ocorr_ano = px.line(
            data_frame=df_ocorr_ocorr_ano,
            x=df_ocorr_ocorr_ano["ocorrencia_ano"],
            y=(df_ocorr_ocorr_ano["count"]/df_ocorr_ocorr_ano["count"].sum())*100,
            title=f"Ocorrências[%] x Ano",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        grf_ocorr_ano.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=10,  # margem esquerda
                r=40,  # margem direita
                b=0,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
            xaxis_range=[2012, 2022],
        )
        grf_ocorr_ano.update_traces(
            hovertemplate='%{x} : %{y}% ocorrências', 
            fill='tozeroy', 
            text=(df_ocorr_ocorr_ano["count"] / df_ocorr_ocorr_ano["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            mode='lines+text', 
            textposition='top center',
            )
        grf_ocorr_ano.update_xaxes(title = "", tickangle=45)
        grf_ocorr_ano.update_yaxes(visible=False)

        st.plotly_chart(grf_ocorr_ano, use_container_width=True)
