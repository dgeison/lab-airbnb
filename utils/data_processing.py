"""
Utilidades para Processamento de Dados - Projeto Airbnb Rio
===========================================================

Este módulo contém funções utilitárias para:
- Carregamento e limpeza de dados
- Pré-processamento de features
- Validação de dados
- Transformações comuns

Autor: Projeto Airbnb Rio
Data: 2024
"""

import pandas as pd
import numpy as np
import pathlib
from typing import List, Dict, Tuple, Optional
from config.settings import Config, DataConfig


def load_raw_data(data_path: pathlib.Path = None) -> pd.DataFrame:
    """
    Carrega e consolida todos os arquivos CSV da pasta de dados brutos
    
    Args:
        data_path (pathlib.Path, optional): Caminho para dados brutos. 
                                          Se None, usa configuração padrão.
    
    Returns:
        pd.DataFrame: DataFrame consolidado com todos os dados
        
    Raises:
        FileNotFoundError: Se o diretório não existe ou não contém arquivos CSV
    """
    if data_path is None:
        data_path = Config.RAW_DATA_DIR
    
    if not data_path.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {data_path}")
    
    # Buscar todos os arquivos CSV
    csv_files = list(data_path.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {data_path}")
    
    print(f"📁 Carregando {len(csv_files)} arquivos CSV...")
    
    dataframes = []
    
    for arquivo in csv_files:
        try:
            print(f"   📄 Processando: {arquivo.name}")
            
            # Extrair informações do nome do arquivo
            nome_arquivo = arquivo.stem.lower()
            ano, mes = extract_date_from_filename(nome_arquivo)
            
            # Carregar dados
            df = pd.read_csv(arquivo)
            
            # Adicionar colunas de data
            df['ano'] = ano
            df['mes'] = mes
            df['arquivo_origem'] = arquivo.name
            
            dataframes.append(df)
            
        except Exception as e:
            print(f"   ⚠️  Erro ao processar {arquivo.name}: {e}")
            continue
    
    if not dataframes:
        raise ValueError("Nenhum arquivo foi carregado com sucesso")
    
    # Consolidar todos os DataFrames
    base_consolidada = pd.concat(dataframes, ignore_index=True)
    
    print(f"✅ Dados consolidados: {base_consolidada.shape[0]:,} registros, {base_consolidada.shape[1]} colunas")
    
    return base_consolidada


def extract_date_from_filename(filename: str) -> Tuple[int, int]:
    """
    Extrai ano e mês do nome do arquivo
    
    Args:
        filename (str): Nome do arquivo (ex: 'abril2018', 'janeiro2020')
    
    Returns:
        Tuple[int, int]: (ano, mês_numérico)
        
    Examples:
        >>> extract_date_from_filename('abril2018')
        (2018, 4)
        >>> extract_date_from_filename('dezembro2019')
        (2019, 12)
    """
    # Dicionário para conversão mês nome -> número
    meses_num = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'maro': 3,  # maro é erro no dataset
        'abril': 4, 'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
        'setembro': 9, 'outubro': 10, 'novembro': 11, 'novrmbro': 11,  # novrmbro é erro
        'dezembro': 12
    }
    
    # Encontrar o ano (4 dígitos)
    import re
    ano_match = re.search(r'(\d{4})', filename)
    if not ano_match:
        raise ValueError(f"Ano não encontrado no nome do arquivo: {filename}")
    
    ano = int(ano_match.group(1))
    
    # Encontrar o mês
    mes_encontrado = None
    for mes_nome, mes_num in meses_num.items():
        if mes_nome in filename.lower():
            mes_encontrado = mes_num
            break
    
    if mes_encontrado is None:
        raise ValueError(f"Mês não encontrado no nome do arquivo: {filename}")
    
    return ano, mes_encontrado


def clean_price_column(df: pd.DataFrame, price_col: str = 'price') -> pd.DataFrame:
    """
    Limpa e converte a coluna de preços
    
    Args:
        df (pd.DataFrame): DataFrame com coluna de preços
        price_col (str): Nome da coluna de preços
    
    Returns:
        pd.DataFrame: DataFrame com preços limpos
    """
    df_clean = df.copy()
    
    if price_col not in df_clean.columns:
        print(f"⚠️  Coluna '{price_col}' não encontrada")
        return df_clean
    
    print(f"🧹 Limpando coluna de preços: {price_col}")
    
    # Remover símbolos de moeda e converter para float
    df_clean[price_col] = (df_clean[price_col]
                          .astype(str)
                          .str.replace('$', '', regex=False)
                          .str.replace(',', '', regex=False)
                          .str.replace('R', '', regex=False)
                          .str.strip())
    
    # Converter para numérico
    df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
    
    # Remover valores nulos ou zero
    initial_count = len(df_clean)
    df_clean = df_clean[df_clean[price_col].notna()]
    df_clean = df_clean[df_clean[price_col] > 0]
    
    print(f"   📊 Removidos {initial_count - len(df_clean)} registros com preços inválidos")
    
    return df_clean


def remove_outliers(df: pd.DataFrame, 
                   column: str, 
                   method: str = 'iqr',
                   factor: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers de uma coluna específica
    
    Args:
        df (pd.DataFrame): DataFrame
        column (str): Nome da coluna
        method (str): Método ('iqr', 'zscore', 'percentile')
        factor (float): Fator para definição de outliers
    
    Returns:
        pd.DataFrame: DataFrame sem outliers
    """
    df_clean = df.copy()
    initial_count = len(df_clean)
    
    if column not in df_clean.columns:
        print(f"⚠️  Coluna '{column}' não encontrada")
        return df_clean
    
    if method == 'iqr':
        Q1 = df_clean[column].quantile(0.25)
        Q3 = df_clean[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        df_clean = df_clean[
            (df_clean[column] >= lower_bound) & 
            (df_clean[column] <= upper_bound)
        ]
        
    elif method == 'percentile':
        lower_percentile = (1 - factor) * 100 / 2
        upper_percentile = 100 - lower_percentile
        
        lower_bound = df_clean[column].quantile(lower_percentile / 100)
        upper_bound = df_clean[column].quantile(upper_percentile / 100)
        
        df_clean = df_clean[
            (df_clean[column] >= lower_bound) & 
            (df_clean[column] <= upper_bound)
        ]
    
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df_clean[column]))
        df_clean = df_clean[z_scores < factor]
    
    removed_count = initial_count - len(df_clean)
    print(f"   🎯 Removidos {removed_count} outliers da coluna '{column}' (método: {method})")
    
    return df_clean


def encode_categorical_variables(df: pd.DataFrame, 
                                columns: List[str] = None) -> pd.DataFrame:
    """
    Codifica variáveis categóricas usando pd.get_dummies
    
    Args:
        df (pd.DataFrame): DataFrame
        columns (List[str], optional): Lista de colunas para codificar.
                                     Se None, usa todas as colunas object/category.
    
    Returns:
        pd.DataFrame: DataFrame com variáveis codificadas
    """
    df_encoded = df.copy()
    
    if columns is None:
        # Selecionar colunas categóricas automaticamente
        columns = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
    
    print(f"🔢 Codificando {len(columns)} variáveis categóricas...")
    
    for col in columns:
        if col in df_encoded.columns:
            print(f"   📝 Codificando: {col}")
            # Criar variáveis dummy
            dummies = pd.get_dummies(df_encoded[col], prefix=col)
            # Adicionar ao DataFrame
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            # Remover coluna original
            df_encoded = df_encoded.drop(columns=[col])
    
    print(f"✅ Codificação concluída. Shape final: {df_encoded.shape}")
    
    return df_encoded


def validate_data_quality(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analisa a qualidade dos dados e retorna métricas
    
    Args:
        df (pd.DataFrame): DataFrame para analisar
    
    Returns:
        Dict[str, any]: Dicionário com métricas de qualidade
    """
    print("🔍 Analisando qualidade dos dados...")
    
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'dtypes_count': df.dtypes.value_counts().to_dict(),
        'columns_with_nulls': df.columns[df.isnull().any()].tolist(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict()
    }
    
    # Relatório detalhado
    print(f"   📊 Total de registros: {quality_report['total_rows']:,}")
    print(f"   📊 Total de colunas: {quality_report['total_columns']}")
    print(f"   ❌ Valores ausentes: {quality_report['missing_values']:,}")
    print(f"   🔄 Linhas duplicadas: {quality_report['duplicate_rows']:,}")
    print(f"   💾 Uso de memória: {quality_report['memory_usage_mb']:.2f} MB")
    
    if quality_report['columns_with_nulls']:
        print(f"   ⚠️  Colunas com valores nulos: {len(quality_report['columns_with_nulls'])}")
    
    return quality_report


def save_processed_data(df: pd.DataFrame, 
                       filename: str = "dados_processados.csv",
                       output_dir: pathlib.Path = None) -> pathlib.Path:
    """
    Salva dados processados
    
    Args:
        df (pd.DataFrame): DataFrame para salvar
        filename (str): Nome do arquivo
        output_dir (pathlib.Path, optional): Diretório de saída
    
    Returns:
        pathlib.Path: Caminho do arquivo salvo
    """
    if output_dir is None:
        output_dir = Config.PROCESSED_DATA_DIR
    
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename
    
    print(f"💾 Salvando dados processados: {file_path}")
    
    # Salvar com compressão para economizar espaço
    df.to_csv(file_path, index=False, compression='gzip' if filename.endswith('.gz') else None)
    
    file_size_mb = file_path.stat().st_size / 1024**2
    print(f"✅ Arquivo salvo: {file_size_mb:.2f} MB")
    
    return file_path


def create_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria um resumo das features do dataset
    
    Args:
        df (pd.DataFrame): DataFrame para analisar
    
    Returns:
        pd.DataFrame: Resumo das features
    """
    print("📈 Criando resumo das features...")
    
    summary_data = []
    
    for col in df.columns:
        col_info = {
            'feature': col,
            'dtype': str(df[col].dtype),
            'non_null_count': df[col].count(),
            'null_count': df[col].isnull().sum(),
            'null_percentage': round(df[col].isnull().sum() / len(df) * 100, 2),
            'unique_values': df[col].nunique(),
            'is_numeric': pd.api.types.is_numeric_dtype(df[col])
        }
        
        # Estatísticas específicas para colunas numéricas
        if col_info['is_numeric']:
            col_info.update({
                'mean': round(df[col].mean(), 2) if df[col].notna().any() else None,
                'std': round(df[col].std(), 2) if df[col].notna().any() else None,
                'min': df[col].min() if df[col].notna().any() else None,
                'max': df[col].max() if df[col].notna().any() else None,
                'median': round(df[col].median(), 2) if df[col].notna().any() else None
            })
        else:
            # Para colunas categóricas, mostrar valores mais frequentes
            if col_info['unique_values'] > 0:
                most_frequent = df[col].value_counts().index[0] if len(df[col].value_counts()) > 0 else None
                col_info['most_frequent'] = most_frequent
        
        summary_data.append(col_info)
    
    summary_df = pd.DataFrame(summary_data)
    
    print(f"✅ Resumo criado para {len(summary_df)} features")
    
    return summary_df


if __name__ == "__main__":
    # Teste das funções utilitárias
    print("=== TESTE DAS FUNÇÕES UTILITÁRIAS ===")
    
    # Teste da extração de data
    test_files = ['abril2018', 'dezembro2019', 'maro2020', 'novrmbro2018']
    for filename in test_files:
        try:
            ano, mes = extract_date_from_filename(filename)
            print(f"{filename} -> Ano: {ano}, Mês: {mes}")
        except ValueError as e:
            print(f"Erro em {filename}: {e}")