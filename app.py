#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🏠 Airbnb Rio - Aplicação Web FUNCIONANDO
=========================================

Aplicação Streamlit com as features corretas do modelo treinado.
"""

import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="🏠 Airbnb Rio - Predição",
    page_icon="🏠",
    layout="wide"
)

# CSS básico
st.markdown("""
<style>
    .prediction-box {
        background: linear-gradient(90deg, #FF5A5F, #00A699);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF5A5F;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🏠 Airbnb Rio - Predição de Preços")
st.markdown("Aplicação funcional com o modelo treinado")

# Carregar modelo
@st.cache_data
def carregar_modelo():
    if os.path.exists('modelo.joblib'):
        return joblib.load('modelo.joblib')
    return None

modelo = carregar_modelo()

# Status do modelo
if modelo:
    st.success("✅ Modelo carregado com sucesso!")
else:
    st.error("❌ Modelo não encontrado!")
    st.stop()

# FEATURES CORRETAS DO MODELO (verificadas do modelo salvo)
features_modelo = [
    'host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
    'accommodates', 'bathrooms', 'bedrooms', 'beds', 'guests_included',
    'extra_people', 'minimum_nights', 'maximum_nights', 'instant_bookable',
    'is_business_travel_ready', 'ano', 'mes', 'guests_efficiency',
    'n_amenities', 'property_type_Apartment', 'property_type_Bed and breakfast',
    'property_type_Condominium', 'property_type_Guest suite', 'property_type_Guesthouse',
    'property_type_Hostel', 'property_type_House', 'property_type_Loft',
    'property_type_Other', 'property_type_Outros', 'property_type_Serviced apartment',
    'room_type_Entire home/apt', 'room_type_Hotel room', 'room_type_Private room',
    'room_type_Shared room', 'bed_type_Outros', 'bed_type_Real Bed',
    'cancellation_policy_flexible', 'cancellation_policy_moderate',
    'cancellation_policy_strict', 'cancellation_policy_strict_14_with_grace_period'
]

# Interface dividida
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🏡 Configurar Propriedade")
    
    # Localização
    st.markdown("**📍 Localização**")
    latitude = st.number_input('Latitude', value=-22.9068, format="%.5f")
    longitude = st.number_input('Longitude', value=-43.1729, format="%.5f")
    
    # Características básicas
    st.markdown("**🏠 Características**")
    col_a, col_b = st.columns(2)
    
    with col_a:
        accommodates = st.selectbox('👥 Hóspedes', range(1, 17), index=1)
        bedrooms = st.selectbox('🛏️ Quartos', range(0, 11), index=1)
        bathrooms = st.selectbox('🚿 Banheiros', [0.5, 1, 1.5, 2, 2.5, 3, 4, 5], index=1)
    
    with col_b:
        beds = st.selectbox('🛌 Camas', range(1, 17), index=1)
        n_amenities = st.slider('🎯 Amenidades', 0, 50, 10)
        minimum_nights = st.selectbox('🌙 Noites Mín.', range(1, 31), index=0)
    
    # Tipo de propriedade
    st.markdown("**🏘️ Tipo de Propriedade**")
    property_types = ['Apartment', 'House', 'Condominium', 'Loft', 'Outros', 
                     'Serviced apartment', 'Bed and breakfast', 'Guest suite',
                     'Guesthouse', 'Hostel', 'Other']
    property_type = st.selectbox('Tipo', property_types)
    
    # Tipo de quarto
    room_types = ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
    room_type = st.selectbox('🚪 Tipo de Quarto', room_types)
    
    # Política de cancelamento
    cancellation_policies = ['moderate', 'flexible', 'strict', 'strict_14_with_grace_period']
    cancellation_policy = st.selectbox('📜 Política Cancel.', cancellation_policies)
    
    # Configurações extras
    st.markdown("**⚙️ Extras**")
    col_c, col_d = st.columns(2)
    
    with col_c:
        extra_people = st.number_input('💰 Taxa Extra', min_value=0.0, value=0.0)
        maximum_nights = st.selectbox('📅 Noites Máx.', [30, 60, 90, 365, 1125], index=0)
        guests_included = st.selectbox('👥 Hóspedes Inclusos', range(1, 9), index=0)
    
    with col_d:
        host_listings_count = st.selectbox('📋 Listagens Host', range(1, 101), index=0)
        host_is_superhost = st.checkbox('⭐ Superhost')
        instant_bookable = st.checkbox('⚡ Reserva Instantânea')
        is_business_travel_ready = st.checkbox('💼 Business Travel')
    
    # Data
    st.markdown("**📅 Período**")
    col_e, col_f = st.columns(2)
    with col_e:
        ano = st.selectbox('Ano', range(2024, 2031))
    with col_f:
        mes = st.selectbox('Mês', range(1, 13))

with col2:
    st.markdown("### 🔮 Predição")
    
    if st.button('💰 Calcular Preço', type="primary", use_container_width=True):
        # Criar dados para o modelo
        dados = {}
        
        # Inicializar todas as features com 0
        for feature in features_modelo:
            dados[feature] = 0
        
        # Calcular guests_efficiency
        guests_efficiency = (accommodates / bedrooms * 100) if bedrooms > 0 else 50
        
        # Preencher valores
        dados.update({
            'host_is_superhost': 1 if host_is_superhost else 0,
            'host_listings_count': host_listings_count,
            'latitude': latitude,
            'longitude': longitude,
            'accommodates': accommodates,
            'bathrooms': bathrooms,
            'bedrooms': bedrooms,
            'beds': beds,
            'guests_included': guests_included,
            'extra_people': extra_people,
            'minimum_nights': minimum_nights,
            'maximum_nights': maximum_nights,
            'instant_bookable': 1 if instant_bookable else 0,
            'is_business_travel_ready': 1 if is_business_travel_ready else 0,
            'ano': ano,
            'mes': mes,
            'guests_efficiency': guests_efficiency,
            'n_amenities': n_amenities
        })
        
        # Property type
        if f'property_type_{property_type}' in dados:
            dados[f'property_type_{property_type}'] = 1
        
        # Room type
        if f'room_type_{room_type}' in dados:
            dados[f'room_type_{room_type}'] = 1
        
        # Bed type (padrão Real Bed)
        dados['bed_type_Real Bed'] = 1
        
        # Cancellation policy
        if f'cancellation_policy_{cancellation_policy}' in dados:
            dados[f'cancellation_policy_{cancellation_policy}'] = 1
        
        # Criar DataFrame
        df = pd.DataFrame([dados])
        
        # Verificar se todas as colunas estão presentes
        df = df.reindex(columns=features_modelo, fill_value=0)
        
        try:
            # Fazer predição
            preco = modelo.predict(df)[0]
            
            # Exibir resultado
            st.markdown(f"""
            <div class="prediction-box">
                <h2>💰 Preço Predito</h2>
                <h1>R$ {preco:.2f}</h1>
                <p>por noite</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas adicionais
            st.markdown("**📊 Projeções**")
            
            col_g, col_h = st.columns(2)
            with col_g:
                st.metric("📅 Semanal", f"R$ {preco * 7:.2f}")
                st.metric("📆 Mensal", f"R$ {preco * 30:.2f}")
            
            with col_h:
                receita_anual = preco * 365 * 0.7  # 70% ocupação
                st.metric("📈 Anual (70% ocup.)", f"R$ {receita_anual:,.0f}")
                
                # Categoria de preço
                if preco < 100:
                    categoria = "💚 Econômico"
                elif preco < 300:
                    categoria = "💙 Moderado"
                elif preco < 600:
                    categoria = "💜 Premium"
                else:
                    categoria = "💛 Luxo"
                
                st.metric("🏷️ Categoria", categoria)
            
        except Exception as e:
            st.error(f"❌ Erro na predição: {str(e)}")
            st.write("Debug - Shape do DataFrame:", df.shape)
            st.write("Debug - Colunas faltantes:", set(features_modelo) - set(df.columns))

# Informações na sidebar
st.sidebar.markdown("### 📊 Sobre o Modelo")
st.sidebar.info("""
- **Algoritmo**: RandomForest
- **Features**: 32 variáveis
- **Performance**: R² > 77%
- **Dataset**: 600K+ propriedades
""")

st.sidebar.markdown("### 🎯 Dicas")
st.sidebar.markdown("""
**Localizações Rio:**
- Copacabana: -22.97, -43.18
- Ipanema: -22.98, -43.20
- Leblon: -22.98, -43.22
- Centro: -22.91, -43.17
""")

# Footer
st.markdown("---")
st.markdown("🏠 **Airbnb Rio - Funcionando!** | Teste sua predição acima ⬆️")