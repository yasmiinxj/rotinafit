from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: str = ""
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None
    peso: Optional[float] = None
    altura: Optional[float] = None
    objetivo: str = "manter peso"
    email: str = ""
    senha: str = ""
    data_cadastro: datetime = field(default_factory=datetime.now)

    def cadastrar(self) -> None:
        """Prepara o usuário para persistência após validação básica."""
        if not self.nome:
            raise ValueError("O nome do usuário é obrigatório.")
        if self.objetivo not in ("emagrecer", "ganhar peso", "manter peso"):
            raise ValueError("Objetivo inválido.")
        if not self.email:
            raise ValueError("O email é obrigatório.")
        if not self.senha:
            raise ValueError("A senha é obrigatória.")

    def autenticar(self, senha: str) -> bool:
        """Verifica se a senha informada corresponde à senha armazenada."""
        return self.senha == senha

    def atualizar_perfil(
        self,
        nome: Optional[str] = None,
        data_nascimento: Optional[date] = None,
        sexo: Optional[str] = None,
        peso: Optional[float] = None,
        altura: Optional[float] = None,
        objetivo: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        if nome is not None:
            self.nome = nome
        if data_nascimento is not None:
            self.data_nascimento = data_nascimento
        if sexo is not None:
            self.sexo = sexo
        if peso is not None:
            self.peso = peso
        if altura is not None:
            self.altura = altura
        if objetivo is not None:
            if objetivo not in ("emagrecer", "ganhar peso", "manter peso"):
                raise ValueError("Objetivo inválido.")
            self.objetivo = objetivo
        if email is not None:
            self.email = email
