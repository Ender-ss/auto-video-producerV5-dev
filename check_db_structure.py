#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def check_database_structure():
    """Verificar estrutura do banco de dados"""
    db_path = 'backend/instance/auto_video_producer.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"🔍 Examinando banco de dados: {db_path}")
        print("=" * 50)
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📋 Tabelas disponíveis:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # Mostrar estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(f"    Colunas:")
            for col in columns:
                print(f"      {col[1]} ({col[2]})")
            print()
        
        # Buscar por dados relacionados a Pipeline #2025-09-09-009
        print("🔍 Buscando dados relacionados a '2025-09-09-009':")
        print("=" * 50)
        
        for table in tables:
            table_name = table[0]
            try:
                # Tentar buscar em todas as colunas de texto
                cursor.execute(f"SELECT * FROM {table_name} WHERE CAST({table_name} AS TEXT) LIKE '%2025-09-09-009%' LIMIT 5;")
                results = cursor.fetchall()
                if results:
                    print(f"📍 Encontrado em {table_name}:")
                    for row in results:
                        print(f"  {row}")
                    print()
            except Exception as e:
                # Tentar busca mais específica se a busca geral falhar
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
                    sample = cursor.fetchone()
                    if sample:
                        # Buscar em cada coluna individualmente
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        columns = cursor.fetchall()
                        for col in columns:
                            col_name = col[1]
                            try:
                                cursor.execute(f"SELECT * FROM {table_name} WHERE {col_name} LIKE '%2025-09-09-009%' LIMIT 3;")
                                col_results = cursor.fetchall()
                                if col_results:
                                    print(f"📍 Encontrado em {table_name}.{col_name}:")
                                    for row in col_results:
                                        print(f"  {row}")
                                    print()
                            except:
                                continue
                except:
                    continue
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao examinar banco de dados: {e}")

if __name__ == "__main__":
    check_database_structure()