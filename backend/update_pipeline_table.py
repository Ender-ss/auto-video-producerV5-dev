import sqlite3
import os
import shutil
from datetime import datetime

def update_pipeline_table():
    """Atualiza a tabela pipeline para adicionar a coluna script_processing_results"""
    
    # Caminho para o banco de dados
    db_path = '../instance/auto_video_producer.db'
    
    # Verificar se o banco de dados existe
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        return False
    
    # Criar backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"../instance/auto_video_producer_backup_{timestamp}.db"
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup criado em: {backup_path}")
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return False
    
    # Conectar ao banco de dados
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(pipeline)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'script_processing_results' in columns:
            print("✅ A coluna 'script_processing_results' já existe na tabela pipeline")
            conn.close()
            return True
        
        # Adicionar a coluna
        cursor.execute("ALTER TABLE pipeline ADD COLUMN script_processing_results TEXT")
        conn.commit()
        
        # Verificar se a coluna foi adicionada
        cursor.execute("PRAGMA table_info(pipeline)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'script_processing_results' in columns:
            print("✅ Coluna 'script_processing_results' adicionada com sucesso!")
            conn.close()
            return True
        else:
            print("❌ Erro: a coluna não foi adicionada")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Erro ao atualizar o banco de dados: {e}")
        return False

if __name__ == '__main__':
    print("=== Atualização da Tabela Pipeline ===")
    success = update_pipeline_table()
    
    if success:
        print("✅ Atualização concluída com sucesso!")
        print("🔄 Por favor, reinicie o backend para aplicar as alterações.")
    else:
        print("❌ Falha na atualização!")