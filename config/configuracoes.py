#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 CONFIGURAÇÕES LEGADAS DO PROJETO AIRBNB RIO 

ATENÇÃO: Este arquivo mantém compatibilidade com a versão anterior.
Para nova estrutura MVC, use: config/settings.py

Este módulo centraliza estruturas de dados para compatibilidade com:
- Interface Streamlit legada (2_aplicacao_web.py)
- Scripts antigos que dependem destas definições

📋 Conteúdo:
- Definições de variáveis numéricas, booleanas e categóricas
- Estruturas de dados para entrada do usuário
- Mapeamentos e dicionários de referência

🔧 Como usar (LEGADO):
    from config.configuracoes import x_numericos, x_tf, x_listas

🆕 Nova estrutura MVC:
    from config.settings import Config, DataConfig, ModelConfig
    
🗓️ Compatibilidade mantida para: Outubro 2025
👤 Projeto: Predição de Preços Airbnb Rio de Janeiro
"""

# ================================================
# IMPORTAÇÕES E CONFIGURAÇÕES INICIAIS
# ================================================

import pandas as pd    # Manipulação de dados
import streamlit as st  # Interface web
import joblib          # Carregamento do modelo treinado

# ⚠️ AVISO: Estruturas legadas para compatibilidade
# Para novos desenvolvimentos, use config/settings.py

# ================================================
# ESTRUTURAS DE DADOS LEGADAS
# ================================================

# 📊 VARIÁVEIS NUMÉRICAS
# Dicionário com todas as features numéricas que o usuário pode inserir
# Valores iniciais = 0 (serão substituídos pela entrada do usuário)
x_numericos = {
    'latitude': 0,              # Coordenada geográfica (-90 a 90)
    'longitude': 0,             # Coordenada geográfica (-180 a 180)
    'accommodates': 0,          # Número máximo de hóspedes
    'bathrooms': 0,             # Quantidade de banheiros
    'bedrooms': 0,              # Quantidade de quartos
    'beds': 0,                  # Quantidade de camas
    'extra_people': 0,          # Taxa cobrada por pessoa extra (R$)
    'minimum_nights': 0,        # Número mínimo de noites para reserva
    'ano': 0,                   # Ano da estadia (2018-2030)
    'mes': 0,                   # Mês da estadia (1-12)
    'n_amenities': 0,           # Número total de amenidades oferecidas
    'host_listings_count': 0    # Quantidade de imóveis que o host possui
}

# 🔘 VARIÁVEIS BOOLEANAS (True/False)
# Convertidas para 1 (Sim) ou 0 (Não) para o modelo
x_tf = {
    'host_is_superhost': 0,     # Host tem status de "Superhost"?
    'instant_bookable': 0       # Reserva pode ser feita instantaneamente?
}

# 📂 VARIÁVEIS CATEGÓRICAS
# Listas com todas as opções disponíveis para cada categoria
# Serão convertidas em variáveis dummy (one-hot encoding) para o modelo
x_listas = {
    # Tipos de propriedade disponíveis no dataset
    'property_type': [
        'Apartment',           # Apartamento
        'Bed and breakfast',   # Pousada/B&B
        'Condominium',         # Condomínio
        'Guest suite',         # Suíte de hóspedes
        'Guesthouse',          # Casa de hóspedes
        'Hostel',              # Hostel
        'House',               # Casa
        'Loft',                # Loft
        'Outros',              # Outros tipos (agrupados)
        'Serviced apartment'   # Apartamento com serviços
    ],
    
    # Tipos de acomodação
    'room_type': [
        'Entire home/apt',     # Casa/apartamento inteiro
        'Hotel room',          # Quarto de hotel
        'Private room',        # Quarto privado
        'Shared room'          # Quarto compartilhado
    ],
    
    # Políticas de cancelamento
    'cancelation_policy': [
        'flexible',                      # Flexível
        'moderate',                      # Moderada
        'strict',                        # Rígida
        'strict_14_with_grace_period'    # Rígida com período de carência
    ]
}

# ================================================
# FUNÇÕES AUXILIARES
# ================================================

def criar_dicionario_dummy():
    """
    Cria dicionário com todas as variáveis dummy (categóricas) inicializadas em 0.
    
    Returns:
        dict: Dicionário com chaves no formato 'categoria_valor' = 0
    """
    dicionario_dummy = {}
    for categoria in x_listas:
        for valor in x_listas[categoria]:
            chave = f'{categoria}_{valor}'
            dicionario_dummy[chave] = 0
    return dicionario_dummy

def validar_estruturas():
    """
    Valida se todas as estruturas estão consistentes e bem formadas.
    
    Returns:
        bool: True se todas as validações passaram
    """
    try:
        # Verificar se x_numericos tem pelo menos 10 campos
        assert len(x_numericos) >= 10, "x_numericos deve ter pelo menos 10 campos"
        
        # Verificar se x_tf tem campos booleanos
        assert len(x_tf) >= 2, "x_tf deve ter pelo menos 2 campos"
        
        # Verificar se x_listas tem as 3 categorias principais
        categorias_esperadas = ['property_type', 'room_type', 'cancelation_policy']
        for cat in categorias_esperadas:
            assert cat in x_listas, f"Categoria {cat} não encontrada em x_listas"
            assert len(x_listas[cat]) > 0, f"Categoria {cat} está vazia"
        
        return True
    except AssertionError as e:
        print(f"❌ Erro de validação: {e}")
        return False

def exibir_resumo():
    """
    Exibe um resumo completo das estruturas de dados definidas.
    """
    print("=" * 60)
    print("📋 RESUMO DAS ESTRUTURAS DE DADOS DO PROJETO")
    print("=" * 60)
    
    print(f"📊 Variáveis numéricas: {len(x_numericos)} campos")
    for campo in x_numericos:
        print(f"   - {campo}")
    
    print(f"\n🔘 Variáveis booleanas: {len(x_tf)} campos")
    for campo in x_tf:
        print(f"   - {campo}")
    
    print(f"\n📂 Variáveis categóricas: {len(x_listas)} grupos")
    total_opcoes = 0
    for categoria, opcoes in x_listas.items():
        print(f"   - {categoria}: {len(opcoes)} opções")
        total_opcoes += len(opcoes)
    
    print(f"\n📋 Total de opções categóricas: {total_opcoes}")
    print(f"🔢 Total de colunas no modelo: {len(x_numericos) + len(x_tf) + total_opcoes}")
    
    print("\n✅ Validação:", "Passou" if validar_estruturas() else "Falhou")
    print("=" * 60)

# ================================================
# EXEMPLO DE USO
# ================================================

def exemplo_uso():
    """
    Demonstra como usar as estruturas de dados no projeto.
    """
    print("\n🧪 EXEMPLO DE USO:")
    
    # 1. Criar dicionário dummy
    dummy_dict = criar_dicionario_dummy()
    print(f"1️⃣ Dicionário dummy criado com {len(dummy_dict)} colunas")
    
    # 2. Simular entrada do usuário
    exemplo_entrada = x_numericos.copy()
    exemplo_entrada.update({
        'latitude': -22.9068,
        'longitude': -43.1729,
        'accommodates': 4,
        'bathrooms': 2,
        'bedrooms': 2,
        'beds': 2,
        'ano': 2024,
        'mes': 12,
        'n_amenities': 15
    })
    
    print("2️⃣ Exemplo de entrada do usuário:")
    for campo, valor in exemplo_entrada.items():
        print(f"   {campo}: {valor}")
    
    # 3. Simular seleções categóricas
    print("3️⃣ Seleções categóricas:")
    print(f"   Tipo de propriedade: {x_listas['property_type'][0]}")
    print(f"   Tipo de quarto: {x_listas['room_type'][0]}")
    print(f"   Política de cancelamento: {x_listas['cancelation_policy'][0]}")

# ================================================
# EXECUÇÃO PRINCIPAL
# ================================================

if __name__ == "__main__":
    print("🏠 CONFIGURAÇÕES DO PROJETO AIRBNB RIO")
    print("📄 Carregando estruturas de dados...")
    
    exibir_resumo()
    exemplo_uso()
    
    print("\n🎉 Estruturas carregadas com sucesso!")
    print("📖 Para usar em outros arquivos:")
    print("   from configuracoes import x_numericos, x_tf, x_listas")