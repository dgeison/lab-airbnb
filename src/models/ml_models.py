"""
Modelos de Machine Learning - Projeto Airbnb Rio
================================================

Este módulo contém a implementação dos modelos de machine learning para:
- Treinamento de modelos de regressão
- Avaliação de performance
- Seleção do melhor modelo
- Persistência de modelos

Autor: Projeto Airbnb Rio
Data: 2024
"""

import pandas as pd
import numpy as np
import joblib
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Imports locais
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import Config, ModelConfig


class AirbnbPricePredictor:
    """
    Classe principal para predição de preços do Airbnb
    
    Esta classe encapsula todo o pipeline de machine learning:
    - Preparação dos dados
    - Treinamento de múltiplos modelos
    - Avaliação e seleção do melhor modelo
    - Predições
    """
    
    def __init__(self, random_state: int = None):
        """
        Inicializa o preditor
        
        Args:
            random_state (int, optional): Seed para reprodutibilidade
        """
        self.random_state = random_state or Config.RANDOM_STATE
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False
        
        # Configurar modelos disponíveis
        self._setup_models()
    
    def _setup_models(self):
        """Configura os modelos disponíveis para treinamento"""
        self.models = {
            'ExtraTreesRegressor': ExtraTreesRegressor(**Config.EXTRA_TREES_PARAMS),
            'RandomForestRegressor': RandomForestRegressor(**Config.RANDOM_FOREST_PARAMS),
            'LinearRegression': LinearRegression()
        }
        
        print(f"🤖 Modelos configurados: {list(self.models.keys())}")
    
    def prepare_data(self, 
                    df: pd.DataFrame, 
                    target_column: str = 'price',
                    test_size: float = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Prepara os dados para treinamento
        
        Args:
            df (pd.DataFrame): Dataset completo
            target_column (str): Nome da coluna target
            test_size (float, optional): Proporção do conjunto de teste
        
        Returns:
            Tuple: (X_train, X_test, y_train, y_test)
        """
        print("🔧 Preparando dados para treinamento...")
        
        if test_size is None:
            test_size = Config.TEST_SIZE
        
        # Verificar se target existe
        if target_column not in df.columns:
            raise ValueError(f"Coluna target '{target_column}' não encontrada no dataset")
        
        # Separar features e target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Remover colunas não numéricas que não foram codificadas
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X = X[numeric_columns]
        
        print(f"   📊 Features selecionadas: {X.shape[1]}")
        print(f"   📊 Registros: {X.shape[0]:,}")
        
        # Armazenar nomes das features para uso posterior
        self.feature_names = X.columns.tolist()
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=self.random_state,
            stratify=None  # Para regressão, não fazemos stratify
        )
        
        print(f"   ✅ Divisão realizada:")
        print(f"      🔹 Treino: {X_train.shape[0]:,} registros")
        print(f"      🔹 Teste: {X_test.shape[0]:,} registros")
        
        return X_train, X_test, y_train, y_test
    
    def train_models(self, 
                    X_train: pd.DataFrame, 
                    y_train: pd.Series,
                    use_cross_validation: bool = True,
                    cv_folds: int = 5) -> Dict[str, Dict[str, float]]:
        """
        Treina todos os modelos configurados
        
        Args:
            X_train (pd.DataFrame): Features de treino
            y_train (pd.Series): Target de treino
            use_cross_validation (bool): Se deve usar validação cruzada
            cv_folds (int): Número de folds para CV
        
        Returns:
            Dict[str, Dict[str, float]]: Resultados de treinamento
        """
        print("🚀 Iniciando treinamento dos modelos...")
        
        results = {}
        
        for model_name, model in self.models.items():
            print(f"\n🔄 Treinando: {model_name}")
            
            try:
                # Treinar modelo
                model.fit(X_train, y_train)
                
                # Avaliar com validação cruzada (se solicitado)
                if use_cross_validation:
                    cv_scores = cross_val_score(
                        model, X_train, y_train, 
                        cv=cv_folds, 
                        scoring='r2',
                        n_jobs=-1
                    )
                    
                    results[model_name] = {
                        'cv_mean_r2': cv_scores.mean(),
                        'cv_std_r2': cv_scores.std(),
                        'cv_scores': cv_scores.tolist()
                    }
                    
                    print(f"   ✅ R² (CV): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
                else:
                    # Avaliação simples no conjunto de treino
                    train_score = model.score(X_train, y_train)
                    results[model_name] = {
                        'train_r2': train_score
                    }
                    
                    print(f"   ✅ R² (treino): {train_score:.4f}")
                
            except Exception as e:
                print(f"   ❌ Erro ao treinar {model_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        print("\n🎯 Treinamento concluído!")
        self.is_trained = True
        
        return results
    
    def evaluate_models(self, 
                       X_test: pd.DataFrame, 
                       y_test: pd.Series) -> Dict[str, Dict[str, float]]:
        """
        Avalia todos os modelos treinados no conjunto de teste
        
        Args:
            X_test (pd.DataFrame): Features de teste
            y_test (pd.Series): Target de teste
        
        Returns:
            Dict[str, Dict[str, float]]: Métricas de avaliação
        """
        print("📊 Avaliando modelos no conjunto de teste...")
        
        if not self.is_trained:
            raise ValueError("Modelos devem ser treinados antes da avaliação")
        
        evaluation_results = {}
        
        for model_name, model in self.models.items():
            print(f"\n📈 Avaliando: {model_name}")
            
            try:
                # Fazer predições
                y_pred = model.predict(X_test)
                
                # Calcular métricas
                metrics = {
                    'r2_score': r2_score(y_test, y_pred),
                    'mean_absolute_error': mean_absolute_error(y_test, y_pred),
                    'mean_squared_error': mean_squared_error(y_test, y_pred),
                    'root_mean_squared_error': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'mean_absolute_percentage_error': mean_absolute_percentage_error(y_test, y_pred)
                }
                
                evaluation_results[model_name] = metrics
                
                # Exibir resultados
                print(f"   🎯 R²: {metrics['r2_score']:.4f}")
                print(f"   📏 MAE: R$ {metrics['mean_absolute_error']:.2f}")
                print(f"   📐 RMSE: R$ {metrics['root_mean_squared_error']:.2f}")
                print(f"   📊 MAPE: {metrics['mean_absolute_percentage_error']:.2%}")
                
            except Exception as e:
                print(f"   ❌ Erro ao avaliar {model_name}: {e}")
                evaluation_results[model_name] = {'error': str(e)}
        
        return evaluation_results
    
    def select_best_model(self, evaluation_results: Dict[str, Dict[str, float]]) -> str:
        """
        Seleciona o melhor modelo baseado no R²
        
        Args:
            evaluation_results (Dict): Resultados da avaliação
        
        Returns:
            str: Nome do melhor modelo
        """
        print("\n🏆 Selecionando o melhor modelo...")
        
        valid_models = {
            name: results for name, results in evaluation_results.items() 
            if 'error' not in results and 'r2_score' in results
        }
        
        if not valid_models:
            raise ValueError("Nenhum modelo válido encontrado")
        
        # Selecionar modelo com maior R²
        best_model_name = max(valid_models.keys(), 
                             key=lambda k: valid_models[k]['r2_score'])
        
        self.best_model_name = best_model_name
        self.best_model = self.models[best_model_name]
        
        best_r2 = valid_models[best_model_name]['r2_score']
        print(f"🥇 Melhor modelo: {best_model_name} (R² = {best_r2:.4f})")
        
        return best_model_name
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Retorna a importância das features do melhor modelo
        
        Args:
            top_n (int): Número de features mais importantes
        
        Returns:
            pd.DataFrame: DataFrame com importâncias
        """
        if self.best_model is None:
            raise ValueError("Melhor modelo não foi selecionado ainda")
        
        # Verificar se o modelo tem feature_importances_
        if not hasattr(self.best_model, 'feature_importances_'):
            print("⚠️  Modelo selecionado não possui feature_importances_")
            return pd.DataFrame()
        
        # Criar DataFrame com importâncias
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"📊 Top {top_n} features mais importantes:")
        for i, row in importance_df.head(top_n).iterrows():
            print(f"   {row['feature']}: {row['importance']:.4f}")
        
        return importance_df.head(top_n)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Faz predições usando o melhor modelo
        
        Args:
            X (pd.DataFrame): Features para predição
        
        Returns:
            np.ndarray: Predições
        """
        if self.best_model is None:
            raise ValueError("Modelo deve ser treinado e selecionado antes de fazer predições")
        
        # Verificar se as features estão corretas
        if self.feature_names:
            missing_features = set(self.feature_names) - set(X.columns)
            if missing_features:
                raise ValueError(f"Features ausentes: {missing_features}")
            
            # Reordenar colunas
            X = X[self.feature_names]
        
        return self.best_model.predict(X)
    
    def save_model(self, filepath: Path = None) -> Path:
        """
        Salva o melhor modelo treinado
        
        Args:
            filepath (Path, optional): Caminho para salvar. Se None, usa padrão.
        
        Returns:
            Path: Caminho onde o modelo foi salvo
        """
        if self.best_model is None:
            raise ValueError("Nenhum modelo foi selecionado para salvar")
        
        if filepath is None:
            filepath = Config.MODEL_FILE
        
        # Criar dicionário com todos os dados necessários
        model_data = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'feature_names': self.feature_names,
            'scaler': self.scaler,
            'random_state': self.random_state
        }
        
        print(f"💾 Salvando modelo: {filepath}")
        joblib.dump(model_data, filepath)
        
        file_size_kb = filepath.stat().st_size / 1024
        print(f"✅ Modelo salvo: {file_size_kb:.2f} KB")
        
        return filepath
    
    @classmethod
    def load_model(cls, filepath: Path = None) -> 'AirbnbPricePredictor':
        """
        Carrega um modelo salvo
        
        Args:
            filepath (Path, optional): Caminho do modelo. Se None, usa padrão.
        
        Returns:
            AirbnbPricePredictor: Instância com modelo carregado
        """
        if filepath is None:
            filepath = Config.MODEL_FILE
        
        if not filepath.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {filepath}")
        
        print(f"📂 Carregando modelo: {filepath}")
        
        # Carregar dados do modelo
        model_data = joblib.load(filepath)
        
        # Criar nova instância
        predictor = cls(random_state=model_data.get('random_state', Config.RANDOM_STATE))
        
        # Restaurar estado
        predictor.best_model = model_data['model']
        predictor.best_model_name = model_data['model_name']
        predictor.feature_names = model_data['feature_names']
        predictor.scaler = model_data.get('scaler', StandardScaler())
        predictor.is_trained = True
        
        print(f"✅ Modelo carregado: {predictor.best_model_name}")
        
        return predictor


def create_model_comparison_report(evaluation_results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Cria um relatório comparativo dos modelos
    
    Args:
        evaluation_results (Dict): Resultados da avaliação
    
    Returns:
        pd.DataFrame: Relatório comparativo
    """
    print("📋 Criando relatório comparativo dos modelos...")
    
    report_data = []
    
    for model_name, metrics in evaluation_results.items():
        if 'error' not in metrics:
            report_data.append({
                'Modelo': model_name,
                'R²': f"{metrics.get('r2_score', 0):.4f}",
                'MAE (R$)': f"{metrics.get('mean_absolute_error', 0):.2f}",
                'RMSE (R$)': f"{metrics.get('root_mean_squared_error', 0):.2f}",
                'MAPE (%)': f"{metrics.get('mean_absolute_percentage_error', 0):.2%}"
            })
    
    report_df = pd.DataFrame(report_data)
    
    if not report_df.empty:
        # Ordenar por R²
        report_df['R²_numeric'] = report_df['R²'].astype(float)
        report_df = report_df.sort_values('R²_numeric', ascending=False)
        report_df = report_df.drop('R²_numeric', axis=1)
        
        print("🏆 Ranking dos modelos (por R²):")
        for i, row in report_df.iterrows():
            print(f"   {i+1}º {row['Modelo']} - R²: {row['R²']}")
    
    return report_df


if __name__ == "__main__":
    # Teste da classe AirbnbPricePredictor
    print("=== TESTE DO SISTEMA DE MODELOS ===")
    
    # Criar dados sintéticos para teste
    np.random.seed(42)
    n_samples = 1000
    
    test_data = pd.DataFrame({
        'accommodates': np.random.randint(1, 10, n_samples),
        'bedrooms': np.random.randint(1, 5, n_samples),
        'bathrooms': np.random.uniform(1, 3, n_samples),
        'latitude': np.random.uniform(-23.1, -22.8, n_samples),
        'longitude': np.random.uniform(-43.8, -43.1, n_samples),
        'price': np.random.uniform(50, 500, n_samples)
    })
    
    # Teste do predictor
    predictor = AirbnbPricePredictor()
    X_train, X_test, y_train, y_test = predictor.prepare_data(test_data)
    
    training_results = predictor.train_models(X_train, y_train, use_cross_validation=False)
    evaluation_results = predictor.evaluate_models(X_test, y_test)
    
    best_model = predictor.select_best_model(evaluation_results)
    
    print(f"\n✅ Teste concluído! Melhor modelo: {best_model}")