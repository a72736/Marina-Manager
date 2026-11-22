
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
        livres = total - ocupados - manutencao
        taxa = (ocupados / total * 100) if total > 0 else 0.0

        return {
            "total": total,
            "ocupados": ocupados,
            "livres": livres,
            "manutencao": manutencao,
            "taxa_ocupacao": round(taxa, 2)
        }



     def listar_estadias_em_atraso(self) -> list:
        """Identifica embarcações com data de saída prevista ultrapassada (US15)."""
        hoje = datetime.now().strftime("%Y-%m-%d")
        atrasadas = []
        for stay in self.stays:
            if stay.get("ativa") and stay.get("data_saida_prevista", "9999-12-31") < hoje:
                atrasadas.append(stay)
        return atrasadas
        


     def exportar_estadias_csv(self, caminho_ficheiro: str = "relatorio_estadias.csv") -> str:
        """Exporta o registo de estadias para formato CSV nativo."""
        if not self.stays:
            raise ValueError("Não existem estadias registadas para exportar.")

        campos = self.stays[0].keys()
        with open(caminho_ficheiro, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(self.stays)
        return caminho_ficheiro
