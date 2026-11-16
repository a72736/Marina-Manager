import unittest
# Ajusta os imports conforme os nomes exatos das tuas classes
# from stays import StayManager

class TestRegrasNegocioMarina(unittest.TestCase):
    """Testes unitários às regras de compatibilidade e faturação."""

    def test_calculo_tarifa_estadia(self):
        # Exemplo: 3 dias a 25.00€/dia = 75.00€
        dias = 3
        tarifa_diaria = 25.0
        self.assertEqual(dias * tarifa_diaria, 75.0)
