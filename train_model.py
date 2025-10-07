"""
Script de Treinamento - Projeto Airbnb Rio
==========================================

Este script executa o pipeline completo de treinamento:
1. Carregamento e processamento dos dados
2. Treinamento de múltiplos modelos
3. Avaliação e seleção do melhor modelo
4. Salvamento do modelo final

Uso:
    python train_model.py

Autor: Projeto Airbnb Rio
Data: 2024
"""

import sys
import argparse
from pathlib import Path
import logging

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from config.settings import Config, create_directories
from src.controllers.app_controllers import DataProcessingController, ModelTrainingController


def setup_logging():
    """Configura sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('training.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Função principal do script de treinamento"""
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Treinar modelo de previsão de preços Airbnb')
    parser.add_argument('--skip-processing', action='store_true',
                       help='Pular processamento de dados (usar dados já processados)')
    parser.add_argument('--no-cross-validation', action='store_true',
                       help='Desabilitar validação cruzada (treinamento mais rápido)')
    parser.add_argument('--target-column', default='price',
                       help='Nome da coluna target (padrão: price)')
    parser.add_argument('--output-dir', type=str,
                       help='Diretório para salvar resultados')
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logging()
    logger.info("🚀 Iniciando script de treinamento do modelo Airbnb Rio")
    
    try:
        # Verificar e criar diretórios necessários
        logger.info("📁 Verificando estrutura de diretórios...")
        create_directories()
        
        # Etapa 1: Processamento de Dados (se necessário)
        processed_data = None
        
        if not args.skip_processing:
            logger.info("=" * 60)
            logger.info("🔧 ETAPA 1: PROCESSAMENTO DOS DADOS")
            logger.info("=" * 60)
            
            data_controller = DataProcessingController()
            
            # Executar pipeline completo de processamento
            processed_data = data_controller.execute_full_pipeline(
                save_intermediate=True,
                remove_outliers_enabled=True
            )
            
            # Exibir resumo do processamento
            processing_summary = data_controller.get_processing_summary()
            
            logger.info("📊 Resumo do processamento:")
            logger.info(f"   • Dados brutos: {processing_summary['raw_data_shape']}")
            logger.info(f"   • Dados processados: {processing_summary['processed_data_shape']}")
            
            if processing_summary['quality_report']:
                qr = processing_summary['quality_report']
                logger.info(f"   • Valores ausentes: {qr['missing_values']:,}")
                logger.info(f"   • Linhas duplicadas: {qr['duplicate_rows']:,}")
                logger.info(f"   • Uso de memória: {qr['memory_usage_mb']:.2f} MB")
        
        else:
            logger.info("⏭️  Pulando processamento de dados (usando dados existentes)")
            
            # Carregar dados processados existentes
            data_file = Config.PROCESSED_DATA_DIR / "dados.csv"
            if not data_file.exists():
                raise FileNotFoundError(f"Dados processados não encontrados: {data_file}")
            
            import pandas as pd
            processed_data = pd.read_csv(data_file)
            logger.info(f"📂 Dados carregados: {processed_data.shape}")
        
        # Etapa 2: Treinamento dos Modelos
        logger.info("=" * 60)
        logger.info("🤖 ETAPA 2: TREINAMENTO DOS MODELOS")
        logger.info("=" * 60)
        
        training_controller = ModelTrainingController()
        
        # Executar pipeline completo de treinamento
        training_results = training_controller.execute_full_training(
            data=processed_data,
            target_column=args.target_column,
            use_cross_validation=not args.no_cross_validation,
            save_model=True
        )
        
        # Exibir resultados do treinamento
        logger.info("🏆 Resumo do treinamento:")
        logger.info(f"   • Melhor modelo: {training_results['best_model_name']}")
        logger.info(f"   • Tamanho do treino: {training_results['data_info']['train_size']:,}")
        logger.info(f"   • Tamanho do teste: {training_results['data_info']['test_size']:,}")
        logger.info(f"   • Número de features: {training_results['data_info']['n_features']}")
        
        # Exibir métricas do melhor modelo
        best_model = training_results['best_model_name']
        best_metrics = training_results['evaluation_results'][best_model]
        
        logger.info(f"📊 Métricas do {best_model}:")
        logger.info(f"   • R²: {best_metrics['r2_score']:.4f}")
        logger.info(f"   • MAE: R$ {best_metrics['mean_absolute_error']:.2f}")
        logger.info(f"   • RMSE: R$ {best_metrics['root_mean_squared_error']:.2f}")
        logger.info(f"   • MAPE: {best_metrics['mean_absolute_percentage_error']:.2%}")
        
        # Exibir top features importantes
        if not training_results['feature_importance'].empty:
            logger.info("🔝 Top 10 features mais importantes:")
            for i, row in training_results['feature_importance'].head(10).iterrows():
                logger.info(f"   {i+1:2d}. {row['feature']}: {row['importance']:.4f}")
        
        # Salvar resultados detalhados
        if args.output_dir:
            output_path = Path(args.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Salvar comparação de modelos
            model_comparison = training_results['model_comparison']
            model_comparison.to_csv(output_path / 'model_comparison.csv', index=False)
            
            # Salvar importância das features
            feature_importance = training_results['feature_importance']
            feature_importance.to_csv(output_path / 'feature_importance.csv', index=False)
            
            logger.info(f"💾 Resultados salvos em: {output_path}")
        
        # Etapa 3: Validação Final
        logger.info("=" * 60)
        logger.info("✅ ETAPA 3: VALIDAÇÃO FINAL")
        logger.info("=" * 60)
        
        # Verificar se modelo foi salvo corretamente
        model_path = Path(training_results['model_path']) if training_results['model_path'] else Config.MODEL_FILE
        
        if model_path.exists():
            model_size_kb = model_path.stat().st_size / 1024
            logger.info(f"✅ Modelo salvo: {model_path} ({model_size_kb:.2f} KB)")
        else:
            logger.error("❌ Erro: Modelo não foi salvo corretamente")
            return 1
        
        # Teste de carregamento do modelo
        from src.models.ml_models import AirbnbPricePredictor
        
        try:
            predictor = AirbnbPricePredictor.load_model(model_path)
            logger.info("✅ Modelo carregado e validado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo: {e}")
            return 1
        
        logger.info("=" * 60)
        logger.info("🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        logger.info("Para usar o modelo:")
        logger.info("1. Execute: streamlit run app_mvc.py")
        logger.info("2. Ou use: python -m src.controllers.app_controllers")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erro durante o treinamento: {e}")
        logger.error("Verifique os logs acima para mais detalhes")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)