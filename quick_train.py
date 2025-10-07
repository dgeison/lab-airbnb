"""
Script Rápido de Treinamento - Compatibilidade MVC
=================================================

Script simplificado para gerar modelo compatível com nova estrutura MVC
usando os dados já processados existentes.

Uso: python quick_train.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adicionar ao path
sys.path.append(str(Path(__file__).parent))

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
from config.settings import Config

def quick_train():
    """Treinamento rápido para compatibilidade MVC"""
    print("🚀 Iniciando treinamento rápido...")
    
    # Verificar se dados processados existem
    data_file = Path("data/processed/dados.csv")
    if not data_file.exists():
        print("❌ Dados processados não encontrados!")
        print("Execute: notebooks/1_analise_e_treinamento.ipynb primeiro")
        return
    
    # Carregar dados
    print("📂 Carregando dados...")
    df = pd.read_csv(data_file)
    print(f"   📊 Shape: {df.shape}")
    
    # Preparar dados
    if 'price' not in df.columns:
        print("❌ Coluna 'price' não encontrada!")
        return
    
    # Separar features e target
    X = df.drop(['price'], axis=1)
    y = df['price']
    
    # Manter apenas colunas numéricas
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    X = X[numeric_cols]
    
    print(f"   🔢 Features numéricas: {len(numeric_cols)}")
    
    # Split treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    # Treinar modelo
    print("🤖 Treinando ExtraTreesRegressor...")
    model = ExtraTreesRegressor(
        n_estimators=300,
        random_state=42,
        max_depth=15,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Avaliar
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"   ✅ R²: {r2:.4f}")
    print(f"   ✅ MAE: R$ {mae:.2f}")
    
    # Criar dados do modelo no formato MVC
    model_data = {
        'model': model,
        'model_name': 'ExtraTreesRegressor',
        'feature_names': X.columns.tolist(),
        'scaler': None,  # Não usando scaler neste exemplo
        'random_state': 42
    }
    
    # Salvar modelo
    model_path = Path("modelo.joblib")
    print(f"💾 Salvando modelo: {model_path}")
    joblib.dump(model_data, model_path)
    
    # Verificar tamanho
    size_kb = model_path.stat().st_size / 1024
    print(f"   📦 Tamanho: {size_kb:.2f} KB")
    
    print("✅ Treinamento concluído! Execute: streamlit run app_mvc.py")

if __name__ == "__main__":
    quick_train()