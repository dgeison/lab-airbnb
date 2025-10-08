#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔧 Teste Corrigido do Modelo
===========================
"""

import pandas as pd
import joblib
import os

print("🔍 TESTANDO MODELO COM FEATURES CORRETAS...")
print("=" * 50)

# Verificar se modelo existe
if os.path.exists('modelo.joblib'):
    print("✅ Arquivo modelo.joblib encontrado!")
    
    try:
        # Carregar modelo
        print("📥 Carregando modelo...")
        modelo = joblib.load('modelo.joblib')
        print(f"✅ Modelo carregado: {type(modelo).__name__}")
        
        # Ler colunas corretas
        with open('colunas_modelo.txt', 'r', encoding='utf-8') as f:
            colunas_corretas = [linha.strip() for linha in f.readlines() if linha.strip()]
        
        print(f"📋 Total de colunas esperadas: {len(colunas_corretas)}")
        
        # Criar dados de teste com todas as colunas corretas
        dados_teste = {}
        
        # Inicializar todas as colunas com 0
        for col in colunas_corretas:
            dados_teste[col] = 0
        
        # Preencher valores básicos
        dados_teste.update({
            'latitude': -22.9068,
            'longitude': -43.1729, 
            'accommodates': 2,
            'bathrooms': 1.0,
            'bedrooms': 1,
            'beds': 2,
            'extra_people': 0,
            'minimum_nights': 1,
            'maximum_nights': 30,
            'ano': 2024,
            'mes': 1,
            'n_amenities': 10,
            'host_listings_count': 1,
            'guests_included': 1,
            'guests_efficiency': 50.0,  # accommodates/bedrooms * 100
            'host_is_superhost': 0,
            'instant_bookable': 0
        })
        
        # Features categóricas - ativar apenas as relevantes
        dados_teste['property_type_Apartment'] = 1
        dados_teste['room_type_Entire home/apt'] = 1  
        dados_teste['bed_type_Real Bed'] = 1
        dados_teste['cancellation_policy_moderate'] = 1
        
        # Criar DataFrame
        print("📊 Criando DataFrame de teste...")
        df = pd.DataFrame([dados_teste])
        
        # Verificar se todas as colunas estão presentes
        colunas_faltantes = set(colunas_corretas) - set(df.columns)
        colunas_extras = set(df.columns) - set(colunas_corretas)
        
        if colunas_faltantes:
            print(f"⚠️ Colunas faltantes: {colunas_faltantes}")
        if colunas_extras:
            print(f"⚠️ Colunas extras: {colunas_extras}")
        
        # Reordenar colunas na ordem correta
        df = df.reindex(columns=colunas_corretas, fill_value=0)
        
        print(f"📏 Shape final: {df.shape}")
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
        import traceback
        print("📝 Traceback completo:")
        traceback.print_exc()
        
else:
    print("❌ Arquivo modelo.joblib não encontrado!")
    print("💡 Execute o notebook primeiro para gerar o modelo.")

print("=" * 50)