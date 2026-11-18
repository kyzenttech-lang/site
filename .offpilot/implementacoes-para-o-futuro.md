# Implementações para o futuro

Ideias combinadas com o Otavio para fazer depois. Nada disto está no site ainda.

## 1. Uma parte do site focada em testes e demonstrações (2026-11-18)

- **Por quê:** o "Teste aqui" das páginas de solução não deixava testar de verdade. Eram simulações dentro da página, e o visitante acabava não testando nada. Por isso saiu do site.
- **A ideia:** ter um lugar próprio do site para testar e ver demonstrações de verdade, separado das páginas que explicam as soluções.
- **Pontos para pensar quando formos fazer:**
  - o que o visitante consegue fazer de verdade em cada demonstração, não só clicar e ver um número mudar;
  - demonstrações completas de cada pilar, no formato do cardápio e do agendamento, que já estão no ar como sistemas inteiros:
    - ERP;
    - BI;
    - Aurora;
    - vendas e site;
  - dados de exemplo de cada ramo de negócio;
  - como fica no celular;
  - como as páginas de solução levam para essa parte.
- **O que já existe e pode ser reaproveitado:**
  - As simulações antigas continuam no gerador (`tools/monta_paginas.py`), só desligadas:
    - `ABAS_DEMO` e `central_demos`;
    - `DEMOS_MOD`, que diz quais simulações eram de qual solução;
    - Painel, Estoque, Pedidos, Clientes, Agendamento e Automação.
  - Os sistemas completos do cardápio online e do agendamento online, que já estão no ar.
  - A conversa com a Aurora, que continua na página dela.
