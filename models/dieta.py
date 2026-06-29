from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Dieta:
    id: Optional[int] = None
    usuario_id: int = 0
    nome: str = ""
    objetivo: Optional[str] = None
    descricao: Optional[str] = None
    calorias_meta: Optional[int] = None
    data_criacao: datetime = field(default_factory=datetime.now)

    def criar(self) -> None:
        """Valida os dados da dieta antes da persistência."""
        if not self.usuario_id:
            raise ValueError("O ID do usuário é obrigatório.")
        if not self.nome:
            raise ValueError("O nome da dieta é obrigatório.")

    def editar(
        self,
        nome: Optional[str] = None,
        objetivo: Optional[str] = None,
        descricao: Optional[str] = None,
        calorias_meta: Optional[int] = None,
    ) -> None:
        if nome is not None:
            self.nome = nome
        if objetivo is not None:
            self.objetivo = objetivo
        if descricao is not None:
            self.descricao = descricao
        if calorias_meta is not None:
            self.calorias_meta = calorias_meta

    def excluir(self) -> None:
        """Marca a dieta para exclusão. A persistência ficou para a camada de serviço."""
        pass

    @classmethod
    def listar(cls, usuario_id: int) -> List["Dieta"]:
        """Retorna a lista de dietas para um usuário.
        A implementação de listagem deve ser feita por serviços ou repositórios.
        """
        raise NotImplementedError("A listagem deve ser implementada na camada de serviço.")
