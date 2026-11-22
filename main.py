
import sys
from vessels import VesselManager
from berths import BerthManager
from stays import StayManager
from storage import save_database, load_database
from reports import (
    gerar_relatorio_ocupacao,
    gerar_relatorio_financeiro,
    gerar_relatorio_alertas,
)

try:
    from backups import criar_backup
except ImportError:
    criar_backup = None


def seed_sample_data(vn: VesselManager, bm: BerthManager):
    """Inicializa postos e barcos de exemplo caso a base de dados esteja limpa."""
    if not bm.berths:
        bm.create_berth("A-01", max_length=10.0, max_draft=2.5, has_water=True, has_electricity=True)
        bm.create_berth("A-02", max_length=12.5, max_draft=3.0, has_water=True, has_electricity=True)
        bm.create_berth("B-01", max_length=15.0, max_draft=3.5, has_water=True, has_electricity=False)
        bm.create_berth("B-02", max_length=8.0, max_draft=1.8, has_water=False, has_electricity=False)
    if not vn.vessels:
        vn.create_vessel("PT-1001-L", "Santa Maria", "Veleiro", length=11.2, draft=2.1, owner="Manuel Silva", contact="910000001")
        vn.create_vessel("PT-2004-F", "Oceano Azul", "Lancha Rápida", length=7.5, draft=1.2, owner="Ana Costa", contact="920000002")


def print_banner():
    print("\n" + "=" * 60)
    print("          MARINAMANAGER CLI - GESTAO DE MARINAS")
    print("=" * 60)


def menu_vessels(vn: VesselManager, sm: StayManager):
    while True:
        print("\n--- MENU: GESTAO DE EMBARCACOES (CRUD) ---")
        print("1. Registar nova embarcacao (Create)")
        print("2. Listar todas as embarcacoes (Read)")
        print("3. Pesquisar embarcacao por nome/registo (Read)")
        print("4. Atualizar dados de uma embarcacao (Update)")
        print("5. Remover registo de embarcacao (Delete)")
        print("0. Voltar ao menu principal")
        opcao = input("Opcao: ").strip()

        if opcao == "1":
            try:
                reg = input("Matricula/Registo: ").strip()
                nome = input("Nome do barco: ").strip()
                tipo = input("Tipo/Classe (ex: Veleiro, Iate, Lancha): ").strip()
                comp = float(input("Comprimento (m): ").strip())
                calado = float(input("Calado (m): ").strip())
                dono = input("Nome do Proprietario: ").strip()
                contacto = input("Contacto telefonico: ").strip()
                vn.create_vessel(reg, nome, tipo, comp, calado, dono, contacto)
                print(f"[OK] Embarcacao '{nome}' ({reg}) registada com sucesso.")
            except Exception as e:
                print(f"[ERRO] Falha ao registar: {e}")

        elif opcao == "2":
            barcos = vn.list_vessels()
            if not barcos:
                print("Nenhuma embarcacao registada.")
            else:
                print(f"{'REGISTO':<12} | {'NOME':<18} | {'TIPO':<12} | {'COMP(m)':<8} | {'CALADO(m)':<9} | {'DONO':<15}")
                print("-" * 80)
                for b in barcos:
                    print(f"{b['reg_num']:<12} | {b['name']:<18} | {b['type']:<12} | {b['length']:<8.2f} | {b['draft']:<9.2f} | {b['owner']:<15}")

        elif opcao == "3":
            termo = input("Termo de pesquisa: ").strip()
            res = vn.list_vessels(search_term=termo)
            if not res:
                print(f"Nenhum barco corresponde a '{termo}'.")
            else:
                for b in res:
                    print(f"-> [{b['reg_num']}] {b['name']} ({b['type']}) | Comp: {b['length']}m | Calado: {b['draft']}m | Contacto: {b['contact']}")

        elif opcao == "4":
            reg = input("Matricula do barco a atualizar: ").strip()
            if not vn.get_vessel(reg):
                print("[ERRO] Barco nao encontrado.")
                continue
            print("Deixe em branco os campos que nao deseja alterar.")
            n_nome = input("Novo Nome: ").strip() or None
            n_tipo = input("Novo Tipo: ").strip() or None
            n_dono = input("Novo Dono: ").strip() or None
            n_cont = input("Novo Contacto: ").strip() or None
            try:
                vn.update_vessel(reg, name=n_nome, vessel_type=n_tipo, owner=n_dono, contact=n_cont)
                print("[OK] Embarcacao atualizada com sucesso.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "5":
            reg = input("Matricula do barco a remover: ").strip()
            is_active = sm.get_active_stay_for_vessel(reg) is not None
            try:
                vn.delete_vessel(reg, is_berthed=is_active)
                print(f"[OK] Embarcacao {reg} removida com sucesso.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_berths(bm: BerthManager):
    while True:
        print("\n--- MENU: GESTAO DE PONTOES E VAGAS (CRUD) ---")
        print("1. Criar novo posto de amarro (Create)")
        print("2. Mapa esquematico de ocupacao dos pontões (Read)")
        print("3. Filtrar vagas por estado/pontao (Read)")
        print("4. Colocar ou retirar posto de manutencao (Update)")
        print("5. Eliminar posto de amarro (Delete)")
        print("0. Voltar ao menu principal")
        opcao = input("Opcao: ").strip()

        if opcao == "1":
            try:
                p_id = input("ID do Posto (ex: A-03): ").strip()
                max_c = float(input("Comprimento maximo (m): ").strip())
                max_d = float(input("Calado maximo (m): ").strip())
                w = input("Tem ligacao de agua? (s/n): ").strip().lower() == "s"
                e = input("Tem ligacao eletrica? (s/n): ").strip().lower() == "s"
                bm.create_berth(p_id, max_c, max_d, w, e)
                print(f"[OK] Posto {p_id} criado.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "2":
            vagas = bm.list_berths()
            if not vagas:
                print("Sem postos registados.")
            else:
                print(f"{'POSTO':<8} | {'ESTADO':<12} | {'BARCO ATRACADO':<15} | {'COMP. MAX':<10} | {'AGUA/LUZ'}")
                print("-" * 65)
                for v in sorted(vagas, key=lambda x: x["berth_id"]):
                    ocupante = v["current_vessel"] if v["current_vessel"] else "---"
                    apoios = f"{'Agua ' if v['has_water'] else ''}{'+ Luz' if v['has_electricity'] else ''}".strip() or "Nenhum"
                    print(f"{v['berth_id']:<8} | {v['status']:<12} | {ocupante:<15} | {v['max_length']:<10.1f} | {apoios}")

        elif opcao == "3":
            filtro = input("Filtrar por estado (LIVRE, OCUPADA, MANUTENCAO) ou ENTER para todos: ").strip()
            vagas = bm.list_berths(status_filter=filtro or None)
            for v in vagas:
                print(f"[{v['berth_id']}] Estado: {v['status']} | Max Comp: {v['max_length']}m | Barco: {v['current_vessel']}")

        elif opcao == "4":
            p_id = input("ID do Posto: ").strip()
            sub = input("Deseja colocar em manutencao (1) ou repor em servico (2)? ")
            try:
                bm.update_berth_maintenance(p_id, in_maintenance=(sub == "1"))
                print("[OK] Estado do posto alterado.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "5":
            p_id = input("ID do Posto a eliminar: ").strip()
            try:
                bm.delete_berth(p_id)
                print(f"[OK] Posto {p_id} eliminado.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_stays(vn: VesselManager, bm: BerthManager, sm: StayManager):
    while True:
        print("\n--- MENU: CONTROLO DE TRAFEGO E ESTADIAS ---")
        print("1. Check-in de embarcacao (Alocacao automatica)")
        print("2. Listar barcos atualmente amarrados (Estadias ativas)")
        print("3. Check-out de embarcacao (Apuramento tarifario)")
        print("4. Prolongar dias de estadia")
        print("0. Voltar ao menu principal")
        opcao = input("Opcao: ").strip()

        if opcao == "1":
            reg = input("Matricula do barco para check-in: ").strip().upper()
            barco = vn.get_vessel(reg)
            if not barco:
                print("[ERRO] Barco nao registado. Cadastre-o primeiro no Menu de Embarcacoes.")
                continue
            if sm.get_active_stay_for_vessel(reg):
                print("[ERRO] Este barco ja possui uma estadia ativa na marina.")
                continue

            vaga = bm.find_suitable_berth(barco["length"], barco["draft"])
            if not vaga:
                print("[AVISO] Nao existe nenhuma vaga livre compativel com o tamanho e calado desta embarcacao.")
                continue

            print(f"[SUGESTAO] Vaga compativel encontrada: {vaga['berth_id']} (Max: {vaga['max_length']}m)")
            confirma = input("Confirmar amarracao neste posto? (s/n): ").strip().lower()
            if confirma == "s":
                try:
                    dias = int(input("Numero de dias previstos de permanencia: ").strip())
                    w = input("Requer servico de agua? (s/n): ").strip().lower() == "s"
                    p = input("Requer servico de luz? (s/n): ").strip().lower() == "s"
                    stay_id = sm.create_stay(reg, vaga["berth_id"], dias, use_water=w, use_power=p)
                    bm.set_berth_occupancy(vaga["berth_id"], reg)
                    print(f"[SUCESSO] Check-in efetuado! Registo de estadia: {stay_id} no Posto {vaga['berth_id']}.")
                except Exception as e:
                    print(f"[ERRO] {e}")

        elif opcao == "2":
            ativas = sm.list_stays(active_only=True)
            if not ativas:
                print("Nenhuma embarcacao atracada de momento.")
            else:
                print(f"{'ID ESTADIA':<12} | {'MATRICULA':<12} | {'POSTO':<8} | {'ENTRADA':<16} | {'DIAS PREV.'}")
                print("-" * 65)
                for s in ativas:
                    print(f"{s['stay_id']:<12} | {s['vessel_reg']:<12} | {s['berth_id']:<8} | {s['check_in_date']:<16} | {s['planned_days']}")

        elif opcao == "3":
            reg = input("Matricula do barco para check-out: ").strip().upper()
            stay = sm.get_active_stay_for_vessel(reg)
            if not stay:
                print("[ERRO] Nao existe estadia ativa para esse barco.")
                continue
            barco = vn.get_vessel(reg)
            try:
                total = sm.checkout_stay(stay["stay_id"], barco["length"])
                bm.set_berth_occupancy(stay["berth_id"], None)
                print("\n--- FATURA DE CHECK-OUT ---")
                print(f"Embarcacao: {barco['name']} ({reg})")
                print(f"Posto desocupado: {stay['berth_id']}")
                print(f"Total a liquidar: {total:.2f} EUR")
                print("[SUCESSO] Lugar libertado e estadia encerrada.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "4":
            reg = input("Matricula do barco: ").strip().upper()
            stay = sm.get_active_stay_for_vessel(reg)
            if not stay:
                print("[ERRO] Nao existe estadia ativa para esta matricula.")
                continue
            try:
                dias = int(input("Quantos dias adicionais deseja acrescentar? ").strip())
                sm.update_stay_duration(stay["stay_id"], dias)
                print(f"[OK] Estadia prolongada. Novo total de dias planeados: {stay['planned_days']}.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_relatorios(bm: BerthManager, sm: StayManager):
    while True:
        print("\n--- RELATORIOS E ESTATISTICAS ---")
        print("1. Taxa de Ocupacao dos Pontoes")
        print("2. Resumo Financeiro e Trafego")
        print("3. Alertas de Estadias Prolongadas")
        print("0. Voltar ao menu principal")
        op = input("Opcao: ").strip()

        if op == "1":
            print(gerar_relatorio_ocupacao(bm.berths))
        elif op == "2":
            print(gerar_relatorio_financeiro(sm.stays))
        elif op == "3":
            print(gerar_relatorio_alertas(sm.stays))
        elif op == "0":
            break
        else:
            print("Opcao invalida.")


def main():
    vessels_data, berths_data, stays_data = load_database()
    vn = VesselManager(vessels_data)
    bm = BerthManager(berths_data)
    sm = StayManager(stays_data)

    seed_sample_data(vn, bm)

    try:
        while True:
            print_banner()
            print("1. Gestao de Embarcacoes (CRUD Barcos)")
            print("2. Gestao de Pontoes e Vagas (CRUD Postos)")
            print("3. Controlo de Trafego e Estadias (Check-in/Check-out)")
            print("4. Relatorios e Estatisticas")
            print("5. Guardar Dados em Disco")
            print("6. Criar Backup de Seguranca")
            print("0. Gravar e Sair")
            print("=" * 60)
            escolha = input("Selecione uma opcao: ").strip()

            if escolha == "1":
                menu_vessels(vn, sm)
            elif escolha == "2":
                menu_berths(bm)
            elif escolha == "3":
                menu_stays(vn, bm, sm)
            elif escolha == "4":
                menu_relatorios(bm, sm)
            elif escolha == "5":
                save_database(vn.vessels, bm.berths, sm.stays)
                print("[OK] Dados gravados com sucesso em 'marina_data.json'.")
            elif escolha == "6":
                save_database(vn.vessels, bm.berths, sm.stays)
                if criar_backup:
                    try:
                        destino = criar_backup()
                        print(f"[OK] Backup criado com sucesso em: {destino}")
                    except Exception as e:
                        print(f"[ERRO] Falha ao criar backup: {e}")
                else:
                    print("[AVISO] Modulo de backups nao disponivel.")
            elif escolha == "0":
                save_database(vn.vessels, bm.berths, sm.stays)
                print("A gravar alteracoes... Ate a proxima!")
                sys.exit(0)
            else:
                print("Opcao invalida. Prima ENTER para continuar...")
    except KeyboardInterrupt:
        save_database(vn.vessels, bm.berths, sm.stays)
        print("\n[INFO] Execucao interrompida. Alteracoes gravadas de forma segura.")
        sys.exit(0)


if __name__ == "__main__":
    main()