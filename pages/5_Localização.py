import pandas as pd
import streamlit as st
import unidecode
import re
import plotly.express as px

import folium
from folium.plugins import HeatMap
from folium.plugins import MousePosition
from folium import plugins

from streamlit_folium import folium_static

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

    # st.title("Distribuição Geográfica das Ocorrências")

    # obtendo a contagem de ocorrências por coordenada
    df_ocorr_ocorr_localizacao = df_ocorr[["ocorrencia_latitude", "ocorrencia_longitude", "ocorrencia_uf", "ocorrencia_cidade"]]
    df_ocorr_ocorr_localizacao["localizacao"] = df_ocorr_ocorr_localizacao.apply(lambda linha : (linha["ocorrencia_latitude"], linha["ocorrencia_longitude"]),axis=1)
    df_ocorr_ocorr_localizacao = pd.DataFrame(df_ocorr_ocorr_localizacao.value_counts())
    df_ocorr_ocorr_localizacao.reset_index(inplace=True)

    # removendo registros com localizações fora da região analisada
    df_ocorr_ocorr_localizacao = df_ocorr_ocorr_localizacao.drop(df_ocorr_ocorr_localizacao[df_ocorr_ocorr_localizacao["ocorrencia_latitude"] > 5.7].index, axis=0)
    df_ocorr_ocorr_localizacao = df_ocorr_ocorr_localizacao.drop(df_ocorr_ocorr_localizacao[df_ocorr_ocorr_localizacao["ocorrencia_longitude"] > -32.7].index, axis=0)
    df_ocorr_ocorr_localizacao = df_ocorr_ocorr_localizacao.drop(df_ocorr_ocorr_localizacao[df_ocorr_ocorr_localizacao["localizacao"] == (0.0, 0.0)].index, axis=0)

    # gerando mapa base
    mapa = folium.Map(
        width="100%",
        height="100%",
        location=[-15.7801, -47.9292], 
        zoom_start=5,
        tiles='cartodbpositron',)

    # adicionando exibição de coordenadas
    MousePosition().add_to(mapa)

    # gerando uma lista com a contagem de ocorrências por par de coordenadas
    coordenadas = df_ocorr_ocorr_localizacao[["ocorrencia_latitude", "ocorrencia_longitude", "count"]].values.tolist()

    # Criando tooltips com as informações
    for i in range(0, len(df_ocorr_ocorr_localizacao)):
        folium.Circle(
            location = [df_ocorr_ocorr_localizacao.iloc[i]['ocorrencia_latitude'], df_ocorr_ocorr_localizacao.iloc[i]['ocorrencia_longitude']],
            color = '#0000cc',
            fill = '#A4D3EE',
            tooltip='<li><b>Estado: </b>' + str(df_ocorr_ocorr_localizacao.iloc[i]["ocorrencia_uf"]) +
                    '<li><b>Município: </b>' + str(df_ocorr_ocorr_localizacao.iloc[i]["ocorrencia_cidade"]) +
                    '<li><b>Ocorrências Aeronáuticas: </b>' + str(df_ocorr_ocorr_localizacao.iloc[i]['count']),
            radius=10
        ).add_to(mapa)

    # gerando mapar de calor
    HeatMap(coordenadas, radius=15).add_to(mapa)

    folium_static(mapa, 
                  width=1024, 
                  height=500,
                  )
