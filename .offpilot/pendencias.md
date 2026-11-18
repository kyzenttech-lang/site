# Pendências para revisar (combinado com o Otavio em 2026-11-16)

Só anotado. Nada disto foi feito ainda.

## 1. Revisar e melhorar as demonstrações
- As 3 simulações (Painel, Estoque, Pedidos) saíram do Início. No Início ficou só "Sistemas prontos para testar" (cardápio online e agendamento online, os sistemas completos).
- As 7 simulações continuam na página Demonstrações (Painel, Estoque, Pedidos, Clientes, Agendamento, Aurora, Automação).
- Revisar juntos:
  - se cada simulação mostra bem a solução (o que falta, o que sobra);
  - dados de exemplo mais próximos de cada segmento (hoje quase tudo é da "Lanchonete Exemplo");
  - uma simulação para o Site;
  - uma demonstração completa de sistema de gestão/estoque, no formato do cardápio e do agendamento;
  - como as simulações ficam no celular;
  - para onde devem levar os links "KYZENT" dentro das demos completas (repositórios cardapio e agendamento).

## 2. Juntar Soluções e Demonstrações: FEITO em 2026-11-16 (commit 9b4febe), com o OK do Otavio
- Textos novos [REVISAR]: "Como funciona no dia a dia" de cada solução (COMO_FUNCIONA no gerador).

(anotação original abaixo)
- O Otavio vê sentido em ligar as duas, ou até fundir tudo em Soluções, porque a demonstração mostra a solução.
- Uma forma possível (só ideia, não decidida): cada simulação na página da solução que ela demonstra (Gestão: Painel, Estoque, Pedidos, Clientes; Vendas: Agendamento; Atendimento: Aurora; IA: Automação), a página Demonstrações sai do menu e o endereço antigo leva ao Início.
- Ligado a isso: o "Conhecer solução" das simulações leva a páginas de solução que hoje estão simples e resumidas; elas precisam explicar melhor cada solução, o que mexe também na página Soluções.

## 3. Navegação do site (não mexer ainda)
- Rever o menu como um todo: quais páginas entram, a ordem e os nomes.
- Como o visitante chega a cada solução e como volta (rodapé, "Todas as soluções").
- O que cada botão principal faz em cada página (orçamento, testar, WhatsApp), sem caminhos repetidos ou sem saída.
- Navegação no celular: menu lateral, barra fixa de WhatsApp e botões que ficam por cima do conteúdo.

### Análise da seção "Soluções para cada parte do seu negócio" (Início), 2026-11-16 (só análise, nada feito)
- São 11 cliques, e vários levam a lugares rasos ou repetidos:
  - as 7 etiquetas do card Gestão (Estoque, Financeiro...) parecem botões e não fazem nada; o card inteiro não é clicável, só o link do rodapé;
  - "Ver os 24 serviços" cai no topo de Soluções (os mesmos pilares de novo), não na lista;
  - os mini-cards Cardápio e Agendamento abrem outro site em nova aba, sem explicação;
  - os links do rodapé dos cards repetem o título do card.
- Páginas de destino desiguais: Gestão tem ~1100 palavras; Site ~300 (sem simulação), IA ~400, Atendimento ~500, Vendas ~600.
- Otavio: o topo diz "24 serviços" e o card diz "11 serviços": parece contradição. Sugestão: tirar a contagem dos cards; o topo vira "Ver todos os serviços", indo direto para a lista.
- Otavio: Aurora repetida (menu, página dela, mini-card "Aurora", link "Atendimento e Aurora" e uma página de solução com o mesmo chat). Já existe uma página só para ela.
  - Opção A (sugestão do Claude): a Aurora vira a página da solução Atendimento (com o sistema de atendimento da equipe dentro), solucao-atendimento sai e o endereço antigo leva para aurora.html.
  - Opção B: Atendimento fica só com o sistema da equipe e cita a Aurora uma vez.
  - Com A, o card "Atendimento e vendas" leva para Vendas e para a Aurora, sem caminhos pela metade.
- Também: Cardápio e Agendamento aparecem em 3 lugares (Início, Vendas, Atendimento); Atendimento e Aurora apontam uma para a outra (caminho circular).

## 4. Textos que dependem dos sócios
- [CONFIRMAR] 3 serviços de BI (Dados de várias fontes num lugar só, Análise de vendas, clientes e estoque, Alertas de indicadores) e a página solucao-bi.html; 6 serviços novos, 3 respostas do FAQ e a frase de estoque e almoxarifado em Quem somos.
- [REVISAR] fichas dos serviços (páginas de solução).

## 5. Próxima conversa: os serviços do site
- Discutir com o Otavio os serviços que estão no site (os 24 do catálogo): quais a Kyzent entrega hoje, quais tirar, quais juntar.
- Atenção: os [CONFIRMAR] já estão no ar; se algum serviço não é entregue hoje, o cliente pode pedir e ouvir "não".

## 6. Sugestões do Claude (só sugestão, nada decidido)
- Itens 2 e 3 (juntar Soluções/Demonstrações e navegação) mexem no mesmo menu e caminho: decidir juntos para não refazer. Ordem sugerida: definir o caminho (problema, solução, ver funcionando, orçamento), depois as páginas de solução, depois encaixar as demonstrações.
- O pilar principal (sistema de gestão/ERP) é o que tem menos prova: só simulações, sem sistema completo como cardápio e agendamento. Uma demo completa de gestão/estoque seria prioridade.
- Quando houver o primeiro cliente real, um caso curto (o que tinha, o que foi feito, o que mudou).
- Medir visitas e de onde vêm os orçamentos com uma ferramenta simples e sem cookies (ligado à LGPD, que ficou para depois).
- O site no ar está atrás do local (branches refinamento e solucoes-completas sem push): talvez subir antes da reestruturação grande.
