from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ItemRefeicao:
    id: Optional[int] = None
    refeicao_id: int = 0
    alimento_id: int = 0
    quantidade: float = 1.0
    alimento: Optional["Alimento"] = field(default=None)

    def calcular_nutrientes(self) -> Dict[str, float]:
        """Calcula nutrientes com base na quantidade e no alimento associado."""
        if self.quantidade <= 0:
            raise ValueError("A quantidade do alimento deve ser maior que zero.")
        if self.alimento is None:
            raise ValueError("É necessário associar o objeto Alimento para calcular nutrientes.")

        factor = self.quantidade
        calorias = float(self.alimento.calorias or 0) * factor
        proteinas = float(self.alimento.proteinas or 0.0) * factor
        carboidratos = float(self.alimento.carboidratos or 0.0) * factor
        gorduras = float(self.alimento.gorduras or 0.0) * factor
        fibras = float(self.alimento.fibras or 0.0) * factor

        return {
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras,
            "fibras": fibras,
        }
