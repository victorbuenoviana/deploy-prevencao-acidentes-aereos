import pandas as pd
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

    # st.title("Danos e Fatalidades")

    # Analisando a Correlação entre Danos e Fatalidades
    df_ocorr_danos_fatal = df_ocorr.loc[df_ocorr["ocorrencia_classificacao"] == 'acidente',:]
    df_ocorr_danos_fatal['aeronave_nivel_dano'] = df_ocorr_danos_fatal['aeronave_nivel_dano'].astype(str)
    df_ocorr_danos_fatal = df_ocorr_danos_fatal[df_ocorr_danos_fatal['aeronave_nivel_dano'] != 'desconhecido']
    df_ocorr_danos_fatal = df_ocorr_danos_fatal.loc[:,['aeronave_nivel_dano', 'aeronave_fatalidades_total']]
    df_ocorr_danos_fatal = df_ocorr_danos_fatal.groupby(by=['aeronave_nivel_dano', 'aeronave_fatalidades_total']).value_counts()
    df_ocorr_danos_fatal = df_ocorr_danos_fatal.reset_index()
    df_ocorr_danos_fatal["aeronave_fatalidades_total"] = df_ocorr_danos_fatal["aeronave_fatalidades_total"].astype(str)

    grf_danos_fatal = px.bar(
        data_frame=df_ocorr_danos_fatal,
        x=df_ocorr_danos_fatal["aeronave_fatalidades_total"],
        y=df_ocorr_danos_fatal["count"],
        color=df_ocorr_danos_fatal["aeronave_nivel_dano"],
        title= 'Danos e Fatalidades',
        barmode='group',
        height=500,
        width=800,
        )
    grf_danos_fatal.update_layout(
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
    grf_danos_fatal.update_traces(
        hovertemplate='%{y}',
        text=df_ocorr_danos_fatal["count"],
        textposition='outside',
        textangle=270,
        )
    grf_danos_fatal.update_xaxes(title = "")
    grf_danos_fatal.update_yaxes(visible=False)

    st.plotly_chart(grf_danos_fatal, use_container_width=True)