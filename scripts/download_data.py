#!/usr/bin/env python3
"""
📥 SCRIPT DE DOWNLOAD DE DADOS - PROJETO AIRBNB

Este script faz o download automático dos dados do Inside Airbnb
para reproduzir o ambiente de desenvolvimento.

Uso:
    python scripts/download_data.py
"""

import os
import sys
import requests
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URLs dos dados (exemplo - ajustar conforme necessário)
DATA_URLS = {
    "abril2018.csv": "http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2018-04-03/data/listings.csv.gz",
    "maio2018.csv": "http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2018-05-02/data/listings.csv.gz",
    # Adicionar mais URLs conforme necessário
}

def create_directories():
    """Criar estrutura de diretórios necessária"""
    directories = [
        "data/raw",
        "data/processed", 
        "models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Diretório criado/verificado: {directory}")

def download_file(url: str, filename: str) -> bool:
    """
    Download de um arquivo individual
    
    Args:
        url (str): URL do arquivo
        filename (str): Nome do arquivo local
        
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        filepath = Path("data/raw") / filename
        
        if filepath.exists():
            logger.info(f"⏭️  Arquivo já existe: {filename}")
            return True
            
        logger.info(f"📥 Baixando: {filename}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logger.info(f"✅ Download concluído: {filename}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no download de {filename}: {str(e)}")
        return False

def download_all_data():
    """Download de todos os arquivos de dados"""
    logger.info("🚀 Iniciando download dos dados...")
    
    create_directories()
    
    success_count = 0
    total_files = len(DATA_URLS)
    
    for filename, url in DATA_URLS.items():
        if download_file(url, filename):
            success_count += 1
    
    logger.info(f"📊 Resultado: {success_count}/{total_files} arquivos baixados com sucesso")
    
    if success_count == total_files:
        logger.info("🎉 Todos os dados foram baixados com sucesso!")
        logger.info("➡️  Próximo passo: Execute o notebook de análise")
    else:
        logger.warning("⚠️  Alguns downloads falharam. Verifique os logs acima.")

def main():
    """Função principal"""
    print("=" * 60)
    print("📊 DOWNLOAD DE DADOS - PROJETO AIRBNB")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path("requirements.txt").exists():
        logger.error("❌ Execute este script a partir do diretório raiz do projeto!")
        sys.exit(1)
    
    try:
        download_all_data()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Download interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()