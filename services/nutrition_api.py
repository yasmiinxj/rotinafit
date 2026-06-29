"""
Serviço de alimentação do FitLife
Responsável por buscar informações nutricionais em arquivo local
"""

import json
import streamlit as st
from typing import List, Dict, Optional


class NutritionAPI:
    """Classe para gerenciamento dos alimentos"""

    @staticmethod
    def buscar_alimentos(nome: str, limite: int = 10) -> List[Dict]:
        """
        Busca alimentos no arquivo local alimentos.json.
        """

        if not nome or len(nome.strip()) < 2:
            return []

        try:
            with open("data/alimentos.json", "r", encoding="utf-8") as arquivo:
                alimentos = json.load(arquivo)

            nome = nome.lower().strip()

            resultados = [
                alimento
                for alimento in alimentos
                if nome in alimento["nome"].lower()
            ]

            return resultados[:limite]

        except FileNotFoundError:
            st.error(
                "❌ Arquivo data/alimentos.json não encontrado."
            )
            return []

        except Exception as e:
            st.error(
                f"❌ Erro ao buscar alimentos: {str(e)}"
            )
            return []

    @staticmethod
    def buscar_alimento_por_id(
        id_alimento: str,
    ) -> Optional[Dict]:
        """
        Busca alimento pelo ID no arquivo local.
        """

        try:
            with open("data/alimentos.json", "r", encoding="utf-8") as arquivo:
                alimentos = json.load(arquivo)

            for alimento in alimentos:
                if str(alimento.get("id")) == str(id_alimento):
                    return alimento

            return None

        except Exception:
            return None

    @staticmethod
    def obter_nutrientes(
        alimento: Dict,
        quantidade: float = 100,
    ) -> Dict:
        """
        Calcula os nutrientes proporcionalmente
        à quantidade consumida.
        """

        if not alimento:
            return {
                "calorias": 0,
                "proteinas": 0,
                "carboidratos": 0,
                "gorduras": 0,
                "fibras": 0,
                "porcao": 0,
            }

        porcao_base = alimento.get("porcao", 100)

        if porcao_base <= 0:
            porcao_base = 100

        multiplicador = quantidade / porcao_base

        return {
            "calorias": round(
                alimento.get("calorias", 0) * multiplicador,
                1,
            ),
            "proteinas": round(
                alimento.get("proteinas", 0) * multiplicador,
                1,
            ),
            "carboidratos": round(
                alimento.get("carboidratos", 0) * multiplicador,
                1,
            ),
            "gorduras": round(
                alimento.get("gorduras", 0) * multiplicador,
                1,
            ),
            "fibras": round(
                alimento.get("fibras", 0) * multiplicador,
                1,
            ),
            "porcao": quantidade,
        }

    @staticmethod
    def calcular_totais(
        alimentos_consumidos: List[Dict],
    ) -> Dict:
        """
        Calcula os totais nutricionais.
        """

        totais = {
            "calorias": 0,
            "proteinas": 0,
            "carboidratos": 0,
            "gorduras": 0,
            "fibras": 0,
        }

        for alimento in alimentos_consumidos:
            totais["calorias"] += alimento.get(
                "calorias", 0
            )
            totais["proteinas"] += alimento.get(
                "proteinas", 0
            )
            totais["carboidratos"] += alimento.get(
                "carboidratos", 0
            )
            totais["gorduras"] += alimento.get(
                "gorduras", 0
            )
            totais["fibras"] += alimento.get(
                "fibras", 0
            )

        for chave in totais:
            totais[chave] = round(
                totais[chave],
                1,
            )

        return totais


# Instância global
nutrition_api = NutritionAPI()