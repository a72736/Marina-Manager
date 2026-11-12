"""
Módulo: stays.py
Descrição: Gestão de check-in, check-out, diário de tráfego e apuramento tarifário (Stays).
"""

from datetime import datetime
from typing import Dict, List, Optional


class StayManager:
    """Gere o histórico de estadias e cálculo financeiro da marina."""

    DAILY_RATE_PER_METER = 2.50  # Tarifa base diária: 2,50€ por metro de comprimento
    WATER_FEE_PER_DAY = 3.00     # Taxa diária fixa de água
    POWER_FEE_PER_DAY = 5.00     # Taxa diária fixa de energia

    def __init__(self, stays_data: Optional[Dict[str, dict]] = None):
        # Dicionário de estadias indexado por stay_id
        self.stays: Dict[str, dict] = stays_data if stays_data is not None else {}
        self._next_id = len(self.stays) + 1

    def create_stay(self, vessel_reg: str, berth_id: str, planned_days: int, use_water: bool = False, use_power: bool = False) -> str:
        """Regista uma nova estadia / Check-in (Create)."""
        if planned_days <= 0:
            raise ValueError("O número de dias planeados deve ser superior a 0.")

        stay_id = f"STAY-{self._next_id:04d}"
        self._next_id += 1

        self.stays[stay_id] = {
            "stay_id": stay_id,
            "vessel_reg": vessel_reg.strip().upper(),
            "berth_id": berth_id.strip().upper(),
            "check_in_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "planned_days": planned_days,
            "use_water": bool(use_water),
            "use_power": bool(use_power),
            "status": "ATIVA",  # Estados: ATIVA, CONCLUIDA
            "check_out_date": None,
            "total_cost": 0.0
        }
        return stay_id

    def get_active_stay_for_vessel(self, vessel_reg: str) -> Optional[dict]:
        """Devolve a estadia ativa de uma dada embarcação, se existir."""
        v_reg = vessel_reg.strip().upper()
        for stay in self.stays.values():
            if stay["vessel_reg"] == v_reg and stay["status"] == "ATIVA":
                return stay
        return None

    def list_stays(self, active_only: bool = True) -> List[dict]:
        """Lista estadias com filtro por estado ativo (Read)."""
        if active_only:
            return [s for s in self.stays.values() if s["status"] == "ATIVA"]
        return list(self.stays.values())

    
    def update_stay_duration(self, stay_id: str, additional_days: int) -> bool:
        """Prorroga o número de dias de estadia (Update)."""
        stay = self.stays.get(stay_id)
        if not stay:
            raise KeyError(f"Estadia {stay_id} não encontrada.")
        if stay["status"] != "ATIVA":
            raise ValueError("Apenas estadias ativas podem ser prolongadas.")
        if additional_days <= 0:
            raise ValueError("Os dias adicionais devem ser superiores a 0.")

        stay["planned_days"] += additional_days
        return True

    def checkout_stay(self, stay_id: str, vessel_length: float, actual_days: Optional[int] = None) -> float:
        """Conclui a estadia e apura a fatura total (Update de fecho / fecho de ciclo)."""
        stay = self.stays.get(stay_id)
        if not stay:
            raise KeyError(f"Estadia {stay_id} não encontrada.")
        if stay["status"] != "ATIVA":
            raise ValueError("Esta estadia já foi finalizada anteriormente.")

        days = actual_days if actual_days is not None else stay["planned_days"]
        if days < 1:
            days = 1

        cost = days * (vessel_length * self.DAILY_RATE_PER_METER)
        if stay["use_water"]:
            cost += days * self.WATER_FEE_PER_DAY
        if stay["use_power"]:
            cost += days * self.POWER_FEE_PER_DAY

        stay["status"] = "CONCLUIDA"
        stay["check_out_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        stay["total_cost"] = round(cost, 2)
        return stay["total_cost"]
