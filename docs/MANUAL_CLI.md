# Manual de Operacao - Marina Manager CLI

Guia de utilizacao da aplicacao de consola para operadores de cais e capitania.

## 1. Arranque do Sistema
Para iniciar o menu principal a partir da raiz do repositorio execute: `python3 main.py`

## 2. Opcoes do Menu Principal
* **1. Gestao de Embarcacoes (CRUD):** Registar novas embarcacoes, pesquisar por termo, atualizar dados cadastrais e remover registos inativos.
* **2. Gestao de Pontoes e Vagas (CRUD):** Apresenta o estado de cada vaga (LIVRE, OCUPADA, MANUTENCAO) e permite gerir postos de amarracao.
* **3. Controlo de Estadias:** Executa o check-in com atribuicao de vaga compativel e calcula a faturacao no check-out.
* **4. Relatorios e Estatisticas:**
  * Taxa de Ocupacao: Calcula a percentagem de vagas ocupadas, livres e em manutencao.
  * Resumo Financeiro: Apresenta o numero de estadias ativas, concluidas e o total faturado em euros.
* **5. Criar Backup de Seguranca:** Gera uma copia de salvaguarda dos registos do sistema.

## 3. Boas Praticas de Operacao
* Utilize sempre a opcao 0. Sair para encerrar o programa de forma limpa.
* Antes de colocar um posto em manutencao, confirme que nao existe nenhuma embarcacao atracada nessa vaga.
