"""
Script de inicialização do FitLife.
Execute este arquivo para preparar o ambiente antes de rodar a aplicação.
"""

from database.database import criar_banco

def main():
    """Cria o banco de dados e tabelas."""
    print("🏋️  Inicializando FitLife...")
    
    try:
        criar_banco()
        print("✅ Banco de dados criado/verificado com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Execute: streamlit run app.py")
        print("2. Abra http://localhost:8501 no navegador")
        print("3. Crie uma conta e faça login\n")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        return False

if __name__ == "__main__":
    sucesso = main()
    exit(0 if sucesso else 1)
