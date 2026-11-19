"""
Módulo Principal: main.py
Descrição: Interface de consola de texto (CLI puro) do sistema MarinaManager.
"""

import sys
from reports import (
    gerar_relatorio_ocupacao,
    gerar_relatorio_financeiro,
    gerar_relatorio_alertas,
)

try:
    import vessels
    import berths
    import stays
    import backups
except ImportError as e:
    print(f"[AVISO] Módulo auxiliar não carregado: {e}")


def exibir_cabecalho():
    print("\n" + "=" * 55)
    print("       MARINA MANAGER CLI - GESTÃO PORTUÁRIA")
    print("=" * 55)


def menu_relatorios():
    while True:
        print("\n--- RELATÓRIOS E ESTATÍSTICAS ---")
        print("1. Taxa de Ocupação dos Pontões")
        print("2. Resumo Financeiro e Tráfego")
        print("3. Alertas de Estadias Prolongadas")
        print("0. Voltar")
        op = input("Escolha uma opção: ").strip()

        if op == "1":
            dados_berths = getattr(berths, "berths_db", {})
            print(gerar_relatorio_ocupacao(dados_berths))
        elif op == "2":
            dados_stays = getattr(stays, "stays_db", {})
            print(gerar_relatorio_financeiro(dados_stays))
        elif op == "3":
            dados_stays = getattr(stays, "stays_db", {})
            print(gerar_relatorio_alertas(dados_stays))
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def main():
    try:
        while True:
            exibir_cabecalho()
            print("1. Gestão de Embarcações (CRUD)")
            print("2. Gestão de Pontões e Vagas (CRUD)")
            print("3. Controlo de Estadias (Check-in / Check-out)")
            print("4. Relatórios e Estatísticas")
            print("5. Criar Backup de Segurança")
            print("0. Sair")
            print("=" * 55)

            escolha = input("Selecione uma opção: ").strip()

            if escolha == "1":
                if hasattr(vessels, "menu_vessels"):
                    vessels.menu_vessels()
                else:
                    print("[INFO] Aceder ao módulo de embarcações.")
            elif escolha == "2":
                if hasattr(berths, "menu_berths"):
                    berths.menu_berths()
                else:
                    print("[INFO] Aceder ao módulo de pontões.")
            elif escolha == "3":
                if hasattr(stays, "menu_stays"):
                    stays.menu_stays()
                else:
                    print("[INFO] Aceder ao módulo de estadias.")
            elif escolha == "4":
                menu_relatorios()
            elif escolha == "5":
                if hasattr(backups, "criar_backup"):
                    backups.criar_backup()
                    print("[OK] Backup efetuado com sucesso.")
                else:
                    print("[INFO] Módulo de backups aguardando integração.")
            elif escolha == "0":
                print("A encerrar o MarinaManager CLI. Até breve!")
                sys.exit(0)
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        print("\n[INFO] Execução interrompida pelo utilizador. A encerrar de forma segura...")
        sys.exit(0)


if __name__ == "__main__":
    main()
