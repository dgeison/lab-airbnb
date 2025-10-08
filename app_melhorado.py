#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🏠 Airbnb Rio - Predição de Preços (Versão Melhorada)
=======================================================

Aplicação Streamlit avançada para predição de preços de imóveis Airbnb no Rio de Janeiro.
Inclui interface melhorada, validações e funcionalidades extras.

Autor: Projeto Airbnb Rio
Data: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# =======================
# CONFIGURAÇÃO DA PÁGINA
# =======================

st.set_page_config(
    page_title="🏠 Airbnb Rio - Predição de Preços",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar visual
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF5A5F 0%, #00A699 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF5A5F;
        margin: 0.5rem 0;
    }
    .prediction-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.2em;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =======================
# FUNÇÕES AUXILIARES
# =======================

@st.cache_data
def carregar_modelo():
    """Carrega o modelo treinado com cache para performance"""
    if os.path.exists('modelo.joblib'):
        try:
            modelo = joblib.load('modelo.joblib')
            return modelo, "✅ Modelo carregado com sucesso!"
        except Exception as e:
            return None, f"❌ Erro ao carregar modelo: {str(e)}"
    else:
        return None, "⚠️ Arquivo 'modelo.joblib' não encontrado!"

def validar_inputs(dados):
    """Valida os inputs do usuário"""
    erros = []
    
    if dados['accommodates'] <= 0:
        erros.append("🚫 Número de hóspedes deve ser maior que 0")
    
    if dados['latitude'] == 0 and dados['longitude'] == 0:
        erros.append("📍 Por favor, informe a localização (latitude/longitude)")
    
    if dados['accommodates'] < dados['bedrooms']:
        erros.append("🛏️ Número de hóspedes não pode ser menor que quartos")
    
    return erros

def criar_previsao_chart(preco_previsto):
    """Cria gráfico visual da previsão"""
    ranges = {
        'Econômico': (0, 100),
        'Moderado': (100, 300),
        'Premium': (300, 600),
        'Luxo': (600, float('inf'))
    }
    
    categoria = 'Luxo'
    for cat, (min_val, max_val) in ranges.items():
        if min_val <= preco_previsto < max_val:
            categoria = cat
            break
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = preco_previsto,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Categoria: {categoria}"},
        delta = {'reference': 200},
        gauge = {
            'axis': {'range': [None, 1000]},
            'bar': {'color': "#FF5A5F"},
            'steps': [
                {'range': [0, 100], 'color': "lightgray"},
                {'range': [100, 300], 'color': "gray"},
                {'range': [300, 600], 'color': "lightblue"},
                {'range': [600, 1000], 'color': "gold"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': preco_previsto
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

# =======================
# LAYOUT PRINCIPAL
# =======================

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏠 Airbnb Rio - Predição de Preços</h1>
    <p>Inteligência Artificial para precificação inteligente de imóveis</p>
</div>
""", unsafe_allow_html=True)

# Carregamento do modelo
modelo, status_modelo = carregar_modelo()
st.sidebar.markdown("### 🤖 Status do Modelo")
st.sidebar.info(status_modelo)

# =======================
# SIDEBAR - INFORMAÇÕES
# =======================

st.sidebar.markdown("### 📊 Sobre o Projeto")
st.sidebar.markdown("""
- **Dataset**: +600K propriedades
- **Algoritmo**: ExtraTrees Regressor
- **Precisão**: R² > 77%
- **Features**: 32 variáveis
""")

st.sidebar.markdown("### 🎯 Como Usar")
st.sidebar.markdown("""
1. 📍 Informe a localização
2. 🏡 Configure o imóvel
3. 📅 Escolha data/período
4. 🔮 Clique em 'Prever Preço'
""")

# =======================
# FORMULÁRIO PRINCIPAL
# =======================

# Inicializar variáveis
x_numericos = {
    'latitude': 0, 'longitude': 0, 'accommodates': 1, 'bathrooms': 1, 
    'bedrooms': 1, 'beds': 1, 'extra_people': 0, 'minimum_nights': 1, 
    'ano': 2024, 'mes': 1, 'n_amenities': 5, 'host_listings_count': 1
}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {
    'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 
                     'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
    'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
    'cancelation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
}

# Criar dicionário para features categóricas
dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0

# Interface dividida em abas
tab1, tab2, tab3 = st.tabs(["🏡 Configurar Imóvel", "📊 Análise", "ℹ️ Ajuda"])

with tab1:
    # LOCALIZAÇÃO
    st.markdown("### 📍 Localização")
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input(
            'Latitude', 
            step=0.00001, 
            value=-22.9068,  # Centro do Rio
            format="%.5f",
            help="Coordenada de latitude (exemplo: -22.9068 para Rio)"
        )
        x_numericos['latitude'] = latitude
    
    with col2:
        longitude = st.number_input(
            'Longitude', 
            step=0.00001, 
            value=-43.1729,  # Centro do Rio
            format="%.5f",
            help="Coordenada de longitude (exemplo: -43.1729 para Rio)"
        )
        x_numericos['longitude'] = longitude
    
    # CARACTERÍSTICAS DO IMÓVEL
    st.markdown("### 🏡 Características do Imóvel")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        accommodates = st.selectbox('👥 Hóspedes', range(1, 17), index=1)
        x_numericos['accommodates'] = accommodates
    
    with col2:
        bedrooms = st.selectbox('🛏️ Quartos', range(0, 11), index=1)
        x_numericos['bedrooms'] = bedrooms
    
    with col3:
        bathrooms = st.selectbox('🚿 Banheiros', [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6], index=1)
        x_numericos['bathrooms'] = bathrooms
    
    with col4:
        beds = st.selectbox('🛌 Camas', range(1, 17), index=1)
        x_numericos['beds'] = beds
    
    # TIPO DE PROPRIEDADE E QUARTO
    st.markdown("### 🏠 Tipo de Propriedade")
    col1, col2 = st.columns(2)
    
    with col1:
        property_type = st.selectbox('🏘️ Tipo de Propriedade', x_listas['property_type'])
        dicionario[f'property_type_{property_type}'] = 1
    
    with col2:
        room_type = st.selectbox('🚪 Tipo de Quarto', x_listas['room_type'])
        dicionario[f'room_type_{room_type}'] = 1
    
    # CONFIGURAÇÕES AVANÇADAS
    st.markdown("### ⚙️ Configurações Avançadas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        extra_people = st.number_input('💰 Taxa Extra/Pessoa (R$)', min_value=0.0, value=0.0, step=10.0)
        x_numericos['extra_people'] = extra_people
        
        minimum_nights = st.selectbox('🌙 Noites Mínimas', range(1, 31), index=0)
        x_numericos['minimum_nights'] = minimum_nights
    
    with col2:
        n_amenities = st.slider('🎯 Amenidades', 0, 50, 10)
        x_numericos['n_amenities'] = n_amenities
        
        host_listings_count = st.selectbox('📋 Listagens do Host', range(1, 101), index=0)
        x_numericos['host_listings_count'] = host_listings_count
    
    with col3:
        cancelation_policy = st.selectbox('📜 Política Cancelamento', x_listas['cancelation_policy'], index=1)
        dicionario[f'cancelation_policy_{cancelation_policy}'] = 1
        
        host_is_superhost = st.checkbox('⭐ Host é Superhost')
        x_tf['host_is_superhost'] = 1 if host_is_superhost else 0
        
        instant_bookable = st.checkbox('⚡ Reserva Instantânea')
        x_tf['instant_bookable'] = 1 if instant_bookable else 0
    
    # DATA
    st.markdown("### 📅 Período")
    col1, col2 = st.columns(2)
    
    with col1:
        ano = st.selectbox('📅 Ano', range(2024, 2031), index=0)
        x_numericos['ano'] = ano
    
    with col2:
        mes = st.selectbox('📆 Mês', range(1, 13), index=0)
        x_numericos['mes'] = mes
    
    # BOTÃO DE PREDIÇÃO
    st.markdown("---")
    
    if st.button('🔮 Prever Preço do Imóvel', type="primary", use_container_width=True):
        if modelo is None:
            st.error("❌ Não é possível fazer predições sem o modelo treinado!")
            st.info("💡 Execute o notebook '1_analise_e_treinamento.ipynb' para treinar e salvar o modelo.")
        else:
            # Validar inputs
            dados_completos = {**x_numericos, **x_tf}
            erros = validar_inputs(dados_completos)
            
            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                # Fazer predição
                try:
                    dicionario.update(x_numericos)
                    dicionario.update(x_tf)
                    valores_x = pd.DataFrame(dicionario, index=[0])
                    preco = modelo.predict(valores_x)[0]
                    
                    # Exibir resultado
                    st.markdown("""
                    <div class="prediction-result">
                        <h2>💰 Preço Predito</h2>
                        <h1>R$ {:.2f}</h1>
                        <p>por noite</p>
                    </div>
                    """.format(preco), unsafe_allow_html=True)
                    
                    # Gráfico gauge
                    fig = criar_previsao_chart(preco)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Estatísticas adicionais
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("💵 Preço/Noite", f"R$ {preco:.2f}")
                    with col2:
                        st.metric("📅 Preço Semanal", f"R$ {preco * 7:.2f}")
                    with col3:
                        st.metric("📆 Preço Mensal", f"R$ {preco * 30:.2f}")
                    with col4:
                        receita_anual = preco * 365 * 0.7  # 70% ocupação
                        st.metric("📈 Receita Anual Est.", f"R$ {receita_anual:,.0f}")
                    
                except Exception as e:
                    st.error(f"❌ Erro na predição: {str(e)}")

with tab2:
    st.markdown("### 📊 Análise de Mercado")
    st.info("🚧 Funcionalidade em desenvolvimento - Em breve análises comparativas do mercado!")

with tab3:
    st.markdown("### ℹ️ Como Usar Esta Aplicação")
    
    st.markdown("""
    #### 🎯 Objetivo
    Esta aplicação utiliza Inteligência Artificial para prever preços de imóveis Airbnb no Rio de Janeiro.
    
    #### 📋 Passos para Usar:
    1. **📍 Localização**: Informe as coordenadas GPS (use Google Maps se necessário)
    2. **🏡 Características**: Configure quartos, banheiros, capacidade, etc.
    3. **🏠 Tipo**: Escolha o tipo de propriedade e quarto
    4. **⚙️ Extras**: Configure amenidades, políticas e características do host
    5. **📅 Data**: Selecione ano e mês para a análise
    6. **🔮 Prever**: Clique no botão para obter a predição
    
    #### 🤖 Sobre o Modelo
    - **Algoritmo**: ExtraTrees Regressor
    - **Dados**: Mais de 600.000 propriedades analisadas
    - **Features**: 32 variáveis diferentes
    - **Performance**: R² Score > 77%
    
    #### 📍 Dicas de Localização (Rio de Janeiro):
    - **Copacabana**: -22.9711, -43.1822
    - **Ipanema**: -22.9838, -43.2043
    - **Leblon**: -22.9840, -43.2189
    - **Botafogo**: -22.9519, -43.1896
    - **Centro**: -22.9068, -43.1729
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    🏠 Airbnb Rio - Predição de Preços | Projeto Data Science | 2024
</div>
""", unsafe_allow_html=True)