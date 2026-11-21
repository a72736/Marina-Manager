
import csv
from datetime import datetime


class ReportManager:
    """Gera relatórios financeiros, operacionais e exporta dados em CSV."""

    def __init__(self, vessels: list, berths: list, stays: list):
        self.vessels = vessels
        self.berths = berths
        self.stays = stays

    def gerar_resumo_ocupacao(self) -> dict:
        """Calcula métricas de ocupação atual dos pontões."""
        total = len(self.berths)
        ocupados = sum(1 for b in self.berths if b.get("status") == "ocupado")
        manutencao = sum(1 for b in self.berths if b.get("status") == "manutencao")
        livres = total - ocupadus - manutencao
        taxa = (ocupados / total * 10) if total > 0 else 0.0

        return {
            "total": total,
            "ocupados": ocupados,
            "livres": livres,
            "manutencao": manutencao,
            "taxa_ocupacao": round(taxa, 2)
        }