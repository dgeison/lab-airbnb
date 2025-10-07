"""
Controladores - Projeto Airbnb Rio
==================================

Este módulo contém os controladores que coordenam:
- Pipeline de processamento de dados
- Treinamento de modelos
- Validação de entrada
- Lógica de negócio da aplicação

Autor: Projeto Airbnb Rio
Data: 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import logging

# Imports locais
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import Config, DataConfig, ModelConfig
from utils.data_processing import (
    load_raw_data, clean_price_column, remove_outliers, 
    encode_categorical_variables, validate_data_quality,
    save_processed_data, create_feature_summary
)
from src.models.ml_models import AirbnbPricePredictor, create_model_comparison_report


class DataProcessingController:
    """
    Controlador responsável pelo pipeline completo de processamento de dados
    """
    
    def __init__(self):
        """Inicializa o controlador de processamento de dados"""
        self.raw_data = None
        self.processed_data = None
        self.quality_report = None
        self.feature_summary = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def execute_full_pipeline(self, 
                             save_intermediate: bool = True,
                             remove_outliers_enabled: bool = True) -> pd.DataFrame:
        """
        Executa o pipeline completo de processamento de dados
        
        Args:
            save_intermediate (bool): Se deve salvar dados intermediários
            remove_outliers_enabled (bool): Se deve remover outliers
        
        Returns:
            pd.DataFrame: Dados processados e prontos para ML
        """
        self.logger.info("🚀 Iniciando pipeline completo de processamento de dados")
        
        try:
            # 1. Carregamento dos dados brutos
            self.logger.info("📂 Etapa 1: Carregamento dos dados brutos")
            self.raw_data = self._load_data()
            
            # 2. Limpeza inicial
            self.logger.info("🧹 Etapa 2: Limpeza inicial dos dados")
            cleaned_data = self._initial_cleaning(self.raw_data)
            
            # 3. Análise de qualidade
            self.logger.info("🔍 Etapa 3: Análise de qualidade dos dados")
            self.quality_report = validate_data_quality(cleaned_data)
            
            # 4. Limpeza específica
            self.logger.info("🎯 Etapa 4: Limpeza específica por domínio")
            domain_cleaned = self._domain_specific_cleaning(cleaned_data)
            
            # 5. Remoção de outliers (opcional)
            if remove_outliers_enabled:
                self.logger.info("📊 Etapa 5: Remoção de outliers")
                outlier_cleaned = self._remove_outliers(domain_cleaned)
            else:
                outlier_cleaned = domain_cleaned
            
            # 6. Codificação de variáveis categóricas
            self.logger.info("🔢 Etapa 6: Codificação de variáveis categóricas")
            encoded_data = self._encode_features(outlier_cleaned)
            
            # 7. Preparação final
            self.logger.info("✨ Etapa 7: Preparação final dos dados")
            self.processed_data = self._final_preparation(encoded_data)
            
            # 8. Salvar dados processados
            if save_intermediate:
                self.logger.info("💾 Etapa 8: Salvando dados processados")
                save_processed_data(self.processed_data, "dados_processados_pipeline.csv")
            
            # 9. Criar resumo das features
            self.logger.info("📋 Etapa 9: Criando resumo das features")
            self.feature_summary = create_feature_summary(self.processed_data)
            
            self.logger.info("✅ Pipeline de processamento concluído com sucesso!")
            self.logger.info(f"   📊 Dados finais: {self.processed_data.shape[0]:,} registros, {self.processed_data.shape[1]} features")
            
            return self.processed_data
            
        except Exception as e:
            self.logger.error(f"❌ Erro no pipeline de processamento: {e}")
            raise
    
    def _load_data(self) -> pd.DataFrame:
        """Carrega dados brutos"""
        return load_raw_data(Config.RAW_DATA_DIR)
    
    def _initial_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpeza inicial dos dados"""
        df_clean = df.copy()
        
        # Remover colunas com muitos valores nulos (>80%)
        null_threshold = 0.8
        null_percentages = df_clean.isnull().sum() / len(df_clean)
        columns_to_drop = null_percentages[null_percentages > null_threshold].index.tolist()
        
        if columns_to_drop:
            self.logger.info(f"   🗑️  Removendo {len(columns_to_drop)} colunas com >80% nulos")
            df_clean = df_clean.drop(columns=columns_to_drop)
        
        # Remover duplicatas
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        duplicates_removed = initial_rows - len(df_clean)
        
        if duplicates_removed > 0:
            self.logger.info(f"   🔄 Removidas {duplicates_removed:,} linhas duplicadas")
        
        return df_clean
    
    def _domain_specific_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpeza específica do domínio Airbnb"""
        df_clean = df.copy()
        
        # Limpar coluna de preços
        if 'price' in df_clean.columns:
            df_clean = clean_price_column(df_clean, 'price')
        
        # Filtrar por limites de preço (remover valores extremos)
        if 'price' in df_clean.columns:
            initial_count = len(df_clean)
            df_clean = df_clean[
                (df_clean['price'] >= Config.PRICE_LIMITS['min']) & 
                (df_clean['price'] <= Config.PRICE_LIMITS['max'])
            ]
            removed = initial_count - len(df_clean)
            if removed > 0:
                self.logger.info(f"   💰 Removidos {removed:,} registros com preços extremos")
        
        # Filtrar por número de acomodações
        if 'accommodates' in df_clean.columns:
            initial_count = len(df_clean)
            df_clean = df_clean[df_clean['accommodates'] <= Config.ACCOMMODATES_LIMIT]
            removed = initial_count - len(df_clean)
            if removed > 0:
                self.logger.info(f"   🏠 Removidos {removed:,} registros com muitas acomodações")
        
        # Converter colunas boolean
        for col in Config.BOOLEAN_COLUMNS:
            if col in df_clean.columns:
                # Converter 't'/'f' para True/False
                df_clean[col] = df_clean[col].map({'t': True, 'f': False})
                # Converter para int (True=1, False=0)
                df_clean[col] = df_clean[col].astype(int)
        
        return df_clean
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers das colunas numéricas principais"""
        df_clean = df.copy()
        
        # Colunas para remoção de outliers
        outlier_columns = ['price', 'accommodates', 'bedrooms', 'bathrooms', 'beds']
        
        for col in outlier_columns:
            if col in df_clean.columns:
                df_clean = remove_outliers(df_clean, col, method='iqr', factor=1.5)
        
        return df_clean
    
    def _encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Codifica variáveis categóricas"""
        df_encoded = df.copy()
        
        # Identificar colunas categóricas para codificação
        categorical_cols = []
        
        for col in Config.CATEGORICAL_COLUMNS:
            if col in df_encoded.columns:
                categorical_cols.append(col)
        
        if categorical_cols:
            df_encoded = encode_categorical_variables(df_encoded, categorical_cols)
        
        return df_encoded
    
    def _final_preparation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preparação final dos dados"""
        df_final = df.copy()
        
        # Selecionar apenas colunas numéricas para ML
        numeric_columns = df_final.select_dtypes(include=[np.number]).columns
        df_final = df_final[numeric_columns]
        
        # Remover colunas identificadoras que não devem ser usadas para ML
        id_columns = ['id', 'host_id', 'ano', 'mes']
        id_columns_present = [col for col in id_columns if col in df_final.columns]
        
        if id_columns_present:
            self.logger.info(f"   🔢 Removendo colunas ID: {id_columns_present}")
            df_final = df_final.drop(columns=id_columns_present)
        
        # Remover linhas com valores nulos restantes
        initial_rows = len(df_final)
        df_final = df_final.dropna()
        removed_nulls = initial_rows - len(df_final)
        
        if removed_nulls > 0:
            self.logger.info(f"   ❌ Removidas {removed_nulls:,} linhas com valores nulos")
        
        return df_final
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo do processamento realizado
        
        Returns:
            Dict: Resumo das operações de processamento
        """
        summary = {
            'raw_data_shape': self.raw_data.shape if self.raw_data is not None else None,
            'processed_data_shape': self.processed_data.shape if self.processed_data is not None else None,
            'quality_report': self.quality_report,
            'feature_summary': self.feature_summary.to_dict() if self.feature_summary is not None else None
        }
        
        return summary


class ModelTrainingController:
    """
    Controlador responsável pelo treinamento e avaliação de modelos
    """
    
    def __init__(self):
        """Inicializa o controlador de treinamento"""
        self.predictor = None
        self.training_results = None
        self.evaluation_results = None
        self.model_comparison = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def execute_full_training(self, 
                             data: pd.DataFrame,
                             target_column: str = 'price',
                             use_cross_validation: bool = True,
                             save_model: bool = True) -> Dict[str, Any]:
        """
        Executa o pipeline completo de treinamento de modelos
        
        Args:
            data (pd.DataFrame): Dados preprocessados
            target_column (str): Nome da coluna target
            use_cross_validation (bool): Se deve usar validação cruzada
            save_model (bool): Se deve salvar o melhor modelo
        
        Returns:
            Dict: Resultados completos do treinamento
        """
        self.logger.info("🚀 Iniciando pipeline completo de treinamento")
        
        try:
            # 1. Inicializar predictor
            self.logger.info("🤖 Etapa 1: Inicializando predictor")
            self.predictor = AirbnbPricePredictor()
            
            # 2. Preparar dados
            self.logger.info("🔧 Etapa 2: Preparando dados para treinamento")
            X_train, X_test, y_train, y_test = self.predictor.prepare_data(data, target_column)
            
            # 3. Treinar modelos
            self.logger.info("🚀 Etapa 3: Treinando modelos")
            self.training_results = self.predictor.train_models(
                X_train, y_train, 
                use_cross_validation=use_cross_validation
            )
            
            # 4. Avaliar modelos
            self.logger.info("📊 Etapa 4: Avaliando modelos")
            self.evaluation_results = self.predictor.evaluate_models(X_test, y_test)
            
            # 5. Selecionar melhor modelo
            self.logger.info("🏆 Etapa 5: Selecionando melhor modelo")
            best_model_name = self.predictor.select_best_model(self.evaluation_results)
            
            # 6. Criar relatório comparativo
            self.logger.info("📋 Etapa 6: Criando relatório comparativo")
            self.model_comparison = create_model_comparison_report(self.evaluation_results)
            
            # 7. Analisar importância das features
            self.logger.info("📈 Etapa 7: Analisando importância das features")
            feature_importance = self.predictor.get_feature_importance()
            
            # 8. Salvar modelo (opcional)
            model_path = None
            if save_model:
                self.logger.info("💾 Etapa 8: Salvando melhor modelo")
                model_path = self.predictor.save_model()
            
            # Compilar resultados
            results = {
                'best_model_name': best_model_name,
                'training_results': self.training_results,
                'evaluation_results': self.evaluation_results,
                'model_comparison': self.model_comparison,
                'feature_importance': feature_importance,
                'model_path': str(model_path) if model_path else None,
                'data_info': {
                    'train_size': len(X_train),
                    'test_size': len(X_test),
                    'n_features': len(X_train.columns),
                    'target_column': target_column
                }
            }
            
            self.logger.info("✅ Pipeline de treinamento concluído com sucesso!")
            self.logger.info(f"   🥇 Melhor modelo: {best_model_name}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Erro no pipeline de treinamento: {e}")
            raise
    
    def get_training_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo do treinamento realizado
        
        Returns:
            Dict: Resumo das operações de treinamento
        """
        summary = {
            'training_completed': self.predictor is not None and self.predictor.is_trained,
            'best_model': self.predictor.best_model_name if self.predictor else None,
            'training_results': self.training_results,
            'evaluation_results': self.evaluation_results,
            'model_comparison': self.model_comparison.to_dict() if self.model_comparison is not None else None
        }
        
        return summary


class PredictionController:
    """
    Controlador responsável por fazer predições com modelo treinado
    """
    
    def __init__(self, model_path: Path = None):
        """
        Inicializa o controlador de predições
        
        Args:
            model_path (Path, optional): Caminho para modelo salvo
        """
        self.model_path = model_path or Config.MODEL_FILE
        self.predictor = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Carregar modelo se existir
        self._load_model_if_exists()
    
    def _load_model_if_exists(self):
        """Carrega modelo se ele existir"""
        if self.model_path.exists():
            try:
                self.predictor = AirbnbPricePredictor.load_model(self.model_path)
                self.logger.info("✅ Modelo carregado com sucesso")
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao carregar modelo: {e}")
                self.predictor = None
        else:
            self.logger.info("ℹ️  Nenhum modelo encontrado")
    
    def predict_price(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prediz o preço de um imóvel
        
        Args:
            property_data (Dict): Dados do imóvel
        
        Returns:
            Dict: Resultado da predição
        """
        if self.predictor is None:
            raise ValueError("Nenhum modelo carregado. Treine um modelo primeiro.")
        
        try:
            # Converter dados para DataFrame
            df_input = pd.DataFrame([property_data])
            
            # Fazer predição
            prediction = self.predictor.predict(df_input)
            
            result = {
                'predicted_price': float(prediction[0]),
                'input_data': property_data,
                'model_used': self.predictor.best_model_name,
                'success': True
            }
            
            self.logger.info(f"💰 Predição realizada: R$ {prediction[0]:.2f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erro na predição: {e}")
            return {
                'error': str(e),
                'success': False
            }
    
    def validate_input_data(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida os dados de entrada para predição
        
        Args:
            property_data (Dict): Dados do imóvel
        
        Returns:
            Dict: Resultado da validação
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Verificar se modelo está carregado
        if self.predictor is None:
            validation_result['is_valid'] = False
            validation_result['errors'].append("Modelo não carregado")
            return validation_result
        
        # Verificar features obrigatórias
        required_features = self.predictor.feature_names
        missing_features = set(required_features) - set(property_data.keys())
        
        if missing_features:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Features ausentes: {list(missing_features)}")
        
        # Validações específicas do domínio
        if 'price' in property_data:
            validation_result['warnings'].append("Campo 'price' será ignorado na predição")
        
        if 'accommodates' in property_data:
            if property_data['accommodates'] <= 0 or property_data['accommodates'] > 20:
                validation_result['is_valid'] = False
                validation_result['errors'].append("'accommodates' deve estar entre 1 e 20")
        
        return validation_result
    
    def is_model_available(self) -> bool:
        """
        Verifica se modelo está disponível para predições
        
        Returns:
            bool: True se modelo disponível
        """
        return self.predictor is not None and self.predictor.is_trained


if __name__ == "__main__":
    # Teste dos controladores
    print("=== TESTE DOS CONTROLADORES ===")
    
    # Teste do controlador de processamento
    print("\n1. Testando DataProcessingController...")
    try:
        data_controller = DataProcessingController()
        # Note: Este teste requer dados reais no diretório configurado
        print("✅ DataProcessingController inicializado")
    except Exception as e:
        print(f"⚠️  Erro no teste do DataProcessingController: {e}")
    
    # Teste do controlador de predições
    print("\n2. Testando PredictionController...")
    pred_controller = PredictionController()
    print(f"   Modelo disponível: {pred_controller.is_model_available()}")
    
    print("\n✅ Testes dos controladores concluídos")