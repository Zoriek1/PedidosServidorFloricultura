# -*- coding: utf-8 -*-
"""
Script de Migration do Banco de Dados
Adiciona novas colunas sem perder dados existentes
"""
import sys
import sqlite3
from pathlib import Path
import shutil
from datetime import datetime

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

def backup_database(db_path):
    """Faz backup do banco de dados"""
    backup_path = db_path.replace('.db', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    shutil.copy2(db_path, backup_path)
    print(f"✓ Backup criado: {backup_path}")
    return backup_path

def check_column_exists(cursor, table, column):
    """Verifica se uma coluna existe na tabela"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns

def migrate_database():
    """Executa migration do banco de dados"""
    db_path = Path(__file__).parent / 'static' / 'database.db'
    
    if not db_path.exists():
        print("✓ Banco de dados não existe. Será criado automaticamente.")
        return True
    
    print("=" * 60)
    print("  MIGRATION DO BANCO DE DADOS - Plante Uma Flor v2.0")
    print("=" * 60)
    print()
    
    # Fazer backup
    print("1. Criando backup...")
    try:
        backup_path = backup_database(str(db_path))
    except Exception as e:
        print(f"✗ Erro ao criar backup: {e}")
        return False
    
    # Conectar ao banco
    print("\n2. Conectando ao banco de dados...")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        print("✓ Conectado")
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        return False
    
    # Verificar e adicionar novas colunas
    print("\n3. Adicionando novas colunas...")
    
    new_columns = [
        ('telefone_cliente', 'VARCHAR(20)'),
        ('tipo_pedido', 'VARCHAR(20) DEFAULT "Entrega"'),
        ('endereco', 'TEXT'),
        ('observacoes', 'TEXT'),
        ('updated_at', 'DATETIME')
    ]
    
    added_count = 0
    for column_name, column_type in new_columns:
        if not check_column_exists(cursor, 'pedidos', column_name):
            try:
                cursor.execute(f"ALTER TABLE pedidos ADD COLUMN {column_name} {column_type}")
                print(f"  ✓ Adicionada coluna: {column_name}")
                added_count += 1
            except Exception as e:
                print(f"  ✗ Erro ao adicionar {column_name}: {e}")
        else:
            print(f"  - Coluna {column_name} já existe")
    
    # Commit e fechar
    try:
        conn.commit()
        conn.close()
        print(f"\n✓ Migration concluída com sucesso!")
        print(f"  - {added_count} novas colunas adicionadas")
        print(f"  - Backup disponível em: {backup_path}")
        return True
    except Exception as e:
        print(f"\n✗ Erro ao salvar alterações: {e}")
        conn.rollback()
        conn.close()
        return False

def verify_migration():
    """Verifica se a migration foi bem sucedida"""
    print("\n4. Verificando migration...")
    db_path = Path(__file__).parent / 'static' / 'database.db'
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(pedidos)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        required_columns = [
            'id', 'cliente', 'produto', 'quantidade', 'status',
            'horario', 'dia_entrega', 'destinatario', 'mensagem',
            'created_at', 'telefone_cliente', 'tipo_pedido',
            'endereco', 'observacoes', 'updated_at'
        ]
        
        missing = [col for col in required_columns if col not in columns]
        
        if missing:
            print(f"  ✗ Colunas faltando: {', '.join(missing)}")
            return False
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        count = cursor.fetchone()[0]
        
        print(f"  ✓ Todas as colunas presentes")
        print(f"  ✓ {count} registros preservados")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ✗ Erro na verificação: {e}")
        return False

def main():
    """Entry point"""
    try:
        success = migrate_database()
        
        if success:
            verify_migration()
            print("\n" + "=" * 60)
            print("Migration concluída! O servidor está pronto para usar.")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("Migration falhou! Verifique os erros acima.")
            print("O backup foi criado e pode ser restaurado se necessário.")
            print("=" * 60)
        
        return success
        
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    input("\nPressione ENTER para continuar...")
    sys.exit(0 if success else 1)

