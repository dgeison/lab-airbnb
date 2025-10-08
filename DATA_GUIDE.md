# 📊 **GUIA DE DADOS - PROJETO AIRBNB**

## 🚨 **ARQUIVOS GRANDES NÃO INCLUSOS NO REPOSITÓRIO**

### 📁 **Dados Brutos (`data/raw/`)**
Os seguintes arquivos CSV **NÃO estão inclusos** no repositório devido ao tamanho (>100MB cada):

```
abril2018.csv      → 117.85 MB
maio2018.csv       → 117.35 MB  
julho2018.csv      → 115.85 MB
fevereiro2020.csv  → 114.39 MB
agosto2018.csv     → 114.07 MB
maro2020.csv       → 113.04 MB
maro2019.csv       → 112.67 MB
abril2019.csv      → 112.03 MB
abril2020.csv      → 111.88 MB
maio2019.csv       → 111.69 MB
setembro2018.csv   → 111.57 MB
fevereiro2019.csv  → 111.41 MB
maio2020.csv       → 111.33 MB
junho2019.csv      → 111.29 MB
julho2019.csv      → 110.53 MB
janeiro2020.csv    → 109.79 MB
janeiro2019.csv    → 109.58 MB
dezembro2019.csv   → 109.57 MB
outubro2018.csv    → 109.31 MB
... (demais arquivos)
```

### 🤖 **Modelo Treinado**
- **`modelo.joblib`** → **593.04 MB** (arquivo do modelo RandomForest treinado)

## 📥 **COMO OBTER OS DADOS**

### **Opção 1: Download Direto**
Os dados originais podem ser obtidos do **Inside Airbnb**:
- 🌐 **Site**: http://insideairbnb.com/get-the-data.html
- 📍 **Cidade**: Rio de Janeiro, Brazil
- 📅 **Período**: 2018-2020

### **Opção 2: Script de Download**
Execute o script de download automático:
```bash
python scripts/download_data.py
```

### **Opção 3: Dados Processados**
Para desenvolvimento rápido, use a amostra incluída:
- ✅ `data/processed/primeiros_registros.csv` (incluído no repo)

## 🔧 **REPRODUÇÃO DO MODELO**

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Executar Treinamento**
```bash
python train_model.py
```
ou use o notebook:
```bash
jupyter notebook notebooks/1_analise_e_treinamento.ipynb
```

### **3. Regenerar Modelo**
```bash
python quick_train.py  # Treinamento rápido
```

## 📁 **ESTRUTURA RECOMENDADA**

```
airbnb/
├── data/
│   ├── raw/                 # Dados originais (GRANDES - não no git)
│   │   ├── *.csv           # ~110MB cada
│   └── processed/           # Dados processados
│       ├── dados.csv       # Dataset completo (GRANDE - não no git)
│       └── primeiros_registros.csv  # Amostra (incluído)
├── notebooks/              # Jupyter notebooks (incluídos)
├── src/                    # Código fonte (incluído)
├── modelo.joblib          # Modelo treinado (GRANDE - não no git)
├── requirements.txt       # Dependências (incluído)
└── README.md             # Documentação (incluído)
```

## ⚡ **DESENVOLVIMENTO LOCAL**

### **Setup Inicial**
1. Clone o repositório
2. Instale dependências: `pip install -r requirements.txt`
3. Baixe os dados (Opção 1, 2 ou 3 acima)
4. Execute o notebook de análise

### **Modificações**
- ✅ **Commitar**: Código, notebooks, documentação
- ❌ **NÃO commitar**: CSVs grandes, modelo.joblib, dados processados

## 🎯 **PRODUÇÃO E DEPLOY**

Para produção, considere:
- **☁️ Cloud Storage**: AWS S3, Google Cloud Storage
- **🤖 Model Registry**: MLflow, Weights & Biases
- **📦 Model Serving**: Docker + API
- **🔄 CI/CD**: GitHub Actions para retreinamento automático

---

> **💡 Dica**: Este projeto foca na **reprodutibilidade** e **colaboração**. Os dados e modelos grandes ficam fora do Git, mas o código para recriá-los está incluso!