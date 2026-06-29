import sqlite3
from pathlib import Path

# Caminho do arquivo SQLite dentro da pasta database.
DB_PATH = Path(__file__).resolve().parent / "fitlife.db"


def conectar() -> sqlite3.Connection:
    """Abre uma conexão com o banco SQLite e ativa as foreign keys."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco() -> None:
    """Cria as tabelas do banco de dados caso ainda não existam."""
    with conectar() as conexao:
        cursor = conexao.cursor()

        # Tabela de usuários com objetivo restrito e email único.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT,
                sexo TEXT,
                peso REAL,
                altura REAL,
                objetivo TEXT NOT NULL CHECK(objetivo IN ('emagrecer', 'ganhar peso', 'manter peso')),
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                data_cadastro TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
            );
            """
        )

        # Tabela de dietas associada ao usuário.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dietas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                objetivo TEXT,
                descricao TEXT,
                calorias INTEGER,
                metadata_criacao TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
            """
        )

        # Tabela de refeições associada ao usuário.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS refeicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                tipo_refeicao TEXT NOT NULL CHECK(tipo_refeicao IN ('café da manhã', 'almoço', 'jantar', 'lanche')),
                data_refeicao TEXT NOT NULL,
                calorias_totais INTEGER DEFAULT 0,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
            """
        )

        # Tabela de alimentos que podem ser usados em refeições.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                calorias INTEGER,
                proteinas REAL,
                carboidratos REAL,
                gorduras REAL,
                fibras REAL,
                porcao TEXT
            );
            """
        )

        # Tabela de itens de refeição para calcular calorias e nutrientes.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS item_refeicao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                refeicao_id INTEGER NOT NULL,
                alimento_id INTEGER NOT NULL,
                quantidade REAL NOT NULL CHECK(quantidade > 0),
                FOREIGN KEY(refeicao_id) REFERENCES refeicoes(id) ON DELETE CASCADE,
                FOREIGN KEY(alimento_id) REFERENCES alimentos(id) ON DELETE RESTRICT
            );
            """
        )

        conexao.commit()


if __name__ == "__main__":
    criar_banco()
    print(f"Banco de dados criado em: {DB_PATH}")
