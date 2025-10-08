#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🏠 Teste Rápido - Aplicação Airbnb
===================================
"""

import streamlit as st
import pandas as pd
import joblib
import os

# Configuração básica
st.title("🏠 Teste Airbnb Rio - Predição")

# Verificar modelo
if os.path.exists('modelo.joblib'):
    st.success("✅ Modelo encontrado!")
    modelo = joblib.load('modelo.joblib')
    st.success("✅ Modelo carregado com sucesso!")
    
    # Interface simples
    st.markdown("### Configuração Rápida")
    
    accommodates = st.number_input('Hóspedes', min_value=1, value=2)
    bedrooms = st.number_input('Quartos', min_value=0, value=1)
    bathrooms = st.number_input('Banheiros', min_value=0.5, value=1.0, step=0.5)
    
    if st.button('🔮 Prever Preço'):
        # Dados básicos para teste
        dados_teste = {
            'latitude': -22.9068, 'longitude': -43.1729,
            'accommodates': accommodates, 'bathrooms': bathrooms,
            'bedrooms': bedrooms, 'beds': accommodates,
            'extra_people': 0, 'minimum_nights': 1,
            'ano': 2024, 'mes': 1, 'n_amenities': 10,
            'host_listings_count': 1, 'host_is_superhost': 0,
            'instant_bookable': 0
        }
        
        # Features categóricas (padrão Apartment)
        categoricas = {
            'property_type_Apartment': 1, 'property_type_Bed and breakfast': 0,
            'property_type_Condominium': 0, 'property_type_Guest suite': 0,
            'property_type_Guesthouse': 0, 'property_type_Hostel': 0,
            'property_type_House': 0, 'property_type_Loft': 0,
            'property_type_Outros': 0, 'property_type_Serviced apartment': 0,
            'room_type_Entire home/apt': 1, 'room_type_Hotel room': 0,
            'room_type_Private room': 0, 'room_type_Shared room': 0,
            'cancelation_policy_flexible': 0, 'cancelation_policy_moderate': 1,
            'cancelation_policy_strict': 0, 'cancelation_policy_strict_14_with_grace_period': 0
        }
        
        # Combinar dados
        dados_completos = {**dados_teste, **categoricas}
        
        # Criar DataFrame
        df = pd.DataFrame([dados_completos])
        
        # Predição
        try:
            preco = modelo.predict(df)[0]
            st.success(f"💰 Preço predito: R$ {preco:.2f}")
            
            # Métricas extras
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📅 Semanal", f"R$ {preco * 7:.2f}")
            with col2:
                st.metric("📆 Mensal", f"R$ {preco * 30:.2f}")
            with col3:
                st.metric("📈 Anual", f"R$ {preco * 365:.0f}")
                
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            
else:
    st.error("❌ Modelo não encontrado!")
    st.info("Execute o notebook primeiro para gerar o modelo.")

st.markdown("---")
st.markdown("🎯 **Teste Básico da Aplicação Funcionando!**")