from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Alimento:
    id: Optional[int] = None
    nome: str = ""
    calorias: Optional[int] = None
    proteinas: Optional[float] = None
    carboidratos: Optional[float] = None
    gorduras: Optional[float] = None
    fibras: Optional[float] = None
    porcao: Optional[str] = None

    def consultar(self) -> Dict[str, Optional[object]]:
        """Retorna os dados básicos do alimento para visualização ou cálculo."""
        return {
            "id": self.id,
            "nome": self.nome,
            "calorias": self.calorias,
            "proteinas": self.proteinas,
            "carboidratos": self.carboidratos,
            "gorduras": self.gorduras,
            "fibras": self.fibras,
            "porcao": self.porcao,
        }
