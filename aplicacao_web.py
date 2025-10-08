#!/usr/bin/env python
# coding: utf-8

# # Deploy
# - passo 1 -> Criar arquivo do Modelo (joblib)
# - passo 2 -> Escolher a forma de deploy:
#     - Arquivo executável + Tkinter
#     - Deploy em um microsite (Flask)
#     - Deploy apenas para uso direto (Streamlit)
# - passo 3 -> Outro arquivo Python (pode ser jupyter ou PyCharm)
# - passo 4 -> Importar streamlit e criar código
# - passo 5 -> atribuir ao botão o carregamento do modelo
# - passo 6 -> Deply feito

# In[1]:


import pandas as pd
import streamlit as st
import joblib
import os

# Configuração da página
st.set_page_config(
    page_title="Predição Airbnb Rio",
    page_icon="🏠",
    layout="wide"
)

# Título principal
st.title("🏠 Predição de Preços - Airbnb Rio de Janeiro")
st.markdown("---")

# Verificar se o modelo existe
if os.path.exists('modelo.joblib'):
    modelo = joblib.load('modelo.joblib')
    st.success("✅ Modelo carregado com sucesso!")
else:
    modelo = None
    st.error("⚠️ Arquivo 'modelo.joblib' não encontrado! Execute o notebook de treinamento primeiro.")

        
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancelation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }


dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0

# Seções da interface
st.markdown("## 📍 Localização")
col1, col2 = st.columns(2)


# Seções da interface
st.markdown("## 📍 Localização")
col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input('Latitude', step=0.00001, value=0.0, format="%.5f")
    x_numericos['latitude'] = latitude

with col2:
    longitude = st.number_input('Longitude', step=0.00001, value=0.0, format="%.5f")
    x_numericos['longitude'] = longitude

st.markdown("## 🏡 Características do Imóvel")
col1, col2, col3, col4 = st.columns(4)

with col1:
    accommodates = st.number_input('Número de Hóspedes', step=1, value=0, min_value=0)
    x_numericos['accommodates'] = accommodates

with col2:
    bedrooms = st.number_input('Quartos', step=1, value=0, min_value=0)
    x_numericos['bedrooms'] = bedrooms

with col3:
    bathrooms = st.number_input('Banheiros', step=1, value=0, min_value=0)
    x_numericos['bathrooms'] = bathrooms

with col4:
    beds = st.number_input('Camas', step=1, value=0, min_value=0)
    x_numericos['beds'] = beds

st.markdown("## 💰 Informações Adicionais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    extra_people = st.number_input('Taxa por Pessoa Extra', step=0.01, value=0.0, min_value=0.0)
    x_numericos['extra_people'] = extra_people

with col2:
    minimum_nights = st.number_input('Noites Mínimas', step=1, value=0, min_value=0)
    x_numericos['minimum_nights'] = minimum_nights

with col3:
    n_amenities = st.number_input('Número de Amenidades', step=1, value=0, min_value=0)
    x_numericos['n_amenities'] = n_amenities

with col4:
    host_listings_count = st.number_input('Listagens do Host', step=1, value=0, min_value=0)
    x_numericos['host_listings_count'] = host_listings_count

st.markdown("## 📅 Data")
col1, col2 = st.columns(2)

with col1:
    ano = st.number_input('Ano', step=1, value=2024, min_value=2018, max_value=2030)
    x_numericos['ano'] = ano

with col2:
    mes = st.number_input('Mês', step=1, value=1, min_value=1, max_value=12)
    x_numericos['mes'] = mes

st.markdown("## ⚙️ Configurações")
col1, col2 = st.columns(2)

with col1:
    for item in x_tf:
        valor = st.selectbox(f'{item.replace("_", " ").title()}', ('Sim', 'Não'))
        if valor == "Sim":
            x_tf[item] = 1
        else:
            x_tf[item] = 0

with col2:
    for item in x_listas:
        valor = st.selectbox(f'{item.replace("_", " ").title()}', x_listas[item])
        dicionario[f'{item}_{valor}'] = 1

st.markdown("---")
    
st.markdown("---")
    
botao = st.button('🔮 Prever Valor do Imóvel', type="primary", use_container_width=True)

if botao:
    if modelo is None:
        st.error("❌ Não é possível fazer predições sem o modelo treinado!")
        st.info("💡 Execute o notebook '1_analise_e_treinamento.ipynb' para treinar e salvar o modelo.")
    else:
        dicionario.update(x_numericos)
        dicionario.update(x_tf)
        valores_x = pd.DataFrame(dicionario, index=[0])
        preco = modelo.predict(valores_x)
        st.success(f"💰 Preço predito: R$ {preco[0]:.2f}")
    
    


# In[ ]:




