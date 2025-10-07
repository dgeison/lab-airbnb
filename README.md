# Projeto Airbnb Rio - Predição de Preços

Este projeto utiliza Machine Learning para prever preços de imóveis do Airbnb no Rio de Janeiro.

## 📋 Descrição

O projeto analisa dados históricos do Airbnb do Rio de Janeiro e cria um modelo de predição de preços baseado em características dos imóveis como localização, tipo de propriedade, número de quartos, amenidades, entre outros fatores.

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
pip install -r requirements.txt
```

3. Execute a aplicação Streamlit:
```bash
streamlit run DeployProjetoAirbnb.py
```

## 📊 Dados

O projeto utiliza dados do Airbnb do Rio de Janeiro coletados entre 2018 e 2020, incluindo informações sobre:

- Localização (latitude, longitude)
- Características do imóvel (quartos, banheiros, camas)
- Tipo de propriedade e quarto
- Política de cancelamento
- Amenidades disponíveis
- Informações do host

## 🛠️ Tecnologias utilizadas

- **Python** - Linguagem de programação principal
- **Pandas** - Manipulação e análise de dados
- **Scikit-learn** - Machine Learning
- **Streamlit** - Interface web interativa
- **Joblib** - Serialização do modelo

## 📈 Funcionalidades

- Interface web intuitiva para inserção de dados do imóvel
- Predição em tempo real do preço sugerido
- Validação de entrada de dados
- Visualização dos resultados

## 🔧 Estrutura do projeto

```
├── DeployProjetoAirbnb.py          # Aplicação principal Streamlit
├── DeployProjetoAirbnb.ipynb       # Notebook de desenvolvimento
├── Solução Airbnb Rio.ipynb        # Análise exploratória e modelagem
├── dataset/                        # Dados históricos do Airbnb
├── requirements.txt                # Dependências do projeto
└── README.md                       # Documentação
```

## 📝 Como usar

1. Acesse a aplicação através do Streamlit
2. Preencha as informações do imóvel:
   - Coordenadas (latitude/longitude)
   - Número de hóspedes, quartos, banheiros
   - Tipo de propriedade e quarto
   - Política de cancelamento
   - Outras características
3. Clique em "Prever Valor do Imóvel"
4. Visualize o preço predito

## ⚠️ Nota importante

Certifique-se de ter o arquivo `modelo.joblib` no diretório raiz para que a predição funcione corretamente.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- Seu Nome - Desenvolvimento inicial

## 🙏 Agradecimentos

- Dados fornecidos pelo Inside Airbnb
- Comunidade Streamlit pela excelente documentação