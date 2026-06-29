from __future__ import annotations
from datetime import date, datetime
from typing import Dict, Optional, Union

import sqlite3

from database.database import conectar
from models.usuario import Usuario


def _serialize_date(data_nascimento: Optional[Union[date, str]]) -> Optional[str]:
    if data_nascimento is None:
        return None
    if isinstance(data_nascimento, date):
        return data_nascimento.isoformat()
    return str(data_nascimento)


def _parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_datetime(value: Optional[str]) -> datetime:
    if value is None:
        return datetime.now()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.now()


def _row_to_usuario(row: sqlite3.Row) -> Usuario:
    return Usuario(
        id=row["id"],
        nome=row["nome"],
        data_nascimento=_parse_date(row["data_nascimento"]),
        sexo=row["sexo"],
        peso=row["peso"],
        altura=row["altura"],
        objetivo=row["objetivo"],
        email=row["email"],
        senha=row["senha"],
        data_cadastro=_parse_datetime(row["data_cadastro"]),
    )


def cadastrar_usuario(
    nome: str,
    data_nascimento: Optional[Union[date, str]],
    sexo: Optional[str],
    peso: Optional[float],
    altura: Optional[float],
    objetivo: str,
    email: str,
    senha: str,
) -> Dict[str, object]:
    """Cadastra um usuário no banco de dados.

    Regras:
    - o email deve ser único;
    - o objetivo deve ser válido;
    - retorna mensagem de sucesso ou erro.
    """
    if objetivo not in ("emagrecer", "ganhar peso", "manter peso"):
        raise ValueError("Objetivo inválido. Escolha entre: emagrecer, ganhar peso ou manter peso.")

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone() is not None:
            raise ValueError("O email informado já está cadastrado.")

        cursor.execute(
            """
            INSERT INTO usuarios (
                nome,
                data_nascimento,
                sexo,
                peso,
                altura,
                objetivo,
                email,
                senha
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nome,
                _serialize_date(data_nascimento),
                sexo,
                peso,
                altura,
                objetivo,
                email,
                senha,
            ),
        )
        conexao.commit()
        usuario_id = cursor.lastrowid

    usuario = buscar_usuario(usuario_id)
    return {
        "success": True,
        "message": "Usuário cadastrado com sucesso.",
        "usuario": usuario,
    }


def autenticar_usuario(email: str, senha: str) -> Usuario:
    """Autentica um usuário pelo email e senha."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Usuário não encontrado.")
        if row["senha"] != senha:
            raise ValueError("Senha inválida.")
        return _row_to_usuario(row)


def buscar_usuario(id_usuario: int) -> Usuario:
    """Busca um usuário pelo seu identificador."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Usuário não encontrado.")
        return _row_to_usuario(row)
