#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🧪 Teste do Modelo - Validação Rápida
=====================================
"""

import pandas as pd
import joblib
import os

print("🔍 TESTANDO MODELO AIRBNB...")
print("=" * 40)

# Verificar se modelo existe
if os.path.exists('modelo.joblib'):
    print("✅ Arquivo modelo.joblib encontrado!")
    
    try:
        # Carregar modelo
        print("📥 Carregando modelo...")
        modelo = joblib.load('modelo.joblib')
        print(f"✅ Modelo carregado: {type(modelo).__name__}")
        
        # Dados de teste
        dados_teste = {
            'latitude': -22.9068, 'longitude': -43.1729,
            'accommodates': 2, 'bathrooms': 1.0, 'bedrooms': 1, 'beds': 2,
            'extra_people': 0, 'minimum_nights': 1, 'ano': 2024, 'mes': 1,
            'n_amenities': 10, 'host_listings_count': 1,
            'host_is_superhost': 0, 'instant_bookable': 0,
            
            # Property type: Apartment
            'property_type_Apartment': 1, 'property_type_Bed and breakfast': 0,
            'property_type_Condominium': 0, 'property_type_Guest suite': 0,
            'property_type_Guesthouse': 0, 'property_type_Hostel': 0,
            'property_type_House': 0, 'property_type_Loft': 0,
            'property_type_Outros': 0, 'property_type_Serviced apartment': 0,
            
            # Room type: Entire home/apt
            'room_type_Entire home/apt': 1, 'room_type_Hotel room': 0,
            'room_type_Private room': 0, 'room_type_Shared room': 0,
            
            # Cancelation policy: moderate
            'cancelation_policy_flexible': 0, 'cancelation_policy_moderate': 1,
            'cancelation_policy_strict': 0, 'cancelation_policy_strict_14_with_grace_period': 0
        }
        
        # Criar DataFrame
        print("📊 Criando DataFrame de teste...")
        df = pd.DataFrame([dados_teste])
        print(f"📏 Shape: {df.shape}")
        print(f"📋 Colunas: {len(df.columns)}")
        
        # Fazer predição
        print("🔮 Fazendo predição...")
        preco = modelo.predict(df)[0]
        
        print("🎉 RESULTADO:")
        print(f"💰 Preço predito: R$ {preco:.2f}")
        print(f"📅 Preço semanal: R$ {preco * 7:.2f}")
        print(f"📆 Preço mensal: R$ {preco * 30:.2f}")
        
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ Erro ao testar modelo: {str(e)}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")
        
else:
    print("❌ Arquivo modelo.joblib não encontrado!")
    print("💡 Execute o notebook primeiro para gerar o modelo.")

print("=" * 40)