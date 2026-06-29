from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional

import sqlite3

from database.database import conectar
from models.dieta import Dieta


def _parse_datetime(value: Optional[str]) -> datetime:
    if value is None:
        return datetime.now()
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _row_to_dieta(row: sqlite3.Row) -> Dieta:
    return Dieta(
        id=row["id"],
        usuario_id=row["usuario_id"],
        nome=row["nome"],
        objetivo=row["objetivo"],
        descricao=row["descricao"],
        calorias_meta=row["calorias"],
        data_criacao=_parse_datetime(row["metadata_criacao"]),
    )


def _verificar_usuario(usuario_id: int) -> None:
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
        if cursor.fetchone() is None:
            raise ValueError("Usuário não encontrado.")


def _verificar_proprietario_dieta(dieta_id: int, usuario_id: int) -> None:
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT usuario_id FROM dietas WHERE id = ?", (dieta_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Dieta não encontrada.")
        if row["usuario_id"] != usuario_id:
            raise PermissionError("Apenas o proprietário pode modificar essa dieta.")


def criar_dieta(
    usuario_id: int,
    nome: str,
    objetivo: Optional[str] = None,
    descricao: Optional[str] = None,
    calorias_meta: Optional[int] = None,
) -> Dieta:
    """Cria uma nova dieta para o usuário."""
    _verificar_usuario(usuario_id)
    if not nome:
        raise ValueError("O nome da dieta é obrigatório.")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            INSERT INTO dietas (usuario_id, nome, objetivo, descricao, calorias)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario_id, nome, objetivo, descricao, calorias_meta),
        )
        conexao.commit()
        dieta_id = cursor.lastrowid

    return buscar_dieta_por_id(dieta_id)


def editar_dieta(
    dieta_id: int,
    usuario_id: Optional[int] = None,
    nome: Optional[str] = None,
    objetivo: Optional[str] = None,
    descricao: Optional[str] = None,
    calorias_meta: Optional[int] = None,
) -> Dieta:
    """Edita os dados de uma dieta existente."""
    if usuario_id is not None:
        _verificar_proprietario_dieta(dieta_id, usuario_id)

    fields = []
    values = []
    if nome is not None:
        fields.append("nome = ?")
        values.append(nome)
    if objetivo is not None:
        fields.append("objetivo = ?")
        values.append(objetivo)
    if descricao is not None:
        fields.append("descricao = ?")
        values.append(descricao)
    if calorias_meta is not None:
        fields.append("calorias = ?")
        values.append(calorias_meta)

    if not fields:
        raise ValueError("Nenhum campo informado para atualização.")

    values.append(dieta_id)
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            f"UPDATE dietas SET {', '.join(fields)} WHERE id = ?",
            tuple(values),
        )
        if cursor.rowcount == 0:
            raise ValueError("Dieta não encontrada.")
        conexao.commit()

    return buscar_dieta_por_id(dieta_id)


def excluir_dieta(dieta_id: int, usuario_id: Optional[int] = None) -> None:
    """Exclui uma dieta cadastrada."""
    if usuario_id is not None:
        _verificar_proprietario_dieta(dieta_id, usuario_id)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM dietas WHERE id = ?", (dieta_id,))
        if cursor.rowcount == 0:
            raise ValueError("Dieta não encontrada.")
        conexao.commit()


def listar_dietas(usuario_id: int) -> List[Dieta]:
    """Lista todas as dietas de um usuário."""
    _verificar_usuario(usuario_id)

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM dietas WHERE usuario_id = ? ORDER BY metadata_criacao DESC",
            (usuario_id,),
        )
        rows = cursor.fetchall()
        return [_row_to_dieta(row) for row in rows]


def buscar_dieta_por_id(dieta_id: int) -> Dieta:
    """Busca uma dieta pelo identificador."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM dietas WHERE id = ?", (dieta_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Dieta não encontrada.")
        return _row_to_dieta(row)


def verificar_aderencia_dieta(usuario_id: int, dieta_id: int) -> Dict[str, object]:
    """Verifica a aderência do usuário à dieta com base nas refeições consumidas hoje."""
    dieta = buscar_dieta_por_id(dieta_id)
    if dieta.usuario_id != usuario_id:
        raise PermissionError("Apenas o proprietário pode verificar a aderência dessa dieta.")
    if dieta.calorias_meta is None:
        raise ValueError("A dieta não possui meta de calorias definida.")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT COALESCE(SUM(calorias_totais), 0) AS total_calorias
            FROM refeicoes
            WHERE usuario_id = ?
              AND date(data_refeicao) = date('now')
            """,
            (usuario_id,),
        )
        row = cursor.fetchone()
        total_calorias = row["total_calorias"] or 0

    diferenca = total_calorias - dieta.calorias_meta
    if abs(diferenca) <= max(1, dieta.calorias_meta * 0.1):
        status = "dentro"
    elif diferenca > 0:
        status = "acima"
    else:
        status = "abaixo"

    return {
        "dieta": dieta,
        "total_calorias_consumidas": total_calorias,
        "meta_calorias": dieta.calorias_meta,
        "diferenca": diferenca,
        "status": status,
        "analisado_em": datetime.now().isoformat(),
    }
