"""Monta as páginas do site com o mesmo topo, rodapé e janelas.
Uso (na raiz do site): python tools/monta_paginas.py .
Atenção: sobrescreve index.html, quem-somos.html e servicos.html.
Edite o texto aqui e rode de novo, para as páginas não ficarem diferentes entre si."""
import json, os, sys
from html import escape
from urllib.parse import quote

SITE = sys.argv[1]
BASE = "https://kyzenttech-lang.github.io/site/"
VERSAO = "53"   # aumente a cada mudança no CSS/JS, para o navegador baixar o arquivo novo

WHATS = [("5519988728894", "(19) 98872-8894"), ("5519971246077", "(19) 97124-6077")]
MSG = quote("Olá, vim pelo site da Kyzent")
BOTAO = "Chamar no WhatsApp"   # o nome dos botões de contato do topo, menu, janelas e barra fixa

# Black Friday: implantação grátis (decisão do Otavio, 2026-11-12). Depois do fim, o JS esconde o que é da promoção.
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
    "instagram": svg('<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17 7h.01"/>'),
}
TIQUES = ('<svg class="zap-tiques" viewBox="0 0 18 11" aria-hidden="true"><path d="M1 6.2l3 3L11 1.5M7 9.2l.8.8L15 1.5" '
          'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

PAGINAS = [("index.html", "Início"), ("servicos.html", "Soluções"), ("quem-somos.html", "Quem somos"), ("orcamento.html", "Orçamento")]

# ------------------------------------------------------------------ catálogo de serviços (sem preço: o valor é combinado com cada cliente)
# ramos: para quais tipos de negócio o serviço é indicado (filtro da página Serviços)
TODOS = ["lanchonete", "barbearia", "salao", "consultorio", "petshop"]
CATALOGO = {
    "Chatbots inteligentes": ("Atendimento automatizado pelo WhatsApp e Instagram, disponível 24 horas.", TODOS),
    "Respostas inteligentes": ("Resolução automática de dúvidas e perguntas frequentes.", TODOS),
    "Triagem de atendimento": ("Identificação das necessidades dos clientes e encaminhamento para atendentes humanos.", ["salao", "consultorio"]),
    "Centrais inteligentes de atendimento": ("Múltiplos agentes de IA trabalhando em diferentes funções.", []),
    "Agendamentos automáticos": ("Organização de reuniões, consultas e serviços.", ["barbearia", "salao", "consultorio", "petshop"]),
    "Captação e qualificação de leads": ("Identificação e classificação de potenciais clientes.", ["salao", "consultorio"]),
    "Follow-up inteligente": ("Acompanhamento automático de clientes e recuperação de oportunidades.", TODOS),
    "Orçamentos automatizados": ("Geração e envio de propostas comerciais.", ["salao"]),
    "Automação de processos comerciais": ("Integração e otimização de etapas do processo de vendas.", []),
    "Gestão de cadastros e pedidos": ("Organização automatizada de informações e solicitações.", ["lanchonete", "petshop"]),
    "Integração com CRM": ("Centralização e gerenciamento do relacionamento com clientes.", ["barbearia", "salao", "consultorio", "petshop"]),
    "Relatórios automatizados": ("Geração de relatórios para acompanhamento empresarial.", ["lanchonete", "barbearia", "petshop"]),
    "Automação de documentos": ("Organização e envio automático de documentos.", ["consultorio"]),
    "Integração de sistemas": ("Conexão entre diferentes plataformas e ferramentas empresariais.", []),
    "Integração com estoque e ERP": ("Automatização e conexão de sistemas de gestão empresarial.", ["lanchonete", "petshop"]),
    "Agentes de IA personalizados": ("Inteligência artificial desenvolvida conforme as necessidades da empresa.", []),
    "Assistentes internos de IA": ("Ferramentas inteligentes para auxiliar funcionários.", []),
    "Sistemas personalizados": ("Desenvolvimento de soluções de atendimento e automação sob medida.", []),
    "Site personalizado": ("Site feito sob medida para o seu negócio, conforme o que você quer mostrar e o que mais interessa aos seus clientes.", TODOS),
}

# módulos da página Serviços: (id, nome, nome curto (celular), ícone, resumo, [serviços])
MODULOS = [
    ("whatsapp", "WhatsApp e atendimento", "WhatsApp", "conversa",
     "Chatbots, respostas automáticas e triagem para atender bem o cliente a qualquer hora.",
     ["Chatbots inteligentes", "Respostas inteligentes", "Triagem de atendimento", "Centrais inteligentes de atendimento"]),
    ("agenda", "Agendamento e vendas", "Agenda", "agenda",
     "Horários marcados, clientes acompanhados e oportunidades que não se perdem.",
     ["Agendamentos automáticos", "Captação e qualificação de leads", "Follow-up inteligente", "Orçamentos automatizados", "Automação de processos comerciais"]),
    ("gestao", "Gestão e sistemas", "Gestão", "gestao",
     "Cadastros, pedidos, relatórios e documentos organizados, com os seus sistemas conversando entre si.",
     ["Gestão de cadastros e pedidos", "Integração com CRM", "Relatórios automatizados", "Automação de documentos", "Integração de sistemas", "Integração com estoque e ERP"]),
    ("site", "Site e presença online", "Site", "site",
     "Um site feito sob medida para o seu negócio, do jeito que você quer apresentá-lo.",
     ["Site personalizado"]),
    ("ia", "IA sob medida", "IA", "avancado",
     "Inteligência artificial desenvolvida para o jeito de trabalhar da sua empresa.",
     ["Agentes de IA personalizados", "Assistentes internos de IA", "Sistemas personalizados"]),
]

# as 4 frentes oficiais da empresa (Início): (título, ícone, resumo, módulo que abre, serviços)
AREAS = [
    ("Atendimento e relacionamento", "conversa",
     "Chatbots no WhatsApp e no Instagram, respostas automáticas e triagem para atendentes.", "whatsapp",
     ["Chatbots inteligentes", "Respostas inteligentes", "Triagem de atendimento"]),
    ("Vendas e captação de clientes", "vendas",
     "Leads qualificados, agendamentos, follow-up e orçamentos no automático.", "agenda",
     ["Captação e qualificação de leads", "Agendamentos automáticos", "Follow-up inteligente", "Orçamentos automatizados"]),
    ("Administração e gestão empresarial", "gestao",
     "Cadastros, pedidos, CRM, relatórios, documentos e sistemas conectados.", "gestao",
     ["Gestão de cadastros e pedidos", "Integração com CRM", "Relatórios automatizados", "Automação de documentos",
      "Assistentes internos de IA", "Integração de sistemas"]),
    ("Soluções avançadas e personalizadas", "avancado",
     "Agentes de IA, integração com ERP e sistemas sob medida para a sua empresa.", "ia",
     ["Agentes de IA personalizados", "Integração com estoque e ERP", "Centrais inteligentes de atendimento",
      "Automação de processos comerciais", "Sistemas personalizados"]),
]

# ------------------------------------------------------------------ ramos (cartões com janela)
RAMOS = [
    ("lanchonete", "Lanchonetes", "lanche", "uma lanchonete", "Pedido anotado sem parar o caixa.",
     "Pedidos, dúvidas e clientes atendidos sem parar o caixa.", [
        ("Chatbot no WhatsApp e no Instagram", "Recebe os pedidos e apresenta o cardápio a qualquer hora, inclusive no horário de pico."),
        ("Respostas inteligentes", "Horário de funcionamento, endereço, entrega e formas de pagamento respondidos na hora."),
        ("Gestão de pedidos", "Cada pedido chega organizado, sem anotação perdida em papel."),
        ("Follow-up inteligente", "Chama de volta o cliente que não pede há algum tempo."),
        ("Relatórios automatizados", "Pedidos e vendas do período reunidos para você acompanhar."),
        ("Integração com estoque", "Os pedidos conversando com o controle do que tem na cozinha."),
    ]),
    ("barbearia", "Barbearias", "tesoura", "uma barbearia", "Agenda cheia sem largar a máquina.",
     "Agenda cheia e organizada, sem responder mensagem entre um corte e outro.", [
        ("Agendamentos automáticos", "O cliente escolhe o serviço e o horário direto na conversa."),
        ("Chatbot no WhatsApp e no Instagram", "Atende quem chama de noite, no domingo ou enquanto você está cortando."),
        ("Respostas inteligentes", "Preços, serviços e horários livres respondidos na hora."),
        ("Follow-up inteligente", "Lembra o cliente do horário e chama de volta quem já está na hora do próximo corte."),
        ("Cadastro de clientes e CRM", "Histórico de cada cliente guardado em um só lugar."),
        ("Relatórios automatizados", "Atendimentos e faturamento do período para acompanhar o negócio."),
    ]),
    ("salao", "Salões de beleza", "pente", "um salão de beleza", "Horário marcado com cada profissional.",
     "Agenda de cada profissional organizada e cliente bem atendida do primeiro contato ao retorno.", [
        ("Agendamentos automáticos", "Marcação por serviço e por profissional, sem conflito de horário."),
        ("Respostas inteligentes", "Serviços, preços e duração de cada procedimento respondidos na hora."),
        ("Triagem de atendimento", "Pedidos que precisam de avaliação vão direto para a pessoa certa da equipe."),
        ("Orçamentos automatizados", "Propostas para pacotes, eventos e noivas montadas e enviadas."),
        ("Follow-up inteligente", "Lembretes de horário e convite de retorno para manutenção."),
        ("Cadastro de clientes e CRM", "Preferências e histórico de cada cliente sempre à mão."),
    ]),
    ("consultorio", "Clínicas", "dente", "uma clínica", "Consulta confirmada sem a recepção ligar.",
     "Recepção mais leve, agenda confirmada e pacientes acompanhados, de consultórios a clínicas.", [
        ("Agendamentos automáticos", "Marcação e confirmação de consultas pelo WhatsApp."),
        ("Triagem de atendimento", "Identifica se é avaliação, retorno ou urgência e encaminha para a recepção."),
        ("Respostas inteligentes", "Convênios, endereço, horários e tipos de tratamento respondidos na hora."),
        ("Follow-up inteligente", "Lembrete de consulta e de retorno para exames e revisões."),
        ("Automação de documentos", "Envio automático de orientações e documentos ao paciente."),
        ("Cadastro de pacientes e CRM", "Informações de cada paciente organizadas, com cuidado com os dados (LGPD)."),
    ]),
    ("petshop", "Pet shops", "pata", "um pet shop", "Banho e tosa marcados, sem perder mensagem.",
     "Agenda de banho e tosa organizada, tutores lembrados da vacina e pedidos de ração sem se perder no WhatsApp.", [
        ("Agendamentos automáticos", "Banho, tosa e consulta marcados direto na conversa, sem choque de horário."),
        ("Chatbot no WhatsApp e no Instagram", "Atende a qualquer hora quem quer saber de serviço, preço e horário."),
        ("Respostas inteligentes", "Valores de banho e tosa, vacinas, produtos e horários respondidos na hora."),
        ("Follow-up inteligente", "Lembra o tutor da vacina, do vermífugo e do próximo banho do pet."),
        ("Gestão de pedidos", "Pedidos de ração e de produtos organizados, para retirar na loja ou receber em casa."),
        ("Cadastro de pets e tutores", "Histórico de cada pet e dados do tutor guardados em um só lugar."),
    ]),
]

# fotos de banco (Unsplash, licença livre; origem em assets/fotos/CREDITOS.md): arquivo, largura, altura
FOTO_RAMO = {
    "lanchonete": ("lanchonete.jpg", 1200, 675),
    "barbearia": ("barbearia.jpg", 880, 1100),
    "salao": ("salao.jpg", 734, 1100),
    "consultorio": ("consultorio.jpg", 1200, 800),
    "petshop": ("petshop.jpg", 1200, 900),
}

# ------------------------------------------------------------------ partes comuns
def menu(atual, classe):
    itens = []
    for arq, nome in PAGINAS:
        cur = ' aria-current="page"' if arq == atual else ""
        itens.append(f'<li><a href="{arq}"{cur}>{nome}</a></li>')
    c = f' class="{classe}"' if classe else ""
    return f'<ul{c}>' + "".join(itens) + "</ul>"

MENU_DESCRICAO = {"index.html": "Soluções, demonstrações e segmentos", "servicos.html": "Catálogo completo de serviços",
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
    partes = "".join(f'<span class="relogio-parte"><b data-{k}>00</b><small>{n}</small></span>' for k, n in
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
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Kyzent Technology Solutions",
    "alternateName": "Kyzent", "url": BASE, "logo": BASE + "assets/icons/apple-touch-icon.png", "image": BASE + "assets/og-image.png",
    "description": "Empresa de Tecnologia e Inovação que automatiza o atendimento, as vendas e a gestão de pequenas empresas com Inteligência Artificial.",
    "telephone": "+55-19-98872-8894", "areaServed": "Paulínia e região, SP",
    "address": {"@type": "PostalAddress", "addressLocality": "Paulínia", "addressRegion": "SP", "addressCountry": "BR"},
    "sameAs": ["https://www.instagram.com/kyzent.tech/"]}, ensure_ascii=False)

def pagina(arq, titulo, descricao, corpo, janelas="", ativo=None):
    url = BASE + ("" if arq == "index.html" else arq)
    ativo = ativo or arq
    servicos_rodape = "".join(f'<li><a href="{PAGINA_MOD[mid]}">{nome}</a></li>' for mid, nome, *_ in MODULOS)
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark">
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

  <script>document.documentElement.classList.add("js");</script>
  <link rel="preload" href="assets/fonts/mona-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css?v={VERSAO}">
  <script src="js/main.js?v={VERSAO}" defer></script>
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
          <p>Empresa de Tecnologia e Inovação de Paulínia/SP. Automação e Inteligência Artificial para o atendimento, as vendas e a gestão de pequenas empresas.</p>
          <a class="botao botao-contorno" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}{BOTAO}</a>
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
            <li><a href="{link_whats(None, 0)}" target="_blank" rel="noopener">WhatsApp {WHATS[0][1]}</a></li>
            <li><a href="{link_whats(None, 1)}" target="_blank" rel="noopener">WhatsApp {WHATS[1][1]}</a></li>
            <li><a href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">Instagram @kyzent.tech</a></li>
          </ul>
        </div>
      </div>
      <div class="rodape-base">
        <p>© <span data-ano>2026</span> Kyzent Technology Solutions. Todos os direitos reservados.</p>
        <p>Paulínia/SP</p>
      </div>
    </div>
  </footer>
  <a class="whats-flutuante" href="{link_whats()}" target="_blank" rel="noopener" data-contato aria-label="{BOTAO}">{I["conversa"]}<span>Fale com a gente</span></a>
  <div class="barra-fixa">
    <a class="whats-fixo" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}<span class="whats-longo">{BOTAO}</span><span class="whats-curto">WhatsApp</span></a>
  </div>

{JANELAS_GERAIS}
{janelas}
</body>
</html>
"""

# ------------------------------------------------------------------ blocos comuns
def chamada(titulo="Vamos transformar a maneira como sua empresa trabalha?"):
    return f"""    <section class="chamada" aria-labelledby="titulo-chamada">
      <div class="container">
        <div class="chamada-caixa revelar-bloco">
          <svg class="chamada-orbita" viewBox="0 0 800 400" aria-hidden="true"><ellipse cx="400" cy="200" rx="380" ry="110" transform="rotate(-24 400 200)"/><ellipse cx="400" cy="200" rx="300" ry="80" transform="rotate(-24 400 200)"/></svg>
          <div class="chamada-texto">
            <p class="hero-bf" data-promo><span class="hero-bf-selo">Black Friday</span><span>Implantação grátis até {PROMO_DATA}</span></p>
            <h2 id="titulo-chamada" data-revelar-texto>{titulo}</h2>
            <p>Conte como é o seu dia a dia. A gente responde no WhatsApp e monta um orçamento personalizado para a sua empresa.</p>
            <div data-promo>{relogio("relogio-claro")}</div>
          </div>
          <div class="chamada-acoes">
            <a class="botao botao-grande botao-claro" href="{link_whats(MSG_BF)}" target="_blank" rel="noopener" data-contato data-msg="{MSG_BF}" data-fora-msg="Olá, vim pelo site da Kyzent e quero começar um projeto." data-magnetico>Comece seu projeto com a Kyzent</a>
            <a class="link-seta" href="servicos.html#catalogo">Ver todos os serviços</a>
          </div>
        </div>
      </div>
    </section>"""

ETAPAS = [
    ("Diagnóstico", "busca", "Entendemos as necessidades do negócio: como você atende, vende e organiza o dia."),
    ("Planejamento", "mapa", "Identificamos oportunidades de melhoria e definimos o que vale automatizar primeiro."),
    ("Desenvolvimento", "codigo", "Construímos soluções adequadas ao seu negócio, com o seu jeito de atender."),
    ("Implementação", "foguete", "Colocamos as soluções em funcionamento, junto com a sua equipe."),
    ("Suporte e evolução", "repetir", "Acompanhamos os resultados, fazemos a manutenção e evoluímos as soluções."),
]
def como_trabalhamos(faixa=True):
    passos = "\n".join(
        f'          <li class="etapa"><span class="etapa-marca"><span class="etapa-icone">{I[ic]}</span></span>'
        f'<div class="etapa-cartao"><span class="etapa-num">Etapa {i+1}</span><span class="etapa-grande" aria-hidden="true">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, ic, d) in enumerate(ETAPAS))
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

PILARES = f"""    <section class="secao claro" aria-labelledby="titulo-pilares">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-pilares" data-revelar-texto>Missão, visão e valores.</h2>
        </div>
        <div class="grade grade-3">
          <article class="pilar brilho">
            <span class="pilar-icone">{I["alvo"]}</span>
            <h3>Nossa missão</h3>
            <p>Oferecer soluções tecnológicas que promovam produtividade, automação e crescimento, otimizando processos e potencializando os resultados dos nossos clientes.</p>
          </article>
          <article class="pilar brilho">
            <span class="pilar-icone">{I["olho"]}</span>
            <h3>Nossa visão</h3>
            <p>Ser referência em Tecnologia e Inovação, reconhecida por transformar negócios e contribuir para a evolução do mercado.</p>
          </article>
          <article class="pilar brilho">
            <span class="pilar-icone">{I["valores"]}</span>
            <h3>Nossos valores</h3>
            <p>Atuar com respeito, ética e compromisso com nossos clientes e colaboradores, construindo relações sólidas e duradouras, pautadas na lealdade, transparência e dignidade.</p>
          </article>
        </div>
      </div>
    </section>"""

FAIXA_PALAVRAS = ["Black Friday Kyzent", f"Implantação grátis até {PROMO_DATA}", "Atendimento 24 horas no WhatsApp",
                  "Agendamentos automáticos", "Pedidos organizados", "IA sob medida", "Relatórios automáticos", "Suporte da nossa equipe"]
def faixa_animada():
    itens = "".join(f'<li>{p}<span class="faixa-orbita"></span></li>' for p in FAIXA_PALAVRAS)
    return f"""    <div class="faixa-animada" aria-hidden="true" data-promo>
      <ul class="faixa-trilho">{itens}{itens}</ul>
    </div>"""

# perguntas frequentes (texto do Claude a partir do KYZENT.md; os sócios precisam confirmar)
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
     "Lanchonetes, barbearias, salões de beleza, clínicas, pet shops e comércios parecidos, em Paulínia e região. Se o seu ramo não está na lista, chame no WhatsApp e conte como é o seu dia a dia."),
]
def perguntas():
    itens = "\n".join(
        f'          <details class="pergunta"{" open" if i == 0 else ""}><summary><span>{q}</span><span class="pergunta-icone">{I["mais"]}</span></summary><div class="pergunta-resposta"><p>{r}</p></div></details>'
        for i, (q, r) in enumerate(PERGUNTAS))
    return f"""    <section class="secao" id="perguntas" aria-labelledby="titulo-perguntas">
      <div class="container perguntas-grade">
        <div class="cabeca">
          <h2 id="titulo-perguntas" data-revelar-texto>Perguntas frequentes.</h2>
          <p>Ficou alguma dúvida? A gente responde no WhatsApp.</p>
          <a class="botao botao-contorno" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}{BOTAO}</a>
        </div>
        <div class="perguntas">
{itens}
        </div>
      </div>
    </section>"""

# demonstrações (todas exemplos ilustrativos)
PEDIDOS_DEMO = [("#1043", "Marina", "2 marmitas", "preparo", "Em preparo"),
                ("#1042", "Carlos", "1 X-salada e 1 suco", "rota", "Saiu para entrega"),
                ("#1041", "Ana", "3 pastéis", "ok", "Entregue")]
SEMANA = [("Seg", 42), ("Ter", 55), ("Qua", 48), ("Qui", 63), ("Sex", 86), ("Sáb", 100), ("Dom", 71)]
def demo_gestao():
    pedidos = "".join(f'<li><span class="pd-num">{n}</span><span class="pd-quem"><strong>{q}</strong><small>{o}</small></span><span class="estado estado-{c}">{e}</span></li>'
                      for n, q, o, c, e in PEDIDOS_DEMO)
    barras = "".join(f'<div class="gd-barra"><i style="--h:{h}%;--d:{k*70}ms"></i><small>{d}</small></div>' for k, (d, h) in enumerate(SEMANA))
    return f"""<figure class="demo-visual">
            <div class="gd" data-gestao role="img" aria-label="Exemplo ilustrativo de painel de gestão com pedidos, gráfico da semana, lista de pedidos e o andamento de um processo.">
              <div class="gd-topo" aria-hidden="true"><strong>Painel da semana</strong><span>Atualizado às 18:40</span></div>
              <div class="gd-kpis" aria-hidden="true">
                <div><small>Pedidos</small><strong data-contar="312">312</strong></div>
                <div><small>Clientes novos</small><strong data-contar="46">46</strong></div>
                <div><small>Entregas no prazo</small><strong><span data-contar="96">96</span>%</strong></div>
              </div>
              <div class="gd-meio" aria-hidden="true">
                <div class="gd-grafico"><p>Pedidos por dia</p><div class="gd-barras">{barras}</div></div>
                <div class="gd-processo">
                  <p>Processos</p>
                  <div class="gd-proc"><span>Reposição de estoque</span><span class="gd-trilho"><i style="--p:72%"></i></span><small>72%</small></div>
                  <div class="gd-proc"><span>Notas do mês</span><span class="gd-trilho"><i style="--p:45%"></i></span><small>45%</small></div>
                  <div class="gd-proc"><span>Retornos agendados</span><span class="gd-trilho"><i style="--p:90%"></i></span><small>90%</small></div>
                </div>
              </div>
              <ul class="gd-pedidos" aria-hidden="true">{pedidos}</ul>
            </div>
            <figcaption><span class="selo-exemplo">Exemplo ilustrativo com dados fictícios</span></figcaption>
          </figure>"""

FLUXO_IA = [("busca", "Entende o pedido", "2 marmitas, sexta, entrega ao meio-dia"),
            ("estoque", "Confere o estoque", "Ingredientes disponíveis"),
            ("agenda", "Agenda a entrega", "Sexta, 12h, na rota do centro"),
            ("conversa", "Responde e avisa a equipe", "Cliente confirmado, cozinha avisada")]
def demo_ia():
    passos = "".join(f'<li class="fluxo-passo" data-passo><span class="fluxo-icone">{I[ic]}</span><span><strong>{t}</strong><small>{d}</small></span><span class="fluxo-ok">{I["check"]}</span></li>'
                     for ic, t, d in FLUXO_IA)
    return f"""<figure class="demo-visual">
            <div class="fluxo" data-fluxo role="img" aria-label="Exemplo ilustrativo: a IA recebe a mensagem de um cliente, entende o pedido, confere o estoque, agenda a entrega e responde o cliente.">
              <div class="fluxo-entrada" aria-hidden="true"><small>Mensagem recebida</small><p>"Quero 2 marmitas para sexta, com entrega ao meio-dia."</p></div>
              <div class="fluxo-nucleo" aria-hidden="true"><span class="fluxo-orbita"></span>{I["avancado"]}<strong>Assistente de IA</strong></div>
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

# ------------------------------------------------------------------ soluções (uma página para cada módulo)
# textos comerciais escritos pelo Claude a partir do catálogo oficial; os sócios precisam confirmar
PAGINA_MOD = {"whatsapp": "solucao-atendimento.html", "agenda": "solucao-vendas.html", "gestao": "solucao-gestao.html",
              "site": "solucao-site.html", "ia": "solucao-ia.html"}
SOLUCOES = {
    "whatsapp": ("Atendimento com IA no WhatsApp e no Instagram",
                 "Seu cliente é respondido a qualquer hora, com as informações do seu negócio, e a sua equipe só entra quando precisa.",
                 ["Respostas na hora, inclusive à noite e no fim de semana", "Menos mensagens repetidas para a equipe responder", "Pedidos de atendimento humano chegam organizados"],
                 ["Mensagens acumulando no horário de pico", "As mesmas perguntas respondidas o dia inteiro", "Cliente que desiste porque ninguém respondeu"]),
    "agenda": ("Agendamento e vendas no automático",
               "Horários marcados e confirmados pela conversa, clientes lembrados de voltar e orçamentos enviados sem você parar o que está fazendo.",
               ["Agenda organizada, com confirmação e lembrete", "Clientes antigos chamados de volta no momento certo", "Orçamentos e propostas enviados com rapidez"],
               ["Horário marcado em papel ou de cabeça", "Cliente que falta sem avisar", "Oportunidade perdida por falta de retorno"]),
    "gestao": ("Gestão e sistemas conectados",
               "Pedidos, cadastros, documentos e relatórios organizados, com os sistemas que você já usa conversando entre si.",
               ["Informações de clientes e pedidos num lugar só", "Relatórios prontos para acompanhar o negócio", "Menos digitação repetida entre um sistema e outro"],
               ["Planilhas soltas e anotações perdidas", "Dados digitados duas vezes em sistemas diferentes", "Dificuldade para saber como o mês está indo"]),
    "site": ("Site sob medida para o seu negócio",
             "Um site feito para o seu negócio, com o que os seus clientes procuram e o caminho direto para o WhatsApp.",
             ["Presença profissional na internet", "Serviços, horários e contato num lugar só", "Visitante levado direto para a conversa"],
             ["Cliente que não encontra o seu negócio na internet", "Informações espalhadas em várias redes", "Perfil que não passa a imagem que o negócio merece"]),
    "ia": ("IA sob medida para a sua empresa",
           "Agentes e assistentes de inteligência artificial desenvolvidos para o jeito de trabalhar da sua empresa, integrados aos seus sistemas.",
           ["Tarefas repetitivas feitas por um assistente", "Equipe com apoio para consultar e organizar informações", "Solução desenhada para o seu processo, não um pacote pronto"],
           ["Processos que nenhum sistema pronto resolve", "Equipe sobrecarregada com tarefas manuais", "Informação difícil de encontrar na hora certa"]),
}
MOD = {mid: (nome, curto, ic, resumo, servs) for mid, nome, curto, ic, resumo, servs in MODULOS}

def msg_modulo(mid):
    return f"Olá, vim pelo site da Kyzent e quero um orçamento de {MOD[mid][0].lower()}."

def cartao_solucao(mid, destaque=False):
    nome, curto, ic, resumo, servs = MOD[mid]
    titulo, chamada_txt, benef, _ = SOLUCOES[mid]
    lis = "".join(f"<li>{I['check']}{b}</li>" for b in benef)
    selo = '<span class="plano-selo">Porta de entrada</span>' if destaque else ""
    return (f'<li><article class="solucao brilho{" solucao-destaque" if destaque else ""}">{selo}'
            f'<div class="solucao-topo"><span class="frente-icone">{I[ic]}</span>'
            f'<span class="solucao-tag" data-promo>Implantação grátis até {PROMO_DATA}</span></div>'
            f'<h3>{titulo}</h3><p>{chamada_txt}</p><ul class="frente-itens">{lis}</ul>'
            f'<p class="solucao-qtd">{len(servs)} {"serviço" if len(servs) == 1 else "serviços"} nesta solução</p>'
            f'<div class="solucao-acoes"><a class="botao{"" if destaque else " botao-contorno"}" href="{PAGINA_MOD[mid]}">Conhecer a solução</a>'
            f'<a class="link-seta" href="{link_whats(msg_modulo(mid))}" target="_blank" rel="noopener" data-contato data-msg="{msg_modulo(mid)}">Pedir orçamento</a></div>'
            f'</article></li>')

SOLUCOES_SECAO = f"""    <section class="secao claro" id="solucoes" aria-labelledby="titulo-solucoes">
      <div class="container">
        <div class="cabeca-linha">
          <div class="cabeca">
            <h2 id="titulo-solucoes" data-revelar-texto>Soluções para cada parte do seu negócio.</h2>
            <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
          </div>
          <a class="link-seta" href="servicos.html#catalogo">Ver o catálogo completo</a>
        </div>
        <ul class="solucoes carrossel" data-carrossel aria-label="Soluções da Kyzent">
          {"".join(cartao_solucao(mid, i == 0) for i, mid in enumerate(MOD))}
        </ul>
      </div>
    </section>"""

# ------------------------------------------------------------------ central de demonstrações (simulações)
ROTEIRO = {
    "inicio": {"msg": ["Olá! Sou o assistente virtual da Barbearia Exemplo.", "Como posso ajudar?"],
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
              <div class="chat-topo"><span class="chat-avatar">{I["avancado"]}</span><span class="chat-nome"><strong>Assistente virtual</strong><small data-chat-estado>online</small></span></div>
              <div class="chat-corpo" data-chat-corpo aria-live="polite"><p class="demo-sem-js">Ative o JavaScript para conversar com o assistente.</p></div>
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
                <li><time>09:00</time><span><strong>Ana</strong><small>Escova</small></span><em class="estado estado-ok">Confirmado</em></li>
                <li><time>11:00</time><span><strong>Júlia</strong><small>Manicure</small></span><em class="estado estado-ok">Confirmado</em></li>
              </ul></div>
            </div>"""

CARDAPIO = [("X-salada", 22), ("X-bacon", 26), ("Porção de batata", 15), ("Refrigerante lata", 6)]
def tela_pedidos():
    itens = "".join(
        f'<li data-produto="{n}" data-preco="{p}"><span><strong>{n}</strong><small>R$ {p},00</small></span>'
        f'<span class="pd-qtd"><button type="button" data-menos aria-label="Tirar um {n}">−</button><output data-qtd>0</output>'
        f'<button type="button" data-mais aria-label="Pôr mais um {n}">+</button></span></li>' for n, p in CARDAPIO)
    return f"""<div class="pd" data-pedidos>
              <div class="pd-cardapio"><p class="pd-titulo">Cardápio da Lanchonete Exemplo</p><ul>{itens}</ul>
                <div class="pd-total"><span>Total</span><strong data-pd-total>R$ 0,00</strong></div>
                <button type="button" class="botao" data-pd-registrar disabled>Registrar pedido</button></div>
              <div class="pd-fila"><p class="pd-titulo">Pedidos de hoje</p><ul data-pd-lista aria-live="polite">
                <li><span class="pd-num">#1042</span><span><strong>Carlos</strong><small>1 X-salada, 1 refrigerante</small></span><em class="estado estado-rota">Saiu para entrega</em></li>
                <li><span class="pd-num">#1041</span><span><strong>Ana</strong><small>2 porções de batata</small></span><em class="estado estado-ok">Entregue</em></li>
              </ul></div>
            </div>"""

CLIENTES = [("Marina Lopes", "recorrente", "Último atendimento há 6 dias"), ("Carlos Souza", "inativo", "Sem visita há 42 dias"),
            ("Ana Ribeiro", "novo", "Primeiro atendimento ontem"), ("João Pereira", "recorrente", "Último atendimento há 12 dias"),
            ("Paula Martins", "inativo", "Sem visita há 35 dias"), ("Rita Alves", "novo", "Primeiro atendimento há 3 dias"),
            ("Lucas Ferreira", "recorrente", "Último atendimento há 9 dias"), ("Bia Santos", "inativo", "Sem visita há 60 dias")]
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
    ("chatbot", "Chatbot", "conversa", "Atendimento com IA", "Escolha as respostas e veja o assistente conduzir a conversa: agendar, informar preços ou passar para uma pessoa da equipe.", "whatsapp", tela_chatbot),
    ("agendamento", "Agendamento", "agenda", "Agendamento automático", "Escolha o serviço, o dia e o horário. O agendamento entra na agenda e o lembrete fica programado.", "agenda", tela_agendamento),
    ("pedidos", "Pedidos", "lanche", "Registro de pedidos", "Monte um pedido no cardápio e registre. Ele entra na fila da cozinha com o total calculado.", "gestao", tela_pedidos),
    ("clientes", "Clientes", "olho", "Organização de clientes", "Busque, filtre e envie um lembrete para quem não aparece há algum tempo.", "agenda", tela_clientes),
    ("painel", "Painel", "grafico", "Painel administrativo", "Pedidos, clientes, processos e indicadores reunidos num painel atualizado sozinho.", "gestao", demo_gestao),
    ("automacao", "Automação", "avancado", "Automação de processos", "A IA entende o pedido, consulta os sistemas, organiza a tarefa e avisa quem precisa saber.", "ia", demo_ia),
]
def central_demos(ids=None, titulo="Veja a Kyzent funcionando.", classe=""):
    abas_ = [a for a in ABAS_DEMO if ids is None or a[0] in ids]
    botoes, paineis_ = [], []
    for i, (did, curto, ic, titulo_aba, texto, mod, tela) in enumerate(abas_):
        sel = i == 0
        botoes.append(f'<button type="button" class="demo-aba" role="tab" id="daba-{did}" aria-controls="dpainel-{did}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}">{I[ic]}<span>{curto}</span></button>')
        paineis_.append(f"""          <div class="demo-painel" id="dpainel-{did}" role="tabpanel" aria-labelledby="daba-{did}"{"" if sel else " hidden"}>
            <div class="demo-info">
              <span class="selo-exemplo">Simulação demonstrativa</span>
              <h3>{titulo_aba}</h3>
              <p>{texto}</p>
              <a class="link-seta" href="{PAGINA_MOD[mod]}">Conhecer a solução</a>
            </div>
            <div class="demo-tela">{tela()}</div>
          </div>""")
    abas_html = "" if len(abas_) == 1 else f'<div class="demo-abas" role="tablist" aria-label="Demonstrações">{"".join(botoes)}</div>'
    return f"""    <section class="secao secao-demos {classe}" id="demonstracoes" aria-labelledby="titulo-demos">
      <div class="container">
        <div class="cabeca cabeca-centro">
          <h2 id="titulo-demos" data-revelar-texto>{titulo}</h2>
          <p>Simulações demonstrativas, com dados fictícios. Toque, escolha e veja o que acontece.</p>
        </div>
        <div class="demo-centro" data-demo-centro>
          {abas_html}
{chr(10).join(paineis_)}
        </div>
      </div>
    </section>"""

# ------------------------------------------------------------------ segmentos (texto do Claude, a confirmar)
SEGMENTOS = [
    ("lanchonete", "Restaurantes e lanchonetes", "lanche", "lanchonete.jpg", (1200, 675), "um restaurante ou lanchonete",
     ["Pedidos chegando por mensagem no horário de pico", "Cardápio, horário e taxa de entrega perguntados o dia todo", "Anotação em papel que se perde"],
     ["Chatbot que apresenta o cardápio e anota o pedido", "Respostas automáticas para horário, endereço e entrega", "Pedidos organizados e ligados ao estoque"],
     ["Caixa livre para atender quem está no balcão", "Pedidos organizados do recebimento à entrega", "Cliente respondido mesmo fora do horário"]),
    ("barbearia", "Barbearias", "tesoura", "barbearia.jpg", (880, 1100), "uma barbearia",
     ["Responder mensagem no meio de um corte", "Horários vagos por falta de lembrete", "Cliente que demora a voltar"],
     ["Agendamento direto na conversa", "Lembrete antes do horário", "Mensagem chamando o cliente para o próximo corte"],
     ["Agenda mais organizada", "Menos interrupções durante o atendimento", "Relacionamento contínuo com cada cliente"]),
    ("salao", "Salões de beleza", "pente", "salao.jpg", (734, 1100), "um salão de beleza",
     ["Agenda de várias profissionais ao mesmo tempo", "Dúvidas sobre preço e duração de cada serviço", "Orçamentos de pacotes e eventos"],
     ["Marcação por serviço e por profissional", "Respostas com preços e duração", "Orçamentos montados e enviados automaticamente"],
     ["Menos conflito de horário", "Clientes bem informadas antes de chegar", "Mais tempo da equipe para o atendimento"]),
    ("consultorio", "Clínicas", "cruz", "consultorio.jpg", (1200, 800), "uma clínica",
     ["Recepção sobrecarregada com ligações e mensagens", "Pacientes que esquecem a consulta", "Orientações enviadas uma a uma"],
     ["Marcação e confirmação de consultas pelo WhatsApp", "Triagem entre avaliação, retorno e urgência", "Envio automático de orientações e documentos"],
     ["Recepção mais leve", "Agenda confirmada com antecedência", "Dados dos pacientes tratados com cuidado (LGPD)"]),
    ("petshop", "Pet shops", "pata", "petshop.jpg", (1200, 900), "um pet shop",
     ["Banho e tosa marcados por mensagem solta", "Tutores que esquecem vacina e vermífugo", "Pedidos de ração perdidos na conversa"],
     ["Agendamento de banho, tosa e consulta", "Lembretes de vacina, vermífugo e próximo banho", "Pedidos de produtos organizados"],
     ["Agenda sem choque de horário", "Tutores lembrados no momento certo", "Histórico de cada pet num lugar só"]),
    ("empresa", "Pequenas e médias empresas", "gestao", "equipe-computador.jpg", (1600, 900), "uma empresa",
     ["Processos manuais repetidos todos os dias", "Informações espalhadas em planilhas e sistemas", "Atendimento que não acompanha o crescimento"],
     ["Automação de processos comerciais", "Integração com CRM, estoque e ERP", "Agentes de IA e sistemas sob medida"],
     ["Equipe focada no que exige pessoas", "Informações conectadas para decidir melhor", "Tecnologia que acompanha o crescimento da empresa"]),
]
def segmentos_secao(classe="claro"):
    chips, paineis_ = [], []
    for i, (sid, nome, ic, arq, (w, h), artigo, desafios, solucoes, beneficios) in enumerate(SEGMENTOS):
        chips.append(f'<button type="button" class="seg-chip" data-seg="{sid}" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="seg-{sid}">{I[ic]}<span>{nome}</span></button>')
        msg = f"Olá, vim pelo site da Kyzent. Tenho {artigo} e quero saber o que vocês podem automatizar."
        col = lambda titulo, itens, cls: f'<div class="seg-col {cls}"><h4>{titulo}</h4><ul>' + "".join(f"<li>{x}</li>" for x in itens) + "</ul></div>"
        paineis_.append(f"""          <article class="seg-painel{" ativo" if i == 0 else ""}" id="seg-{sid}" aria-labelledby="seg-{sid}-titulo">
            <div class="seg-foto">{foto(arq, w, h, sizes="(max-width: 760px) 100vw, 40vw")}<span class="seg-icone">{I[ic]}</span></div>
            <div class="seg-texto">
              <h3 id="seg-{sid}-titulo">{nome}</h3>
              <div class="seg-colunas">
                {col("Desafios comuns", desafios, "seg-desafios")}
                {col("Como a Kyzent ajuda", solucoes, "seg-solucoes")}
                {col("O que melhora", beneficios, "seg-beneficios")}
              </div>
              <div class="seg-acoes">
                <a class="botao" href="orcamento.html?ramo={sid}">Simular o meu orçamento</a>
                <a class="link-seta" href="{link_whats(msg)}" target="_blank" rel="noopener" data-contato data-msg="{msg}">Conversar no WhatsApp</a>
              </div>
            </div>
          </article>""")
    return f"""    <section class="secao {classe}" id="segmentos" aria-labelledby="titulo-segmentos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-segmentos" data-revelar-texto>Tecnologia para o seu tipo de negócio.</h2>
          <p>Escolha o seu segmento e veja os desafios mais comuns e como a automação pode ajudar. Os benefícios dependem de cada negócio e do que for automatizado.</p>
        </div>
        <div class="seg-chips" role="group" aria-label="Segmentos" data-segmentos>{"".join(chips)}</div>
        <div class="seg-paineis">
{chr(10).join(paineis_)}
        </div>
      </div>
    </section>"""

# ------------------------------------------------------------------ metodologia, diferenciais e projetos
DIFERENCIAIS = [
    ("escudo", "WhatsApp pela API oficial", "Conexão aprovada pela Meta, sem atalhos que coloquem o número da sua empresa em risco."),
    ("medida", "Feito para o seu negócio", "Cada automação é configurada com os seus produtos, preços, horários e jeito de atender."),
    ("suporte", "Manutenção e suporte", "A nossa equipe acompanha cada solução depois de pronta, para a tecnologia seguir funcionando."),
    ("orcamento", "Mensalidade, sem contratação", "Você assina um serviço que trabalha junto com a sua equipe, em vez de contratar mais gente."),
]
def diferenciais(classe=""):
    cards = "\n".join(f'          <li class="diferencial brilho"><span class="pilar-icone">{I[ic]}</span><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in DIFERENCIAIS)
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

# Projetos reais entram aqui, com a autorização de cada cliente: (nome, segmento, o que foi feito, foto ou "")
PROJETOS = []
def projetos_secao():
    if PROJETOS:
        cards = "".join(f'<li class="projeto"><h3>{n}</h3><p class="projeto-seg">{s}</p><p>{d}</p></li>' for n, s, d, _ in PROJETOS)
    else:
        cards = "".join(f'<li class="projeto projeto-vazio" aria-hidden="true"><span class="projeto-linha"></span><span class="projeto-linha curta"></span><span class="projeto-linha"></span></li>' for _ in range(2))
    return f"""    <section class="secao claro" id="projetos" aria-labelledby="titulo-projetos">
      <div class="container">
        <div class="projetos-grade">
          <div class="cabeca">
            <h2 id="titulo-projetos" data-revelar-texto>Projetos e cases.</h2>
            <p>Os cases da Kyzent aparecem aqui, com o que foi feito em cada negócio, sempre com a autorização do cliente. Não publicamos números nem depoimentos que não sejam reais.</p>
          </div>
          <ul class="projetos">
            {cards}
            <li class="projeto projeto-chamada"><span class="pilar-icone">{I["foguete"]}</span><h3>O seu negócio pode ser o próximo.</h3><p>Conte como funciona o seu dia a dia e receba uma recomendação de solução.</p><a class="botao" href="orcamento.html">Simular o meu orçamento</a></li>
          </ul>
        </div>
      </div>
    </section>"""

# ------------------------------------------------------------------ Início (Kyzent 2.0)
MSG_ESPECIALISTA = "Olá, vim pelo site da Kyzent e quero falar com um especialista."
HERO = f"""    <section class="hero hero-cinema" aria-labelledby="titulo-inicio">
      <div class="hero-fundo" aria-hidden="true">
        <div class="hero-gradiente"></div>
        <canvas class="hero-rede" data-rede></canvas>
      </div>
      <div class="container hero-grade">
        <div class="hero-texto">
          <p class="hero-bf" data-promo><span class="hero-bf-selo">Black Friday</span><span>Implantação grátis até {PROMO_DATA}</span></p>
          <h1 id="titulo-inicio" data-revelar-texto>Seu negócio no próximo nível.</h1>
          <p class="hero-apoio">Inteligência artificial, automação e tecnologia para transformar a maneira como sua empresa trabalha, vende e cresce.</p>
          <div class="hero-acoes">
            <a class="botao botao-grande" href="#solucoes" data-magnetico>Conhecer nossas soluções</a>
            <a class="botao botao-grande botao-vidro" href="{link_whats(MSG_ESPECIALISTA)}" target="_blank" rel="noopener" data-contato data-msg="{MSG_ESPECIALISTA}" data-magnetico>{I["conversa"]}Falar com um especialista</a>
          </div>
          <div class="hero-oferta-linha" data-promo><p><strong>Implantação grátis</strong> para quem fechar até {PROMO_DATA}.</p>{relogio("relogio-mini")}</div>
        </div>
        <div class="hero-esfera" aria-hidden="true">
          <div class="esfera-luz"></div>
          <canvas class="esfera" data-esfera></canvas>
          <div class="hero-flutua vidro hero-flutua-1"><span class="flutua-icone">{I["conversa"]}</span><span><strong>Atendimento 24 h</strong><small>WhatsApp e Instagram</small></span></div>
          <div class="hero-flutua vidro hero-flutua-2"><span class="flutua-icone">{I["agenda"]}</span><span><strong>Agenda organizada</strong><small>Confirmação e lembrete</small></span></div>
          <div class="hero-flutua vidro hero-flutua-3"><span class="flutua-icone">{I["grafico"]}</span><span><strong>Relatórios</strong><small>Os números do negócio</small></span></div>
        </div>
      </div>
      <a class="rolar" href="#solucoes"><span class="rolar-mouse" aria-hidden="true"><i></i></span><span>Role para conhecer</span></a>
    </section>"""

N_SERVICOS = len(CATALOGO)
NUMEROS = f"""    <section class="numeros-faixa claro" aria-label="A Kyzent em números">
      <div class="container">
        <ul class="hero-numeros">
          <li><strong data-contar="5">5</strong><span>soluções para o seu negócio</span></li>
          <li><strong data-contar="{N_SERVICOS}">{N_SERVICOS}</strong><span>serviços de automação</span></li>
          <li><strong data-contar="6">6</strong><span>segmentos com soluções pensadas</span></li>
          <li><strong><span data-contar="24">24</span> h</strong><span>de atendimento no WhatsApp e no Instagram</span></li>
        </ul>
      </div>
    </section>"""

PERGUNTAS.insert(1, ("Como contratar a Kyzent?",
    "Você conta como funciona o seu negócio pelo WhatsApp ou pelo simulador de orçamento. A gente entende o que vale automatizar, envia a proposta e, depois do aceite, configura e coloca a solução em funcionamento, com suporte depois."))

INICIO = f"""{HERO}

{faixa_animada()}

{SOLUCOES_SECAO}

{NUMEROS}

{central_demos()}

{segmentos_secao()}

{como_trabalhamos(faixa=False)}

{diferenciais("secao-faixa")}

{projetos_secao()}

{perguntas().replace('class="secao"', 'class="secao claro"', 1)}

{chamada()}"""

# ------------------------------------------------------------------ páginas de cada solução
DEMO_DO_MODULO = {"whatsapp": ["chatbot"], "agenda": ["agendamento", "clientes"], "gestao": ["pedidos", "painel"], "ia": ["automacao"]}
def pagina_solucao(mid):
    nome, curto, ic, resumo, servs = MOD[mid]
    titulo, chamada_txt, benef, problemas = SOLUCOES[mid]
    itens = "\n".join(
        f'''              <li class="item brilho">
                <h4>{a}</h4>
                <p>{CATALOGO[a][0]}</p>
              </li>''' for a in servs)
    ramos = sorted({r for a in servs for r in CATALOGO[a][1]}, key=TODOS.index)
    seg_nomes = {s[0]: s[1] for s in SEGMENTOS}
    seg_links = "".join(f'<li><a class="seg-link" href="orcamento.html?ramo={r}">{seg_nomes[r]}</a></li>' for r in ramos) + \
                '<li><a class="seg-link" href="orcamento.html?ramo=empresa">Pequenas e médias empresas</a></li>'
    if mid in DEMO_DO_MODULO:
        demo = central_demos(DEMO_DO_MODULO[mid], "Veja funcionando.", "")
    else:
        demo = f"""    <section class="secao" id="demonstracoes" aria-labelledby="titulo-demos">
      <div class="container dupla">
        <div class="dupla-texto"><span class="selo-exemplo">Exemplo ilustrativo</span><h2 id="titulo-demos">Um site com a cara do seu negócio.</h2><p>Cada site é desenhado conforme o que você quer mostrar e o que mais interessa aos seus clientes, sempre com o caminho direto para o WhatsApp.</p></div>
        <div>{mock_site("todos")}</div>
      </div>
    </section>"""
    probs = "".join(f"<li>{p}</li>" for p in problemas)
    bens = "".join(f"<li>{I['check']}{b}</li>" for b in benef)
    msg = msg_modulo(mid)
    return f"""    <section class="pagina-topo solucao-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <a class="voltar-link" href="servicos.html">{I["voltar"]}Todas as soluções</a>
          <span class="solucao-topo-icone">{I[ic]}</span>
          <h1 id="titulo-pagina" data-revelar-texto>{titulo}</h1>
          <p class="pagina-topo-apoio">{chamada_txt}</p>
        </div>
        <div class="pagina-topo-texto">
          <p class="topo-bf" data-promo><span class="hero-bf-selo">Black Friday</span>Implantação grátis para quem fechar até {PROMO_DATA}.</p>
          <a class="botao botao-grande" href="{link_whats(msg)}" target="_blank" rel="noopener" data-contato data-msg="{msg}" data-magnetico>{I["conversa"]}Pedir orçamento</a>
          <a class="link-seta" href="orcamento.html">Simular o meu orçamento</a>
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
          <h3>O que melhora</h3>
          <ul class="lista-simples">{bens}</ul>
          <p class="nota">Os resultados dependem de cada negócio e do que for automatizado.</p>
        </div>
      </div>
    </section>

    <section class="secao claro secao-faixa" aria-labelledby="titulo-incluido">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-incluido" data-revelar-texto>O que está incluído.</h2>
          <p>Todos os serviços desta solução. No simulador, você responde quatro perguntas e recebe a recomendação certa para o seu negócio.</p>
        </div>
        <ul class="painel-itens itens-solucao">
{itens}
        </ul>
        <div class="itens-acao"><a class="botao" href="orcamento.html">Simular o meu orçamento</a></div>
      </div>
    </section>

{demo}

    <section class="secao claro" aria-labelledby="titulo-para-quem">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-para-quem">Para quais negócios.</h2>
          <p>Escolha o seu e simule o orçamento.</p>
        </div>
        <ul class="seg-links">{seg_links}</ul>
      </div>
    </section>

{chamada()}"""

# ------------------------------------------------------------------ Orçamento: simulador e contato
DESAFIOS = [
    ("perguntas", "Responder as mesmas perguntas no WhatsApp", ["Respostas inteligentes", "Chatbots inteligentes"]),
    ("horarios", "Marcar e confirmar horários", ["Agendamentos automáticos"]),
    ("pedidos", "Anotar e organizar pedidos", ["Gestão de cadastros e pedidos", "Chatbots inteligentes"]),
    ("retorno", "Clientes que somem e não voltam", ["Follow-up inteligente"]),
    ("orcamentos", "Montar e enviar orçamentos", ["Orçamentos automatizados"]),
    ("dados", "Organizar os dados dos clientes", ["Integração com CRM"]),
    ("numeros", "Acompanhar os números do negócio", ["Relatórios automatizados"]),
    ("estoque", "Controlar o estoque", ["Integração com estoque e ERP"]),
    ("site", "Ter um site profissional", ["Site personalizado"]),
    ("medida", "Algo sob medida para a minha empresa", ["Agentes de IA personalizados", "Sistemas personalizados"]),
]
SERV_MOD = {a: (mid, PAGINA_MOD[mid], MOD[mid][0]) for mid in MOD for a in MOD[mid][4]}
def opcao(tipo, nome, valor, texto, icone=""):
    return (f'<label class="sim-opcao"><input type="{tipo}" name="{nome}" value="{valor}">'
            f'<span class="sim-opcao-caixa">{I[icone] if icone else ""}<span>{texto}</span><span class="sim-marca">{I["check"]}</span></span></label>')

SIM_NEGOCIOS = [(s[0], s[1], s[2]) for s in SEGMENTOS] + [("outro", "Outro tipo de negócio", "site")]
ORCAMENTO = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Monte o seu projeto.</h1>
          <p class="pagina-topo-apoio">Responda quatro perguntas rápidas e receba uma recomendação de solução. No fim, ela vai pronta para o nosso WhatsApp, sem compromisso.</p>
        </div>
        <div class="pagina-topo-texto">
          <p class="topo-bf" data-promo><span class="hero-bf-selo">Black Friday</span>Implantação grátis para quem fechar até {PROMO_DATA}.</p>
          <p>Prefere conversar direto? <a href="{link_whats()}" target="_blank" rel="noopener" data-contato>Chame no WhatsApp</a>.</p>
        </div>
      </div>
    </section>

    <section class="secao claro" id="simulador" aria-labelledby="titulo-simulador">
      <div class="container">
        <h2 id="titulo-simulador" class="visualmente-oculto">Simulador de orçamento</h2>
        <noscript><p class="sim-sem-js">O simulador precisa de JavaScript. Você pode chamar a Kyzent direto no WhatsApp: {WHATS[0][1]} ou {WHATS[1][1]}.</p></noscript>
        <div class="simulador-grade">
          <form class="simulador" data-simulador novalidate data-mapa="{escape(json.dumps({k: v for k, _, v in DESAFIOS}, ensure_ascii=False))}" data-servmod="{escape(json.dumps(SERV_MOD, ensure_ascii=False))}">
            <div class="sim-progresso" aria-hidden="true"><span data-sim-barra></span></div>
            <p class="sim-num" data-sim-num aria-live="polite">Passo 1 de 4</p>
            <fieldset class="sim-passo" data-passo="1">
              <legend>Qual é o seu tipo de negócio?</legend>
              <div class="sim-opcoes sim-opcoes-2">{"".join(opcao("radio", "negocio", sid, nome, ic) for sid, nome, ic in SIM_NEGOCIOS)}</div>
            </fieldset>
            <fieldset class="sim-passo" data-passo="2" hidden>
              <legend>O que mais toma o seu tempo hoje?</legend>
              <p class="sim-dica">Marque quantas quiser.</p>
              <div class="sim-opcoes sim-opcoes-2">{"".join(opcao("checkbox", "desafio", k, t) for k, t, _ in DESAFIOS)}</div>
            </fieldset>
            <fieldset class="sim-passo" data-passo="3" hidden>
              <legend>Como os clientes falam com você?</legend>
              <div class="sim-opcoes sim-opcoes-4">{"".join(opcao("checkbox", "canal", c, c) for c in ("WhatsApp", "Instagram", "Telefone", "Presencial"))}</div>
              <p class="sim-subtitulo" id="sim-volume">Quantas mensagens por dia, mais ou menos?</p>
              <div class="sim-opcoes sim-opcoes-4" role="radiogroup" aria-labelledby="sim-volume">{"".join(opcao("radio", "volume", v, v) for v in ("Até 20", "De 20 a 50", "De 50 a 100", "Mais de 100"))}</div>
            </fieldset>
            <fieldset class="sim-passo" data-passo="4" hidden>
              <legend>Para a gente falar com você</legend>
              <div class="sim-campos">
                <label>Seu nome <span class="sim-obrigatorio">(obrigatório)</span><input name="nome" autocomplete="name" maxlength="60" required></label>
                <label>Nome da empresa <span>(opcional)</span><input name="empresa" autocomplete="organization" maxlength="80"></label>
                <label>Cidade<input name="cidade" autocomplete="address-level2" maxlength="60" value="Paulínia"></label>
                <label class="sim-campo-largo">Observação <span>(opcional)</span><textarea name="obs" rows="3" maxlength="400" placeholder="Ex.: atendo 40 clientes por dia no WhatsApp"></textarea></label>
                <div class="sim-mel" aria-hidden="true"><label>Não preencha este campo<input name="site" tabindex="-1" autocomplete="off"></label></div>
              </div>
              <p class="sim-dica">Seus dados vão só na mensagem do WhatsApp que você mesmo envia. O site não guarda nada em servidor.</p>
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
              <span class="pilar-icone">{I["alvo"]}</span>
              <h3>A sua recomendação aparece aqui.</h3>
              <p>Com base nas respostas, mostramos as soluções que mais combinam com o seu negócio e montamos a mensagem para o WhatsApp.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section class="secao" id="contato" aria-labelledby="titulo-contato">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-contato" data-revelar-texto>Fale com a Kyzent.</h2>
          <p>Atendemos Paulínia e região. A conversa começa pelo WhatsApp.</p>
        </div>
        <ul class="grade grade-3 contatos">
          <li class="contato-cartao brilho"><span class="pilar-icone">{I["conversa"]}</span><h3>WhatsApp</h3>
            <p><a href="{link_whats(None, 0)}" target="_blank" rel="noopener">{WHATS[0][1]}</a><br><a href="{link_whats(None, 1)}" target="_blank" rel="noopener">{WHATS[1][1]}</a></p>
            <a class="botao" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a></li>
          <li class="contato-cartao brilho"><span class="pilar-icone">{I["instagram"]}</span><h3>Instagram</h3>
            <p>Novidades, exemplos e bastidores da Kyzent.</p>
            <a class="botao botao-contorno" href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">@kyzent.tech</a></li>
          <li class="contato-cartao brilho"><span class="pilar-icone">{I["mapa"]}</span><h3>Onde atendemos</h3>
            <p>Paulínia/SP e região. As soluções funcionam pela internet, então o atendimento acontece pelo WhatsApp.</p>
            <a class="botao botao-contorno" href="#simulador">Simular o meu orçamento</a></li>
        </ul>
      </div>
    </section>"""

# ------------------------------------------------------------------ Quem somos
QUEM = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Quem somos</h1>
          <p class="pagina-topo-apoio">Somos a Kyzent, uma empresa de Tecnologia e Inovação de Paulínia, dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio.</p>
        </div>
        <div class="pagina-topo-texto">
          <p>Trabalhamos com Inteligência Artificial para melhorar o atendimento, apoiar as vendas e organizar a gestão do dia a dia, e também criamos soluções sob medida quando o seu negócio pede algo diferente.</p>
          <p>Cada solução é pensada para a realidade do seu comércio e vem com manutenção e suporte da nossa equipe, para você ter a tecnologia funcionando sem se preocupar com a parte técnica.</p>
        </div>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-proposito">
      <div class="container dupla">
        <div class="dupla-foto">
          {foto("equipe-reuniao.jpg", 1600, 900, "Equipe conversando em uma reunião num escritório")}
        </div>
        <div class="dupla-texto">
          <h2 id="titulo-proposito" data-revelar-texto>Transformar processos por meio da tecnologia.</h2>
          <p>Nosso propósito é transformar processos por meio da tecnologia, oferecendo mais produtividade, automação e eficiência para impulsionar os resultados dos nossos clientes.</p>
          <p>A Kyzent é uma empresa de tecnologia de Paulínia que automatiza o trabalho repetitivo do seu comércio. Em vez de contratar mais gente, você assina um serviço que trabalha junto com a sua equipe.</p>
        </div>
      </div>
    </section>

{PILARES}

    <section class="secao" aria-labelledby="titulo-proposta">
      <div class="container">
        <div class="proposta revelar-bloco">
          <h2 id="titulo-proposta" data-revelar-texto>Mais eficiência, menos tarefas manuais e processos mais inteligentes.</h2>
          <p>Transformamos tecnologia em resultados para o seu negócio.</p>
        </div>
      </div>
    </section>

{diferenciais("claro")}"""

# ------------------------------------------------------------------ Serviços
def balao(quem, texto, hora):
    tiques = TIQUES if quem == "ia" else ""
    return f'<div class="zap-msg zap-{quem}"><p>{texto}</p><span class="zap-hora">{hora}{tiques}</span></div>'

# Os exemplos mudam com o tipo de negócio escolhido no filtro ("todos" é o padrão).
RAMOS_IDS = ["todos", "lanchonete", "barbearia", "salao", "consultorio", "petshop"]

# conversa de WhatsApp: (nome, iniciais, texto do aria-label, [(quem, texto, hora)])
CONVERSAS = {
    "lanchonete": ("Sua lanchonete", "SL", "um cliente pede um lanche às 21h47 e a IA anota o pedido, soma o total e combina o pagamento", [
        ("cliente", "Boa noite! Ainda dá pra pedir?", "21:47"),
        ("ia", "Boa noite! Dá sim, a cozinha vai até as 23h. O que vai ser?", "21:47"),
        ("cliente", "1 X-salada e 1 refri lata. Entrega na Rua das Flores, 120", "21:48"),
        ("ia", "Anotado:<br>1 X-salada: R$ 22,00<br>1 refri lata: R$ 6,00<br>Entrega: R$ 5,00<br><strong>Total: R$ 33,00</strong><br>Vai pagar no Pix ou na entrega?", "21:48"),
        ("cliente", "Pix", "21:49"),
        ("ia", "Perfeito! Mandei a chave Pix aqui embaixo. Seu pedido chega em uns 40 minutos.", "21:49")]),
    "barbearia": ("Sua barbearia", "SB", "um cliente pede horário para corte e barba e a IA oferece horários livres e confirma a marcação", [
        ("cliente", "Boa tarde! Tem horário hoje pra corte e barba?", "15:02"),
        ("ia", "Boa tarde! Tem sim. Hoje restam 16h30 e 18h. Qual prefere?", "15:02"),
        ("cliente", "18h", "15:03"),
        ("ia", "Marcado: <strong>corte e barba, hoje às 18h</strong>.<br>Valor: R$ 55,00.", "15:03"),
        ("cliente", "Fechou, valeu!", "15:03"),
        ("ia", "Combinado! Te aviso 1 hora antes para você não esquecer.", "15:04")]),
    "salao": ("Seu salão", "SS", "uma cliente pede escova e hidratação e a IA oferece horários por profissional e confirma a marcação", [
        ("cliente", "Oi! Quero fazer escova e hidratação no sábado", "10:12"),
        ("ia", "Oi! Dá sim. Sábado temos 9h30 com a Camila ou 14h com a Bia. Qual prefere?", "10:12"),
        ("cliente", "9h30 com a Camila", "10:13"),
        ("ia", "Marcado: <strong>sábado, 9h30, com a Camila</strong>.<br>Duração: cerca de 2 horas.", "10:13"),
        ("cliente", "Perfeito!", "10:14"),
        ("ia", "Na sexta eu te lembro por aqui. Até lá!", "10:14")]),
    "consultorio": ("Sua clínica", "SC", "um paciente pede um retorno e a IA oferece horários e confirma a consulta", [
        ("cliente", "Bom dia! Preciso marcar um retorno", "08:41"),
        ("ia", "Bom dia! Claro. Tenho quinta às 10h ou sexta às 15h. Qual fica melhor?", "08:41"),
        ("cliente", "Quinta, 10h", "08:42"),
        ("ia", "Retorno marcado para <strong>quinta, às 10h</strong>.<br>Posso confirmar pelo convênio ou como particular?", "08:42"),
        ("cliente", "Convênio", "08:43"),
        ("ia", "Anotado. Um dia antes eu confirmo com você por aqui.", "08:43")]),
    "petshop": ("Seu pet shop", "SP", "um tutor pergunta o valor do banho e tosa e a IA informa e agenda o horário", [
        ("cliente", "Oi! Quanto é o banho e tosa pra um shih-tzu?", "11:20"),
        ("ia", "Oi! Banho e tosa do shih-tzu: <strong>R$ 70,00</strong>. Quer agendar? Tenho sábado às 10h ou 14h.", "11:20"),
        ("cliente", "10h, por favor", "11:21"),
        ("ia", "Agendado: <strong>sábado, 10h</strong>. Pode deixar o Thor com a gente!", "11:21"),
        ("cliente", "Ele tem a vacina em dia?", "11:22"),
        ("ia", "Posso te lembrar da próxima vacina também. Qual foi a data da última?", "11:22")]),
}

def conversa(r):
    nome, ini, aria, msgs = CONVERSAS["lanchonete" if r == "todos" else r]
    baloes = "\n              ".join(balao(q, t, h) for q, t, h in msgs)
    return f"""<figure class="zap-figura">
          <div class="zap" role="img" aria-label="Exemplo de conversa no WhatsApp: {aria}.">
            <div class="zap-topo" aria-hidden="true">
              <span class="zap-voltar">{I["voltar"]}</span>
              <span class="zap-avatar">{ini}</span>
              <span class="zap-nome"><strong>{nome}</strong><small>online</small></span>
            </div>
            <div class="zap-corpo" aria-hidden="true">
              <p class="zap-dia">Hoje</p>
              {baloes}
            </div>
            <div class="zap-base" aria-hidden="true"><span class="zap-campo">Mensagem</span><span class="zap-mic">{I["mic"]}</span></div>
          </div>
          <figcaption>Exemplo ilustrativo. A IA responde com os serviços, os preços e o horário do seu negócio.</figcaption>
        </figure>"""

# agenda: (título, resumo, [(hora, nome, serviço, estado, texto do estado)])
AGENDAS = {
    "todos": ("Agenda de hoje", "4 horários", [("09:00", "Carlos", "Corte", "ok", "Confirmado"), ("10:30", "Marina", "Retorno", "ok", "Confirmado"),
              ("11:15", "", "", "livre", "Horário livre"), ("14:00", "João", "Avaliação", "lembrete", "Lembrete enviado")]),
    "lanchonete": ("Clientes para chamar de volta", "3 mensagens", [("15 d", "Carlos", "Não pede há 15 dias", "lembrete", "Mensagem enviada"),
              ("20 d", "Marina", "Não pede há 20 dias", "lembrete", "Mensagem enviada"), ("30 d", "João", "Não pede há 30 dias", "ok", "Voltou a pedir")]),
    "barbearia": ("Agenda de hoje", "4 horários", [("09:00", "Carlos", "Corte e barba", "ok", "Confirmado"), ("10:30", "Lucas", "Corte", "ok", "Confirmado"),
              ("11:15", "", "", "livre", "Horário livre"), ("14:00", "André", "Barba", "lembrete", "Lembrete enviado")]),
    "salao": ("Agenda de hoje", "4 horários", [("09:30", "Ana", "Escova, com Camila", "ok", "Confirmado"), ("11:00", "Júlia", "Hidratação, com Bia", "ok", "Confirmado"),
              ("13:30", "", "", "livre", "Horário livre"), ("15:00", "Paula", "Coloração, com Camila", "lembrete", "Lembrete enviado")]),
    "consultorio": ("Agenda de hoje", "4 horários", [("09:00", "Marina", "Retorno", "ok", "Confirmado"), ("10:30", "João", "Consulta", "ok", "Confirmado"),
              ("11:15", "", "", "livre", "Horário livre"), ("14:00", "Rita", "Exame", "lembrete", "Lembrete enviado")]),
    "petshop": ("Agenda de hoje", "4 horários", [("09:00", "Thor", "Banho e tosa", "ok", "Confirmado"), ("10:30", "Mel", "Vacina", "ok", "Confirmado"),
              ("11:15", "", "", "livre", "Horário livre"), ("14:00", "Bob", "Banho", "lembrete", "Lembrete enviado")]),
}

def mock_agenda(r):
    titulo, resumo, linhas = AGENDAS[r]
    lis = ""
    for hora, nome, serv, cls, estado in linhas:
        quem = f"<strong>{nome}</strong><small>{serv}</small>" if nome else "<small>Pode ser preenchido pela IA</small>"
        lis += f'<li class="mock-linha mock-{cls}"><time>{hora}</time><span class="mock-quem">{quem}</span><span class="mock-chip">{estado}</span></li>'
    legenda = ("A IA lembra o cliente de voltar, sem você precisar procurar." if r == "lanchonete"
               else "A IA marca, confirma e lembra o cliente, sem você parar o que está fazendo.")
    return f"""<figure class="mock-figura">
          <div class="mock mock-agenda" role="img" aria-label="Exemplo de {titulo.lower()}, com mensagens e confirmações feitas automaticamente.">
            <div class="mock-topo" aria-hidden="true"><strong>{titulo}</strong><span>{resumo}</span></div>
            <ul class="mock-corpo" aria-hidden="true">{lis}</ul>
          </div>
          <figcaption>Exemplo ilustrativo. {legenda}</figcaption>
        </figure>"""

GESTOES = {
    "todos": [("Pedidos", "128"), ("Clientes", "214"), ("Retornos", "37")],
    "lanchonete": [("Pedidos", "128"), ("Clientes", "214"), ("Entregas", "96")],
    "barbearia": [("Atendimentos", "128"), ("Clientes", "214"), ("Retornos", "37")],
    "salao": [("Atendimentos", "96"), ("Clientes", "180"), ("Retornos", "41")],
    "consultorio": [("Consultas", "84"), ("Pacientes", "312"), ("Retornos", "29")],
    "petshop": [("Banhos", "72"), ("Pets", "241"), ("Pedidos", "38")],
}

def mock_gestao(r):
    barras = "".join(f'<i style="--h:{h}%"></i>' for h in (38, 52, 44, 70, 58, 86, 64))
    nums = "".join(f"<div><small>{a}</small><strong>{b}</strong></div>" for a, b in GESTOES[r])
    return f"""<figure class="mock-figura">
          <div class="mock mock-gestao" role="img" aria-label="Exemplo de painel com os números da semana e um gráfico.">
            <div class="mock-topo" aria-hidden="true"><strong>Resumo da semana</strong><span>Atualizado agora</span></div>
            <div class="mock-numeros" aria-hidden="true">{nums}</div>
            <div class="mock-barras" aria-hidden="true">{barras}</div>
          </div>
          <figcaption>Exemplo ilustrativo. Cadastros, pedidos e relatórios organizados sem planilha na mão.</figcaption>
        </figure>"""

SITES = {
    "todos": ("seunegocio.com.br", "O seu negócio, do seu jeito.", "Serviços, horários e contato num lugar só."),
    "lanchonete": ("sualanchonete.com.br", "Peça o seu lanche sem fila.", "Cardápio, entrega e horários num lugar só."),
    "barbearia": ("suabarbearia.com.br", "Corte e barba, no seu horário.", "Serviços, valores e agenda num lugar só."),
    "salao": ("seusalao.com.br", "Beleza com hora marcada.", "Serviços, profissionais e agenda num lugar só."),
    "consultorio": ("suaclinica.com.br", "Cuidado com a sua saúde.", "Especialidades, convênios e agendamento."),
    "petshop": ("seupetshop.com.br", "Banho, tosa e muito carinho.", "Serviços, produtos e agendamento num lugar só."),
}

def mock_site(r):
    url, titulo, sub = SITES[r]
    return f"""<figure class="mock-figura">
          <div class="mock mock-site" role="img" aria-label="Exemplo de site: {titulo} Botão de WhatsApp e três blocos de serviços.">
            <div class="mock-topo mock-navegador" aria-hidden="true"><span class="mock-pontos"><i></i><i></i><i></i></span><span class="mock-url">{url}</span></div>
            <div class="mock-pagina" aria-hidden="true">
              <p class="mock-titulo">{titulo}</p>
              <p class="mock-sub">{sub}</p>
              <span class="mock-botao">{BOTAO}</span>
              <div class="mock-blocos"><i></i><i></i><i></i></div>
            </div>
          </div>
          <figcaption>Exemplo ilustrativo. O site é feito sob medida, com o seu jeito e o que você quer mostrar.</figcaption>
        </figure>"""

SAIDAS_IA = {"todos": ["Agenda", "Estoque", "Clientes"], "lanchonete": ["Pedidos", "Estoque", "Clientes"],
             "petshop": ["Agenda", "Estoque", "Clientes"]}

def mock_ia(r):
    def fila(nomes, cls):
        return f'<ul class="mock-fila {cls}">' + "".join(f"<li>{n}</li>" for n in nomes) + "</ul>"
    saida = SAIDAS_IA.get(r, ["Agenda", "Clientes", "Relatórios"])
    return f"""<figure class="mock-figura">
          <div class="mock mock-ia" role="img" aria-label="Exemplo de como uma IA sob medida recebe mensagens do WhatsApp, Instagram e site e conversa com {', '.join(s.lower() for s in saida)}.">
            <div class="mock-fluxo" aria-hidden="true">
              {fila(["WhatsApp", "Instagram", "Site"], "mock-entrada")}
              <div class="mock-seta"></div>
              <div class="mock-ia-centro">{I["avancado"]}<strong>IA sob medida</strong><small>Do jeito da sua empresa</small></div>
              <div class="mock-seta"></div>
              {fila(saida, "mock-saida")}
            </div>
          </div>
          <figcaption>Exemplo ilustrativo. A IA conversa com os canais e com os sistemas que a sua empresa já usa.</figcaption>
        </figure>"""

def variantes(fn):
    """Uma versão do exemplo para cada tipo de negócio; o JS mostra a do filtro escolhido."""
    return "\n".join(f'<div class="ex-var" data-ex="{r}"{"" if r == "todos" else " hidden"}>{fn(r)}</div>' for r in RAMOS_IDS)

EXEMPLOS = {"whatsapp": variantes(conversa), "agenda": variantes(mock_agenda), "gestao": variantes(mock_gestao),
            "site": variantes(mock_site), "ia": variantes(mock_ia)}

FILTRO_RAMOS = {"lanchonete": ("Lanchonete", "lanche"), "barbearia": ("Barbearia", "tesoura"),
                "salao": ("Salão de beleza", "pente"), "consultorio": ("Clínica", "cruz"), "petshop": ("Pet shop", "pata")}

abas = []
paineis = []
for i, (mid, t, curto, ic, resumo, nomes) in enumerate(MODULOS):
    sel = "true" if i == 0 else "false"
    abas.append(
        f'<button class="aba" type="button" role="tab" id="aba-{mid}" aria-controls="modulo-{mid}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="aba-icone">{I[ic]}</span><span class="aba-texto"><span class="aba-longo">{t}</span><span class="aba-curto">{curto}</span></span>'
        f'<span class="aba-qtd" data-qtd>{len(nomes)}</span></button>')
    cards = "\n".join(
        f'''              <li class="item brilho" data-ramos="{" ".join(CATALOGO[a][1])}">
                <h4>{a}</h4>
                <p>{CATALOGO[a][0]}</p>
              </li>''' for a in nomes)
    paineis.append(f"""        <section class="painel tem-exemplo" id="modulo-{mid}" role="tabpanel" aria-labelledby="aba-{mid}" tabindex="-1">
          <div class="painel-lado">
            <span class="painel-icone">{I[ic]}</span>
            <span class="painel-num" data-painel-num>{len(nomes)} {"serviço" if len(nomes) == 1 else "serviços"}</span>
            <h2>{t}</h2>
            <p>{resumo}</p>
            <a class="link-seta" href="{PAGINA_MOD[mid]}">Conhecer a solução</a>
          </div>
          <ul class="painel-itens">
{cards}
          </ul>
          <div class="painel-exemplo">
{EXEMPLOS[mid]}
          </div>
        </section>""")

opcoes = '<button class="filtro-opcao" type="button" data-ramo="todos" aria-pressed="true"><span>Todos</span>' + I["check"] + '</button>' + "".join(
    f'<button class="filtro-opcao" type="button" data-ramo="{rid}" aria-pressed="false">{I[ic]}<span>{nome}</span>{I["check"]}</button>'
    for rid, (nome, ic) in FILTRO_RAMOS.items())
FILTRO_JANELA = f"""  <dialog class="janela janela-pequena" id="janela-filtro" aria-labelledby="filtro-janela-titulo">
    <button class="janela-fechar" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    <div class="janela-corpo">
      <h2 id="filtro-janela-titulo" tabindex="-1" autofocus>Qual é o seu tipo de negócio?</h2>
      <p class="janela-resumo">Mostramos só os serviços que mais combinam com o seu negócio.</p>
      <div class="filtro-opcoes">{opcoes}</div>
    </div>
  </dialog>"""

chips = "".join(
    f'<button class="filtro-chip" type="button" data-ramo="{rid}" aria-pressed="false">{I[ic]}<span>{nome}</span></button>'
    for rid, (nome, ic) in FILTRO_RAMOS.items())
NOMES_RAMOS = {rid: nome for rid, nome, *_ in RAMOS}
nomes_js = json.dumps(NOMES_RAMOS, ensure_ascii=False)

SERVICOS_PAG = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Automação inteligente para empresas.</h1>
          <p class="pagina-topo-apoio">Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
        </div>
        <div class="pagina-topo-texto">
          <p class="topo-bf" data-promo><span class="hero-bf-selo">Black Friday</span>Implantação grátis em qualquer módulo para quem fechar até {PROMO_DATA}.</p>
          <p>Escolha o seu tipo de negócio e veja os serviços de cada solução. Para receber uma recomendação, responda as perguntas do simulador de orçamento.</p>
          <a class="botao" href="orcamento.html" data-magnetico>Simular o meu orçamento</a>
          <a class="link-seta" href="#catalogo">Ver os serviços</a>
        </div>
      </div>
    </section>

    <section class="secao secao-servicos claro" id="catalogo" aria-label="Serviços por módulo">
      <div class="container filtro" data-filtro data-nomes='{nomes_js}'>
        <p class="filtro-titulo" id="filtro-titulo">Qual é o seu tipo de negócio?</p>
        <button class="filtro-abrir" type="button" data-abrir-janela="janela-filtro" aria-haspopup="dialog">
          <span class="filtro-abrir-rotulo">Tipo de negócio</span><strong data-filtro-atual>Todos</strong>{I["seta_baixo"]}
        </button>
        <div class="filtro-botoes" role="group" aria-labelledby="filtro-titulo">
          <button class="filtro-chip" type="button" data-ramo="todos" aria-pressed="true"><span>Todos</span></button>
          {chips}
        </div>
      </div>
      <div class="abas-faixa">
        <div class="container">
          <div class="abas" role="tablist" aria-label="Módulos de serviço">
            {"".join(abas)}
          </div>
        </div>
      </div>
      <div class="container paineis">
{chr(10).join(paineis)}
        <div class="itens-acao"><p class="precos-nota">Valores combinados conforme a necessidade de cada negócio.</p><a class="botao" href="orcamento.html">Simular o meu orçamento</a></div>
      </div>
    </section>

{chamada()}
"""

DESC = "A Kyzent é uma empresa de Tecnologia e Inovação de Paulínia/SP que automatiza processos, conecta sistemas e leva Inteligência Artificial ao atendimento, às vendas e à gestão de pequenas empresas."

saidas = [
    ("index.html", "Kyzent | Inteligência artificial e automação para o seu negócio", DESC, INICIO, "", None),
    ("servicos.html", "Soluções e serviços | Kyzent", "Catálogo de soluções da Kyzent: atendimento com IA no WhatsApp, agendamento e vendas, gestão, site e IA sob medida. Simule o seu orçamento.", SERVICOS_PAG, FILTRO_JANELA, None),
    ("quem-somos.html", "Quem somos | Kyzent", "A Kyzent é uma empresa de Tecnologia e Inovação de Paulínia/SP. Conheça o nosso propósito, a missão, a visão, os valores e os diferenciais.", QUEM, "", None),
    ("orcamento.html", "Orçamento | Kyzent", "Simule o seu orçamento em quatro passos e receba uma recomendação de solução da Kyzent pelo WhatsApp.", ORCAMENTO, "", None),
] + [(PAGINA_MOD[mid], f"{SOLUCOES[mid][0]} | Kyzent", SOLUCOES[mid][1], pagina_solucao(mid), "", "servicos.html") for mid in MOD]

for arq, titulo, desc, corpo, janelas, ativo in saidas:
    with open(os.path.join(SITE, arq), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina(arq, titulo, desc, corpo, janelas, ativo))
    print("ok", arq)

with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for arq, *_ in saidas:
        f.write(f"  <url><loc>{BASE}{'' if arq == 'index.html' else arq}</loc><priority>{'1.0' if arq == 'index.html' else '0.8'}</priority></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
print("ok sitemap.xml e robots.txt")
