import os
import shutil
from datetime import datetime

def criar_backup(ficheiro_origem: str = "marina_data.json", pasta_destino: str = "backups") -> str:
    """Cria uma cópia de segurança datada do ficheiro de dados JSON."""
    if not os.path.exists(ficheiro_origem):
        raise FileNotFoundError("Ficheiro principal de dados não encontrado.")

    os.makedirs(pasta_destino, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"marina_backup_{timestamp}.json"
    caminho_completo = os.path.join(pasta_destino, nome_backup)

    shutil.copy2(ficheiro_origem, caminho_completo)
    return caminho_completo