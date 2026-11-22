"""
Módulo: reports.py
Descrição: Geração de relatórios operacionais, taxa de ocupação e métricas da marina.
Autor: Rafael Coelho
"""

from typing import Dict


def gerar_relatorio_ocupacao(berths: Dict[str, dict]) -> str:
    """Calcula a taxa de ocupação global e por pontão em formato de texto."""
    if not berths:
        return "Sem postos de amarração registados para gerar relatório."

    total = len(berths)
    ocupados = sum(1 for b in berths.values() if b.get("status") == "OCUPADA")
    manutencao = sum(1 for b in berths.values() if b.get("status") == "MANUTENCAO")
    livres = total - ocupados - manutencao
    taxa = (ocupados / total) * 100

    linhas = [
        "\n=== RELATÓRIO DE OCUPAÇÃO DA MARINA ===",
        f"Total de Postos: {total}",
        f"  - Ocupados:      {ocupados} ({taxa:.1f}%)",
        f"  - Livres:        {livres}",
        f"  - Em Manutenção: {manutencao}",
        "========================================"
    ]
    return "\n".join(linhas)


def gerar_relatorio_financeiro(stays: Dict[str, dict]) -> str:
    """Apura a receita acumulada de estadias concluídas e ativas."""
    concluidas = [s for s in stays.values() if s.get("status") == "CONCLUIDA"]
    ativas = [s for s in stays.values() if s.get("status") == "ATIVA"]
    total_faturado = sum(float(s.get("total_cost", 0.0)) for s in concluidas)

    linhas = [
        "\n=== RESUMO FINANCEIRO E TRÁFEGO ===",
        f"Estadias Ativas no Cais: {len(ativas)}",
        f"Estadias Concluídas:     {len(concluidas)}",
        f"Receita Total Faturada:  {total_faturado:.2f} EUR",
        "==================================="
    ]
    return "\n".join(linhas)


def gerar_relatorio_alertas(stays: Dict[str, dict], limite_dias: int = 7) -> str:
    """Identifica estadias ativas que ultrapassam o limite padrão de permanência."""
    alertas = []
    for stay_id, dados in stays.items():
        if dados.get("status") == "ATIVA":
            dias = int(dados.get("dias_decorridos", 0))
            if dias >= limite_dias:
                vessel = dados.get("vessel_id", "Desconhecida")
                berth = dados.get("berth_id", "N/A")
                alertas.append(f"  - [{stay_id}] Embarcação {vessel} no posto {berth} ({dias} dias)")

    if not alertas:
        return "\n=== ALERTAS OPERACIONAIS ===\nSem estadias prolongadas ou alertas ativos.\n============================"

    cabecalho = f"\n=== ALERTAS OPERACIONAIS (>= {limite_dias} DIAS) ==="
    rodape = "=" * len(cabecalho.strip())
    return "\n".join([cabecalho] + alertas + [rodape])
