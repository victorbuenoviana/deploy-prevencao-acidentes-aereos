import pandas as pd
import plotly.express as px
import streamlit as st
import unidecode
import re
import plotly.express as px

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

    # st.title("Fatores Críticos")

    ocorr_fat_area, ocorr_fat_asp, ocorr_fat_cond, ocorr_fator = st.tabs(["Ocorrências[%] x Área do Fator", "Ocorrências[%] x Aspecto do Fator", "Ocorrências[%] x Fator Condicionante", "Ocorrências[%] x Fator"])

    with ocorr_fat_area:

        # Ocorrências[%] x Área do Fator
        df_ocorr_fat_area = df_ocorr["fator_area"].value_counts().sort_values(ascending=False)
        df_ocorr_fat_area = pd.DataFrame(df_ocorr_fat_area)
        df_ocorr_fat_area.reset_index(inplace=True)

        hist_ocorr_fat_area = px.bar(
            data_frame=df_ocorr_fat_area,
            x=df_ocorr_fat_area["fator_area"],
            y=(df_ocorr_fat_area["count"]/df_ocorr_fat_area["count"].sum())*100,
            title=f"Ocorrências[%] x Área do Fator",
            width=600,
            height=500,
            color_discrete_sequence=["#2570DC"],
            )
        hist_ocorr_fat_area.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            yaxis_showgrid=False,  # Remover linhas de grade do eixo y
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=10,  # margem esquerda
                r=10,  # margem direita
                b=0,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
        )
        hist_ocorr_fat_area.update_traces(
            hovertemplate='%{x} : %{y}%',
            text=(df_ocorr_fat_area["count"] / df_ocorr_fat_area["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            textposition='outside',
            )
        hist_ocorr_fat_area.update_xaxes(title = "", tickangle=45)
        hist_ocorr_fat_area.update_yaxes(visible=False)

        st.plotly_chart(hist_ocorr_fat_area, use_container_width=True)

    with ocorr_fat_asp:
        # Ocorrências[%] x Aspecto do Fator
        df_ocorr_fat_asp = df_ocorr["fator_aspecto"].value_counts().sort_values(ascending=False)
        df_ocorr_fat_asp = pd.DataFrame(df_ocorr_fat_asp)
        df_ocorr_fat_asp = df_ocorr_fat_asp.head(6)
        df_ocorr_fat_asp.reset_index(inplace=True)

        hist_ocorr_fat_asp = px.bar(
            data_frame=df_ocorr_fat_asp,
            x=df_ocorr_fat_asp["fator_aspecto"],
            y=(df_ocorr_fat_asp["count"]/df_ocorr_fat_asp["count"].sum())*100,
            title=f"Ocorrências[%] x Aspecto do Fator",
            width=600,
            height=600,
            color_discrete_sequence=["#2570DC"],
            )
        hist_ocorr_fat_asp.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            yaxis_showgrid=False,  # Remover linhas de grade do eixo y
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=10,  # margem esquerda
                r=10,  # margem direita
                b=0,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
        )
        hist_ocorr_fat_asp.update_traces(
            hovertemplate='%{x} : %{y}%',
            text=(df_ocorr_fat_asp["count"] / df_ocorr_fat_asp["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            textposition='outside',
            )
        hist_ocorr_fat_asp.update_xaxes(title = "", tickangle=45)
        hist_ocorr_fat_asp.update_yaxes(visible=False)

        st.plotly_chart(hist_ocorr_fat_asp, use_container_width=True)

    with ocorr_fat_cond:

        # Ocorrências[%] x Fator Condicionante
        df_ocorr_fat_cond = df_ocorr["fator_condicionante"].value_counts().sort_values(ascending=False)
        df_ocorr_fat_cond = pd.DataFrame(df_ocorr_fat_cond)
        df_ocorr_fat_cond.reset_index(inplace=True)

        hist_ocorr_fat_cond = px.bar(
            data_frame=df_ocorr_fat_cond,
            x=df_ocorr_fat_cond["fator_condicionante"],
            y=(df_ocorr_fat_cond["count"]/df_ocorr_fat_cond["count"].sum())*100,
            title=f"Ocorrências[%] x Fator Condicionante",
            width=600,
            height=550,
            color_discrete_sequence=["#2570DC"],
            )
        hist_ocorr_fat_cond.update_layout(
            title_x = 0.5,
            title_y = 0.95,
            plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
            paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
            xaxis_showgrid=False,  # Remover linhas de grade do eixo x
            yaxis_showgrid=False,  # Remover linhas de grade do eixo y
            bargap = 0.1,
            xaxis=dict(
                tickmode='linear',  # Modo linear
                tick0=0,  # Posição inicial dos ticks
                dtick=1  # Passo entre os ticks
            ),
            margin=dict(
                l=10,  # margem esquerda
                r=10,  # margem direita
                b=0,  # margem inferior
                t=35,  # margem superior
                pad=0  # preenchimento
            ),
        )
        hist_ocorr_fat_cond.update_traces(
            hovertemplate='%{x} : %{y}%',
            text=(df_ocorr_fat_cond["count"] / df_ocorr_fat_cond["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
            textposition='outside',
            )
        hist_ocorr_fat_cond.update_xaxes(title = "", tickangle=45)
        hist_ocorr_fat_cond.update_yaxes(visible=False)

        st.plotly_chart(hist_ocorr_fat_cond, use_container_width=True)

    with ocorr_fator:

            # Ocorrências[%] x Fator
            df_ocorr_fator = df_ocorr["fator_nome"].value_counts().sort_values(ascending=False)
            df_ocorr_fator = pd.DataFrame(df_ocorr_fator)
            df_ocorr_fator = df_ocorr_fator.head(15)
            df_ocorr_fator.reset_index(inplace=True)

            hist_ocorr_fator = px.bar(
                data_frame=df_ocorr_fator,
                x=df_ocorr_fator["fator_nome"],
                y=(df_ocorr_fator["count"]/df_ocorr_fator["count"].sum())*100,
                title=f"Ocorrências[%] x Fator",
                width=600,
                height=500,
                color_discrete_sequence=["#2570DC"],
                )
            hist_ocorr_fator.update_layout(
                title_x = 0.5,
                title_y = 0.95,
                plot_bgcolor='#BDE4F4',  # Cor de fundo do gráfico
                paper_bgcolor='#BDE4F4',  # Cor de fundo do papel
                xaxis_showgrid=False,  # Remover linhas de grade do eixo x
                yaxis_showgrid=False,  # Remover linhas de grade do eixo y
                bargap = 0.1,
                xaxis=dict(
                    tickmode='linear',  # Modo linear
                    tick0=0,  # Posição inicial dos ticks
                    dtick=1  # Passo entre os ticks
                ),
                margin=dict(
                    l=10,  # margem esquerda
                    r=10,  # margem direita
                    b=0,  # margem inferior
                    t=35,  # margem superior
                    pad=0  # preenchimento
                ),
            )
            hist_ocorr_fator.update_traces(
                hovertemplate='%{x} : %{y}%',
                text=(df_ocorr_fator["count"] / df_ocorr_fator["count"].sum() * 100).round(0).astype(int).astype(str) + "%",
                textposition='outside',
                )
            hist_ocorr_fator.update_xaxes(title = "", tickangle=45)
            hist_ocorr_fator.update_yaxes(visible=False)

            st.plotly_chart(hist_ocorr_fator, use_container_width=True)
