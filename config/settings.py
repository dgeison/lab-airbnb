"""
Configurações do Projeto Airbnb Rio - Previsão de Preços
=========================================================

Este módulo centraliza todas as configurações do projeto, incluindo:
- Caminhos de arquivos e diretórios
- Parâmetros de modelos de machine learning
- Configurações da aplicação web
- Variáveis de ambiente

Autor: Projeto Airbnb Rio
Data: 2024
"""

import os
from pathlib import Path


class Config:
    """Classe de configuração principal do projeto"""
    
    # ===== CAMINHOS DE DIRETÓRIOS =====
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    MODELS_DIR = PROJECT_ROOT / "models"
    
    # ===== ARQUIVOS PRINCIPAIS =====
    PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "dados.csv"
    MODEL_FILE = PROJECT_ROOT / "modelo.joblib"
    
    # ===== CONFIGURAÇÕES DE MACHINE LEARNING =====
    RANDOM_STATE = 42
    TEST_SIZE = 0.3
    
    # Parâmetros dos modelos
    EXTRA_TREES_PARAMS = {
        'n_estimators': 300,
        'random_state': RANDOM_STATE,
        'max_depth': 15,
        'min_samples_split': 2,
        'n_jobs': -1
    }
    
    RANDOM_FOREST_PARAMS = {
        'n_estimators': 200,
        'random_state': RANDOM_STATE,
        'max_depth': 20,
        'min_samples_split': 5,
        'n_jobs': -1
    }
    
    # ===== CONFIGURAÇÕES DA APLICAÇÃO WEB =====
    APP_TITLE = "Airbnb Rio - Previsão de Preços"
    APP_DESCRIPTION = "Ferramenta para prever preços de imóveis no Airbnb do Rio de Janeiro"
    
    # Configurações do Streamlit
    STREAMLIT_CONFIG = {
        'page_title': APP_TITLE,
        'page_icon': '🏠',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded'
    }
    
    # ===== CONFIGURAÇÕES DE DADOS =====
    # Colunas numéricas para análise
    NUMERIC_COLUMNS = [
        'latitude', 'longitude', 'accommodates', 'bathrooms',
        'bedrooms', 'beds', 'price', 'minimum_nights',
        'maximum_nights', 'number_of_reviews', 'review_scores_rating',
        'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication',
        'review_scores_location', 'review_scores_value'
    ]
    
    # Limites para remoção de outliers
    PRICE_LIMITS = {
        'min': 10,     # Preço mínimo em R$
        'max': 4000    # Preço máximo em R$
    }
    
    ACCOMMODATES_LIMIT = 20  # Máximo de pessoas acomodadas
    
    # ===== MAPEAMENTOS E DICIONÁRIOS =====
    # Meses em português para inglês
    MONTH_MAPPING = {
        'janeiro': 'january',
        'fevereiro': 'february', 
        'março': 'march',
        'maro': 'march',  # Correção para nome incorreto
        'abril': 'april',
        'maio': 'may',
        'junho': 'june',
        'julho': 'july',
        'agosto': 'august',
        'setembro': 'september',
        'outubro': 'october',
        'novembro': 'november',
        'novrmbro': 'november',  # Correção para nome incorreto
        'dezembro': 'december'
    }
    
    # Colunas categóricas True/False
    BOOLEAN_COLUMNS = [
        'host_is_superhost', 'host_has_profile_pic', 'host_identity_verified',
        'is_location_exact', 'instant_bookable'
    ]
    
    # Colunas categóricas com múltiplas opções
    CATEGORICAL_COLUMNS = [
        'property_type', 'room_type', 'bed_type', 'cancellation_policy'
    ]


class DataConfig:
    """Configurações específicas para processamento de dados"""
    
    # Colunas a serem mantidas após limpeza
    COLUMNS_TO_KEEP = [
        'id', 'host_id', 'host_since', 'host_is_superhost',
        'host_has_profile_pic', 'host_identity_verified', 'neighbourhood_group_cleansed',
        'latitude', 'longitude', 'property_type', 'room_type', 'accommodates',
        'bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities', 'price',
        'minimum_nights', 'maximum_nights', 'number_of_reviews',
        'first_review', 'last_review', 'review_scores_rating',
        'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location', 'review_scores_value',
        'instant_bookable', 'is_location_exact', 'cancellation_policy'
    ]
    
    # Amenidades importantes (exemplo)
    IMPORTANT_AMENITIES = [
        'Wifi', 'Air conditioning', 'Kitchen', 'Free parking',
        'Pool', 'Gym', 'Elevator', 'Doorman'
    ]


class ModelConfig:
    """Configurações específicas para modelos de ML"""
    
    # Métricas a serem calculadas
    METRICS = ['r2_score', 'mean_absolute_error', 'mean_squared_error']
    
    # Modelos a serem testados
    MODELS_TO_TEST = {
        'ExtraTreesRegressor': Config.EXTRA_TREES_PARAMS,
        'RandomForestRegressor': Config.RANDOM_FOREST_PARAMS,
        'LinearRegression': {}
    }


# ===== FUNÇÕES UTILITÁRIAS =====
def get_data_files():
    """
    Retorna lista de arquivos CSV na pasta de dados brutos
    
    Returns:
        list: Lista de caminhos para arquivos CSV
    """
    raw_data_path = Config.RAW_DATA_DIR
    return list(raw_data_path.glob("*.csv"))


def validate_paths():
    """
    Valida se todos os diretórios necessários existem
    
    Returns:
        bool: True se todos os caminhos existem, False caso contrário
    """
    required_dirs = [
        Config.DATA_DIR,
        Config.RAW_DATA_DIR, 
        Config.PROCESSED_DATA_DIR,
        Config.MODELS_DIR
    ]
    
    return all(dir_path.exists() for dir_path in required_dirs)


def create_directories():
    """Cria diretórios necessários se não existirem"""
    directories = [
        Config.DATA_DIR,
        Config.RAW_DATA_DIR,
        Config.PROCESSED_DATA_DIR, 
        Config.MODELS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("Diretórios criados com sucesso!")


if __name__ == "__main__":
    # Teste das configurações
    print("=== CONFIGURAÇÕES DO PROJETO AIRBNB RIO ===")
    print(f"Diretório raiz: {Config.PROJECT_ROOT}")
    print(f"Dados brutos: {Config.RAW_DATA_DIR}")
    print(f"Dados processados: {Config.PROCESSED_DATA_DIR}")
    print(f"Modelos: {Config.MODELS_DIR}")
    print(f"Validação de caminhos: {validate_paths()}")