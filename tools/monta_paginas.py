"""Monta as páginas do site com o mesmo topo, rodapé e janelas.
Uso (na raiz do site): python tools/monta_paginas.py .
Atenção: sobrescreve index.html, quem-somos.html e servicos.html.
Edite o texto aqui e rode de novo, para as páginas não ficarem diferentes entre si."""
import json, os, sys
from html import escape
from urllib.parse import quote

SITE = sys.argv[1]
BASE = "https://kyzenttech-lang.github.io/site/"
VERSAO = "171"   # aumente a cada mudança no CSS/JS, para o navegador baixar o arquivo novo

WHATS = [("5519988728894", "(19) 98872-8894"), ("5519971246077", "(19) 97124-6077")]
MSG = quote("Olá, vim pelo site da Kyzent")
EMAIL = "kyzent.tech@gmail.com"   # contato geral e de privacidade (LGPD)
PRIVACIDADE_DATA = "13 de novembro de 2026"   # mude ao alterar o texto da política
BOTAO = "Conversar no WhatsApp"   # o nome dos botões de contato do topo, menu, janelas e barra fixa

# Black Friday: implantação grátis (decisão do Otavio, 2026-11-12). Depois do fim, o JS esconde o que é da promoção.
# demonstrações completas (repositórios separados; não editar daqui)
DEMO_CARDAPIO = "https://kyzenttech-lang.github.io/cardapio/"
DEMO_AGENDAMENTO = "https://kyzenttech-lang.github.io/agendamento/"
PROMO_FIM = "2026-12-05T23:59:59-03:00"
PROMO_DATA = "05/12"
MSG_BF = "Olá, vim pelo site da Kyzent e quero aproveitar a implantação grátis da Black Friday."

def link_whats(msg=None, n=0):
    return f"https://wa.me/{WHATS[n][0]}?text={quote(msg) if msg else MSG}"

def svg(d, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

I = {
    "fechar": svg('<path d="M6 6l12 12M18 6L6 18"/>'),
    "mais": svg('<path d="M12 5v14M5 12h14"/>'),
    "conversa": svg('<path d="M20.5 11.5a8.5 8.5 0 0 1-12.4 7.6L3.5 20.5l1.4-4.4A8.5 8.5 0 1 1 20.5 11.5z"/>'),
    "vendas": svg('<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'),
    "gestao": svg('<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M8 13h3M8 16h6"/>'),
    "orcamento": svg('<path d="M9 3.5h6v3H9z"/><path d="M9 5H6.5A1.5 1.5 0 0 0 5 6.5v13A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5v-13A1.5 1.5 0 0 0 17.5 5H15"/><path d="M9 11.5h6M9 15.5h4"/>'),
    "sorteio": svg('<path d="M16 3.5h4.5V8M4 20 20.5 3.5M20.5 16v4.5H16M14.5 14.5l6 6M4 4l5 5"/>'),
    "check": svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    "avancado": svg('<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>'),
    "lanche": svg('<path d="M4 11a8 6 0 0 1 16 0z"/><path d="M3 14.5h18"/><path d="M4.5 18h15a1.5 1.5 0 0 1-1.5 2h-12a1.5 1.5 0 0 1-1.5-2z"/>'),
    "tesoura": svg('<circle cx="6" cy="7" r="3"/><circle cx="6" cy="17" r="3"/><path d="M8.5 8.8 20 19M8.5 15.2 20 5"/>'),
    "pente": svg('<path d="M3.5 7.5h17v3.5h-17z"/><path d="M6 11v7M9 11v7M12 11v7M15 11v7M18 11v7"/>'),
    "dente": svg('<path d="M7.5 3.5c-2.6 0-4.3 2-4.3 4.7 0 3.1 1.6 4.6 2.1 7.6.5 3 1 5.7 2.4 5.7 1.6 0 1.6-4.2 3.3-4.2s1.7 4.2 3.3 4.2c1.4 0 1.9-2.7 2.4-5.7s2.1-4.5 2.1-7.6c0-2.7-1.7-4.7-4.3-4.7-1.9 0-2.8 1-4.5 1s-2.6-1-4.5-1z"/>'),
    "agenda": svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4M8.5 14h2M13.5 14h2M8.5 17h2"/>'),
    "site": svg('<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><path d="M3 9.5h18M6.5 7h.01M9 7h.01M7.5 13.5h5M7.5 16h8"/>'),
    "seta_baixo": svg('<path d="M6 9.5l6 6 6-6"/>'),
    "pata": svg('<circle cx="6.5" cy="11" r="1.8"/><circle cx="10" cy="6.5" r="1.8"/><circle cx="14" cy="6.5" r="1.8"/><circle cx="17.5" cy="11" r="1.8"/><path d="M8 17.2c0-2.3 1.8-4 4-4s4 1.7 4 4c0 1.6-1.2 2.3-2.6 2.3-.9 0-1.1-.4-1.4-.4s-.5.4-1.4.4C9.2 19.5 8 18.8 8 17.2z"/>'),
    "cruz": svg('<path d="M9 4h6v5h5v6h-5v5H9v-5H4V9h5z"/>'),
    "voltar": svg('<path d="M15 5l-7 7 7 7"/>'),
    "mic": svg('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>'),
    "alvo": svg('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8"/>'),
    "olho": svg('<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>'),
    "escudo": svg('<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>'),
    "suporte": svg('<path d="M4.5 13.5v-2a7.5 7.5 0 0 1 15 0v2"/><rect x="3" y="13" width="4" height="6" rx="1.5"/><rect x="17" y="13" width="4" height="6" rx="1.5"/><path d="M19 19c0 1.4-1.6 2-4 2h-2"/>'),
    "medida": svg('<path d="M3.5 16.5 16.5 3.5l4 4-13 13z"/><path d="M7 13l1.5 1.5M10 10l1.5 1.5M13 7l1.5 1.5"/>'),
    "raio": svg('<path d="M13 2.5 4.5 13.5H12l-1 8 8.5-11H12z"/>'),
    "busca": svg('<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>'),
    "mapa": svg('<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6z"/><path d="M9 4v14M15 6v14"/>'),
    "codigo": svg('<path d="M8.5 7 3.5 12l5 5M15.5 7l5 5-5 5"/>'),
    "foguete": svg('<path d="M12 15.5 8.5 12C10 7 13.5 3.8 20.5 3.5 20.2 10.5 17 14 12 15.5z"/><path d="M8.5 12 5 11.5l2.5-3.5h4M12 15.5l.5 3.5 3.5-2.5v-4"/><circle cx="15.5" cy="8.5" r="1.3"/>'),
    "grafico": svg('<path d="M4 20V10M10 20V4M16 20v-7M21 20H3"/>'),
    "estoque": svg('<path d="M3.5 8 12 3.5 20.5 8v8.5L12 21l-8.5-4.5z"/><path d="M3.5 8 12 12.5 20.5 8M12 12.5V21"/>'),
    "repetir": svg('<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8.5M20 4v4.5h-4.5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 15.5M4 20v-4.5h4.5"/>'),
    "valores": svg('<path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z"/>'),
    "externo": svg('<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 19V7.5A1.5 1.5 0 0 1 5.5 6H10"/>'),
    "instagram": svg('<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17 7h.01"/>'),
}
TIQUES = ('<svg class="zap-tiques" viewBox="0 0 18 11" aria-hidden="true"><path d="M1 6.2l3 3L11 1.5M7 9.2l.8.8L15 1.5" '
          'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

PAGINAS = [("index.html", "Início"), ("servicos.html", "Soluções"), ("aurora.html", "Aurora"),
           ("quem-somos.html", "Quem somos"), ("orcamento.html", "Orçamento")]

# ------------------------------------------------------------------ catálogo de serviços (sem preço: o valor é combinado com cada cliente)
# ramos: para quais tipos de negócio o serviço é indicado (filtro da página Serviços)
TODOS = ["lanchonete", "barbearia", "salao", "consultorio", "petshop"]
CATALOGO = {
    "Chatbots inteligentes": ("Atendimento automatizado pelo WhatsApp e Instagram, disponível 24 horas.", TODOS),
    "Respostas inteligentes": ("Resolução automática de dúvidas e perguntas frequentes.", TODOS),
    "Triagem de atendimento": ("Identificação das necessidades dos clientes e encaminhamento para atendentes humanos.", ["salao", "consultorio"]),
    "Centrais inteligentes de atendimento": ("Múltiplos agentes de IA trabalhando em diferentes funções.", []),
    "Agendamento online": ("O cliente escolhe o serviço, o dia e o horário, e a agenda se organiza sozinha.", ["barbearia", "salao", "consultorio", "petshop"]),
    "Cardápio online com pedidos": ("Cardápio com fotos, preços e carrinho; o pedido chega organizado e com o total somado.", ["lanchonete"]),       # [CONFIRMAR]
    "Sistema de atendimento": ("Um lugar para a sua equipe ver e responder todas as conversas dos clientes.", TODOS),                               # [CONFIRMAR]
    "Captação e qualificação de leads": ("Identificação e classificação de potenciais clientes.", ["salao", "consultorio"]),
    "Follow-up inteligente": ("Acompanhamento automático de clientes e recuperação de oportunidades.", TODOS),
    "Orçamentos automatizados": ("Geração e envio de propostas comerciais.", ["salao"]),
    "Automação de processos comerciais": ("Integração e otimização de etapas do processo de vendas.", []),
    "Gestão de cadastros e pedidos": ("Organização automatizada de informações e solicitações.", ["lanchonete", "petshop"]),
    "Integração com CRM": ("Centralização e gerenciamento do relacionamento com clientes.", ["barbearia", "salao", "consultorio", "petshop"]),
    "Relatórios e painel de indicadores": ("Os números do negócio num painel que se atualiza sozinho.", ["lanchonete", "barbearia", "petshop"]),
    "Automação de documentos": ("Organização e envio automático de documentos.", ["consultorio"]),
    "Sistema de gestão sob medida (ERP)": ("O sistema do seu negócio, feito do jeito que você trabalha, só com o que você precisa.", TODOS),     # [CONFIRMAR]
    "Controle de estoque": ("O estoque baixa sozinho a cada venda e avisa quando um produto está acabando.", ["lanchonete", "petshop"]),        # [CONFIRMAR]
    "Financeiro e fluxo de caixa": ("Entradas, saídas e contas a pagar e a receber, com o caixa do dia fechado sem calculadora.", TODOS),     # [CONFIRMAR]
    "Cadastro de clientes e fornecedores": ("Clientes e fornecedores num lugar só, com o histórico de cada um.", TODOS),                       # [CONFIRMAR]
    "Integração com os sistemas que você já usa": ("O que a Kyzent desenvolve conversa com o que você já tem, sem digitar a mesma coisa duas vezes.", []),
    "Agentes de IA personalizados": ("Inteligência artificial desenvolvida conforme as necessidades da empresa.", []),
    "Assistentes internos de IA": ("Uma IA que ajuda a equipe a consultar e organizar as informações da empresa.", []),
    "Sistemas personalizados": ("Sistemas desenvolvidos do zero para um processo que nenhum sistema pronto resolve.", []),
    "Site personalizado": ("Site feito sob medida para o seu negócio, conforme o que você quer mostrar e o que mais interessa aos seus clientes.", TODOS),
    "Dados de várias fontes num lugar só": ("Sistema de gestão, vendas e planilhas reunidos numa base só, prontos para analisar.", []),          # [CONFIRMAR]
    "Análise de vendas, clientes e estoque": ("O que mais vende, quem mais compra e o que está parado no estoque, mês a mês.", TODOS),          # [CONFIRMAR]
    "Alertas de indicadores": ("Um aviso quando um número sai do normal: venda que caiu, custo que subiu, meta que ficou para trás.", []),   # [CONFIRMAR]
}

FICHAS = {
    "Sistema de gestão sob medida (ERP)": ("Controles espalhados em caderno, planilha e vários programas.", "Tudo do negócio num lugar só, sem pagar por funções que você não usa."),
    "Controle de estoque": ("Produto que acaba sem ninguém perceber.", "Você repõe antes de faltar."),
    "Financeiro e fluxo de caixa": ("Não saber quanto entrou e quanto saiu no mês.", "O caixa fecha certo e as contas do mês ficam à vista."),
    "Cadastro de clientes e fornecedores": ("Contatos perdidos em agendas, papéis e conversas.", "Qualquer pessoa da equipe acha o contato e o histórico."),
    "Gestão de cadastros e pedidos": ("Pedidos anotados em vários lugares.", "Cada pedido com a sua situação, do começo ao fim."),
    "Integração com CRM": ("Relacionamento com o cliente sem nenhum registro.", "O histórico de cada cliente à mão na hora de atender."),
    "Relatórios e painel de indicadores": ("Decidir sem saber os números do negócio.", "Os números do mês sem montar planilha."),
    "Automação de documentos": ("Documentos montados e enviados um a um.", "Os documentos saem prontos e no prazo."),
    "Integração com os sistemas que você já usa": ("Digitar a mesma informação em dois sistemas.", "Os dados passam de um sistema para o outro sozinhos."),
    "Cardápio online com pedidos": ("Pedido anotado por mensagem, com erro no item ou no total.", "O pedido chega completo e com o total certo."),
    "Agendamento online": ("Horário marcado por mensagem, com conflito na agenda.", "O cliente marca sozinho, sem choque de horário."),
    "Captação e qualificação de leads": ("Contatos que chegam e ninguém acompanha.", "A equipe atende primeiro quem tem mais chance de fechar."),
    "Follow-up inteligente": ("Cliente que some depois do primeiro contato.", "O retorno sai no momento certo, sem depender da memória de ninguém."),
    "Orçamentos automatizados": ("Orçamento demorado, que esfria a venda.", "A proposta chega enquanto o cliente ainda está interessado."),
    "Automação de processos comerciais": ("Cada etapa da venda feita à mão, uma por uma.", "A venda anda sem alguém empurrar cada etapa."),
    "Sistema de atendimento": ("Conversas espalhadas em vários celulares.", "A equipe divide o atendimento e nada fica sem resposta."),
    "Chatbots inteligentes": ("Cliente sem resposta à noite e no fim de semana.", "Atendimento a qualquer hora, com as informações do negócio."),
    "Respostas inteligentes": ("As mesmas perguntas respondidas o dia inteiro.", "A equipe fica livre para o que precisa de uma pessoa."),
    "Triagem de atendimento": ("Mensagem importante perdida no meio das outras.", "Cada pedido chega para a pessoa certa."),
    "Centrais inteligentes de atendimento": ("Um só atendimento para assuntos muito diferentes.", "Cada assunto atendido por um agente preparado para ele."),
    "Site personalizado": ("Cliente que não encontra o seu negócio na internet.", "Serviços, horários e contato num lugar só, com a sua marca."),
    "Agentes de IA personalizados": ("Tarefa repetitiva que nenhum sistema pronto faz.", "A IA faz a tarefa do jeito do seu processo."),
    "Assistentes internos de IA": ("A equipe perde tempo procurando informação.", "A resposta vem na hora, com base nos dados da empresa."),
    "Sistemas personalizados": ("Um processo que nenhum sistema pronto resolve.", "Um sistema feito do zero para esse processo."),
    "Dados de várias fontes num lugar só": ("Cada número num sistema diferente, sem conversar entre si.", "Uma visão só do negócio, sem juntar planilha à mão."),
    "Análise de vendas, clientes e estoque": ("Decidir compra e promoção no achismo.", "Você vê o que vende, para quem e quando."),
    "Alertas de indicadores": ("Descobrir o problema só no fim do mês.", "O aviso chega enquanto ainda dá tempo de agir."),
}

# módulos da página Serviços: (id, nome, nome curto (celular), ícone, resumo, [serviços])
MODULOS = [
    ("gestao", "Sistemas de gestão sob medida", "Gestão", "gestao",
     "A Kyzent desenvolve o sistema de gestão do seu negócio (ERP): estoque, financeiro, clientes e relatórios num lugar só.",
     ["Sistema de gestão sob medida (ERP)", "Controle de estoque", "Financeiro e fluxo de caixa", "Cadastro de clientes e fornecedores",
      "Gestão de cadastros e pedidos", "Integração com CRM", "Automação de documentos",
      "Integração com os sistemas que você já usa"]),
    ("bi", "BI e análise de dados", "BI", "grafico",
     "Painéis e relatórios com os números do seu negócio, atualizados sozinhos, para decidir com base no que aconteceu.",
     ["Relatórios e painel de indicadores", "Dados de várias fontes num lugar só", "Análise de vendas, clientes e estoque", "Alertas de indicadores"]),
    ("agenda", "Pedidos, agendamento e vendas", "Vendas", "agenda",
     "Cardápio online, agendamento online e ferramentas para vender mais e trazer o cliente de volta.",
     ["Cardápio online com pedidos", "Agendamento online", "Captação e qualificação de leads", "Follow-up inteligente", "Orçamentos automatizados", "Automação de processos comerciais"]),
    ("whatsapp", "Atendimento e Aurora", "Atendimento", "conversa",
     "Um sistema de atendimento para a sua equipe e a Aurora, a IA que atende no WhatsApp e no Instagram.",
     ["Sistema de atendimento", "Chatbots inteligentes", "Respostas inteligentes", "Triagem de atendimento", "Centrais inteligentes de atendimento"]),
    ("site", "Site e presença online", "Site", "site",
     "Um site feito sob medida para o seu negócio, do jeito que você quer apresentá-lo.",
     ["Site personalizado"]),
    ("ia", "IA sob medida", "IA", "avancado",
     "Inteligência artificial e automações desenvolvidas para o jeito de trabalhar da sua empresa.",
     ["Agentes de IA personalizados", "Assistentes internos de IA", "Sistemas personalizados"]),
]

MOD_SERVICOS = {mid: servs for mid, _n, _c, _i, _r, servs in MODULOS}
assert set(FICHAS) == set(CATALOGO), ("serviço sem ficha ou ficha sem serviço", set(FICHAS) ^ set(CATALOGO))

# os 4 pilares das soluções: (id, título, apoio, texto, resultados, [módulos])
PILARES_SOL = [
    ("erp", "ERP sob medida", "O sistema do seu negócio",
     "Estoque, vendas, caixa e clientes num sistema só, tudo ligado. Uma venda já baixa o estoque e entra no caixa.",
     ["Estoque, caixa, clientes e fornecedores num lugar só", "Só as partes que o seu negócio usa", "Começa com um módulo e cresce depois"],
     ["gestao"]),
    ("bi", "BI e análise de dados", "Os números que guiam a decisão",
     "Painéis e relatórios que se atualizam sozinhos, com os dados de todos os seus sistemas num lugar só.",
     ["O que mais vende e o que está parado", "Os números do mês sem montar planilha", "Um aviso quando algo sai do normal"],
     ["bi"]),
    ("ia", "IA de atendimento", "A Aurora e agentes sob medida",
     "A Aurora atende os seus clientes no WhatsApp e no Instagram a qualquer hora, e agentes de IA fazem as tarefas repetitivas da equipe.",
     ["Resposta na hora, até de madrugada", "Uma pessoa entra quando precisa", "Tarefas internas feitas por agentes de IA"],
     ["whatsapp", "ia"]),
    ("vendas", "Vendas e presença online", "Cardápio, agendamento e site",
     "Cardápio online com pedidos, agendamento online e um site com a sua marca, para o cliente comprar e marcar sozinho.",
     ["O cliente pede ou marca o horário sozinho", "Site com a marca e as informações do negócio", "Quem sumiu recebe um lembrete para voltar"],
     ["agenda", "site"]),
]
# pilares do Início (como eram antes; o Início não mudou com os 4 pilares de Soluções)
PILARES_INICIO = [
    ("sistemas", "Sistemas de gestão sob medida", "ERP feito para o seu negócio",
     "Chega de caderno e planilha: estoque, vendas, caixa e clientes num sistema só, tudo ligado. Uma venda já baixa o estoque e entra no caixa.",
     ["Estoque, caixa, clientes e fornecedores num lugar só", "Só as partes que o seu negócio usa", "Começa com um módulo e cresce depois"],
     ["gestao"]),
    ("atendimento", "Atendimento e vendas", "Do primeiro contato ao pedido",
     "Cardápio online, agendamento online, um sistema de atendimento para a equipe e a Aurora, a IA que responde a qualquer hora.",
     ["O cliente faz o pedido ou marca o horário sozinho", "A equipe vê todas as conversas num lugar só", "Quem sumiu recebe um lembrete para voltar"],
     ["agenda", "whatsapp"]),
    ("presenca", "Presença online e IA sob medida", "Para ser encontrado e trabalhar menos",
     "Sites feitos para o seu negócio, inteligência artificial para processos internos e automações sob medida.",
     ["Site com a marca e as informações do negócio", "IA para as tarefas internas da equipe", "Automação para o processo que só você tem"],
     ["site", "ia"]),
]

# caminhos de cada pilar: (texto, endereço); o primeiro é o principal
CAMINHOS_PILAR = {
    "erp": [("Conhecer o ERP", "solucao-gestao.html")],
    "bi": [("Conhecer o BI", "solucao-bi.html")],
    "ia": [("Conhecer a Aurora", "aurora.html"), ("Agentes sob medida", "solucao-ia.html")],
    "vendas": [("Cardápio e agendamento", "solucao-vendas.html"), ("Site", "solucao-site.html")],
}
ICONE_PILAR = {"erp": "gestao", "bi": "grafico", "ia": "conversa", "vendas": "vendas"}

# fotos de banco (Unsplash, licença livre; origem em assets/fotos/CREDITOS.md): arquivo, largura, altura

# ------------------------------------------------------------------ partes comuns
def menu(atual, classe):
    itens = []
    for arq, nome in PAGINAS:
        cur = ' aria-current="page"' if arq == atual else ""
        marca = '<span class="menu-marca" aria-hidden="true"></span>' if arq == atual and classe == "menu" else ""
        itens.append(f'<li><a href="{arq}"{cur}>{nome}{marca}</a></li>')
    c = f' class="{classe}"' if classe else ""
    return f'<ul{c}>' + "".join(itens) + "</ul>"

MENU_DESCRICAO = {"index.html": "Soluções, sistemas para testar e segmentos", "servicos.html": "Catálogo completo de serviços",
                  "aurora.html": "A IA de atendimento da Kyzent",
                  "quem-somos.html": "Propósito, missão e valores", "orcamento.html": "Simule e receba uma recomendação"}
def menu_celular(atual):
    return "".join(
        f'<li style="--i:{i}"><a href="{arq}"{ATUAL if arq == atual else ""}>'
        f'<span class="menu-celular-nome">{nome}</span><small>{MENU_DESCRICAO[arq]}</small></a></li>'
        for i, (arq, nome) in enumerate(PAGINAS))
ATUAL = ' aria-current="page"'

def logo():
    return '<img src="assets/img/kyzent-horizontal-escuro.svg" alt="Kyzent, automação e IA" width="590" height="140">'


JANELAS_GERAIS = ""   # o carrinho de orçamento saiu em 2026-11-12: o orçamento agora é pelo simulador (orcamento.html)

def relogio(cls=""):
    """Contador regressivo até o fim da Black Friday (o JS atualiza a cada segundo)."""
    partes = "".join(f'<span class="relogio-parte"><b data-{k}>--</b><small>{n}</small></span>' for k, n in
                     (("dias", "dias"), ("horas", "horas"), ("min", "min"), ("seg", "seg")))
    return f'<div class="relogio {cls}" data-relogio role="timer" aria-label="A promoção termina em {PROMO_DATA}">{partes}</div>'

def faixa_promo():
    return f"""  <div class="promo-faixa" data-promo>
    <div class="container promo-faixa-conteudo">
      <p class="promo-faixa-texto"><span class="promo-selo">Black Friday</span><span><strong>Implantação grátis</strong><span class="promo-faixa-extra"> em qualquer automação</span> até {PROMO_DATA}</span></p>
      {relogio("relogio-mini")}
      <a class="promo-faixa-botao" href="{link_whats(MSG_BF)}" target="_blank" rel="noopener" data-contato data-msg="{MSG_BF}">Garantir</a>
    </div>
  </div>
"""

DADOS_ESTRUTURADOS = json.dumps({
    "@context": "https://schema.org", "@type": "Organization", "name": "Kyzent Technology Solutions",
    "alternateName": "Kyzent", "url": BASE, "logo": BASE + "assets/icons/apple-touch-icon.png", "image": BASE + "assets/og-image.png",
    "description": "A Kyzent desenvolve sistemas de gestão sob medida (ERP), cardápio online, agendamento online, atendimento com IA e sites para pequenos e médios negócios.",
    "email": EMAIL, "telephone": "+55-19-98872-8894", "areaServed": {"@type": "Country", "name": "Brasil"},
    "sameAs": ["https://www.instagram.com/kyzent.tech/"],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Soluções da Kyzent", "itemListElement": [
        {"@type": "OfferCatalog", "name": titulo, "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": servico, "description": CATALOGO[servico][0]}}
            for m in mods for servico in MOD_SERVICOS[m]]}
        for _pid, titulo, _a, _t, _r, mods in PILARES_SOL]}}, ensure_ascii=False)

def pagina(arq, titulo, descricao, corpo, janelas="", ativo=None):
    url = BASE + ("" if arq == "index.html" else arq)
    ativo = ativo or arq
    servicos_rodape = "".join(f'<li><a href="{PAGINA_MOD[mid]}">{nome}</a></li>' for mid, nome, *_ in MODULOS if mid in MOD_PAGINA and mid != "bi")   # rodapé como antes dos 4 pilares
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark" data-v="{VERSAO}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{descricao}">
  <meta name="theme-color" content="#0B0B0F">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{url}">

  <!-- Open Graph (prévia do link no WhatsApp e no Instagram) -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Kyzent">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descricao}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Logo da Kyzent com o texto: automação e IA para empresas">
  <meta name="twitter:card" content="summary_large_image">

  <script type="application/ld+json">{DADOS_ESTRUTURADOS}</script>

  <link rel="icon" href="assets/icons/icon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/icons/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">

  <script>document.documentElement.classList.add("js");
  // transição entre páginas: o conteúdo desliza no sentido do menu (avançar ou voltar)
  (function () {{
    var ordem = ["index.html", "servicos.html", "solucao-", "aurora.html", "quem-somos.html", "orcamento.html", "privacidade.html"];
    function pos(u) {{ try {{ var a = new URL(u).pathname.split("/").pop() || "index.html";
      for (var i = 0; i < ordem.length; i++) if (a.indexOf(ordem[i]) === 0) return i; }} catch (e) {{}} return -1; }}
    addEventListener("pagereveal", function (e) {{
      var n = window.navigation;
      if (!e.viewTransition || !n || !n.activation || !n.activation.from) return;
      var de = pos(n.activation.from.url), para = pos(n.activation.entry.url);
      if (de < 0 || para < 0 || de === para) return;
      e.viewTransition.types.add(para > de ? "avancar" : "voltar");
    }});
  }})();</script>
  <link rel="preload" href="assets/fonts/mona-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css?v={VERSAO}">
  <script src="assets/vendor/gsap/gsap.min.js?v=3130" defer></script>
  <script src="assets/vendor/gsap/ScrollTrigger.min.js?v=3130" defer></script>
  <script src="assets/vendor/gsap/CustomEase.min.js?v=3130" defer></script>
  <script src="js/main.js?v={VERSAO}" defer></script>
  <script src="js/animacoes.js?v={VERSAO}" defer></script>
</head>
<body data-promo-fim="{PROMO_FIM}" data-whats="{" ".join(n for n, _ in WHATS)}">
  <a class="pular" href="#conteudo">Pular para o conteúdo</a>
{faixa_promo()}
  <header class="barra" data-barra>
    <div class="container barra-conteudo">
      <a class="barra-logo" href="index.html" aria-label="Kyzent, página inicial">{logo()}</a>
      <nav aria-label="Principal">{menu(ativo, "menu")}</nav>
      <div class="barra-acoes">
        <button class="icone-botao botao-menu" type="button" data-abrir-menu aria-expanded="false" aria-controls="menu-celular" aria-label="Abrir menu"><span class="hamburguer" aria-hidden="true"><i></i><i></i><i></i></span></button>
        <a class="botao botao-barra" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a>
      </div>
    </div>
    <nav class="menu-celular" id="menu-celular" aria-label="Menu">
      <ul class="menu-celular-links">{menu_celular(ativo)}</ul>
      <div class="menu-celular-base">
        <p class="menu-celular-promo" data-promo><span class="promo-selo">Black Friday</span>Implantação grátis até {PROMO_DATA}</p>
        <a class="botao botao-grande" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}{BOTAO}</a>
        <a class="menu-celular-insta" href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">{I["instagram"]}@kyzent.tech</a>
      </div>
    </nav>
  </header>
  <div class="menu-fundo" data-fechar-menu aria-hidden="true"></div>

  <main id="conteudo">
{corpo}
  </main>

  <footer class="rodape">
    <div class="container">
      <div class="rodape-grade">
        <div class="rodape-marca">
          <a href="index.html" aria-label="Kyzent, página inicial">{logo()}</a>
          <p>Empresa de Tecnologia e Inovação. Sistemas de gestão, atendimento e Inteligência Artificial sob medida para pequenos e médios negócios.</p>
        </div>
        <div>
          <h2>Navegação</h2>
          {menu(None, "")}
        </div>
        <div>
          <h2>Serviços</h2>
          <ul>{servicos_rodape}</ul>
        </div>
        <div>
          <h2>Contato</h2>
          <ul>
            <li class="rodape-whats">WhatsApp <a href="{link_whats(None, 0)}" target="_blank" rel="noopener" aria-label="WhatsApp {WHATS[0][1]}">{WHATS[0][1]}</a> · <a href="{link_whats(None, 1)}" target="_blank" rel="noopener" aria-label="WhatsApp {WHATS[1][1]}">{WHATS[1][1]}</a></li>
            <li><a href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">Instagram @kyzent.tech</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          </ul>
        </div>
      </div>
      <div class="rodape-base">
        <p>© <span data-ano>2026</span> Kyzent Technology Solutions. Todos os direitos reservados.</p>
        <p><a href="privacidade.html">Política de Privacidade</a></p>
      </div>
    </div>
  </footer>
  <a class="whats-flutuante" href="{link_whats()}" target="_blank" rel="noopener" data-contato aria-label="Fale com a gente no WhatsApp">{I["conversa"]}<span>Fale com a gente</span></a>
  <div class="barra-fixa">
    <a class="whats-fixo" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}<span class="whats-longo">{BOTAO}</span><span class="whats-curto">WhatsApp</span></a>
  </div>

{JANELAS_GERAIS}
{janelas}
</body>
</html>
"""

# ------------------------------------------------------------------ blocos comuns
PERGUNTAS = [
    ("Como funciona a implantação grátis da Black Friday?",
     f"Quem fechar com a Kyzent até {PROMO_DATA}/2026 não paga a implantação: a configuração inicial da automação fica por nossa conta. Você paga só a mensalidade, combinada conforme o seu negócio."),
    ("Quanto custa a mensalidade?",
     "Depende do que for automatizado, das integrações e do volume de uso. A gente entende como funciona o seu negócio pelo WhatsApp e monta um orçamento personalizado, sem compromisso."),
    ("O WhatsApp da minha empresa corre risco de bloqueio?",
     "Usamos a API oficial da Meta, a conexão aprovada pelo próprio WhatsApp. Não usamos conexões não oficiais por QR Code, que podem levar ao bloqueio do número."),
    ("Vocês dão suporte depois que a automação está funcionando?",
     "Sim. Cada solução vem com manutenção e suporte da nossa equipe, para a tecnologia seguir funcionando sem você se preocupar com a parte técnica."),
    ("Para quais tipos de negócio a Kyzent trabalha?",
     "Lanchonetes, pizzarias, barbearias, salões de beleza, clínicas, pet shops, lojas e pequenas e médias empresas de qualquer lugar do Brasil. Se o seu ramo não está na lista, fale com a gente e conte como é o seu dia a dia."),
    ("Vocês fazem sistema de gestão (ERP) do zero?",
     "Sim. A Kyzent desenvolve o sistema a partir de como o seu negócio funciona, só com as partes que você precisa: estoque, financeiro, clientes, pedidos e relatórios."),   # [CONFIRMAR]
    ("Vocês conseguem usar o sistema que eu já tenho?",
     "Em muitos casos, sim: ligamos o que você já usa ao que desenvolvemos. Isso depende de o seu sistema permitir, e a gente confere no diagnóstico."),   # [CONFIRMAR]
    ("Preciso ter a Aurora para contratar um sistema?",
     "Não. Cada solução pode ser contratada separada: o sistema de gestão, o cardápio online, o agendamento, o site ou a Aurora."),
    ("Funciona no computador e no celular?",
     "Sim. Os sistemas funcionam pelo navegador, no computador e no celular, sem precisar instalar nada."),   # [CONFIRMAR]
    ("Posso testar antes de contratar?",
     'Sim. O <a href="#testar">cardápio online e o agendamento online</a> estão no ar para você testar, e a <a href="solucao-gestao.html">página do sistema de gestão</a> mostra como ele funciona no dia a dia.'),
]
# as perguntas do Início em 3 assuntos (todas continuam; só ficam agrupadas)
GRUPOS_PERGUNTAS = [
    ("contratacao", "Contratação e preço", ["Como funciona a implantação grátis da Black Friday?", "Quanto custa a mensalidade?",
                                             "Posso testar antes de contratar?", "Vocês dão suporte depois que a automação está funcionando?"]),
    ("sistemas", "Sistemas", ["Vocês fazem sistema de gestão (ERP) do zero?", "Vocês conseguem usar o sistema que eu já tenho?",
                              "Funciona no computador e no celular?", "Para quais tipos de negócio a Kyzent trabalha?"]),
    ("aurora", "Aurora e WhatsApp", ["O WhatsApp da minha empresa corre risco de bloqueio?", "Preciso ter a Aurora para contratar um sistema?"]),
]
assert sorted(q for _g, _n, qs in GRUPOS_PERGUNTAS for q in qs) == sorted(q for q, _r in PERGUNTAS), "pergunta fora dos grupos"

def perguntas():
    resp = dict(PERGUNTAS)
    abas, paineis = [], []
    for k, (gid, nome, qs) in enumerate(GRUPOS_PERGUNTAS):
        sel = k == 0
        abas.append(f'<button type="button" class="perg-aba" role="tab" id="perg-aba-{gid}" aria-controls="perg-{gid}" aria-selected="{"true" if sel else "false"}"'
                    f' tabindex="{0 if sel else -1}">{nome}<span class="perg-qtd">{len(qs)}</span></button>')
        itens = "".join(f'<details class="pergunta"><summary><span>{q}</span><span class="pergunta-icone">{I["mais"]}</span></summary>'
                        f'<div class="pergunta-resposta"><p>{resp[q]}</p></div></details>' for q in qs)
        paineis.append(f'          <div class="perg-painel" id="perg-{gid}" role="tabpanel" aria-labelledby="perg-aba-{gid}">{itens}</div>')
    return f"""    <section class="secao" id="perguntas" aria-labelledby="titulo-perguntas">
      <div class="container perguntas-grade">
        <div class="cabeca perguntas-cabeca">
          <h2 id="titulo-perguntas" data-revelar-texto>Perguntas frequentes.</h2>
          <p>Ficou alguma dúvida? Monte uma simulação e a gente responde com uma proposta para o seu negócio.</p>
          <a class="botao botao-contorno" href="orcamento.html">Simular meu orçamento</a>
        </div>
        <div class="perguntas perguntas-grupos" data-perguntas>
          <div class="perg-abas" role="tablist" aria-label="Assuntos das perguntas">{"".join(abas)}</div>
{chr(10).join(paineis)}
        </div>
      </div>
    </section>"""

# ------------------------------------------------------------------ base fictícia das demonstrações
# Pedidos, Clientes, Painel e Automação são da mesma Lanchonete Exemplo e leem daqui, para nunca se contradizerem.
# Os itens dos pedidos usam só produtos do CARDAPIO. (Chatbot é da Barbearia Exemplo e Agendamento do Salão Exemplo.)
CARDAPIO = [("X-salada", 22), ("X-bacon", 26), ("Porção de batata", 15), ("Refrigerante lata", 6)]
# (nome completo, tipo, situação)
CLIENTES = [("Marina Lopes", "recorrente", "Pediu hoje, cliente há 8 meses"), ("Carlos Souza", "recorrente", "Pediu hoje, último pedido há 5 dias"),
            ("Ana Ribeiro", "novo", "Primeiro pedido hoje"), ("João Pereira", "recorrente", "Último pedido há 12 dias"),
            ("Paula Martins", "inativo", "Sem pedir há 35 dias"), ("Rita Alves", "novo", "Primeiro pedido há 3 dias"),
            ("Roberto Lima", "inativo", "Sem pedir há 42 dias"), ("Bia Santos", "inativo", "Sem pedir há 60 dias")]
# pedidos de hoje: (número, cliente, itens, classe do estado, estado)
PEDIDOS_DEMO = [("#1043", "Marina", "2 X-bacon e 2 refrigerantes lata", "preparo", "Em preparo"),
                ("#1042", "Carlos", "1 X-salada e 1 refrigerante lata", "rota", "Saiu para entrega"),
                ("#1041", "Ana", "2 porções de batata", "ok", "Entregue")]
# estoque dos mesmos produtos do CARDAPIO: (produto, quantidade, mínimo). X-bacon começa perto do mínimo.
ESTOQUE_DEMO = [("X-salada", 14, 5), ("X-bacon", 7, 5), ("Porção de batata", 9, 4), ("Refrigerante lata", 24, 10)]
assert [p for p, _, _ in ESTOQUE_DEMO] == [n for n, _ in CARDAPIO], "o estoque precisa ter os mesmos produtos do cardápio"
PROXIMO_PEDIDO = 1044   # o primeiro pedido registrado na demo recebe este número
# pedidos por dia na semana; a soma é o KPI "Pedidos" do painel
SEMANA = [("Seg", 28), ("Ter", 36), ("Qua", 33), ("Qui", 43), ("Sex", 59), ("Sáb", 68), ("Dom", 45)]
DIA_EXTENSO = {"Seg": "segunda", "Ter": "terça", "Qua": "quarta", "Qui": "quinta", "Sex": "sexta", "Sáb": "sábado", "Dom": "domingo"}
for _n, _q, _o, _c, _e in PEDIDOS_DEMO:   # trava: quem pediu hoje existe na base e não está inativo
    assert any(c.split()[0] == _q and t != "inativo" for c, t, _ in CLIENTES), f"pedido {_n}: {_q} fora da base ou inativo"

def demo_gestao():
    pedidos = "".join(f'<li><span class="pd-num">{n}</span><span class="pd-quem"><strong>{q}</strong><small>{o}</small></span><span class="estado estado-{c}">{e}</span></li>'
                      for n, q, o, c, e in PEDIDOS_DEMO)
    maior = max(v for _, v in SEMANA)
    total = sum(v for _, v in SEMANA)
    barras = "".join(f'<div class="gd-barra"><i style="--h:{round(v * 100 / maior)}%;--d:{k*70}ms"></i><small>{d}</small></div>' for k, (d, v) in enumerate(SEMANA))
    por_dia = ", ".join(f"{DIA_EXTENSO[d]} {v}" for d, v in SEMANA)
    ultimos = "; ".join(f"{n} de {q}, {o}, {e.lower()}" for n, q, o, _, e in PEDIDOS_DEMO)
    rotulo = (f"Exemplo ilustrativo de painel de gestão da semana: {total} pedidos e 96% das entregas no prazo. "
              f"Pedidos por dia: {por_dia}. Processos: reposição de estoque 72%, notas fiscais emitidas 45%, retornos agendados 90%. Últimos pedidos: {ultimos}.")
    return f"""<figure class="demo-visual">
            <div class="gd" data-gestao role="img" aria-label="{escape(rotulo)}">
              <div class="gd-topo" aria-hidden="true"><strong>Painel da semana</strong><span>Atualizado às 18:40</span></div>
              <div class="gd-kpis" aria-hidden="true">
                <div><small>Pedidos</small><strong data-contar="{total}">{total}</strong></div>
                <div><small>Entregas no prazo</small><strong><span data-contar="96">96</span>%</strong></div>
              </div>
              <div class="gd-meio" aria-hidden="true">
                <div class="gd-grafico"><p>Pedidos por dia</p><div class="gd-barras">{barras}</div></div>
                <div class="gd-processo">
                  <p>Processos</p>
                  <div class="gd-proc"><span>Reposição de estoque</span><span class="gd-trilho"><i style="--p:72%"></i></span><small>72%</small></div>
                  <div class="gd-proc"><span>Notas fiscais emitidas</span><span class="gd-trilho"><i style="--p:45%"></i></span><small>45%</small></div>
                  <div class="gd-proc"><span>Retornos agendados</span><span class="gd-trilho"><i style="--p:90%"></i></span><small>90%</small></div>
                </div>
              </div>
              <ul class="gd-pedidos" aria-hidden="true">{pedidos}</ul>
            </div>
            <figcaption><span class="selo-exemplo">Exemplo ilustrativo com dados fictícios</span></figcaption>
          </figure>"""

FLUXO_IA = [("busca", "Entende o pedido", "2 X-bacon, sexta, entrega ao meio-dia"),
            ("estoque", "Confere o estoque", "Pão, carne e bacon disponíveis"),
            ("agenda", "Agenda a entrega", "Sexta, 12h, na rota do centro"),
            ("conversa", "Responde e avisa a equipe", "Cliente confirmado, cozinha avisada")]
def demo_ia():
    passos = "".join(f'<li class="fluxo-passo" data-passo><span class="fluxo-icone fluxo-n"></span><span><strong>{t}</strong><small>{d}</small></span><span class="fluxo-ok">{I["check"]}</span></li>'
                     for ic, t, d in FLUXO_IA)
    return f"""<figure class="demo-visual">
            <div class="fluxo" data-fluxo role="img" aria-label="Exemplo ilustrativo: chega a mensagem &quot;Quero 2 X-bacon para sexta, com entrega ao meio-dia.&quot; A IA entende o pedido, confere o estoque, agenda a entrega para sexta às 12h e responde o cliente, avisando a cozinha.">
              <div class="fluxo-entrada" aria-hidden="true"><small>Mensagem recebida</small><p>"Quero 2 X-bacon para sexta, com entrega ao meio-dia."</p></div>
              <div class="fluxo-nucleo" aria-hidden="true"><span class="fluxo-orbita"></span><strong>Assistente de IA</strong></div>
              <ol class="fluxo-passos" aria-hidden="true">{passos}</ol>
            </div>
            <figcaption><span class="selo-exemplo">Exemplo ilustrativo</span></figcaption>
          </figure>"""

# ------------------------------------------------------------------ Kyzent 2.0: fotos com AVIF/WebP
def foto(arquivo, w, h, alt="", sizes="(max-width: 760px) 100vw, 50vw", eager=False, pos=""):
    """<picture> com AVIF e WebP (gerados por tools/otimiza_fotos.py) e o JPG como reserva."""
    base = arquivo.rsplit(".", 1)[0]
    grande = min(1200, w)
    def srcset(ext):
        return f"assets/fotos/{base}-640.{ext} 640w, assets/fotos/{base}-{grande}.{ext} {grande}w"
    estilo = f' style="object-position:{pos}"' if pos else ""
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="assets/fotos/{arquivo}" alt="{alt}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async"{estilo}></picture>')




# ------------------------------------------------------------------ Aurora: o rosto da IA de atendimento (assets/img/aurora)
def avatar_aurora(cls=""):
    """A arte inteira da Aurora, só reduzida (sem cortar). Parada, sem efeito."""
    return (f'<span class="aurora-avatar {cls}" aria-hidden="true"><img src="assets/img/aurora/aurora-avatar-96.webp" srcset="assets/img/aurora/aurora-avatar-96.webp 1x, assets/img/aurora/aurora-avatar-256.webp 3x" '
            f'alt="" width="96" height="96" decoding="async"></span>')

AURORA_PERGUNTAS = [
    ("Quem responde os meus clientes: uma pessoa ou a IA?",
     "A Aurora responde o que é rotina com o nome e as informações do seu negócio, e sempre se apresenta como assistente virtual. Quando o cliente precisa de uma pessoa, ela chama a sua equipe."),
    ("Em quais canais a Aurora atende?",
     "No WhatsApp e no Instagram, 24 horas por dia. No WhatsApp usamos a API oficial da Meta, a conexão aprovada pelo próprio WhatsApp."),
]
def aurora_pagina():
    perg = "\n".join(f'          <details class="pergunta"{" open" if k == 0 else ""}><summary><span>{q}</span><span class="pergunta-icone">{I["mais"]}</span></summary><div class="pergunta-resposta"><p>{r}</p></div></details>'
                     for k, (q, r) in enumerate(AURORA_PERGUNTAS))
    return f"""    <section class="pagina-topo aurora-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container aurora-grade">
        <figure class="aurora" data-aurora>
          <div class="aurora-quadro" data-aurora-quadro>
            <picture>
              <source type="image/webp" srcset="assets/img/aurora/aurora-640.webp 640w, assets/img/aurora/aurora.webp 800w" sizes="(max-width: 999px) 86vw, 520px">
              <img src="assets/img/aurora/aurora.webp" alt="Aurora, a coruja mascote da IA de atendimento da Kyzent" width="800" height="800" fetchpriority="high" decoding="async">
            </picture>
          </div>
        </figure>
        <div class="aurora-texto">
          <p class="pilar-rotulo">A IA da Kyzent</p>
          <h1 id="titulo-pagina">Conheça a Aurora, a IA de atendimento da Kyzent.</h1>
          <p>A Aurora trabalha para o seu negócio, com o nome e as informações dele. Ela atende os seus clientes no WhatsApp e no Instagram, 24 horas por dia, e sempre se apresenta como assistente virtual.</p>
          <div class="hero-acoes">
            <a class="botao botao-grande" href="#conversar">Conversar com a Aurora</a>
            <a class="botao botao-grande botao-vidro" href="orcamento.html">Simular meu orçamento</a>
          </div>
        </div>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-aurora-como">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-como" data-revelar-texto>Como funciona.</h2>
        </div>
        <ol class="processo processo-4">
          <li class="processo-passo"><span class="processo-n">1</span><h3>O cliente escreve</h3><p>No WhatsApp ou no Instagram do seu negócio, a qualquer hora do dia.</p></li>
          <li class="processo-passo"><span class="processo-n">2</span><h3>A Aurora responde</h3><p>Com as informações que você passou: horários, preços, serviços e endereço.</p></li>
          <li class="processo-passo"><span class="processo-n">3</span><h3>Resolve o que é rotina</h3><p>Marca o horário, registra o pedido ou tira a dúvida, sem a equipe parar o que está fazendo.</p></li>
          <li class="processo-passo"><span class="processo-n">4</span><h3>Chama uma pessoa</h3><p>Quando o cliente pede ou o assunto foge da rotina, ela chama a sua equipe, que assume a conversa com tudo o que o cliente já disse.</p></li>
        </ol>
      </div>
    </section>

    <section class="secao secao-faixa" aria-labelledby="titulo-aurora-faz">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-faz" data-revelar-texto>O que ela resolve.</h2>
        </div>
        <ul class="aurora-faz">
          <li><strong>Agenda</strong><span>sem você largar o atendimento para marcar horário</span></li>
          <li><strong>Tira dúvidas</strong><span>preço, horário e endereço respondidos na hora, até de madrugada</span></li>
          <li><strong>Registra pedidos</strong><span>que chegam organizados para a equipe</span></li>
          <li><strong>Chama uma pessoa</strong><span>quando o assunto precisa de alguém da equipe</span></li>
        </ul>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-aurora-jeito">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-jeito" data-revelar-texto>Diferenciais da Aurora.</h2>
        </div>
        <ul class="grade grade-4">
          <li class="pilar"><p class="pilar-rotulo">Com o seu nome</p><h3>O cliente conversa com o seu negócio.</h3><p>A Aurora atende com o nome e as informações do seu negócio.</p></li>
          <li class="pilar"><p class="pilar-rotulo">Sem fingir</p><h3>Sempre como assistente virtual.</h3><p>Ela se apresenta como assistente virtual e nunca finge ser uma pessoa.</p></li>
          <li class="pilar"><p class="pilar-rotulo">Com a sua equipe</p><h3>Uma pessoa entra quando precisa.</h3><p>A conversa passa para a equipe sem o cliente repetir tudo.</p></li>
          <li class="pilar"><p class="pilar-rotulo">API oficial</p><h3>WhatsApp pela API oficial da Meta.</h3><p>Conexão aprovada pela Meta, sem atalhos que coloquem o número da sua empresa em risco.</p></li>
        </ul>
      </div>
    </section>

{central_demos(ids=["chatbot"], titulo="Converse com a Aurora.", sec_id="conversar", com_link=False,
               intro="Simulação com dados fictícios. Faça o papel do cliente de uma barbearia de exemplo: marque um horário, pergunte o preço ou peça para falar com uma pessoa.")}

    <section class="secao claro" aria-labelledby="titulo-aurora-perguntas">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-perguntas" data-revelar-texto>Perguntas sobre a Aurora.</h2>
        </div>
        <div class="perguntas">
{perg}
        </div>
      </div>
    </section>

{chamada("aurora")}"""

# ------------------------------------------------------------------ o K da marca em 3D (js/hero-3d.js, modo "marca"); a imagem do logo fica de reserva
def k3d(cls=""):
    return (f'<div class="k3d {cls}" data-k3d aria-hidden="true">'
            '<img class="k3d-reserva" src="assets/img/kyzent-k-escuro.svg" alt="" width="1080" height="520" decoding="async"></div>')

# ------------------------------------------------------------------ soluções (uma página para cada módulo)
# textos comerciais escritos pelo Claude a partir do catálogo oficial; os sócios precisam confirmar
PAGINA_MOD = {"bi": "solucao-bi.html", "whatsapp": "aurora.html", "agenda": "solucao-vendas.html", "gestao": "solucao-gestao.html",
              "site": "solucao-site.html", "ia": "solucao-ia.html"}
SOLUCOES = {
    "whatsapp": ("Atendimento com sistema e com a Aurora",
                 "Um sistema para a sua equipe atender todas as conversas, e a Aurora respondendo a qualquer hora no WhatsApp e no Instagram.",
                 ["Respostas na hora, inclusive à noite e no fim de semana", "Menos mensagens repetidas para a equipe responder", "Pedidos de atendimento humano chegam organizados"],
                 ["Mensagens acumulando no horário de pico", "As mesmas perguntas respondidas o dia inteiro", "Cliente que desiste porque ninguém respondeu"]),
    "agenda": ("Pedidos, agendamento e vendas",
               "Cardápio online com pedidos, agendamento online, clientes lembrados de voltar e orçamentos enviados sem você parar o que está fazendo.",
               ["Agenda organizada, com confirmação e lembrete", "Clientes antigos chamados de volta no momento certo", "Orçamentos e propostas enviados com rapidez"],
               ["Horário marcado em papel ou de cabeça", "Cliente que falta sem avisar", "Oportunidade perdida por falta de retorno"]),
    "gestao": ("Sistemas de gestão sob medida",
               "A Kyzent desenvolve o sistema de gestão do seu negócio (ERP): estoque, financeiro, clientes e relatórios num lugar só, do jeito que você trabalha.",
               ["Você sabe o que tem em estoque sem contar", "O fechamento do dia sai pronto", "Os números do mês num painel"],
               ["Planilhas soltas e anotações perdidas", "Dados digitados duas vezes em sistemas diferentes", "Dificuldade para saber como o mês está indo"]),
    "site": ("Site sob medida para o seu negócio",
             "Um site feito para o seu negócio, com o que os seus clientes procuram e a cara da sua marca.",
             ["Presença profissional na internet", "Serviços, horários e contato num lugar só", "Clientes que encontram o seu negócio e entram em contato"],
             ["Cliente que não encontra o seu negócio na internet", "Informações espalhadas em várias redes", "Perfil que não passa a imagem que o negócio merece"]),
    "bi": ("BI e análise de dados",
           "Painéis e relatórios com os números do seu negócio, atualizados sozinhos, com os dados do sistema de gestão, das vendas e das planilhas num lugar só.",
           ["Você sabe o que mais vende e o que está parado", "Os números do mês sem montar planilha", "Um aviso quando um número sai do normal"],
           ["Cada número num sistema diferente", "Relatório montado à mão no fim do mês", "Decisão de compra e promoção no achismo"]),
    "ia": ("IA sob medida para a sua empresa",
           "Agentes e assistentes de inteligência artificial desenvolvidos para o jeito de trabalhar da sua empresa, integrados aos seus sistemas.",
           ["Tarefas repetitivas feitas por um assistente", "Equipe com apoio para consultar e organizar informações", "Solução desenhada para o seu processo, não um pacote pronto"],
           ["Processos que nenhum sistema pronto resolve", "Equipe sobrecarregada com tarefas manuais", "Informação difícil de encontrar na hora certa"]),
}
MOD = {mid: (nome, curto, ic, resumo, servs) for mid, nome, curto, ic, resumo, servs in MODULOS}
# soluções com página própria (o atendimento é a página da Aurora, no menu)
MOD_PAGINA = [mid for mid in MOD if mid != "whatsapp"]

def msg_modulo(mid):
    return f"Olá, vim pelo site da Kyzent e quero um orçamento de {MOD[mid][0].lower()}."

# ------------------------------------------------------------------ central de demonstrações (simulações)
ROTEIRO = {
    "inicio": {"msg": ["Oi! Eu sou a Aurora, assistente virtual da Barbearia Exemplo.", "Como posso ajudar?"],
               "op": [["Agendar um horário", "agendar"], ["Ver os preços", "precos"], ["Falar com uma pessoa", "humano"]]},
    "agendar": {"msg": ["Claro! Para quando você quer marcar?"], "op": [["Hoje", "hoje"], ["Amanhã", "amanha"]]},
    "hoje": {"msg": ["Hoje ainda temos 16h30 e 18h. Qual prefere?"], "op": [["16h30", "h1"], ["18h", "h2"]]},
    "amanha": {"msg": ["Amanhã temos 10h e 14h. Qual prefere?"], "op": [["10h", "h3"], ["14h", "h4"]]},
    "h1": {"msg": ["Pronto! Seu horário está marcado: hoje às 16h30.", "Vou te lembrar 1 hora antes. Até lá!"], "ok": "Agendamento confirmado: hoje, 16h30", "op": [["Começar de novo", "inicio"]]},
    "h2": {"msg": ["Pronto! Seu horário está marcado: hoje às 18h.", "Vou te lembrar 1 hora antes. Até lá!"], "ok": "Agendamento confirmado: hoje, 18h", "op": [["Começar de novo", "inicio"]]},
    "h3": {"msg": ["Pronto! Seu horário está marcado: amanhã às 10h.", "Vou te lembrar 1 hora antes. Até lá!"], "ok": "Agendamento confirmado: amanhã, 10h", "op": [["Começar de novo", "inicio"]]},
    "h4": {"msg": ["Pronto! Seu horário está marcado: amanhã às 14h.", "Vou te lembrar 1 hora antes. Até lá!"], "ok": "Agendamento confirmado: amanhã, 14h", "op": [["Começar de novo", "inicio"]]},
    "precos": {"msg": ["Estes são os valores:", "Corte: R$ 40,00<br>Barba: R$ 30,00<br>Corte e barba: R$ 60,00"], "op": [["Agendar um horário", "agendar"], ["Começar de novo", "inicio"]]},
    "humano": {"msg": ["Certo! Avisei a equipe e alguém responde por aqui em instantes.", "Enquanto isso, posso ajudar com mais alguma coisa?"], "ok": "Conversa encaminhada para a equipe", "op": [["Agendar um horário", "agendar"], ["Começar de novo", "inicio"]]},
}

def tela_chatbot():
    roteiro = escape(json.dumps(ROTEIRO, ensure_ascii=False))
    return f"""<div class="chat chat-interativo" data-chatbot data-roteiro="{roteiro}">
              <div class="chat-topo">{avatar_aurora("chat-avatar")}<span class="chat-nome"><strong>Aurora</strong><small>Assistente virtual · <span data-chat-estado>online</span></small></span></div>
              <div class="chat-corpo" data-chat-corpo aria-live="polite"><p class="demo-sem-js">Ative o JavaScript para conversar com a Aurora.</p></div>
              <div class="chat-opcoes" data-chat-opcoes role="group" aria-label="Respostas"></div>
            </div>"""

def tela_agendamento():
    return f"""<div class="ag" data-agendamento>
              <div class="ag-topo"><strong>Agenda do Salão Exemplo</strong><span>Escolha o dia e o horário</span></div>
              <div class="ag-corpo">
                <div class="ag-servicos" role="group" aria-label="Serviço">
                  <button type="button" class="ag-chip" data-ag-servico="Escova" aria-pressed="true">Escova</button>
                  <button type="button" class="ag-chip" data-ag-servico="Corte" aria-pressed="false">Corte</button>
                  <button type="button" class="ag-chip" data-ag-servico="Manicure" aria-pressed="false">Manicure</button>
                </div>
                <div class="ag-dias" data-ag-dias role="group" aria-label="Dia"></div>
                <div class="ag-horas" data-ag-horas role="group" aria-label="Horário"></div>
                <button type="button" class="botao ag-confirmar" data-ag-confirmar disabled>Confirmar agendamento</button>
                <p class="ag-aviso" data-ag-aviso role="status" hidden></p>
              </div>
              <div class="ag-lista-caixa"><p>Agenda de hoje</p><ul class="ag-lista" data-ag-lista>
                <li><time>09:00</time><span><strong>Fernanda</strong><small>Escova</small></span><em class="estado estado-ok">Confirmado</em></li>
                <li><time>11:00</time><span><strong>Camila</strong><small>Manicure</small></span><em class="estado estado-ok">Confirmado</em></li>
              </ul></div>
            </div>"""

def tela_estoque():
    lis = "".join(
        f'<li class="est-item" data-est-item="{n}" data-min="{mn}"><span class="est-nome"><strong>{n}</strong><small>Mínimo: {mn}</small></span>'
        f'<span class="est-qtd"><output data-est-qtd>{q}</output><small>em estoque</small></span>'
        f'<span class="est-acoes"><span class="est-aviso" data-est-aviso{"" if q <= mn else " hidden"}>Acabando</span>'
        f'<button type="button" class="est-vender" data-est-vender>Registrar venda</button>'
        f'<button type="button" class="est-repor" data-est-repor{"" if q <= mn else " hidden"}>Fazer pedido ao fornecedor</button></span></li>'
        for n, q, mn in ESTOQUE_DEMO)
    return f"""<div class="est" data-estoque>
              <p class="pd-titulo">Estoque da Lanchonete Exemplo</p>
              <ul class="est-lista">{lis}</ul>
              <p class="est-status" data-est-status role="status">Registre uma venda: o estoque baixa, e a venda entra em Pedidos e no Painel.</p>
            </div>"""

def tela_pedidos():
    itens = "".join(
        f'<li data-produto="{n}" data-preco="{p}"><span><strong>{n}</strong><small>R$ {p},00</small></span>'
        f'<span class="pd-qtd"><button type="button" data-menos aria-label="Tirar um {n}">−</button><output data-qtd>0</output>'
        f'<button type="button" data-mais aria-label="Pôr mais um {n}">+</button></span></li>' for n, p in CARDAPIO)
    fila = "".join(f'<li><span class="pd-num">{n}</span><span><strong>{q}</strong><small>{o}</small></span><em class="estado estado-{c}">{e}</em></li>'
                   for n, q, o, c, e in PEDIDOS_DEMO)
    return f"""<div class="pd" data-pedidos data-proximo="{PROXIMO_PEDIDO}">
              <div class="pd-cardapio"><p class="pd-titulo">Cardápio da Lanchonete Exemplo</p><ul>{itens}</ul>
                <div class="pd-total"><span>Total</span><strong data-pd-total>R$ 0,00</strong></div>
                <button type="button" class="botao" data-pd-registrar disabled>Registrar pedido</button></div>
              <div class="pd-fila"><p class="pd-titulo">Pedidos de hoje</p><ul data-pd-lista aria-live="polite">{fila}</ul></div>
            </div>"""

ROTULO_CLIENTE = {"recorrente": "Recorrente", "novo": "Novo", "inativo": "Inativo"}
def tela_clientes():
    lis = "".join(
        f'<li data-tipo="{t}" data-nome="{n.lower()}"><span class="cl-avatar">{"".join(p[0] for p in n.split()[:2])}</span>'
        f'<span class="cl-info"><strong>{n}</strong><small>{d}</small></span><em class="cl-tag cl-{t}">{ROTULO_CLIENTE[t]}</em>'
        + (f'<button type="button" class="cl-lembrar" data-lembrar>Enviar lembrete</button>' if t == "inativo" else "") + "</li>"
        for n, t, d in CLIENTES)
    return f"""<div class="cl" data-clientes>
              <div class="cl-topo"><label class="cl-busca">{I["busca"]}<span class="visualmente-oculto">Buscar cliente</span><input type="search" placeholder="Buscar cliente" data-cl-busca autocomplete="off"></label>
                <div class="cl-filtros" role="group" aria-label="Filtrar clientes">
                  <button type="button" data-cl-filtro="todos" aria-pressed="true">Todos</button><button type="button" data-cl-filtro="recorrente" aria-pressed="false">Recorrentes</button><button type="button" data-cl-filtro="novo" aria-pressed="false">Novos</button><button type="button" data-cl-filtro="inativo" aria-pressed="false">Inativos</button>
                </div></div>
              <ul class="cl-lista" data-cl-lista>{lis}</ul>
              <p class="cl-rodape" data-cl-conta aria-live="polite">8 clientes</p>
            </div>"""

ABAS_DEMO = [
    ("painel", "Painel", "grafico", "Painel administrativo", "Pedidos, processos e indicadores reunidos num painel que se atualiza sozinho. Registre uma venda em Estoque ou em Pedidos e veja o número mudar aqui.", "gestao", demo_gestao),
    ("estoque", "Estoque", "estoque", "Controle de estoque", "Registre uma venda e veja o estoque baixar. Quando um produto passa do mínimo, o sistema avisa e sugere o pedido ao fornecedor.", "gestao", tela_estoque),
    ("pedidos", "Pedidos", "lanche", "Registro de pedidos", "Monte um pedido no cardápio e registre. Ele entra na fila da cozinha com o total calculado.", "gestao", tela_pedidos),
    ("clientes", "Clientes", "olho", "Organização de clientes", "Busque, filtre e envie um lembrete para quem não aparece há algum tempo.", "agenda", tela_clientes),
    ("agendamento", "Agendamento", "agenda", "Agendamento online", "Escolha o serviço, o dia e o horário. O agendamento entra na agenda e o lembrete fica programado.", "agenda", tela_agendamento),
    ("chatbot", "Aurora", "conversa", "Atendimento com a Aurora", "Escolha as respostas e veja a Aurora conduzir a conversa: agendar, informar preços ou passar para uma pessoa da equipe.", "whatsapp", tela_chatbot),
    ("automacao", "Automação", "avancado", "Automação de processos", "A IA entende o pedido, consulta os sistemas, organiza a tarefa e avisa quem precisa saber.", "ia", demo_ia),
]
VERSAO_COMPLETA = {"pedidos": DEMO_CARDAPIO, "agendamento": DEMO_AGENDAMENTO}
def versao_completa(did):
    if did not in VERSAO_COMPLETA: return ""
    return (f'<a class="link-seta demo-completa-link" href="{VERSAO_COMPLETA[did]}" target="_blank" rel="noopener">Ver a versão completa'
            f'<span class="visualmente-oculto"> (abre em nova aba)</span></a>')
def central_demos(ids=None, titulo="Veja a Kyzent funcionando.", classe="", sec_id="demonstracoes", intro=None, rodape="", com_link=True):
    abas_ = [a for a in ABAS_DEMO if ids is None or a[0] in ids]
    botoes, paineis_ = [], []
    for i, (did, curto, ic, titulo_aba, texto, mod, tela) in enumerate(abas_):
        sel = i == 0
        botoes.append(f'<button type="button" class="demo-aba" role="tab" id="daba-{did}" aria-controls="dpainel-{did}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}"><span>{curto}</span></button>')
        paineis_.append(f"""          <div class="demo-painel" id="dpainel-{did}" role="tabpanel" aria-labelledby="daba-{did}"{"" if sel else " hidden"}>
            <div class="demo-info">
              <span class="selo-exemplo">Simulação demonstrativa</span>
              <h3>{titulo_aba}</h3>
              <p>{texto}</p>
              {f'<a class="link-seta" href="{PAGINA_MOD[mod]}">Conhecer solução</a>' if com_link else ""}
              {versao_completa(did)}
            </div>
            <div class="demo-tela">{tela()}</div>
          </div>""")
    abas_html = "" if len(abas_) == 1 else f'<div class="demo-abas" role="tablist" aria-label="Demonstrações">{"".join(botoes)}</div>'
    intro = intro or "Simulações demonstrativas, com dados fictícios. Toque, escolha e veja o que acontece."
    return f"""    <section class="secao secao-demos {classe}" id="{sec_id}" aria-labelledby="titulo-{sec_id}">
      <div class="container">
        <div class="cabeca cabeca-centro">
          <h2 id="titulo-{sec_id}" data-revelar-texto>{titulo}</h2>
          <p>{intro}</p>
        </div>
        <div class="demo-centro" data-demo-centro>
          {abas_html}
          {'<p class="demo-dica">Deslize para o lado para ver a próxima demonstração.</p>' if len(abas_) > 1 else ''}
{chr(10).join(paineis_)}
        </div>
        {rodape}
      </div>
    </section>"""

# ------------------------------------------------------------------ segmentos (texto do Claude, a confirmar)
SEGMENTOS = [
    ("lanchonete", "Restaurantes e lanchonetes", "lanche", "lanchonete.jpg", (1200, 675), "um restaurante ou lanchonete",
     ["Pedidos chegando por mensagem no horário de pico", "Cardápio, horário e taxa de entrega perguntados o dia todo", "Anotação em papel que se perde"],
     ["Cardápio online com combos e adicionais", "Baixa de insumos: pão, carne e bebida", "Caixa do delivery e do balcão juntos", "A Aurora informando horário e taxa de entrega"],
     ["Caixa livre para atender quem está no balcão", "Pedidos organizados do recebimento à entrega", "Cliente respondido mesmo fora do horário"]),
    ("barbearia", "Barbearias", "tesoura", "barbearia.jpg", (880, 1100), "uma barbearia",
     ["Responder mensagem no meio de um corte", "Horários vagos por falta de lembrete", "Cliente que demora a voltar"],
     ["Agenda por barbeiro", "Ficha de cada cliente com o corte de sempre", "Caixa do dia com os serviços feitos", "Lembrete quando passa da hora de voltar"],
     ["Agenda mais organizada", "Menos interrupções durante o atendimento", "Relacionamento contínuo com cada cliente"]),
    ("salao", "Salões de beleza", "pente", "salao.jpg", (734, 1100), "um salão de beleza",
     ["Agenda de várias profissionais ao mesmo tempo", "Dúvidas sobre preço e duração de cada serviço", "Orçamentos de pacotes e eventos"],
     ["Agenda por profissional e por serviço", "Ficha da cliente com o histórico de serviços", "Caixa do dia do salão", "Preço e duração de cada serviço respondidos na hora"],
     ["Menos conflito de horário", "Clientes bem informadas antes de chegar", "Mais tempo da equipe para o atendimento"]),
    ("consultorio", "Clínicas", "cruz", "consultorio.jpg", (1200, 800), "uma clínica",
     ["Recepção sobrecarregada com ligações e mensagens", "Pacientes que esquecem a consulta", "Orientações enviadas uma a uma"],
     ["Agenda de consultas e retornos", "Cadastro de pacientes com contato e consultas anteriores", "Recebimentos do dia", "Lembrete na véspera da consulta"],
     ["Recepção mais leve", "Agenda confirmada com antecedência", "Dados dos pacientes tratados com cuidado (LGPD)"]),
    ("petshop", "Pet shops", "pata", "petshop.jpg", (1200, 900), "um pet shop",
     ["Banho e tosa marcados por mensagem solta", "Tutores que esquecem vacina e vermífugo", "Pedidos de ração perdidos na conversa"],
     ["Agenda de banho, tosa e consulta", "Ficha de cada pet com o tutor", "Estoque de ração e acessórios", "Lembrete de vacina e do próximo banho"],
     ["Agenda sem choque de horário", "Tutores lembrados no momento certo", "Histórico de cada pet num lugar só"]),
    ("empresa", "Pequenas e médias empresas", "gestao", "equipe-computador.jpg", (1600, 900), "uma empresa",
     ["Processos manuais repetidos todos os dias", "Informações espalhadas em planilhas e sistemas", "Atendimento que não acompanha o crescimento"],
     ["Os módulos que a empresa usa, num sistema só", "Estoque e compras", "Contas a pagar e a receber", "Painel com os números do mês"],
     ["Equipe focada no que exige pessoas", "Informações conectadas para decidir melhor", "Tecnologia que acompanha o crescimento da empresa"]),
]
SEG_FRASE = {'lanchonete': 'Do pedido ao caixa fechado, sem anotação perdida.', 'barbearia': 'Agenda cheia, sem largar a máquina.', 'salao': 'Cada profissional com a sua agenda em ordem.', 'consultorio': 'Recepção mais leve e pacientes lembrados.', 'petshop': 'Banho, tosa e vacina sempre no dia certo.', 'empresa': 'Um sistema feito para a empresa crescer.'}
# ------------------------------------------------------------------ metodologia, diferenciais e projetos
# Projetos reais entram aqui, com a autorização de cada cliente: (nome, segmento, o que foi feito, foto ou "")
PROJETOS = []
# ------------------------------------------------------------------ Orçamento: simulador e contato
# o que a pessoa precisa -> serviços recomendados
NECESSIDADES = [
    ("sistema", "Sistema de gestão (estoque, caixa, clientes)", ["Sistema de gestão sob medida (ERP)", "Controle de estoque", "Financeiro e fluxo de caixa", "Relatórios e painel de indicadores"]),
    ("cardapio", "Cardápio online e pedidos", ["Cardápio online com pedidos", "Gestão de cadastros e pedidos"]),
    ("agendamento", "Agendamento online", ["Agendamento online", "Follow-up inteligente"]),
    ("aurora", "Atendimento com IA (Aurora)", ["Chatbots inteligentes", "Respostas inteligentes", "Sistema de atendimento"]),
    ("site", "Site", ["Site personalizado"]),
    ("outro", "Outra coisa", ["Sistemas personalizados"]),
]
SERV_MOD = {a: (mid, PAGINA_MOD[mid], MOD[mid][0]) for mid in MOD for a in MOD[mid][4]}
def opcao(tipo, nome, valor, texto, icone=""):
    return (f'<label class="sim-opcao"><input type="{tipo}" name="{nome}" value="{valor}">'
            f'<span class="sim-opcao-caixa"><span>{texto}</span><span class="sim-marca">{I["check"]}</span></span></label>')

SIM_NEGOCIOS = [(s[0], s[1], s[2]) for s in SEGMENTOS] + [("outro", "Outro tipo de negócio", "site")]
SIM_ETAPAS = ["O que precisa", "Seu negócio", "Tamanho", "Contato"]
ORCAMENTO = f"""    <section class="pagina-topo orc-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Monte o seu projeto.</h1>
          <p class="pagina-topo-apoio">Responda quatro perguntas rápidas e receba uma recomendação de solução. No fim, você envia para a Kyzent pelo WhatsApp ou por e-mail, sem compromisso.</p>
          <p class="topo-alternativa">Prefere conversar direto? <a href="{link_whats()}" target="_blank" rel="noopener" data-contato>Chame no WhatsApp</a>.</p>
        </div>
        {k3d("k3d-topo")}
      </div>
    </section>

    <section class="secao claro" id="simulador" aria-labelledby="titulo-simulador">
      <div class="container">
        <h2 id="titulo-simulador" class="visualmente-oculto">Simulador de orçamento</h2>
        <noscript><p class="sim-sem-js">O simulador precisa de JavaScript. Você pode chamar a Kyzent direto no WhatsApp: {WHATS[0][1]} ou {WHATS[1][1]}.</p></noscript>
        <div class="simulador-grade">
          <form class="simulador" data-simulador novalidate data-mapa="{escape(json.dumps({k: v for k, _, v in NECESSIDADES}, ensure_ascii=False))}" data-servmod="{escape(json.dumps(SERV_MOD, ensure_ascii=False))}" data-email="{EMAIL}">
            <div class="sim-progresso" aria-hidden="true"><span data-sim-barra></span></div>
            <p class="sim-num" data-sim-num data-etapas="{escape(json.dumps(SIM_ETAPAS, ensure_ascii=False))}" aria-live="polite">Passo 1 de 4 · {SIM_ETAPAS[0]}</p>
            <fieldset class="sim-passo" data-passo="1">
              <legend>O que você precisa?</legend>
              <p class="sim-dica">Marque quantas quiser.</p>
              <div class="sim-opcoes sim-opcoes-2">{"".join(opcao("checkbox", "necessidade", k, t) for k, t, _ in NECESSIDADES)}</div>
              <label class="sim-outro" data-sim-outra-necessidade hidden>O que você precisa?<input name="necessidade_outra" maxlength="80" autocomplete="off" placeholder="Ex.: controle de ordens de serviço"></label>
            </fieldset>
            <fieldset class="sim-passo" data-passo="2" hidden>
              <legend>Qual é o seu tipo de negócio?</legend>
              <div class="sim-opcoes sim-opcoes-2">{"".join(opcao("radio", "negocio", sid, nome, ic) for sid, nome, ic in SIM_NEGOCIOS)}</div>
              <label class="sim-outro" data-sim-outro hidden>Qual é o seu negócio?<input name="negocio_outro" maxlength="60" autocomplete="off" placeholder="Ex.: academia, oficina, loja de roupas"></label>
            </fieldset>
            <fieldset class="sim-passo" data-passo="3" hidden>
              <legend>Quantas pessoas trabalham no negócio?</legend>
              <div class="sim-opcoes sim-opcoes-4">{"".join(opcao("radio", "equipe", v, v) for v in ("Só eu", "De 2 a 5", "De 6 a 20", "Mais de 20"))}</div>
              <p class="sim-subtitulo" id="sim-quando">Quando quer começar? <span class="sim-opcional">(opcional)</span></p>
              <div class="sim-opcoes sim-opcoes-3" role="radiogroup" aria-labelledby="sim-quando">{"".join(opcao("radio", "quando", v, v) for v in ("O quanto antes", "Nos próximos meses", "Só estou pesquisando"))}</div>
            </fieldset>
            <fieldset class="sim-passo" data-passo="4" hidden>
              <legend>Para a gente falar com você</legend>
              <div class="sim-campos">
                <label>Seu nome <span class="sim-obrigatorio">(obrigatório)</span><input name="nome" autocomplete="name" maxlength="60" required></label>
                <label>Nome da empresa <span>(opcional)</span><input name="empresa" autocomplete="organization" maxlength="80"></label>
                <fieldset class="sim-canal sim-campo-largo">
                  <legend>Como prefere receber o retorno?</legend>
                  <label><input type="radio" name="canal_retorno" value="whatsapp" checked> WhatsApp</label>
                  <label><input type="radio" name="canal_retorno" value="email"> E-mail</label>
                </fieldset>
                <label class="sim-campo-largo" data-sim-email hidden>Seu e-mail <span class="sim-obrigatorio">(obrigatório)</span><input name="email" type="email" autocomplete="email" maxlength="80"></label>
                <label class="sim-campo-largo">Observação <span>(opcional)</span><textarea name="obs" rows="3" maxlength="400" placeholder="Ex.: hoje controlo o estoque numa planilha"></textarea></label>
                <div class="sim-mel" aria-hidden="true"><label>Não preencha este campo<input name="site" tabindex="-1" autocomplete="off"></label></div>
              </div>
              <p class="sim-dica">Seus dados vão só na mensagem que você mesmo envia. O site não guarda nada em servidor.</p>
              <label class="sim-consentimento"><input type="checkbox" name="privacidade" required> <span>Li e concordo com a <a href="privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</span></label>
            </fieldset>
            <p class="sim-erro" role="alert" data-sim-erro hidden></p>
            <div class="sim-nav">
              <button type="button" class="botao botao-contorno" data-sim-voltar hidden>Voltar</button>
              <button type="button" class="botao" data-sim-avancar>Continuar</button>
              <button type="submit" class="botao" data-sim-enviar hidden>Ver minha recomendação</button>
            </div>
          </form>
          <aside class="sim-resultado" data-sim-resultado aria-live="polite" aria-label="Recomendação">
            <div class="sim-vazio">
              
              <h3>A sua recomendação aparece aqui.</h3>
              <p>Com base nas respostas, mostramos as soluções que mais combinam com o seu negócio e montamos a mensagem para você enviar pelo WhatsApp ou por e-mail.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section class="secao" id="contato" aria-labelledby="titulo-contato">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-contato" data-revelar-texto>Fale com a Kyzent.</h2>
          <p>As soluções funcionam pela internet. Tudo começa por uma conversa, pelo WhatsApp ou por e-mail.</p>
        </div>
        <ul class="grade contatos">
          <li class="contato-cartao brilho"><h3>WhatsApp</h3>
            <p><a href="{link_whats(None, 0)}" target="_blank" rel="noopener">{WHATS[0][1]}</a><br><a href="{link_whats(None, 1)}" target="_blank" rel="noopener">{WHATS[1][1]}</a></p>
            <a class="botao" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a></li>
          <li class="contato-cartao brilho"><h3>Instagram</h3>
            <p>Novidades, exemplos e bastidores da Kyzent.</p>
            <a class="botao botao-contorno" href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">@kyzent.tech</a></li>
        </ul>
      </div>
    </section>"""


# =====================================================================================
# KYZENT 3 (2026-11-12): sem ícones genéricos como linguagem visual, sem repetições,
# uma chamada final por página e um visual próprio para cada solução.
# =====================================================================================
AVISO_RESULTADOS = "Os resultados dependem de cada negócio e do que for automatizado."
MSG_CONVERSA = "Olá, vim pelo site da Kyzent e quero conversar sobre automação para o meu negócio."

# ---------- ilustrações próprias de cada solução (SVG, sem biblioteca de ícones)
def ilustra(mid, cls="ilu"):
    d = {
        "bi": '''<circle class="ilu-c" cx="30" cy="40" r="22"/><path class="ilu-b" d="M30 40 L30 18 A22 22 0 0 1 50.9 46.8 Z"/>
          <rect class="ilu-a" x="60" y="44" width="8" height="20" rx="2"/><rect class="ilu-a" x="72" y="34" width="8" height="30" rx="2"/>
          <rect class="ilu-b ilu-pisca" x="84" y="22" width="8" height="42" rx="2"/>''',
        "whatsapp": '''<rect class="ilu-a" x="8" y="14" width="58" height="34" rx="12"/><path class="ilu-a" d="M18 48l-6 10 16-10z"/>
          <rect class="ilu-b" x="40" y="34" width="52" height="30" rx="11"/><path class="ilu-b" d="M84 64l6 8-14-8z"/>
          <circle class="ilu-p p1" cx="26" cy="31" r="3.4"/><circle class="ilu-p p2" cx="37" cy="31" r="3.4"/><circle class="ilu-p p3" cx="48" cy="31" r="3.4"/>
          <rect class="ilu-l" x="50" y="44" width="30" height="3.5" rx="1.75"/><rect class="ilu-l" x="50" y="52" width="20" height="3.5" rx="1.75"/>''',
        "agenda": "".join(f'<rect class="{"ilu-b ilu-pisca" if (c, r) in ((1, 1), (3, 2)) else ("ilu-a" if (c + r) % 3 else "ilu-c")}" x="{8 + c * 21}" y="{10 + r * 18}" width="16" height="13" rx="4" style="--d:{(c + r) * .15}s"/>'
                      for c in range(4) for r in range(4)),
        "gestao": '''<rect class="ilu-c" x="10" y="44" width="12" height="22" rx="3"/><rect class="ilu-c" x="28" y="34" width="12" height="32" rx="3"/>
          <rect class="ilu-c" x="46" y="40" width="12" height="26" rx="3"/><rect class="ilu-a" x="64" y="22" width="12" height="44" rx="3"/>
          <path class="ilu-linha" d="M12 36 L34 24 L52 30 L72 12 L90 16"/><circle class="ilu-b" cx="72" cy="12" r="5"/>''',
        "site": '''<rect class="ilu-c" x="6" y="8" width="84" height="58" rx="8"/><rect class="ilu-a" x="6" y="8" width="84" height="12" rx="8"/>
          <rect class="ilu-b ilu-sobe" x="14" y="28" width="38" height="8" rx="3"/><rect class="ilu-l ilu-sobe" x="14" y="40" width="26" height="4" rx="2" style="--d:.2s"/>
          <rect class="ilu-a ilu-sobe" x="58" y="28" width="24" height="28" rx="5" style="--d:.35s"/><rect class="ilu-b ilu-sobe" x="14" y="50" width="20" height="8" rx="4" style="--d:.5s"/>''',
        "ia": '''<path class="ilu-linha" d="M18 20 L48 38 L82 16 M48 38 L22 62 M48 38 L80 60 M48 38 L50 70"/>
          <circle class="ilu-c" cx="18" cy="20" r="6"/><circle class="ilu-c" cx="82" cy="16" r="6"/><circle class="ilu-c" cx="22" cy="62" r="6"/>
          <circle class="ilu-c" cx="80" cy="60" r="6"/><circle class="ilu-c" cx="50" cy="70" r="5"/>
          <circle class="ilu-anel" cx="48" cy="38" r="15"/><circle class="ilu-b" cx="48" cy="38" r="9"/>''',
    }[mid]
    return f'<svg class="{cls} ilu-{mid}" viewBox="0 0 96 76" aria-hidden="true" focusable="false">{d}</svg>'

# ---------- chamada final: uma frase por página
CHAMADAS = {
    "aurora": ("Coloque a Aurora para atender o seu negócio.", "Conte como é o seu atendimento hoje e receba uma recomendação de solução."),
    "index.html": ("Vamos transformar a maneira como sua empresa trabalha?", "Conte como é o seu dia a dia e receba uma recomendação de solução para o seu negócio."),
    "servicos.html": ("Não sabe por onde começar?", "Responda quatro perguntas rápidas e receba a recomendação certa para o seu negócio."),
    "whatsapp": ("Seu atendimento pode trabalhar de forma mais inteligente.", "Mostre como é o atendimento hoje e veja o que a IA pode assumir."),
    "agenda": ("Organize seus horários e aproveite melhor cada oportunidade.", "Agenda, lembretes, retorno de clientes e orçamentos no automático."),
    "gestao": ("Tenha mais controle sobre o que acontece no seu negócio.", "A Kyzent desenvolve o sistema do seu negócio, com só as partes que você precisa."),
    "site": ("Sua empresa merece uma presença digital à altura do seu negócio.", "Um site feito para o seu negócio, com o caminho direto para a conversa."),
    "bi": ("Decida com os números do seu negócio na mão.", "Conte quais números você acompanha hoje e veja como eles podem chegar prontos."),
    "ia": ("Descubra o que a inteligência artificial pode fazer pela sua empresa.", "Conte o processo que mais toma tempo e veja como uma IA sob medida pode ajudar."),
}
def chamada(chave="index.html"):
    titulo, texto = CHAMADAS[chave]
    return f"""    <section class="chamada" aria-labelledby="titulo-chamada">
      <div class="container">
        <div class="chamada-caixa revelar-bloco">
          <svg class="chamada-orbita" viewBox="0 0 800 400" aria-hidden="true"><ellipse cx="400" cy="200" rx="380" ry="110" transform="rotate(-24 400 200)"/><ellipse cx="400" cy="200" rx="300" ry="80" transform="rotate(-24 400 200)"/></svg>
          <div class="chamada-texto">
            <h2 id="titulo-chamada" data-revelar-texto>{titulo}</h2>
            <p>{texto}</p>
          </div>
          <div class="chamada-acoes">
            <a class="botao botao-grande botao-claro" href="orcamento.html" data-magnetico>Simular meu orçamento</a>
            <a class="link-seta" href="{link_whats(MSG_CONVERSA)}" target="_blank" rel="noopener" data-contato data-msg="{MSG_CONVERSA}">Conversar no WhatsApp</a>
          </div>
        </div>
      </div>
    </section>"""

# ---------- etapas com número (é uma sequência), sem ícone
ETAPAS = [
    ("Diagnóstico", "Entendemos as necessidades do negócio: como você atende, vende e organiza o dia."),
    ("Planejamento", "Identificamos oportunidades de melhoria e definimos o que vale automatizar primeiro."),
    ("Desenvolvimento", "Construímos soluções adequadas ao seu negócio, com o seu jeito de atender."),
    ("Implementação", "Colocamos as soluções em funcionamento, junto com a sua equipe."),
    ("Suporte e evolução", "Acompanhamos os resultados, fazemos a manutenção e evoluímos as soluções."),
]
def como_trabalhamos(faixa=True):
    passos = "\n".join(
        f'          <li class="etapa"><span class="etapa-marca"><span class="etapa-icone etapa-numero">{i+1}</span></span>'
        f'<div class="etapa-cartao"><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d) in enumerate(ETAPAS))
    return f"""    <section class="secao{' secao-faixa' if faixa else ''}" id="como-trabalhamos" aria-labelledby="titulo-etapas">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-etapas" data-revelar-texto>Como trabalhamos.</h2>
          <p>Do primeiro contato ao suporte, cada etapa é feita junto com você.</p>
        </div>
        <ol class="etapas" data-linha-tempo>
{passos}
        </ol>
      </div>
    </section>"""

# ---------- missão, visão e valores: cartões tipográficos
PILARES = """    <section class="secao claro" aria-labelledby="titulo-pilares">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-pilares" data-revelar-texto>Missão, visão e valores.</h2>
        </div>
        <div class="grade grade-3 mvv">
          <article class="pilar brilho"><p class="pilar-rotulo">Missão</p>
            <p>Oferecer soluções tecnológicas que promovam produtividade, automação e crescimento, otimizando processos e potencializando os resultados dos nossos clientes.</p></article>
          <article class="pilar brilho"><p class="pilar-rotulo">Visão</p>
            <p>Ser referência em Tecnologia e Inovação, reconhecida por transformar negócios e contribuir para a evolução do mercado.</p></article>
          <article class="pilar brilho"><p class="pilar-rotulo">Valores</p>
            <p>Atuar com respeito, ética e compromisso com nossos clientes e colaboradores, construindo relações sólidas e duradouras, pautadas na lealdade, transparência e dignidade.</p></article>
        </div>
      </div>
    </section>"""

# ---------- diferenciais (só em Quem somos), cartões tipográficos
DIFERENCIAIS = [
    ("Sob medida", "Feito para o seu negócio", "Cada sistema é desenvolvido com os seus produtos, preços, processos e jeito de trabalhar."),
    ("Teste antes", "Demonstrações abertas", "O cardápio online e o agendamento online estão no ar para você testar antes de conversar com a gente."),
    ("Suporte", "Manutenção e suporte", "A nossa equipe acompanha cada solução depois de pronta, para a tecnologia seguir funcionando."),
    ("Mensalidade", "Sem contratar mais gente", "Você assina um serviço que trabalha junto com a sua equipe, em vez de aumentar a folha."),
]
def por_que_kyzent():
    """Início: os 4 diferenciais, título fixo à esquerda e 4 cartões numerados à direita (a versão completa fica em Quem somos)."""
    icones = {"Sob medida": "medida", "Teste antes": "olho", "Suporte": "suporte", "Mensalidade": "repetir"}
    acao = {"Teste antes": '<a class="pq-acao" href="#testar">Testar agora</a>'}
    itens = "".join(f'<li class="pq-item brilho"><span class="pq-n" aria-hidden="true">0{n + 1}</span><span class="pq-icone">{I[icones[k]]}</span>'
                    f'<h3>{t}</h3><p>{d}</p>{acao.get(k, "")}</li>' for n, (k, t, d) in enumerate(DIFERENCIAIS))
    return f"""    <section class="secao secao-faixa porque" aria-labelledby="titulo-porque">
      <div class="porque-luz" aria-hidden="true"></div>
      <div class="container pq-grade">
        <div class="pq-cabeca">
          <h2 id="titulo-porque" data-revelar-texto>Por que a Kyzent.</h2>
          <p>Tecnologia feita para o seu negócio, que você testa antes e que a gente acompanha depois.</p>
          <a class="link-seta" href="quem-somos.html">Conhecer a Kyzent</a>
        </div>
        <ul class="pq-lista">{itens}</ul>
      </div>
    </section>"""

def diferenciais(classe=""):
    cards = "\n".join(f'          <li class="diferencial brilho"><p class="dif-palavra">{k}</p><h3>{t}</h3><p>{d}</p></li>' for k, t, d in DIFERENCIAIS)
    return f"""    <section class="secao {classe}" id="diferenciais" aria-labelledby="titulo-diferenciais">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-diferenciais" data-revelar-texto>Por que a Kyzent.</h2>
          <p>Tecnologia séria, explicada de forma simples e acompanhada de perto.</p>
        </div>
        <ul class="grade grade-4 diferenciais">
{cards}
        </ul>
      </div>
    </section>"""

# ---------- cartões das soluções (Início e Soluções), com ilustração própria
def cartao_solucao(mid, destaque=False):
    nome, curto, ic, resumo, servs = MOD[mid]
    titulo, chamada_txt, benef, _ = SOLUCOES[mid]
    lis = "".join(f"<li>{b}</li>" for b in benef)
    selo = '<span class="plano-selo">Porta de entrada</span>' if destaque else ""
    aurora = ""
    return (f'<li><a class="solucao brilho{" solucao-destaque" if destaque else ""}" href="{PAGINA_MOD[mid]}">{selo}'
            f'{ilustra(mid)}<h3>{titulo}</h3><p>{chamada_txt}</p><ul class="frente-itens">{lis}</ul>{aurora}'
            f'<span class="solucao-rodape"><span class="solucao-qtd">{len(servs)} {"serviço" if len(servs) == 1 else "serviços"}</span>'
            f'<span class="solucao-ir">Conhecer solução</span></span></a></li>')

DEMOS_COMPLETAS = [
    ("cardapio", "Cardápio online com pedidos", DEMO_CARDAPIO, "Pizzaria Exemplo",
     "Tela do cardápio online da Pizzaria Exemplo no celular, com o combo em promoção, as categorias e o botão do carrinho",
     ["Combos, tamanhos e adicionais em cada item", "Carrinho com o total e pagamento em Pix, cartão ou dinheiro",
      "Pedido enviado direto para o restaurante e uma tela para acompanhar"],
     "Para pizzarias, lanchonetes e restaurantes"),
    ("agendamento", "Agendamento online", DEMO_AGENDAMENTO, "Pet Shop Exemplo",
     "Tela do agendamento online do Pet Shop Exemplo no celular, com o serviço de banho, a foto, a duração e o preço",
     ["Serviços com foto, preço e duração", "Calendário com os horários livres de cada dia",
      "A agenda do dono, com todos os horários marcados"],
     "Para pet shops, salões, barbearias e clínicas"),
]
def cartao_demo(did, titulo, url, negocio, alt, itens, publico, compacto=False):
    lis = "" if compacto else "".join(f"<li>{I['check']}<span>{x}</span></li>" for x in itens)
    return f"""<li class="demo-completa">
            <div class="demo-celular" aria-hidden="false">
              <picture><source type="image/webp" srcset="assets/img/demos/{did}-390.webp 390w, assets/img/demos/{did}.webp 780w" sizes="260px">
              <img src="assets/img/demos/{did}-390.webp" alt="{alt}" width="390" height="844" loading="lazy" decoding="async"></picture>
            </div>
            <div class="demo-completa-texto">
              <p class="pilar-apoio">{negocio}</p>
              <h3>{titulo}</h3>
              {f'<ul class="demo-completa-itens">{lis}</ul>' if lis else ""}
              <p class="demo-completa-publico">{publico}</p>
              <a class="botao" href="{url}" target="_blank" rel="noopener">Testar a demonstração {I["externo"]}<span class="visualmente-oculto"> (abre em nova aba)</span></a>
            </div>
          </li>"""

def mini_card(titulo, texto, href, externo=False):
    alvo = ' target="_blank" rel="noopener"' if externo else ""
    aviso = '<span class="visualmente-oculto"> (abre em nova aba)</span>' if externo else ""
    return f'<li><a class="mini-card" href="{href}"{alvo}><strong>{titulo}{aviso}</strong><span>{texto}</span></a></li>'

def cartao_pilar_inicio(pid, titulo, apoio, texto, resultados, mods, modo="inicio"):
    """modo "inicio": apresentação (texto curto, mini cards e painel). modo "catalogo" (Soluções): os resultados em lista."""
    res = "".join(f"<li>{r}</li>" for r in resultados)
    links = "".join(f'<li><a class="link-seta" href="{PAGINA_MOD[m]}">{MOD[m][0]}</a></li>' for m in mods if m in MOD_PAGINA)
    extra = ""
    if modo == "catalogo":
        return (f'<li class="pilar-card pilar-{pid}"><p class="pilar-apoio">{apoio}</p><h3>{titulo}</h3>'
                f'<ul class="frente-itens frente-itens-catalogo">{res}</ul><div class="pilar-rodape">'
                f'<ul class="pilar-links">{links}</ul></div></li>')
    if pid == "atendimento":
        extra = ('<ul class="mini-cards">' + mini_card("Aurora", "A IA que atende os seus clientes a qualquer hora", "aurora.html")
                 + mini_card("Cardápio online", "Teste a demonstração", DEMO_CARDAPIO, True)
                 + mini_card("Agendamento online", "Teste a demonstração", DEMO_AGENDAMENTO, True) + "</ul>")
    if pid == "sistemas":   # as partes que o sistema pode ter, preenchendo o card maior
        nomes = ["Estoque", "Financeiro e caixa", "Clientes e fornecedores", "Pedidos e vendas", "Relatórios e painel", "Documentos", "Integração com o que você já usa"]
        extra = ('<!--VIS_GESTAO--><ul class="pilar-partes" aria-label="Partes que o sistema pode ter">'
                 + "".join(f"<li>{n}</li>" for n in nomes) + "</ul>")   # VIS_GESTAO: o painel da página de Gestão (definido mais abaixo)
    return (f'<li class="pilar-card pilar-{pid}"><p class="pilar-apoio">{apoio}</p><h3>{titulo}</h3><p class="pilar-texto">{texto}</p>'
            f'{extra}<div class="pilar-rodape">'
            f'<ul class="pilar-links">{links}</ul></div></li>')

def previa_pilar(pid):
    """prévia ilustrativa de cada pilar (decorativa, sem números reais)"""
    if pid == "erp":
        linhas = "".join(f'<li><span>{n}</span><i style="--v:{v}%"></i><b class="{c}">{t}</b></li>' for n, v, c, t in
                         (("X-salada", 70, "ok", "Em estoque"), ("Pão de hambúrguer", 22, "alerta", "Repor"), ("Refrigerante lata", 55, "ok", "Em estoque")))
        return (f'<div class="pv pv-erp"><div class="pv-barra"><span>Estoque</span><span>Caixa</span><span>Pedidos</span><span>Clientes</span></div>'
                f'<ul class="pv-estoque">{linhas}</ul></div>')
    if pid == "bi":
        barras = "".join(f'<i style="--h:{h}%;--d:{k * .08:.2f}s"></i>' for k, h in enumerate((38, 52, 46, 64, 58, 80, 92)))
        return (f'<div class="pv pv-bi"><div class="pv-bi-topo"><span>Vendas da semana</span><span class="pv-sobe">em alta</span></div>'
                f'<div class="pv-graf">{barras}<svg viewBox="0 0 100 40" preserveAspectRatio="none"><polyline points="0,30 16,24 33,27 50,16 66,19 83,8 100,4"/></svg></div></div>')
    if pid == "ia":
        return ('<div class="pv pv-ia"><p class="pv-msg pv-cli">Tem horário amanhã de manhã?</p>'
                '<p class="pv-msg pv-aur"><img src="assets/img/aurora/aurora-avatar-96.webp" alt="" width="24" height="24" loading="lazy">Tenho às 9h e às 10h30. Qual fica melhor?</p>'
                '<p class="pv-msg pv-cli">9h, por favor!</p></div>')
    return ('<div class="pv pv-vendas"><div class="pv-site"><span class="pv-url">seunegocio.com.br</span>'
            '<div class="pv-itens"><span><b>Combo da casa</b><em>Adicionar</em></span><span><b>Corte + barba</b><em>Agendar</em></span></div></div>'
            '<div class="pv-horas"><span>9:00</span><span class="on">10:30</span><span>14:00</span></div></div>')

def pilares_destaque():
    """Soluções: cada pilar numa faixa própria (largura toda), com título da seção e um menu para pular entre eles."""
    menu = "".join(f'<li><a class="pe pe-{pid}" href="{CAMINHOS_PILAR[pid][0][1]}"><span class="pe-n" aria-hidden="true">0{k + 1}</span>'
                   f'<span class="pe-icone">{I[ICONE_PILAR[pid]]}</span><strong>{t}</strong><span class="pe-apoio">{ap}</span>'
                   f'<span class="pe-ir">Conhecer<span aria-hidden="true"> →</span></span></a></li>' for k, (pid, t, ap, *_r) in enumerate(PILARES_SOL))
    faixas = []
    for k, (pid, titulo, apoio, texto, resultados, mods) in enumerate(PILARES_SOL):
        res = "".join(f"<li>{I['check']}{r}</li>" for r in resultados)
        (t0, h0), *resto = CAMINHOS_PILAR[pid]
        outros = "".join(f'<a href="{h}">{t}</a>' for t, h in resto)
        faixas.append(f"""    <section class="px px-{pid}{" px-escuro" if k % 2 == 0 else ""}" id="pilar-{pid}" aria-labelledby="titulo-pilar-{pid}">
      <div class="container px-grade">
        <div class="px-texto">
          <p class="px-num"><span>0{k + 1}</span>{apoio}</p>
          <h3 id="titulo-pilar-{pid}">{titulo}</h3>
          <p class="px-frase">{texto}</p>
          <ul class="px-lista">{res}</ul>
          <div class="px-acoes"><a class="pl-principal" href="{h0}">{t0}</a><span class="pl-outros">{outros}</span></div>
        </div>
        <div class="px-previa" aria-hidden="true">{previa_pilar(pid)}</div>
      </div>
    </section>""")
    return f"""    <section class="secao claro px-intro" aria-labelledby="titulo-pilares-sol">
      <div class="container">
        <div class="cabeca" id="pilares">
          <p class="px-rotulo">Os 4 pilares</p>
          <h2 id="titulo-pilares-sol" data-revelar-texto>Tudo o que a Kyzent desenvolve, em quatro frentes.</h2>
          <p>Escolha a frente que mais pesa no seu negócio hoje. Elas funcionam sozinhas ou juntas.</p>
        </div>
        <nav class="pe-nav" aria-label="Os 4 pilares"><ul class="pe-lista">{menu}</ul></nav>
      </div>
    </section>
"""   # só a escolha: cada pilar leva à página que explica (as faixas saíram)

def cartao_pilar(pid, titulo, apoio, texto, resultados, mods, modo="inicio"):
    """modo "inicio": texto de apresentação. modo "catalogo" (Soluções): os resultados em lista."""
    corpo = (f'<p class="pl-texto">{texto}</p>' if modo == "inicio"
             else '<ul class="pl-lista">' + "".join(f"<li>{I['check']}{r}</li>" for r in resultados) + "</ul>")
    (t0, h0), *resto = CAMINHOS_PILAR[pid]
    outros = "".join(f'<a href="{h}">{t}</a>' for t, h in resto)
    return (f'<li class="pl pl-{pid}"><div class="pl-cabeca"><span class="pl-icone">{I[ICONE_PILAR[pid]]}</span><p class="pl-apoio">{apoio}</p></div>'
            f'<h3>{titulo}</h3>{corpo}<div class="pl-previa" aria-hidden="true">{previa_pilar(pid)}</div>'
            f'<div class="pl-rodape"><a class="pl-principal" href="{h0}">{t0}</a><span class="pl-outros">{outros}</span></div></li>')

TESTAR = f"""    <section class="secao testar" id="testar" aria-labelledby="titulo-testar">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-testar" data-revelar-texto>Sistemas prontos para testar.</h2>
          <p>Feito sob medida, com a cara do seu negócio. Cada demonstração tem a identidade visual do negócio de exemplo, não a da Kyzent: é assim que o seu sistema fica, com a sua marca.</p>
        </div>
        <ul class="demos-completas">
          {"".join(cartao_demo(*d, compacto=True) for d in DEMOS_COMPLETAS)}
        </ul>
        <p class="nota">Demonstrações com dados fictícios. Nenhum pedido ou agendamento é feito de verdade.</p>
        <div class="demo-todas"><a class="link-seta" href="servicos.html">Ver todas as soluções</a></div>
      </div>
    </section>"""

# Início: atalho curto para as soluções (o detalhe fica na página Soluções)
ATALHOS_INICIO = [("erp", "ERP sob medida", "O sistema do seu negócio", "solucao-gestao.html"),
                  ("bi", "BI e análise de dados", "Os números na mão", "solucao-bi.html"),
                  ("ia", "IA de atendimento", "A Aurora, 24 horas", "aurora.html"),
                  ("vendas", "Vendas e presença online", "Cardápio, agenda e site", "solucao-vendas.html")]
SOLUCOES_SECAO = f"""    <section class="secao claro atalhos" id="solucoes" aria-labelledby="titulo-solucoes">
      <div class="container">
        <div class="cabeca-linha">
          <div class="cabeca">
            <h2 id="titulo-solucoes" data-revelar-texto>Do que o seu negócio precisa?</h2>
          </div>
          <a class="link-seta" href="servicos.html">Ver todas as soluções</a>
        </div>
        <ul class="atalhos-lista">
          {"".join(f'<li><a class="atalho" href="{h}"><span class="atalho-icone">{I[ICONE_PILAR[pid]]}</span><span class="atalho-txt"><strong>{t}</strong><span>{d}</span></span><span class="atalho-seta" aria-hidden="true">→</span></a></li>' for pid, t, d, h in ATALHOS_INICIO)}
        </ul>
      </div>
    </section>"""

# ---------- experiência marcante do Início: do problema à tarefa feita (diagrama vivo, conduzido pela rolagem)
HISTORIA_PASSOS = [
    ("Atendimento", "A Aurora, o WhatsApp, o Instagram, o cardápio online e o agendamento recebem o cliente e registram tudo no sistema."),
    ("Pedidos e vendas", "Cada pedido ou venda entra organizado, com o total somado e a situação de cada um."),
    ("Estoque", "Cada venda já sai do estoque, e o sistema avisa antes de faltar."),
    ("Financeiro", "O que entrou e o que saiu, dia a dia, sem planilha."),
    ("Clientes", "O cadastro de cada cliente, com o histórico de compras e de visitas."),
    ("Relatórios", "Os números do negócio num painel, para decidir com base no que aconteceu."),
]
HISTORIA = f"""    <section class="secao historia historia-3d" id="como-funciona" aria-labelledby="titulo-historia">
      <div class="container historia-grade">
        <div class="historia-texto">
          <div class="cabeca">
            <h2 id="titulo-historia" data-revelar-texto>Tudo do seu negócio num sistema só.</h2>
            <p>A Kyzent desenvolve um sistema com as partes que o seu negócio precisa, todas ligadas. Toque em cada parte para ver o que ela faz.</p>
          </div>
          <ol class="historia-passos" data-historia-lista>
{chr(10).join(f'            <li class="historia-passo" data-historia="{i + 1}" role="button" tabindex="0" aria-pressed="{"true" if i == 0 else "false"}"><span class="historia-n">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(HISTORIA_PASSOS))}
          </ol>
        </div>
        <div class="historia-palco" data-historia-palco data-etapa="1" aria-hidden="true">
          <img class="historia-poster" src="assets/img/kyzent-k-escuro.svg" alt="" width="1080" height="520" loading="lazy" decoding="async">
          <p class="historia-rotulo"><span data-historia-rotulo>1 de {len(HISTORIA_PASSOS)} · {HISTORIA_PASSOS[0][0]}</span></p>
        </div>
      </div>
    </section>"""

# ---------- segmentos: o que muda em cada ramo, sem repetir os problemas das páginas de solução
SEG_DEMO = {"lanchonete": ("cardápio online", DEMO_CARDAPIO),   # barbearia sem botão: a demo de agendamento é de pet shop
            "salao": ("agendamento online", DEMO_AGENDAMENTO), "consultorio": ("agendamento online", DEMO_AGENDAMENTO),
            "petshop": ("agendamento online", DEMO_AGENDAMENTO)}
SEG_ALT = {
    "lanchonete": "Garçom servindo hambúrguer, batata frita e suco numa bandeja de madeira",
    "barbearia": "Barbeiros cortando o cabelo de clientes numa barbearia",
    "salao": "Cabeleireira atendendo uma cliente num salão de beleza",
    "consultorio": "Dentista examinando um paciente no consultório",
    "petshop": "Cachorro corgi sentado dentro de um pet shop",
    "empresa": "Equipe de uma empresa conversando em volta de um computador",
}
# cartão flutuante de cada segmento (interface de exemplo sobre a foto): (rótulo, linha principal, linha de apoio, estado)
SEG_UI = {
    "lanchonete": ("Pedido #1044", "2 X-bacon e 1 refrigerante", "R$ 58,00 · entrega", "Em preparo"),
    "barbearia": ("Agenda de hoje", "Corte e barba", "15h30 · com o Rafa", "Confirmado"),
    "salao": ("Agenda da equipe", "Escova e hidratação", "10h · cadeira 2", "Confirmado"),
    "consultorio": ("Consulta de amanhã", "Retorno · 9h", "Lembrete enviado ao paciente", "Confirmada"),
    "petshop": ("Banho e tosa", "Thor · porte médio", "Hoje, 14h", "Agendado"),
    "empresa": ("Estoque", "Papel A4 abaixo do mínimo", "Pedido ao fornecedor sugerido", "Atenção"),
}
def segmentos_secao(classe="claro"):
    chips, paineis_ = [], []
    for i, (sid, nome, ic, arq, (w, h), artigo, desafios, solucoes, beneficios) in enumerate(SEGMENTOS):
        chips.append(f'<button type="button" class="seg-chip" role="tab" id="aba-seg-{sid}" data-seg="{sid}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" aria-controls="seg-{sid}">{I[ic]}<span>{nome}</span></button>')
        blocos = "".join(f'<li>{I["check"]}<span>{x}</span></li>' for x in solucoes)
        melhora = "".join(f"<li>{x}</li>" for x in beneficios)
        rot, linha, apoio, estado = SEG_UI[sid]
        if sid in SEG_DEMO:
            nome_demo, url = SEG_DEMO[sid]
            acao = (f'<a class="botao" href="{url}" target="_blank" rel="noopener">Testar o {nome_demo} {I["externo"]}'
                    f'<span class="visualmente-oculto"> (abre em nova aba)</span></a>'
                    f'<a class="link-seta" href="orcamento.html?ramo={sid}">Simular meu orçamento</a>')
        else:
            acao = (f'<a class="botao" href="orcamento.html?ramo={sid}">Simular meu orçamento</a>'
                    f'<a class="link-seta" href="solucao-gestao.html">Conhecer os sistemas de gestão</a>')
        paineis_.append(f"""          <article class="seg-painel sg-painel{" ativo" if i == 0 else ""}" id="seg-{sid}" role="tabpanel" tabindex="0" aria-labelledby="aba-seg-{sid}">
            <div class="sg-texto">
              <p class="pilar-apoio">{nome}</p>
              <h3>{SEG_FRASE[sid]}</h3>
              <p class="sg-rotulo">O sistema que a Kyzent monta</p>
              <ul class="sg-blocos">{blocos}</ul>
              <div class="sg-acoes">{acao}</div>
            </div>
            <div class="sg-visual">
              {foto(arq, w, h, alt=SEG_ALT[sid], sizes="(max-width: 999px) 100vw, 45vw")}
              <div class="sg-ui" aria-hidden="true">
                <span class="sg-ui-topo"><small>{rot}</small><em>{estado}</em></span>
                <strong>{linha}</strong><span class="sg-ui-apoio">{apoio}</span>
              </div>
            </div>
          </article>""")
    return f"""    <section class="secao {classe} segmentos-v2" id="segmentos" aria-labelledby="titulo-segmentos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-segmentos" data-revelar-texto>Feito para o seu tipo de negócio.</h2>
          <p>Escolha o seu segmento e veja o sistema que a Kyzent monta para ele.</p>
        </div>
        <div class="seg-chips" role="tablist" aria-label="Segmentos" data-segmentos>{"".join(chips)}</div>
        <div class="seg-paineis">
          <div class="seg-palco" data-seg-palco data-seg-ativo="{SEGMENTOS[0][0]}" aria-hidden="true">
            {"".join(f'<span class="seg-palco-ic" data-ic="{sid}">{I[ic]}</span>' for sid, _n, ic, *_ in SEGMENTOS)}
          </div>
{chr(10).join(paineis_)}
        </div>
        <p class="nota sg-nota">{AVISO_RESULTADOS} Telas de exemplo, com dados fictícios.</p>
      </div>
    </section>"""

# ---------- apresentação curta (no Início, no lugar dos diferenciais repetidos)
SOBRE_CURTO = """    <section class="secao secao-faixa sobre-curto" aria-labelledby="titulo-sobre">
      <div class="container sobre-grade">
        <h2 id="titulo-sobre" data-revelar-texto>Uma empresa que desenvolve o sistema do seu negócio.</h2>
        <div>
          <p>A Kyzent desenvolve sistemas de gestão, atendimento e inteligência artificial sob medida para pequenos e médios negócios, com suporte da nossa equipe depois de tudo pronto.</p>
          <a class="link-seta" href="quem-somos.html">Conhecer a Kyzent</a>
        </div>
      </div>
    </section>"""

def projetos_secao():
    if not PROJETOS:   # sem case autorizado, a seção não aparece (pedido do Otavio, 2026-11-12)
        return ""
    if PROJETOS:
        cards = "".join(f'<li class="projeto"><h3>{n}</h3><p class="projeto-seg">{s}</p><p>{d}</p></li>' for n, s, d, _ in PROJETOS)
    else:
        cards = "".join('<li class="projeto projeto-vazio" aria-hidden="true"><span class="projeto-linha"></span><span class="projeto-linha curta"></span><span class="projeto-linha"></span></li>' for _ in range(3))
    return f"""    <section class="secao claro" id="projetos" aria-labelledby="titulo-projetos">
      <div class="container">
        <div class="projetos-grade">
          <div class="cabeca">
            <h2 id="titulo-projetos" data-revelar-texto>Projetos e cases.</h2>
            <p>Os cases da Kyzent aparecem aqui, com o que foi feito em cada negócio, sempre com a autorização do cliente. Não publicamos números nem depoimentos que não sejam reais.</p>
          </div>
          <ul class="projetos">{cards}</ul>
        </div>
      </div>
    </section>"""

# ---------- Início
MSG_ESPECIALISTA = MSG_CONVERSA
HERO = f"""    <section class="hero hero-cinema hero-3d" aria-labelledby="titulo-inicio" data-hero>
      <div class="hero-fundo" aria-hidden="true"><div class="hero-gradiente"></div></div>
      <div class="hero-palco" data-hero-palco aria-hidden="true"></div>
      <div class="container hero-grade">
        <div class="hero-k" aria-hidden="true">
          <img class="hero-poster" src="assets/img/kyzent-k-escuro.svg" alt="" width="1080" height="520" decoding="async">
        </div>
        <div class="hero-texto">
          <p class="hero-marca"><img class="marca-mini" src="assets/img/kyzent-k-escuro.svg" alt="" width="1080" height="520">Kyzent Technology Solutions</p>
          <h1 id="titulo-inicio" data-revelar-texto>Seu negócio no próximo nível.</h1>
          <p class="hero-apoio">Sistemas de gestão, atendimento e inteligência artificial feitos para o seu negócio, do primeiro contato ao caixa fechado.</p>
          <div class="hero-acoes">
            <a class="botao botao-grande" href="#solucoes" data-magnetico>Conhecer nossas soluções</a>
            <a class="botao botao-grande botao-vidro" href="#testar" data-magnetico>Testar uma demonstração</a>
          </div>
        </div>
      </div>
    </section>"""

# (a faixa de números saiu do site: a Kyzent não numera o que faz)


TAREFAS = [("Contar o estoque no caderno toda sexta", "O estoque baixa sozinho a cada venda"),
           ("Fechar o caixa somando na calculadora", "O relatório do dia fica pronto sozinho"),
           ("Imprimir cardápio novo a cada aumento", "Cardápio online atualizado em 1 minuto"),
           ("Anotar o pedido no papel no meio do movimento", "O pedido chega organizado e soma o total"),
           ("Responder \"qual o horário de sábado?\" pela 15ª vez", "A Aurora responde na hora"),
           ("Procurar o cliente que não volta há um mês", "O lembrete de retorno sai no dia certo")]
def comparar():
    manual = "".join(f'<li class="cmp-item cmp-manual-item" style="--i:{k}"><span class="cmp-estado">Pendente</span><span>{a}</span></li>' for k, (a, _) in enumerate(TAREFAS))
    auto = "".join(f'<li class="cmp-item cmp-auto-item"><span class="cmp-estado cmp-feito">Feito</span><span>{b}</span></li>' for _, b in TAREFAS)
    return f"""    <section class="secao comparar-secao" id="manual-automatico" aria-labelledby="titulo-comparar">
      <div class="container">
        <div class="cabeca cabeca-centro">
          <h2 id="titulo-comparar" data-revelar-texto>Do jeito manual ao automático.</h2>
          <p>Arraste a divisória e veja as mesmas tarefas do dia com e sem automação.</p>
        </div>
        <div class="comparar" data-comparar style="--corte:50%">
          <div class="cmp-lado cmp-manual">
            <p class="cmp-rotulo">Do jeito manual</p>
            <ul>{manual}</ul>
          </div>
          <div class="cmp-lado cmp-auto">
            <p class="cmp-rotulo">Com a Kyzent</p>
            <ul>{auto}</ul>
          </div>
          <div class="cmp-divisoria" aria-hidden="true"><span class="cmp-alca"></span></div>
          <label class="visualmente-oculto" for="cmp-faixa">Comparar o jeito manual e o automático</label>
          <input class="cmp-faixa" id="cmp-faixa" type="range" min="0" max="100" value="50" data-comparar-faixa>
        </div>
      </div>
    </section>"""

# ---------- depoimentos: para ativar, troque os exemplos por depoimentos reais (com autorização) e tire o comentário
DEPOIMENTOS_COMENTADO = """
<!-- DEPOIMENTOS (desativado até haver clientes reais que autorizem o uso do nome)
    <section class="secao" id="depoimentos" aria-labelledby="titulo-depoimentos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-depoimentos" data-revelar-texto>Quem já usa a Kyzent.</h2>
        </div>
        <ul class="grade grade-3 depoimentos">
          <li class="depoimento">
            <blockquote><p>[TEXTO DO DEPOIMENTO, como o cliente escreveu]</p></blockquote>
            <p class="depoimento-autor"><strong>[NOME]</strong><span>[NEGÓCIO]</span></p>
          </li>
        </ul>
      </div>
    </section>
-->
"""

INICIO = f"""{HERO}

{SOLUCOES_SECAO}

{comparar()}

{TESTAR}

{segmentos_secao()}

{por_que_kyzent()}

{projetos_secao()}{DEPOIMENTOS_COMENTADO}{perguntas().replace('class="secao"', 'class="secao claro"', 1)}

{chamada("index.html")}"""

# ---------- visuais próprios de cada página de solução (simulações em HTML/CSS)
def visual_atendimento():
    entradas = [("WhatsApp", "Qual o horário de sábado?", "ia"), ("Instagram", "Vocês entregam no centro?", "ia"),
                ("WhatsApp", "Quero falar sobre um evento", "equipe"), ("Site", "Quanto custa a escova?", "ia")]
    lis = "".join(f'<li class="tri-msg tri-{d}" style="--i:{n}"><span class="tri-canal">{c}</span><span>{t}</span></li>' for n, (c, t, d) in enumerate(entradas))
    return f"""<div class="vis vis-triagem">
              <div class="vis-topo"><strong>Caixa de entrada</strong><span class="selo-exemplo">Simulação demonstrativa</span></div>
              <div class="tri-grade">
                <ul class="tri-entrada">{lis}</ul>
                <div class="tri-ia"><span class="tri-nucleo">IA</span><small>lê, entende e decide</small></div>
                <div class="tri-saidas">
                  <div class="tri-raia"><p>Respondido na hora</p><span class="tri-conta" data-tri="ia">3</span></div>
                  <div class="tri-raia tri-raia-equipe"><p>Encaminhado à equipe</p><span class="tri-conta">1</span></div>
                </div>
              </div>
            </div>"""

def visual_funil():
    colunas = [("Novo contato", ["Ana", "Rafael"]), ("Qualificado", ["Bruna"]), ("Agendado", ["Diego", "Lia"]), ("Cliente", ["Paulo"])]
    cols = "".join(f'<div class="fun-col"><p>{t}</p>' + "".join(f'<span class="fun-card">{n}</span>' for n in nomes) + "</div>" for t, nomes in colunas)
    return f"""<div class="vis vis-funil">
              <div class="vis-topo"><strong>Oportunidades da semana</strong><span class="selo-exemplo">Simulação demonstrativa</span></div>
              <div class="fun-quadro">{cols}<span class="fun-viajante">Marcos<small>follow-up enviado</small></span></div>
              <p class="vis-legenda">Cada contato anda sozinho pelas etapas: a IA qualifica, agenda e chama de volta quem sumiu.</p>
            </div>"""

def visual_gestao():
    pontos = [(0, 70), (60, 58), (120, 64), (180, 40), (240, 46), (300, 24), (360, 14)]
    linha = " ".join(f"{'M' if i == 0 else 'L'}{x} {y}" for i, (x, y) in enumerate(pontos))
    return f"""<div class="vis vis-gestao" data-desenhar>
              <div class="vis-topo"><strong>Visão do mês</strong><span class="selo-exemplo">Dados fictícios</span></div>
              <div class="ges-kpis">
                <div><small>Faturamento</small><strong>R$ <span data-contar="48">48</span> mil</strong><em class="ges-sobe">acima do mês passado</em></div>
                <div><small>Pedidos</small><strong data-contar="1240">1240</strong></div>
                <div><small>Clientes ativos</small><strong data-contar="386">386</strong></div>
              </div>
              <svg class="ges-grafico" viewBox="0 0 360 90" preserveAspectRatio="none" aria-hidden="true">
                <path class="ges-area" d="{linha} L360 90 L0 90 Z"/><path class="ges-linha" d="{linha}"/>
              </svg>
              <div class="ges-rodape"><span>Semana 1</span><span>Semana 2</span><span>Semana 3</span><span>Semana 4</span></div>
            </div>"""

def visual_ia():
    fontes = ["Vendas", "Estoque", "Agenda"]
    chips = "".join(f'<span class="ia-fonte" style="--i:{n}">{f}</span>' for n, f in enumerate(fontes))
    return f"""<div class="vis vis-ia">
              <div class="vis-topo"><strong>Assistente interno</strong><span class="selo-exemplo">Simulação demonstrativa</span></div>
              <div class="ia-conversa">
                <p class="ia-pergunta">Quanto vendemos ontem e o que precisa de reposição?</p>
                <div class="ia-consulta"><small>Consultando</small>{chips}</div>
                <p class="ia-resposta">Ontem foram <strong>86 pedidos</strong>. Faltam reposição de <strong>pão de hambúrguer</strong> e <strong>embalagens</strong>; já deixei o pedido ao fornecedor pronto para você aprovar.</p>
              </div>
            </div>"""

def visual_site():
    return """<div class="vis vis-site">
              <div class="site-navegador">
                <div class="site-barra"><i></i><i></i><i></i><span>seunegocio.com.br</span></div>
                <div class="site-pagina">
                  <span class="site-bloco site-titulo"></span><span class="site-bloco site-linha"></span><span class="site-bloco site-linha curta"></span>
                  <span class="site-bloco site-botao"></span>
                  <div class="site-cards"><span class="site-bloco"></span><span class="site-bloco"></span><span class="site-bloco"></span></div>
                </div>
              </div>
              <div class="site-celular"><span class="site-bloco site-titulo"></span><span class="site-bloco site-linha"></span><span class="site-bloco site-botao"></span></div>
              <span class="selo-exemplo site-selo">Exemplo ilustrativo</span>
            </div>"""

VISUAL_MOD = {"whatsapp": (visual_atendimento, "Cada mensagem no lugar certo.", "A Aurora responde o que é rotina e o sistema de atendimento passa para a equipe só o que precisa de uma pessoa."),
              "agenda": (visual_funil, "Nenhuma oportunidade parada.", "Contatos qualificados, horários marcados e clientes chamados de volta no momento certo."),
              "bi": (visual_gestao, "Os números do negócio, sem planilha.", "Vendas, clientes e estoque num painel que se atualiza sozinho."),
              "gestao": (visual_gestao, "Os números do negócio, sem planilha.", "Estoque, financeiro, pedidos e clientes num sistema só, com os números atualizados sozinhos."),
              "site": (visual_site, "Um site que trabalha por você.", "Feito para o seu negócio, rápido no celular e com a cara da sua marca."),
              "ia": (visual_ia, "Uma IA que conhece a sua empresa.", "Pergunte em português e receba a resposta com base nos seus próprios sistemas.")}

# o dia a dia de cada solução, em passos  [REVISAR] rascunho do Claude
COMO_FUNCIONA = {
    "gestao": [("A venda acontece", "No balcão, no cardápio online ou pela conversa, cada venda entra no sistema."),
               ("O estoque baixa", "Os produtos vendidos saem do estoque, e o sistema avisa quando algum está acabando."),
               ("O caixa fecha", "Entradas e saídas do dia somadas, sem calculadora."),
               ("Os números aparecem", "O painel mostra pedidos, faturamento e clientes da semana e do mês.")],
    "agenda": [("O cliente escolhe", "No cardápio online ou na página de agendamento, ele escolhe o produto ou o horário."),
               ("Entra organizado", "O pedido chega com o total somado, ou o horário entra na agenda sem conflito."),
               ("Confirmação e lembrete", "O cliente recebe a confirmação e um lembrete antes do horário."),
               ("Ele volta", "Quem sumiu recebe uma mensagem chamando de volta no momento certo.")],
    "whatsapp": [("A mensagem chega", "No WhatsApp ou no Instagram do seu negócio, a qualquer hora."),
                 ("A Aurora responde a rotina", "Horário, preço, endereço e serviços respondidos na hora."),
                 ("A equipe recebe o resto", "O que precisa de uma pessoa vai para o sistema de atendimento, já separado."),
                 ("Nada fica sem resposta", "A equipe vê todas as conversas num lugar só e divide o atendimento.")],
    "site": [("Conversamos sobre o negócio", "O que você vende, para quem e o que o cliente mais procura."),
             ("Você vê antes", "As páginas são mostradas antes de irem para o ar, e você ajusta o que quiser."),
             ("O site vai para o ar", "Rápido no celular, com a sua marca e o caminho para o contato."),
             ("Atualizações depois", "Mudou um horário ou um serviço? A gente atualiza.")],
    "bi": [("Juntamos os dados", "Sistema de gestão, vendas e planilhas ligados numa base só."),
           ("Montamos o painel", "Com os números que importam para o seu negócio, do jeito que você entende."),
           ("Ele se atualiza sozinho", "Cada venda, compra e pagamento já aparece no painel e nos relatórios."),
           ("Você decide com dados", "E recebe um aviso quando algum número sai do normal.")],
    "ia": [("Escolhemos a tarefa", "Um processo repetitivo que toma tempo da equipe."),
           ("A IA é configurada", "Com as informações e as regras da sua empresa."),
           ("Ela faz a tarefa", "Consulta os sistemas, organiza e avisa quem precisa saber."),
           ("A equipe acompanha", "As pessoas conferem o resultado e ficam com o que precisa de decisão.")],
}
# as simulações de cada solução (o Site não tem simulação: mostra a ilustração)
DEMOS_MOD = {"bi": ["painel", "pedidos"], "gestao": ["painel", "estoque", "pedidos", "clientes"], "agenda": ["agendamento"], "whatsapp": ["chatbot"], "ia": ["automacao"]}
INTRO_DEMOS = {"bi": "Registre um pedido em Pedidos e veja o painel se atualizar sozinho, sem ninguém montar relatório.",
               "gestao": "Quatro telas do mesmo sistema, ligadas pela mesma base de dados: registre uma venda no Estoque ou em Pedidos e veja o Painel mudar.",
               "agenda": "Escolha o serviço, o dia e o horário, do jeito que o seu cliente vai fazer.",
               "whatsapp": "Faça o papel do cliente de uma barbearia de exemplo: marque um horário, pergunte o preço ou peça para falar com uma pessoa.",
               "ia": "Uma mensagem do cliente vira uma tarefa feita: a IA entende o pedido, consulta os sistemas e avisa a equipe."}

def pagina_solucao(mid):
    nome, curto, ic, resumo, servs = MOD[mid]
    titulo, chamada_txt, benef, problemas = SOLUCOES[mid]
    fichas = "\n".join(f'              <li class="item ficha brilho"><h3>{a}</h3><p>{CATALOGO[a][0]}</p>'
                       f'<dl><dt>Resolve</dt><dd>{FICHAS[a][0]}</dd><dt>Na prática</dt><dd>{FICHAS[a][1]}</dd></dl></li>' for a in servs)
    fn, vt, vd = VISUAL_MOD[mid]
    probs = "".join(f"<li>{p}</li>" for p in problemas)
    bens = "".join(f"<li>{I['check']}{b}</li>" for b in benef)
    passos = "".join(f'<li class="processo-passo"><span class="processo-n">{k + 1}</span><h3>{t}</h3><p>{d}</p></li>' for k, (t, d) in enumerate(COMO_FUNCIONA[mid]))
    if False and mid in DEMOS_MOD:   # simulações desligadas: vão para a futura área de testes (.offpilot/implementacoes-para-o-futuro.md)
        funcionando = central_demos(ids=DEMOS_MOD[mid], titulo="Teste aqui.", sec_id="funcionando", com_link=False,
                                    intro=f'Simulação com dados fictícios. {INTRO_DEMOS[mid]}')
        link_topo = "Testar agora"
    else:
        funcionando = f"""    <section class="secao" id="funcionando" aria-labelledby="titulo-funcionando">
      <div class="container vis-grade">
        <div class="vis-texto">
          <h2 id="titulo-funcionando" data-revelar-texto>{vt}</h2>
          <p>{vd}</p>
        </div>
        {fn()}
      </div>
    </section>"""
        link_topo = "Ver como fica"
    return f"""    <section class="pagina-topo solucao-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <a class="voltar-link" href="servicos.html#pilares">{I["voltar"]}Todas as soluções</a>
          {ilustra(mid, "ilu ilu-grande")}
          <h1 id="titulo-pagina" data-revelar-texto>{titulo}</h1>
          <p class="pagina-topo-apoio">{chamada_txt}</p>
        </div>
        <div class="pagina-topo-texto">
          <a class="botao botao-grande" href="orcamento.html" data-magnetico>Pedir orçamento</a>
          <a class="link-seta" href="#funcionando">{link_topo}</a>
        </div>
      </div>
    </section>

    <section class="secao claro" aria-labelledby="titulo-problemas">
      <div class="container solucao-duas">
        <div>
          <h2 id="titulo-problemas" data-revelar-texto>O que esta solução resolve.</h2>
          <ul class="lista-problemas">{probs}</ul>
        </div>
        <div class="solucao-beneficios">
          <h3>O que muda</h3>
          <ul class="lista-simples">{bens}</ul>
          <p class="nota">{AVISO_RESULTADOS}</p>
        </div>
      </div>
    </section>

{ERP_EXPLICA if mid == "gestao" else f"""    <section class="secao" aria-labelledby="titulo-dia">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-dia" data-revelar-texto>Como funciona no dia a dia.</h2>
        </div>
        <ol class="processo processo-4">{passos}</ol>
      </div>
    </section>"""}

{funcionando}
{SOLUCAO_EXTRA.get(mid, lambda: "")()}
{"" if mid == "gestao" else f"""    <section class="secao claro secao-faixa" id="incluido" aria-labelledby="titulo-incluido">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-incluido" data-revelar-texto>{"Módulos possíveis." if mid == "gestao" else "O que está incluído."}</h2>
          <p>{"O seu sistema tem só os módulos que o seu negócio precisa. Dá para começar com um e acrescentar os outros depois." if mid == "gestao" else "O que cada serviço faz, o problema que resolve e o que muda na prática."}</p>
        </div>
        <ul class="painel-itens itens-solucao">
{fichas}
        </ul>
      </div>
    </section>"""}

{chamada(mid)}"""

# ---------- página do ERP: o que é um ERP e onde ele economiza tempo  [REVISAR] rascunho do Claude
ERP_SEM = ["A venda é anotada no caixa ou no caderno.",
           "No fim do dia, alguém tira da planilha de estoque o que saiu.",
           "O valor é lançado de novo no controle do financeiro.",
           "No fim do mês, alguém junta tudo isso para descobrir quanto vendeu e o que precisa comprar."]
ERP_COM = ["A venda é registrada uma vez, no caixa ou no pedido online.",
           "O estoque daquele produto baixa no mesmo instante.",
           "O valor já entra no caixa do dia e, se for a prazo, nas contas a receber.",
           "O relatório do mês está pronto a qualquer hora, sem ninguém montar."]
ERP_GANHOS = [
    ("Cada informação entra uma vez", "Uma venda, uma compra ou um cadastro é digitado num lugar só. Acaba o trabalho de passar o mesmo dado do caderno para a planilha e da planilha para o caixa, que é onde mais aparece erro de digitação."),
    ("O fechamento não depende de conferência", "Como o caixa é a soma das vendas registradas, ele fecha sozinho. Ninguém fica somando cupom ou procurando a diferença depois do expediente."),
    ("A compra é feita antes de faltar", "Cada produto tem um estoque mínimo. Quando passa dele, o sistema avisa, e a reposição é feita com base no que realmente saiu, sem comprar a mais nem deixar faltar."),
    ("A resposta está na tela, não na cabeça do dono", "Preço, saldo de um cliente, o que um fornecedor entregou ou quanto entrou ontem: qualquer pessoa da equipe consulta em segundos, sem interromper ninguém."),
]
ERP_EXPLICA = f"""    <section class="secao erp-o-que" aria-labelledby="titulo-erp-o-que">
      <div class="container">
        <div class="erp-intro">
          <div class="cabeca">
            <p class="px-rotulo">O que é um ERP</p>
            <h2 id="titulo-erp-o-que" data-revelar-texto>Um sistema onde todas as áreas usam a mesma informação.</h2>
          </div>
          <div class="erp-def">
            <p>ERP é a sigla em inglês para <em>Enterprise Resource Planning</em>, ou planejamento dos recursos da empresa. Na prática, é um sistema só onde vendas, estoque, compras, financeiro e cadastros trabalham sobre a mesma base de dados.</p>
            <p>A diferença para usar um programa para cada coisa é que nada precisa ser passado de um lugar para o outro: o que acontece numa área já aparece nas outras.</p>
          </div>
        </div>

        <div class="erp-venda">
          <p class="erp-venda-titulo">O caminho de uma venda</p>
          <div class="erp-colunas">
            <div class="erp-col erp-col-sem"><h3>Sem ERP</h3><ol>{"".join(f"<li>{t}</li>" for t in ERP_SEM)}</ol></div>
            <div class="erp-col erp-col-com"><h3>Com ERP</h3><ol>{"".join(f"<li>{t}</li>" for t in ERP_COM)}</ol></div>
          </div>
        </div>

        <h3 class="erp-ganhos-titulo">Onde a equipe ganha tempo</h3>
        <ul class="erp-ganhos">{"".join(f'<li><span class="erp-g-n">0{k + 1}</span><h4>{t}</h4><p>{d}</p></li>' for k, (t, d) in enumerate(ERP_GANHOS))}</ul>
      </div>
    </section>
"""

# ---------- o que cada página de solução tem a mais
PROCESSO_SISTEMA = [
    ("Diagnóstico", "Conversamos sobre como o seu negócio funciona hoje: o que vende, como controla o estoque e o caixa, onde perde tempo."),
    ("Protótipo", "Mostramos as telas do sistema antes de desenvolver, para você ajustar o que quiser."),
    ("Desenvolvimento", "Construímos o sistema com as partes que o seu negócio precisa, já com os seus produtos, serviços e clientes."),
    ("Treinamento", "Ensinamos a sua equipe a usar o sistema no dia a dia."),
    ("Suporte", "Acompanhamos, corrigimos e evoluímos o sistema conforme o seu negócio cresce."),
]
def extra_gestao():
    passos = "".join(f'<li class="processo-passo"><span class="processo-n">{k + 1}</span><h3>{t}</h3><p>{d}</p></li>' for k, (t, d) in enumerate(PROCESSO_SISTEMA))
    return f"""
    <section class="secao secao-faixa" aria-labelledby="titulo-para-quem">
      <div class="container">
        <div>
          <h2 id="titulo-para-quem" data-revelar-texto>Para quem é.</h2>
          <p class="para-quem-texto">Para pequenos e médios negócios que controlam estoque, caixa e clientes em caderno, planilha ou em sistemas que não conversam entre si: lanchonetes e restaurantes, lojas, pet shops, salões, barbearias, clínicas e empresas de serviço.</p>
        </div>
      </div>
    </section>"""
def extra_vendas():
    return f"""
    <section class="secao testar" aria-labelledby="titulo-vendas-demos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-vendas-demos" data-revelar-texto>Os sistemas completos.</h2>
          <p>O cardápio e o agendamento inteiros no ar, cada um com a cara do negócio de exemplo. Faça um pedido ou marque um horário do começo ao fim.</p>
        </div>
        <ul class="demos-completas">{"".join(cartao_demo(*d) for d in DEMOS_COMPLETAS)}</ul>
      </div>
    </section>"""
SOLUCAO_EXTRA = {"gestao": extra_gestao, "agenda": extra_vendas}

# ---------- Quem somos: a empresa apresentada uma vez; propósito, missão e proposta com papéis diferentes
QUEM = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Quem somos</h1>
          <p class="pagina-topo-apoio">Somos a Kyzent, uma empresa de Tecnologia e Inovação dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio.</p>
          <p class="topo-alternativa">A Kyzent desenvolve sistemas de gestão sob medida, com experiência em sistemas de estoque e almoxarifado, além de atendimento, vendas e Inteligência Artificial. Quando o seu negócio pede algo diferente, construímos do zero.</p><!-- [CONFIRMAR] texto da experiência em estoque e almoxarifado -->
        </div>
        {k3d("k3d-topo")}
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-proposito">
      <div class="container dupla">
        <div class="dupla-foto">
          {foto("equipe-reuniao.jpg", 1600, 900, "Equipe conversando em uma reunião num escritório")}
        </div>
        <div class="dupla-texto">
          <h2 id="titulo-proposito" data-revelar-texto>Nosso propósito.</h2>
          <p class="proposito-texto">Transformar processos por meio da tecnologia, oferecendo mais produtividade, automação e eficiência para impulsionar os resultados dos nossos clientes.</p>
        </div>
      </div>
    </section>

{PILARES}

{diferenciais("")}"""

# ---------- Política de Privacidade (LGPD). Texto escrito pelo Claude a partir de como o site funciona; os sócios precisam confirmar.
PRIVACIDADE = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container">
        <h1 id="titulo-pagina">Política de Privacidade</h1>
        <p class="pagina-topo-apoio">Como a Kyzent trata os seus dados pessoais, de acordo com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).</p>
        <p class="legal-data">Última atualização: {PRIVACIDADE_DATA}</p>
      </div>
    </section>

    <section class="secao legal">
      <div class="container legal-texto">
        <h2>1. Quem cuida dos seus dados</h2>
        <p>A Kyzent Technology Solutions é a responsável (controladora) pelos dados pessoais tratados por este site e pelos nossos canais de atendimento. Para qualquer assunto sobre privacidade, fale com a gente pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

        <h2>2. Quais dados recebemos</h2>
        <ul>
          <li><strong>Simulador de orçamento:</strong> as respostas que você marca, o seu nome e, se quiser, o nome da empresa, o seu e-mail e uma observação. O simulador funciona só no seu navegador: nada é enviado ao nosso servidor nem guardado no site. Esses dados só chegam até nós se você enviar a mensagem pronta pelo WhatsApp ou por e-mail.</li>
          <li><strong>WhatsApp, Instagram e e-mail:</strong> o que você nos manda nas conversas e os dados do seu perfil nesses aplicativos, como nome e número de telefone.</li>
          <li><strong>Navegação:</strong> o site não usa cookies, Google Analytics, pixel da Meta nem outra ferramenta de rastreamento. A hospedagem (GitHub Pages) registra dados técnicos de acesso, como o endereço IP, para manter o site funcionando e seguro.</li>
        </ul>

        <h2>3. Para que usamos</h2>
        <ul>
          <li>Responder o seu contato e preparar o orçamento que você pediu;</li>
          <li>Conversar sobre a contratação e prestar os serviços combinados;</li>
          <li>Cumprir obrigações legais.</li>
        </ul>
        <p>Não vendemos os seus dados e não enviamos propaganda sem a sua autorização.</p>

        <h2>4. Com quem compartilhamos</h2>
        <ul>
          <li><strong>Meta</strong> (WhatsApp e Instagram), por onde as conversas acontecem;</li>
          <li><strong>GitHub</strong>, que hospeda este site;</li>
          <li><strong>Google</strong>, quando a conversa for por e-mail (Gmail).</li>
        </ul>
        <p>Essas empresas podem tratar dados fora do Brasil e seguem as suas próprias políticas de privacidade. Também compartilhamos dados quando a lei ou uma autoridade exigir.</p>

        <h2>5. Por quanto tempo guardamos</h2>
        <p>Guardamos as conversas e os dados de contato enquanto houver uma negociação ou um contrato em andamento e, depois disso, pelo tempo necessário para cumprir obrigações legais. Se você não fechar negócio, pode pedir que a gente apague os seus dados a qualquer momento.</p>

        <h2>6. Os seus direitos</h2>
        <p>Pela LGPD, você pode pedir a qualquer momento:</p>
        <ul>
          <li>a confirmação de que tratamos os seus dados e o acesso a eles;</li>
          <li>a correção de dados incompletos ou errados;</li>
          <li>a exclusão dos seus dados ou o bloqueio dos dados desnecessários;</li>
          <li>informações sobre com quem compartilhamos os seus dados;</li>
          <li>a revogação de um consentimento que você tenha dado.</li>
        </ul>
        <p>Para isso, mande um e-mail para <a href="mailto:{EMAIL}">{EMAIL}</a>. Respondemos em até 15 dias. Você também pode reclamar na Autoridade Nacional de Proteção de Dados (ANPD).</p>

        <h2>7. Segurança</h2>
        <p>Usamos as medidas de segurança dos próprios aplicativos e limitamos o acesso às conversas às pessoas da Kyzent que precisam delas para atender você.</p>

        <h2>8. Mudanças nesta política</h2>
        <p>Podemos atualizar esta política quando o site ou os nossos serviços mudarem. A data da última atualização fica no topo desta página.</p>
      </div>
    </section>"""

# ---------- Soluções: central de navegação (cartões e a lista de serviços, sem número, um único acesso ao simulador)
def lista_servicos():
    """Soluções: um abre e fecha por pilar; dentro, os serviços com uma linha cada"""
    blocos = []
    for pid, titulo, apoio, *_resto, mods in PILARES_SOL:
        grupos = []
        for mid in mods:
            nome, curto, ic, resumo, servs = MOD[mid]
            lis = "".join(f'<li><strong>{a}</strong><span>{CATALOGO[a][0]}</span></li>' for a in servs)
            sub = f'<p class="ac-sub"><a href="{PAGINA_MOD[mid]}">{nome}</a></p>' if len(mods) > 1 else ""
            grupos.append(f'<div class="ac-grupo">{sub}<ul class="ac-servicos">{lis}</ul></div>')
        (t0, h0), *_r = CAMINHOS_PILAR[pid]
        blocos.append(f'<details class="ac ac-{pid}"><summary><span class="ac-icone">{I[ICONE_PILAR[pid]]}</span>'
                      f'<span class="ac-nome"><strong>{titulo}</strong><small>{apoio}</small></span><span class="ac-mais" aria-hidden="true">{I["mais"]}</span></summary>'
                      f'<div class="ac-corpo">{"".join(grupos)}<a class="ac-ir" href="{h0}">{t0} →</a></div></details>')
    return '<div class="ac-lista">' + "".join(blocos) + "</div>"


def ecossistema():
    import math
    rx, ry = 250, 120
    nos = []
    n = len(MOD_PAGINA); passo = 360 / n
    for k, mid in enumerate(MOD_PAGINA):
        a = math.radians(-90 + k * passo)
        x, y = 320 + rx * math.cos(a), 190 + ry * math.sin(a)
        nome = MOD[mid][1]
        nos.append(f'<span class="eco-no" style="--x:{x / 640 * 100:.2f}%;--y:{y / 380 * 100:.2f}%;--i:{k}">'
                   f'<span class="eco-bola"></span><span class="eco-nome">{nome}</span></span>')   # só ilustração, sem clique
    return f"""<div class="ecossistema" data-ecossistema>
          <svg viewBox="0 0 640 380" aria-hidden="true" focusable="false">
            <ellipse class="eco-orbita" cx="320" cy="190" rx="{rx}" ry="{ry}"/>
            <ellipse class="eco-orbita eco-orbita-2" cx="320" cy="190" rx="{rx * .62:.0f}" ry="{ry * .62:.0f}"/>
            <path id="eco-trilho" d="M{320 - rx} 190a{rx} {ry} 0 1 0 {2 * rx} 0a{rx} {ry} 0 1 0 {-2 * rx} 0" fill="none"/>
            <circle class="eco-luz" r="5"><animateMotion dur="14s" repeatCount="indefinite"><mpath href="#eco-trilho"/></animateMotion></circle>
            {"".join(f'<line class="eco-raio" x1="320" y1="190" x2="{320 + rx * math.cos(math.radians(-90 + k * passo)):.1f}" y2="{190 + ry * math.sin(math.radians(-90 + k * passo)):.1f}"/>' for k in range(n))}
          </svg>
          {k3d("eco-k3d")}
          <div class="eco-nos" aria-hidden="true">{"".join(nos)}</div>
        </div>"""

SERVICOS_PAG = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade eco-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Soluções</h1>
          <p class="pagina-topo-apoio">ERP, BI e análise de dados, IA de atendimento, e vendas e presença online, desenvolvidos sob medida para o seu negócio. E, quando ele pede algo diferente, a Kyzent constrói do zero.</p>
        </div>
        {ecossistema()}
      </div>
    </section>

{pilares_destaque()}

    <section class="secao testar demos-sol" id="demonstracoes" aria-labelledby="titulo-demos-sol">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-demos-sol" data-revelar-texto>Veja nossas demonstrações de sistemas.</h2>
          <p>Sistemas que a Kyzent desenvolveu, inteiros e no ar, cada um com a cara do negócio de exemplo. Faça um pedido ou marque um horário do começo ao fim.</p>
        </div>
        <ul class="demos-completas">
          {"".join(cartao_demo(*d, compacto=True) for d in DEMOS_COMPLETAS)}
        </ul>
        <p class="nota">Demonstrações com dados fictícios. Nenhum pedido ou agendamento é feito de verdade.</p>
      </div>
    </section>

{chamada("servicos.html")}
"""
FILTRO_JANELA = ""

DESC = "A Kyzent desenvolve sistemas de gestão (ERP), cardápio online, agendamento online e atendimento com IA para pequenos e médios negócios de todo o Brasil."

saidas = [
    ("index.html", "Kyzent | Sistemas de gestão, automação e IA para o seu negócio", DESC, INICIO.replace("<!--VIS_GESTAO-->", f'<div class="pilar-vis" aria-hidden="true">{visual_gestao()}</div>'), "", None),
    ("servicos.html", "Soluções e serviços | Kyzent", "Soluções da Kyzent em quatro pilares: ERP sob medida, BI e análise de dados, IA de atendimento com a Aurora, e vendas e presença online com cardápio, agendamento e site. Simule o seu orçamento.", SERVICOS_PAG.replace("<!--VIS_GESTAO-->", f'<div class="pilar-vis" aria-hidden="true">{visual_gestao()}</div>'), FILTRO_JANELA, None),
    ("quem-somos.html", "Quem somos | Kyzent", "A Kyzent é uma empresa de Tecnologia e Inovação que desenvolve sistemas sob medida. Conheça o nosso propósito, a missão, a visão, os valores e os diferenciais.", QUEM, "", None),
    ("privacidade.html", "Política de Privacidade | Kyzent", "Como a Kyzent trata os seus dados pessoais, de acordo com a LGPD: quais dados recebemos, para que usamos, com quem compartilhamos e como exercer os seus direitos.", PRIVACIDADE, "", None),
    ("aurora.html", "Aurora, a IA de atendimento | Kyzent", "Conheça a Aurora, a IA de atendimento da Kyzent: atende os clientes do seu negócio no WhatsApp e no Instagram, 24 horas, e chama a sua equipe quando precisa.", aurora_pagina(), "", None),
    ("orcamento.html", "Orçamento | Kyzent", "Simule o seu orçamento em quatro passos: diga o que precisa (sistema de gestão, cardápio online, agendamento, atendimento com IA ou site) e receba uma recomendação da Kyzent.", ORCAMENTO, "", None),
] + [(PAGINA_MOD[mid], f"{SOLUCOES[mid][0]} | Kyzent", SOLUCOES[mid][1], pagina_solucao(mid), "", "servicos.html") for mid in MOD_PAGINA]

for arq, titulo, desc, corpo, janelas, ativo in saidas:
    with open(os.path.join(SITE, arq), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina(arq, titulo, desc, corpo, janelas, ativo))
    print("ok", arq)

# demonstracoes.html saiu do menu (as simulações moram nas páginas de solução): o endereço antigo leva para a solução certa
with open(os.path.join(SITE, "demonstracoes.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Kyzent</title><meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}servicos.html">
<script>var d = {{"#completos": "solucao-vendas.html#funcionando", "#gestao": "solucao-gestao.html#funcionando", "#atendimento": "aurora.html#conversar", "#automacao": "solucao-ia.html#funcionando"}};
location.replace(d[location.hash] || "servicos.html");</script>
<noscript><meta http-equiv="refresh" content="0; url=servicos.html"></noscript></head>
<body><p><a href="servicos.html">Ir para as soluções</a></p></body></html>
""")
print("ok demonstracoes.html (redirecionamento)")
# solucao-atendimento.html saiu (o atendimento é a página da Aurora): o endereço antigo leva para lá
with open(os.path.join(SITE, "solucao-atendimento.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Kyzent</title><meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}aurora.html">
<script>location.replace("aurora.html" + (location.hash === "#funcionando" ? "#conversar" : ""));</script>
<noscript><meta http-equiv="refresh" content="0; url=aurora.html"></noscript></head>
<body><p><a href="aurora.html">Ir para a página da Aurora</a></p></body></html>
""")
print("ok solucao-atendimento.html (redirecionamento)")

with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for arq, *_ in saidas:
        f.write(f"  <url><loc>{BASE}{'' if arq == 'index.html' else arq}</loc><priority>{'1.0' if arq == 'index.html' else '0.8'}</priority></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
print("ok sitemap.xml e robots.txt")
