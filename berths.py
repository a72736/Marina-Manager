from typing import Dict, List, Optional


class BerthManager:
    """Gere os pontões, vagas e o estado físico de amarração."""

    def __init__(self, berths_data: Optional[Dict[str, dict]] = None):
        # Dicionário indexado pelo ID do posto (ex.: "A-01", "B-03")
        self.berths: Dict[str, dict] = berths_data if berths_data is not None else {}

    def create_berth(self, berth_id: str, max_length: float, max_draft: float, has_water: bool, has_electricity: bool) -> bool:
        """Regista um novo posto de amarração (Create)."""
        berth_id = berth_id.strip().upper()
        if not berth_id:
            raise ValueError("O identificador do posto não pode estar vazio.")
        if berth_id in self.berths:
            raise ValueError(f"O posto {berth_id} já se encontra cadastrado.")
        if max_length <= 0 or max_draft <= 0:
            raise ValueError("O comprimento máximo e calado suportado devem ser positivos.")

        self.berths[berth_id] = {
            "berth_id": berth_id,
            "max_length": float(max_length),
            "max_draft": float(max_draft),
            "has_water": bool(has_water),
            "has_electricity": bool(has_electricity),
            "status": "LIVRE",  # Estados: LIVRE, OCUPADA, MANUTENCAO
            "current_vessel": None
        }
        return True