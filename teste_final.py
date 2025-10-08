#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔧 Teste Final do Modelo - Features Corretas
============================================
"""

import pandas as pd
import joblib
import os

print("🔍 TESTE FINAL COM FEATURES REAIS DO MODELO...")
print("=" * 50)

# Features corretas do modelo
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

try:
    # Carregar modelo
    modelo = joblib.load('modelo.joblib')
    print(f"✅ Modelo carregado: {type(modelo).__name__}")
    
    # Criar dados de teste
    dados = {}
    for feature in features_modelo:
        dados[feature] = 0
    
    # Valores de exemplo
    dados.update({
        'host_is_superhost': 0,
        'host_listings_count': 1,
        'latitude': -22.9068,
        'longitude': -43.1729,
        'accommodates': 2,
        'bathrooms': 1.0,
        'bedrooms': 1,
        'beds': 2,
        'guests_included': 1,
        'extra_people': 0,
        'minimum_nights': 1,
        'maximum_nights': 30,
        'instant_bookable': 0,
        'is_business_travel_ready': 0,
        'ano': 2024,
        'mes': 1,
        'guests_efficiency': 200.0,  # 2 guests / 1 bedroom * 100
        'n_amenities': 10,
        'property_type_Apartment': 1,
        'room_type_Entire home/apt': 1,
        'bed_type_Real Bed': 1,
        'cancellation_policy_moderate': 1
    })
    
    # Criar DataFrame
    df = pd.DataFrame([dados])
    df = df.reindex(columns=features_modelo, fill_value=0)
    
    print(f"📊 Shape: {df.shape}")
    print(f"📋 Colunas: {len(df.columns)}")
    
    # Predição
    preco = modelo.predict(df)[0]
    
    print("🎉 SUCESSO!")
    print(f"💰 Preço predito: R$ {preco:.2f}")
    print(f"📅 Semanal: R$ {preco * 7:.2f}")
    print(f"📆 Mensal: R$ {preco * 30:.2f}")
    
    print("\n✅ MODELO FUNCIONANDO PERFEITAMENTE!")
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print("=" * 50)