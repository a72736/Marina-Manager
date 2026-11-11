"""Módulo: vessels.py
Descrição: Gestão e operações CRUD para a entidade Embarcações (Vessels).
"""

from typing import Dict, List, Optional


class VesselManager:
    """Gere o catálogo e as operações sobre embarcações."""

    def __init__(self, vessels_data: Optional[Dict[str, dict]] = None):
        # Dicionário indexado pela matrícula/registo
        self.vessels: Dict[str, dict] = vessels_data if vessels_data is not None else {}

    def create_vessel(self, reg_num: str, name: str, vessel_type: str, length: float, draft: float, owner: str, contact: str) -> bool:
        """Regista uma nova embarcação no sistema (Create)."""
        reg_num = reg_num.strip().upper()
        if not reg_num:
            raise ValueError("O registo/matrícula não pode estar vazio.")
        if reg_num in self.vessels:
            raise ValueError(f"Já existe uma embarcação com o registo {reg_num}.")
        if length <= 0 or draft <= 0:
            raise ValueError("O comprimento e o calado devem ser valores estritamente positivos.")

        self.vessels[reg_num] = {
            "reg_num": reg_num,
            "name": name.strip(),
            "type": vessel_type.strip(),
            "length": float(length),
            "draft": float(draft)
        }
        
        return True