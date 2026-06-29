from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional

import sqlite3

from database.database import conectar
from models.refeicao import Refeicao
from models.item_refeicao import ItemRefeicao
from models.alimento import Alimento

TIPOS_VALIDOS = ("café da manhã", "almoço", "jantar", "lanche")


def _parse_datetime(value: Optional[str]) -> str:
    if value is None:
        return datetime.now().isoformat()
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _row_to_alimento(row: sqlite3.Row) -> Alimento:
    return Alimento(
        id=row["alimento_id"],
        nome=row["nome"],
        calorias=row["calorias"],
        proteinas=row["proteinas"],
        carboidratos=row["carboidratos"],
        gorduras=row["gorduras"],
        fibras=row["fibras"],
        porcao=row["porcao"],
    )


def _row_to_item_refeicao(row: sqlite3.Row) -> ItemRefeicao:
    alimento = _row_to_alimento(row)
    return ItemRefeicao(
        id=row["item_id"],
        refeicao_id=row["refeicao_id"],
        alimento_id=row["alimento_id"],
        quantidade=row["quantidade"],
        alimento=alimento,
    )


def _row_to_refeicao(row: sqlite3.Row) -> Refeicao:
    return Refeicao(
        id=row["id"],
        usuario_id=row["usuario_id"],
        tipo_refeicao=row["tipo_refeicao"],
        data_refeicao=datetime.fromisoformat(row["data_refeicao"]),
        calorias_totais=row["calorias_totais"],
    )


def _verificar_usuario(usuario_id: int) -> None:
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
        if cursor.fetchone() is None:
            raise ValueError("Usuário não encontrado.")


def _verificar_proprietario_refeicao(refeicao_id: int, usuario_id: int) -> None:
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT usuario_id FROM refeicoes WHERE id = ?", (refeicao_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Refeição não encontrada.")
        if row["usuario_id"] != usuario_id:
            raise PermissionError("Apenas o proprietário pode modificar essa refeição.")


def _buscar_itens_refeicao(refeicao_id: int) -> List[ItemRefeicao]:
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT
                i.id AS item_id,
                i.refeicao_id,
                i.alimento_id,
                i.quantidade,
                a.nome,
                a.calorias,
                a.proteinas,
                a.carboidratos,
                a.gorduras,
                a.fibras,
                a.porcao
            FROM item_refeicao AS i
            JOIN alimentos AS a ON a.id = i.alimento_id
            WHERE i.refeicao_id = ?
            """,
            (refeicao_id,),
        )
        rows = cursor.fetchall()
        return [_row_to_item_refeicao(row) for row in rows]


def criar_refeicao(
    usuario_id: int,
    tipo_refeicao: str,
    data_refeicao: Optional[str] = None,
) -> Refeicao:
    """Cria uma nova refeição para um usuário autenticado."""
    _verificar_usuario(usuario_id)
    if tipo_refeicao not in TIPOS_VALIDOS:
        raise ValueError(f"Tipo de refeição inválido. Use: {', '.join(TIPOS_VALIDOS)}")

    data_refeicao_text = _parse_datetime(data_refeicao)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO refeicoes (usuario_id, tipo_refeicao, data_refeicao)
            VALUES (?, ?, ?)
            """,
            (usuario_id, tipo_refeicao, data_refeicao_text),
        )
        conexao.commit()
        refeicao_id = cursor.lastrowid

    return buscar_refeicao(refeicao_id)


def adicionar_alimento(
    refeicao_id: int,
    alimento_id: int,
    quantidade: float,
    usuario_id: Optional[int] = None,
) -> Dict[str, float]:
    """Adiciona um alimento a uma refeição e recalcula os totais."""
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    if usuario_id is not None:
        _verificar_proprietario_refeicao(refeicao_id, usuario_id)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM refeicoes WHERE id = ?", (refeicao_id,))
        if cursor.fetchone() is None:
            raise ValueError("Refeição não encontrada.")

        cursor.execute("SELECT id FROM alimentos WHERE id = ?", (alimento_id,))
        if cursor.fetchone() is None:
            raise ValueError("Alimento não encontrado.")

        cursor.execute(
            """
            INSERT INTO item_refeicao (refeicao_id, alimento_id, quantidade)
            VALUES (?, ?, ?)
            """,
            (refeicao_id, alimento_id, quantidade),
        )
        conexao.commit()

    return calcular_totais_refeicao(refeicao_id)


def listar_refeicoes(usuario_id: int) -> List[Refeicao]:
    """Retorna todas as refeições de um usuário."""
    _verificar_usuario(usuario_id)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM refeicoes WHERE usuario_id = ? ORDER BY data_refeicao DESC",
            (usuario_id,),
        )
        rows = cursor.fetchall()

    refeicoes: List[Refeicao] = []
    for row in rows:
        refeicao = _row_to_refeicao(row)
        refeicao.itens = _buscar_itens_refeicao(refeicao.id)
        refeicao.calcular_calorias()
        refeicoes.append(refeicao)

    return refeicoes


def excluir_refeicao(refeicao_id: int, usuario_id: Optional[int] = None) -> None:
    """Exclui uma refeição e seus itens associados."""
    if usuario_id is not None:
        _verificar_proprietario_refeicao(refeicao_id, usuario_id)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM refeicoes WHERE id = ?", (refeicao_id,))
        if cursor.rowcount == 0:
            raise ValueError("Refeição não encontrada.")
        conexao.commit()


def calcular_totais_refeicao(refeicao_id: int) -> Dict[str, float]:
    """Calcula e atualiza as calorias e macronutrientes totais de uma refeição."""
    itens = _buscar_itens_refeicao(refeicao_id)
    totals = {
        "calorias": 0.0,
        "proteinas": 0.0,
        "carboidratos": 0.0,
        "gorduras": 0.0,
        "fibras": 0.0,
    }

    for item in itens:
        nutrientes = item.calcular_nutrientes()
        totals["calorias"] += nutrientes["calorias"]
        totals["proteinas"] += nutrientes["proteinas"]
        totals["carboidratos"] += nutrientes["carboidratos"]
        totals["gorduras"] += nutrientes["gorduras"]
        totals["fibras"] += nutrientes["fibras"]

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE refeicoes SET calorias_totais = ? WHERE id = ?",
            (int(totals["calorias"]), refeicao_id),
        )
        conexao.commit()

    return totals


def buscar_refeicao(refeicao_id: int) -> Refeicao:
    """Busca uma refeição pelo seu identificador."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM refeicoes WHERE id = ?", (refeicao_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Refeição não encontrada.")

    refeicao = _row_to_refeicao(row)
    refeicao.itens = _buscar_itens_refeicao(refeicao.id)
    refeicao.calcular_calorias()
    return refeicao
