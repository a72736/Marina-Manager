# Marina Manager CLI

Aplicacao de consola em Python para gestao logistica de marinas, embarcacoes, postos de amarracao e estadias.

**Unidade Curricular:** Ambientes de Desenvolvimento Colaborativo (ISE - Universidade do Algarve)  
**Docentes:** Pedro Guerreiro, Pedro Santos

---

## Equipa de Desenvolvimento
* **Hugo Coelho** (`a72736`)
* **Joao Gabriel** (`JGabriel47`)
* **Marisa Silverio** (`a94136`)
* **Rafael Coelho** (`rafael-scoelho`)

---

## Requisitos e Execucao
* **Linguagem:** Python 3.8 ou superior (sem dependencias externas graficas ou web).

Para executar a aplicacao no terminal:
1. Clonar o repositorio e mudar para o ramo `desenvolvimento`
2. Executar `python3 main.py`

Para correr os testes unitarios aos relatorios:
`python3 -m unittest test_reports.py`

---

## Estrutura do Projeto
* `main.py` — Ponto de entrada da aplicacao e menus interativos de consola.
* `vessels.py` — Operacoes CRUD e validacoes tecnicas de embarcacoes.
* `berths.py` — Gestao de pontoes, vagas e verificacao de compatibilidade.
* `stays` — Registo de check-in, check-out e calculo tarifario.
* `reports.py` — Relatorios de ocupacao do cais, faturacao e alertas operacionais.
* `backups.py` / `logs.py` — Salvaguarda de dados e registo de auditoria.
* `testes.py` / `test_reports.py` — Testes unitarios as funcoes de validacao e relatorios.
* `docs/MANUAL_CLI.md` — Guia detalhado de operacao para utilizadores.
