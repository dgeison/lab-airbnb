# 🏠 Airbnb Rio - Predição de Preços

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Sistema de predição de preços para imóveis Airbnb no Rio de Janeiro usando Machine Learning

![Airbnb Rio](https://img.shields.io/badge/Dataset-600K%2B%20propriedades-brightgreen)
![Accuracy](https://img.shields.io/badge/R²%20Score-77%25-success)

## � Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias](#️-tecnologias)
- [� Instalação](#-instalação)
- [� Como Usar](#-como-usar)
- [📊 Modelo](#-modelo)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)

## 🎯 Sobre o Projeto

Este projeto utiliza **Machine Learning** para prever preços de imóveis Airbnb no Rio de Janeiro. A aplicação analisa mais de **600.000 propriedades** e oferece predições precisas baseadas em características como localização, tipo de propriedade, amenidades e políticas.

### 🎯 Objetivos

- **Predição Precisa**: R² Score > 77%
- **Interface Intuitiva**: Aplicação web responsiva
- **Análise Completa**: Pipeline end-to-end de Data Science
- **Deploy Pronto**: Configurado para produção

## ✨ Funcionalidades

### 🔮 Predição de Preços
- Estimativa de preços por noite
- Projeções semanal, mensal e anual
- Categorização automática (Econômico, Moderado, Premium, Luxo)

### 🏡 Configuração Detalhada
- **Localização**: Coordenadas GPS precisas
- **Propriedade**: Quartos, banheiros, capacidade, amenidades
- **Tipo**: Apartamento, casa, condomínio, loft, etc.
- **Políticas**: Cancelamento, reserva instantânea, superhost

### 📊 Interface Web
- Design responsivo e moderno
- Validação de dados em tempo real
- Visualizações interativas
- Dicas de localização para o Rio

## 🛠️ Tecnologias

### Core
- **Python 3.13** - Linguagem principal
- **Streamlit** - Interface web
- **Scikit-learn** - Machine Learning
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica

### Visualização
- **Plotly** - Gráficos interativos
- **Matplotlib** - Visualizações estáticas
- **Seaborn** - Análise estatística

### ML Pipeline
- **RandomForest** - Algoritmo principal
- **Joblib** - Serialização do modelo
- **Feature Engineering** - 39 variáveis otimizadas

## � Instalação

### Pré-requisitos
- Python 3.13+
- Git
- 4GB+ RAM (para treinamento)

### Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/dgeison/lab-airbnb.git
cd lab-airbnb
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv .pyenv
.pyenv\Scripts\activate  # Windows
# ou
source .pyenv/bin/activate  # Linux/Mac
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Verifique a Instalação
```bash
python train_model.py --check
```

## 🚀 Como Usar

### Aplicação Web Principal
```bash
streamlit run app.py
```
Acesse: http://localhost:8501

### Aplicação MVC (Avançada)
```bash
streamlit run app_mvc.py
```

### Treinamento do Modelo
```bash
python train_model.py
```

### Exemplo de Uso Programático
```python
import joblib
import pandas as pd

# Carregar modelo
modelo = joblib.load('modelo.joblib')

# Dados de exemplo
dados = {
    'latitude': -22.9068,
    'longitude': -43.1729,
    'accommodates': 2,
    'bedrooms': 1,
    'bathrooms': 1.0,
    # ... outras 34 features
}

# Predição
preco = modelo.predict(pd.DataFrame([dados]))[0]
print(f"Preço estimado: R$ {preco:.2f}")
```

## � Modelo

### Algoritmo: RandomForest Regressor
- **N° Estimadores**: 50 árvores
- **Max Depth**: 15 níveis
- **Features**: 39 variáveis engineered
- **Compressão**: Joblib level 3

### Performance
- **R² Score**: 77.11%
- **RMSE**: R$ 136.80
- **Tamanho**: 20.4 MB
- **Tempo Predição**: <100ms

### Features Principais
1. **Localização**: `latitude`, `longitude`
2. **Capacidade**: `accommodates`, `bedrooms`, `bathrooms`
3. **Amenidades**: `n_amenities`, `guests_efficiency`
4. **Temporais**: `ano`, `mes`
5. **Categóricas**: Tipo propriedade, quarto, políticas

## � Estrutura do Projeto

```
lab-airbnb/
├── 📱 app.py                    # Aplicação web principal
├── 🏗️ app_mvc.py               # Aplicação MVC avançada
├── 🤖 train_model.py           # Script de treinamento
├── 📊 modelo.joblib            # Modelo treinado
├── 📈 dados.csv               # Dataset processado
├── 📋 requirements.txt        # Dependências
├── 📖 README.md              # Documentação
├── 📁 notebooks/             # Análises Jupyter
│   └── analise_e_treinamento.ipynb
├── 📁 data/                  # Dados brutos e processados
│   ├── raw/                  # Dados originais
│   └── processed/            # Dados limpos
├── 📁 src/                   # Código fonte MVC
│   ├── controllers/          # Lógica de negócio
│   ├── models/              # Modelos ML
│   └── views/               # Componentes UI
├── � config/               # Configurações
├── 📁 utils/                # Utilitários
└── 📁 scripts/              # Scripts auxiliares
```

## � Análises

### Dataset
- **Período**: 2018-2020
- **Registros**: 608.794 propriedades
- **Features**: 39 após feature engineering
- **Qualidade**: 98%+ dos dados válidos

### Insights de Negócio
- �️ **Copacabana/Ipanema**: Preços 40% acima da média
- 🏠 **Casas inteiras**: Premium de 25% vs quartos privados
- ⭐ **Superhosts**: Preços 15% superiores
- 🎯 **Amenidades**: Cada 10 amenidades = +R$ 50/noite

---

## 📞 Contato

**Desenvolvido por**: [Dgeison](https://github.com/dgeison)  
**Projeto**: [lab-airbnb](https://github.com/dgeison/lab-airbnb)  
**Data**: Outubro 2024

---

<div align="center">

### 🌟 Se este projeto foi útil, considere dar uma ⭐!

[![GitHub stars](https://img.shields.io/github/stars/dgeison/lab-airbnb.svg?style=social&label=Star)](https://github.com/dgeison/lab-airbnb)
[![GitHub forks](https://img.shields.io/github/forks/dgeison/lab-airbnb.svg?style=social&label=Fork)](https://github.com/dgeison/lab-airbnb/fork)

</div>
**Solução**: Certifique-se de estar na pasta correta do projeto

## 🔍 Métricas do modelo

- **R²**: ~97.5% (alta precisão)
- **RMSE**: ~41.8 (erro médio baixo)
- **Modelo**: ExtraTreesRegressor (melhor performance)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 🙏 Agradecimentos

- Dados fornecidos pelo [Inside Airbnb](http://insideairbnb.com/)
- Inspiração no [notebook do Allan Bruno](https://www.kaggle.com/allanbruno/helping-regular-people-price-listings-on-airbnb)
- Comunidade Streamlit pela excelente documentação