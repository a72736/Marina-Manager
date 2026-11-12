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

    def get_berth(self, berth_id: str) -> Optional[dict]:
        """Consulta um posto de amarração específico (Read individual)."""
        return self.berths.get(berth_id.strip().upper())

    def list_berths(self, pontoon_filter: Optional[str] = None, status_filter: Optional[str] = None) -> List[dict]:
        """Lista os postos com opções de filtro por pontão ou estado (Read com filtro)."""
        results = list(self.berths.values())
        if pontoon_filter:
            p_prefix = pontoon_filter.strip().upper()
            results = [b for b in results if b["berth_id"].startswith(p_prefix)]
        if status_filter:
            s_val = status_filter.strip().upper()
            results = [b for b in results if b["status"] == s_val]
        return results

    def update_berth_maintenance(self, berth_id: str, in_maintenance: bool) -> bool:
        """Altera o estado do posto para manutenção ou liberta-o (Update)."""
        berth = self.get_berth(berth_id)
        if not berth:
            raise KeyError(f"Posto {berth_id} não encontrado.")
        if in_maintenance:
            if berth["status"] == "OCUPADA":
                raise PermissionError("Não é possível colocar em manutenção um posto com barco atracado.")
            berth["status"] = "MANUTENCAO"
        else:
            if berth["status"] == "MANUTENCAO":
                berth["status"] = "LIVRE"
        return True

    def update_berth_maintenance(self, berth_id: str, in_maintenance: bool) -> bool:
        """Altera o estado do posto para manutenção ou liberta-o (Update)."""
        berth = self.get_berth(berth_id)
        if not berth:
            raise KeyError(f"Posto {berth_id} não encontrado.")
        if in_maintenance:
            if berth["status"] == "OCUPADA":
                raise PermissionError("Não é possível colocar em manutenção um posto com barco atracado.")
            berth["status"] = "MANUTENCAO"
        else:
            if berth["status"] == "MANUTENCAO":
                berth["status"] = "LIVRE"
        return True


    def delete_berth(self, berth_id: str) -> bool:
        """Remove um posto de amarração do inventário (Delete)."""
        berth_id = berth_id.strip().upper()
        berth = self.get_berth(berth_id)
        if not berth:
            raise KeyError(f"Posto {berth_id} não encontrado.")
        if berth["status"] == "OCUPADA":
            raise PermissionError("Não é possível eliminar um posto ocupado por uma embarcação.")

        del self.berths[berth_id]
        return True

    def find_suitable_berth(self, length: float, draft: float) -> Optional[dict]:
        """Algoritmo de alocação: devolve a primeira vaga livre compatível com as cotas."""
        for berth in sorted(self.berths.values(), key=lambda b: b["max_length"]):
            if berth["status"] == "LIVRE":
                if berth["max_length"] >= length and berth["max_draft"] >= draft:
                    return berth
        return None