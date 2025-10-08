# Guia de Deploy - Airbnb Rio

## 🚀 Deploy Local

### 1. Preparação
```bash
# Clone e entre no diretório
git clone https://github.com/dgeison/lab-airbnb.git
cd lab-airbnb

# Crie ambiente virtual
python -m venv .pyenv
.pyenv\Scripts\activate  # Windows
source .pyenv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### 2. Execução
```bash
# Aplicação principal
streamlit run app.py

# Aplicação MVC (avançada)
streamlit run app_mvc.py
```

### 3. Acesso
- **URL**: http://localhost:8501
- **Interface**: Web responsiva
- **Performance**: <100ms por predição

---

## ☁️ Deploy na Nuvem

### Streamlit Cloud (Recomendado)

1. **Fork** o repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. **Conecte** sua conta GitHub
4. **Deploy** o repositório
5. **Configure**:
   - App path: `app.py`
   - Python version: `3.13`

### Heroku

```bash
# Instale Heroku CLI
# Crie Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create airbnb-rio-predictor
git push heroku main
```

### AWS EC2

```bash
# Ubuntu 22.04 LTS
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# PM2 para manter rodando
npm install -g pm2
pm2 start "streamlit run app.py" --name airbnb-app
```

---

## 🔧 Configurações de Produção

### Variáveis de Ambiente
```bash
# .env
ENVIRONMENT=production
MODEL_PATH=modelo.joblib
DATA_PATH=dados.csv
STREAMLIT_PORT=8501
DEBUG=False
```

### Otimizações
- **Cache**: Streamlit cache habilitado
- **Modelo**: Compressão joblib level 3
- **Dados**: Dataset otimizado (608K registros)

### Monitoramento
- **Logs**: Streamlit built-in
- **Performance**: <100ms por predição
- **Memória**: ~200MB RAM