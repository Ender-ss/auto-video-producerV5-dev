#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db, Pipeline
except ImportError as e:
    print(f"Erro ao importar modulos: {e}")
    sys.exit(1)

def check_target_pipeline():
    pipeline_id = "aca7fdeb-a9ea-4083-9315-fc16d03798f1"
    
    with app.app_context():
        try:
            pipeline = Pipeline.query.filter_by(pipeline_id=pipeline_id).first()
            if pipeline:
                print(f"Pipeline {pipeline.display_name}:")
                print(f"  Status: {pipeline.status}")
                print(f"  Progresso: {pipeline.progress}%")
                print(f"  Erro: {pipeline.error_message or 'Nenhum'}")
                return True
            else:
                print(f"Pipeline nao encontrada")
                return False
                
        except Exception as e:
            print(f"Erro ao consultar banco: {e}")
            return False

if __name__ == "__main__":
    check_target_pipeline()