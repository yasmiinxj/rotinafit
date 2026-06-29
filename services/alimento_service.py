from __future__ import annotations
from typing import List

import sqlite3

from database.database import conectar
from models.alimento import Alimento


def _row_to_alimento(row: sqlite3.Row) -> Alimento:
    return Alimento(
        id=row["id"],
        nome=row["nome"],
        calorias=row["calorias"],
        proteinas=row["proteinas"],
        carboidratos=row["carboidratos"],
        gorduras=row["gorduras"],
        fibras=row["fibras"],
        porcao=row["porcao"],
    )


def buscar_alimento_por_nome(nome: str) -> List[Alimento]:
    """Retorna a lista de alimentos cujo nome contenha o termo informado."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM alimentos WHERE nome LIKE ? ORDER BY nome",
            (f"%{nome}%",),
        )
        rows = cursor.fetchall()
        return [_row_to_alimento(row) for row in rows]


def buscar_alimento_por_id(alimento_id: int) -> Alimento:
    """Retorna um alimento pelo seu ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM alimentos WHERE id = ?", (alimento_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Alimento não encontrado.")
        return _row_to_alimento(row)


def listar_alimentos() -> List[Alimento]:
    """Retorna todos os alimentos cadastrados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM alimentos ORDER BY nome")
        rows = cursor.fetchall()
        return [_row_to_alimento(row) for row in rows]
