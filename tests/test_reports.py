"""
Módulo: test_reports.py
Descrição: Testes unitários para validar os cálculos dos relatórios operacionais, financeiros e alertas.
Autor: Rafael Coelho
"""

import unittest
from reports import (
    gerar_relatorio_ocupacao,
    gerar_relatorio_financeiro,
    gerar_relatorio_alertas,
)


class TestReports(unittest.TestCase):
    """Testes às funções de relatórios de ocupação, faturação e alertas."""

    def test_relatorio_ocupacao_vazio(self):
        res = gerar_relatorio_ocupacao({})
        self.assertIn("Sem postos", res)

    def test_relatorio_ocupacao_calculos(self):
        berths_mock = {
            "A-01": {"status": "OCUPADA"},
            "A-02": {"status": "LIVRE"},
            "B-01": {"status": "MANUTENCAO"},
            "B-02": {"status": "OCUPADA"},
        }
        res = gerar_relatorio_ocupacao(berths_mock)
        self.assertIn("Total de Postos: 4", res)
        self.assertIn("Ocupados:      2 (50.0%)", res)
        self.assertIn("Livres:        1", res)
        self.assertIn("Em Manutenção: 1", res)

    def test_relatorio_financeiro(self):
        stays_mock = {
            "STAY-0001": {"status": "CONCLUIDA", "total_cost": 45.50},
            "STAY-0002": {"status": "CONCLUIDA", "total_cost": 100.00},
            "STAY-0003": {"status": "ATIVA", "total_cost": 0.0},
        }
        res = gerar_relatorio_financeiro(stays_mock)
        self.assertIn("Estadias Ativas no Cais: 1", res)
        self.assertIn("Estadias Concluídas:     2", res)
        self.assertIn("Receita Total Faturada:  145.50 EUR", res)

    def test_relatorio_alertas(self):
        stays_mock = {
            "STAY-0010": {"status": "ATIVA", "dias_decorridos": 10, "vessel_id": "PT-99", "berth_id": "A-04"},
            "STAY-0011": {"status": "ATIVA", "dias_decorridos": 2, "vessel_id": "PT-12", "berth_id": "B-01"},
        }
        res = gerar_relatorio_alertas(stays_mock, limite_dias=7)
        self.assertIn("STAY-0010", res)
        self.assertNotIn("STAY-0011", res)


if __name__ == "__main__":
    unittest.main()
