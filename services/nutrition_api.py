"""
Serviço de integração com Open Food Facts API
Responsável por buscar informações nutricionais de alimentos
"""

import requests
import streamlit as st
from typing import List, Dict, Optional

# Configurações da API
OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10


class NutritionAPI:
    """Classe para integração com Open Food Facts API"""

    @staticmethod
    def buscar_alimentos(nome: str, limite: int = 10) -> List[Dict]:
        """
        Busca alimentos pelo nome usando a API Open Food Facts.
        """

        if not nome or len(nome.strip()) < 2:
            return []

        try:
            url = f"{OPEN_FOOD_FACTS_URL}/cgi/search.pl"

            params = {
                "search_terms": nome,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": limite,
            }

            headers = {
                "User-Agent": "FitLife/1.0 (Projeto Academico)"
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=TIMEOUT,
            )

            response.raise_for_status()

            dados = response.json()
            alimentos = []

            for produto in dados.get("products", []):
                alimento = NutritionAPI._normalizar_alimento(produto)
                if alimento:
                    alimentos.append(alimento)

            return alimentos

        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout ao conectar com a API.")
            return []

        except requests.exceptions.ConnectionError:
            st.error("🔌 Erro de conexão com a internet.")
            return []

        except Exception as e:
            st.error(f"❌ Erro ao buscar alimentos: {str(e)}")
            return []

    @staticmethod
    def buscar_alimento_por_id(id_alimento: str) -> Optional[Dict]:
        """
        Busca um alimento pelo código de barras.
        """

        if not id_alimento:
            return None

        try:
            url = f"{OPEN_FOOD_FACTS_URL}/api/v2/product/{id_alimento}"

            headers = {
                "User-Agent": "FitLife/1.0 (Projeto Academico)"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
            )

            response.raise_for_status()

            dados = response.json()

            if dados.get("status") == 1 and "product" in dados:
                return NutritionAPI._normalizar_alimento(
                    dados["product"]
                )

            return None

        except Exception as e:
            st.error(f"❌ Erro ao buscar alimento: {str(e)}")
            return None

    @staticmethod
    def _normalizar_alimento(produto: Dict) -> Optional[Dict]:
        """
        Normaliza dados do produto da API.
        """

        try:
            if not produto.get("product_name"):
                return None

            nutrientes = produto.get("nutriments", {})

            calorias = (
                nutrientes.get("energy-kcal_100g")
                or nutrientes.get("energy-kcal")
                or 0
            )

            alimento = {
                "id": produto.get("code", ""),
                "nome": produto.get("product_name", ""),
                "marca": produto.get("brands", ""),
                "porcao": 100,
                "calorias": round(float(calorias or 0), 1),
                "proteinas": round(
                    float(nutrientes.get("proteins_100g", 0) or 0),
                    1,
                ),
                "carboidratos": round(
                    float(nutrientes.get("carbohydrates_100g", 0) or 0),
                    1,
                ),
                "gorduras": round(
                    float(nutrientes.get("fat_100g", 0) or 0),
                    1,
                ),
                "fibras": round(
                    float(nutrientes.get("fiber_100g", 0) or 0),
                    1,
                ),
                "unidade": "g",
            }

            return alimento

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

        multiplicador = quantidade / (
            alimento.get("porcao", 100) or 100
        )

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
            totais["calorias"] += alimento.get("calorias", 0)
            totais["proteinas"] += alimento.get("proteinas", 0)
            totais["carboidratos"] += alimento.get(
                "carboidratos", 0
            )
            totais["gorduras"] += alimento.get("gorduras", 0)
            totais["fibras"] += alimento.get("fibras", 0)

        for chave in totais:
            totais[chave] = round(totais[chave], 1)

        return totais


# Instância global
nutrition_api = NutritionAPI()