# 🏠 Projeto Airbnb Rio - Predição de Preços

Este projeto utiliza Machine Learning para prever preços de imóveis do Airbnb no Rio de Janeiro.

## 📋 Descrição

O projeto analisa dados históricos do Airbnb do Rio de Janeiro e cria um modelo de predição de preços baseado em características dos imóveis como localização, tipo de propriedade, número de quartos, amenidades, entre outros fatores.

## 🔧 Estrutura do projeto

```
📦 airbnb-price-prediction/
├── 🧠 1_analise_e_treinamento.ipynb     # Análise de dados e treinamento do modelo
├── 🎯 2_aplicacao_web.py               # Aplicação web principal (Streamlit) 
├── ⚙️ configuracoes.py                 # Configurações e estruturas de dados
├── 📓 configuracoes.ipynb              # Notebook de configurações (documentado)
├── 📊 dataset/                         # Dados históricos do Airbnb (25 arquivos)
├── 🤖 modelo.joblib                    # Modelo treinado (será gerado)
├── 📖 README.md                        # Esta documentação
└── 📋 Guias auxiliares/
    ├── EXPLICACAO_SIMPLES.md           # Guia super simples do projeto
    ├── ONDE_MODELO_USADO.md            # Explicação visual do uso do modelo
    └── PROPOSTA_NOVOS_NOMES.md         # Histórico da renomeação
```Rio - Predição de Preços

Este projeto utiliza Machine Learning para prever preços de imóveis do Airbnb no Rio de Janeiro.

## 📋 Descrição

O projeto analisa dados históricos do Airbnb do Rio de Janeiro e cria um modelo de predição de preços baseado em características dos imóveis como localização, tipo de propriedade, número de quartos, amenidades, entre outros fatores.

## 🔧 Estrutura do projeto

```
├── DeployProjetoAirbnb.py      # 🎯 APLICAÇÃO PRINCIPAL (Streamlit)
├── config_airbnb.py           # ⚙️ Configurações e estruturas de dados
├── config_airbnb.ipynb        # 📓 Notebook de configurações  
├── Solução Airbnb Rio.ipynb   # 🧠 Análise exploratória e modelagem
├── dataset/                   # 📊 Dados históricos do Airbnb (25 arquivos)
├── modelo.joblib              # 🤖 Modelo treinado (será gerado)
├── LIMPEZA_ARQUIVOS.md        # � Log de limpeza e organização
└── README.md                  # 📖 Esta documentação
```

## 🚀 Como executar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação

1. Clone este repositório:
```bash
git clone https://github.com/SEU_USUARIO/airbnb-rio-prediction.git
cd airbnb-rio-prediction
```

2. Instale as dependências:
```bash
pip install pandas streamlit joblib scikit-learn numpy seaborn matplotlib plotly
```

3. **IMPORTANTE**: Treine o modelo primeiro:
```bash
# Execute o notebook completo para gerar modelo.joblib
jupyter notebook "1_analise_e_treinamento.ipynb"
```

4. Execute a aplicação Streamlit:
```bash
streamlit run 2_aplicacao_web.py
```

## 📊 Dados

O projeto utiliza dados do Airbnb do Rio de Janeiro coletados entre 2018 e 2020, incluindo:

- **25 arquivos** de dados históricos mensais
- **Localização** (latitude, longitude)  
- **Características** do imóvel (quartos, banheiros, camas)
- **Tipo** de propriedade e quarto
- **Política** de cancelamento
- **Amenidades** disponíveis
- **Informações** do host

## 🛠️ Tecnologias utilizadas

- **Python** - Linguagem de programação principal
- **Pandas** - Manipulação e análise de dados
- **Scikit-learn** - Machine Learning (ExtraTreesRegressor)
- **Streamlit** - Interface web interativa
- **Joblib** - Serialização do modelo
- **Seaborn/Matplotlib** - Visualizações
- **Plotly** - Mapas interativos

## 📈 Funcionalidades

- ✅ Interface web intuitiva para inserção de dados
- ✅ Predição em tempo real do preço sugerido
- ✅ Validação de entrada de dados
- ✅ Visualização organizada em seções
- ✅ Tratamento de erros quando modelo não existe
- ✅ Estruturas de dados bem documentadas

## 🔧 Arquivos principais

### 🧠 `1_analise_e_treinamento.ipynb` (⭐ TREINAMENTO)
- **Notebook principal** com análise completa dos dados históricos
- Limpeza e tratamento de 900+ mil registros do Airbnb
- Treinamento e avaliação de modelos de Machine Learning
- **Gera o arquivo `modelo.joblib` (ESSENCIAL para aplicação funcionar)**
- **Resultado**: Modelo com 97.5% de precisão (R² score)

### 🎯 `2_aplicacao_web.py` (⭐ APLICAÇÃO)
- **Aplicação principal** em Streamlit para usuários finais
- Interface web moderna e completa para predições de preços
- Layout organizado em seções com validações de entrada
- Tratamento robusto de erros e feedback visual
- **Execute com**: `streamlit run 2_aplicacao_web.py`

### ⚙️ `configuracoes.py` 
- **Configurações centralizadas** de todo o projeto
- Estruturas de dados bem documentadas e validadas
- Funções auxiliares para manipulação dos dados
- Pode ser importado por outros módulos ou executado independentemente
- **Execute com**: `python configuracoes.py`

### 📓 `configuracoes.ipynb`
- **Versão interativa** das configurações com documentação detalhada
- Define e explica todas as estruturas de dados do projeto
- Exemplos práticos e demonstrações de uso
- Ideal para entender o projeto e fazer modificações

## 📝 Como usar a aplicação

1. **Execute**: `streamlit run 2_aplicacao_web.py`
2. **Abra** o navegador no endereço indicado (geralmente http://localhost:8501)
3. **Preencha** os dados do imóvel:
   - 📍 Localização (latitude/longitude)
   - 🏡 Características (quartos, banheiros, camas)
   - 📂 Tipo de propriedade e quarto
   - ⚙️ Políticas e amenidades
4. **Clique** em "🔮 Prever Valor do Imóvel"
5. **Visualize** o preço predito em reais!

## ⚠️ Resolução de problemas

### Modelo não encontrado
```bash
❌ Arquivo 'modelo.joblib' não encontrado!
```
**Solução**: Execute completamente o notebook `1_analise_e_treinamento.ipynb`

### Dependências não instaladas
```bash
ModuleNotFoundError: No module named 'streamlit'
```
**Solução**: `pip install streamlit pandas joblib scikit-learn`

### Erro ao executar aplicação
```bash
FileNotFoundError: [Errno 2] No such file or directory: '2_aplicacao_web.py'
```
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