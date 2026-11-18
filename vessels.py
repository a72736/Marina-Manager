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
            "draft": float(draft),
            "owner": owner.strip(),
            "contact": contact.strip()
        }
        
        return True



    def get_vessel(self, reg_num: str) -> Optional[dict]:
        """Obtém os detalhes de uma embarcação pelo registo (Read individual)."""
        return self.vessels.get(reg_num.strip().upper())


    
    def update_vessel(self, reg_num: str, name: Optional[str] = None, vessel_type: Optional[str] = None,
                      length: Optional[float] = None, draft: Optional[float] = None,
                      owner: Optional[str] = None, contact: Optional[str] = None) -> bool:
        """Atualiza os dados de uma embarcação existente (Update)."""
        vessel = self.get_vessel(reg_num)

        
        if name is not None and name.strip():
            vessel["name"] = name.strip()
        if vessel_type is not None and vessel_type.strip():
            vessel["type"] = vessel_type.strip()
        if length is not None:
            if length <= 0:
                raise ValueError("O comprimento deve ser maior que zero.")
            vessel["length"] = float(length)
        if draft is not None:
            if draft <= 0:
                raise ValueError("O calado deve ser maior que zero.")
            vessel["draft"] = float(draft)
        if owner is not None and owner.strip():
            vessel["owner"] = owner.strip()
        if contact is not None and contact.strip():
            vessel["contact"] = contact.strip()

        return True