from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Refeicao:
    id: Optional[int] = None
    usuario_id: int = 0
    tipo_refeicao: str = ""
    data_refeicao: datetime = field(default_factory=datetime.now)
    calorias_totais: int = 0
    itens: List["ItemRefeicao"] = field(default_factory=list)

    def adicionar_alimento(self, item: "ItemRefeicao") -> None:
        """Adiciona um item de refeição ao histórico e atualiza as calorias."""
        if item.quantidade <= 0:
            raise ValueError("A quantidade do alimento deve ser maior que zero.")
        self.itens.append(item)
        self.calcular_calorias()

    def remover_alimento(self, item_id: int) -> None:
        """Remove um item de refeição pelo seu identificador."""
        self.itens = [item for item in self.itens if item.id != item_id]
        self.calcular_calorias()

    def calcular_calorias(self) -> int:
        """Calcula o total de calorias da refeição com base nos itens."""
        total = 0.0
        for item in self.itens:
            nutrientes = item.calcular_nutrientes()
            total += nutrientes.get("calorias", 0.0)
        self.calorias_totais = int(total)
        return self.calorias_totais

    def calcular_macronutrientes(self) -> dict[str, float]:
        """Calcula os macronutrientes totais da refeição."""
        totals = {
            "proteinas": 0.0,
            "carboidratos": 0.0,
            "gorduras": 0.0,
            "fibras": 0.0,
        }
        for item in self.itens:
            nutrientes = item.calcular_nutrientes()
            totals["proteinas"] += nutrientes.get("proteinas", 0.0)
            totals["carboidratos"] += nutrientes.get("carboidratos", 0.0)
            totals["gorduras"] += nutrientes.get("gorduras", 0.0)
            totals["fibras"] += nutrientes.get("fibras", 0.0)
        return totals
