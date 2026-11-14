"""Monta as páginas do site com o mesmo topo, rodapé e janelas.
Uso (na raiz do site): python tools/monta_paginas.py .
Atenção: sobrescreve index.html, quem-somos.html e servicos.html.
Edite o texto aqui e rode de novo, para as páginas não ficarem diferentes entre si."""
import json, os, sys
from html import escape
from urllib.parse import quote

SITE = sys.argv[1]
BASE = "https://kyzenttech-lang.github.io/site/"
VERSAO = "117"   # aumente a cada mudança no CSS/JS, para o navegador baixar o arquivo novo

WHATS = [("5519988728894", "(19) 98872-8894"), ("5519971246077", "(19) 97124-6077")]
MSG = quote("Olá, vim pelo site da Kyzent")
EMAIL = "kyzent.tech@gmail.com"   # contato geral e de privacidade (LGPD)
PRIVACIDADE_DATA = "13 de novembro de 2026"   # mude ao alterar o texto da política
BOTAO = "Conversar no WhatsApp"   # o nome dos botões de contato do topo, menu, janelas e barra fixa

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

PAGINAS = [("index.html", "Início"), ("servicos.html", "Soluções"), ("aurora.html", "Aurora"), ("quem-somos.html", "Quem somos"), ("orcamento.html", "Orçamento")]

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

  <script>document.documentElement.classList.add("js");</script>
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
          <p>Empresa de Tecnologia e Inovação de Paulínia/SP. Automação e Inteligência Artificial para o atendimento, as vendas e a gestão de pequenas empresas.</p>
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
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          </ul>
        </div>
      </div>
      <div class="rodape-base">
        <p>© <span data-ano>2026</span> Kyzent Technology Solutions. Todos os direitos reservados.</p>
        <p><a href="privacidade.html">Política de Privacidade</a> · Paulínia/SP</p>
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
          <span class="aurora-halo" aria-hidden="true"></span>
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
            <a class="botao botao-grande" href="#demonstracoes">Conversar com a Aurora</a>
            <a class="botao botao-grande botao-vidro" href="orcamento.html">Simular meu orçamento</a>
          </div>
        </div>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-aurora-faz">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-faz" data-revelar-texto>O que a Aurora faz pelo seu negócio.</h2>
        </div>
        <ul class="aurora-faz">
          <li><strong>Agenda</strong><span>horários, com confirmação e lembrete</span></li>
          <li><strong>Tira dúvidas</strong><span>sobre preço, horário, endereço e serviços</span></li>
          <li><strong>Registra pedidos</strong><span>e manda para a sua equipe organizados</span></li>
          <li><strong>Chama uma pessoa</strong><span>da equipe quando o cliente precisa</span></li>
        </ul>
      </div>
    </section>

    <section class="secao secao-faixa" aria-labelledby="titulo-aurora-jeito">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-aurora-jeito" data-revelar-texto>Como ela trabalha.</h2>
        </div>
        <ul class="grade grade-3">
          <li class="pilar"><p class="pilar-rotulo">Com o seu nome</p><h3>O cliente conversa com o seu negócio.</h3><p>A Aurora atende com o nome, os horários, os preços e as informações que você passar.</p></li>
          <li class="pilar"><p class="pilar-rotulo">Sem fingir</p><h3>Sempre como assistente virtual.</h3><p>Ela se apresenta como assistente virtual e nunca finge ser uma pessoa.</p></li>
          <li class="pilar"><p class="pilar-rotulo">Com a sua equipe</p><h3>Uma pessoa entra quando precisa.</h3><p>Quando o cliente pede uma pessoa ou o assunto foge da rotina, ela chama a sua equipe com a conversa organizada.</p></li>
        </ul>
      </div>
    </section>

{central_demos(ids=["chatbot"], titulo="Converse com a Aurora.")}

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
    ("chatbot", "Chatbot", "conversa", "Atendimento com IA", "Escolha as respostas e veja a Aurora conduzir a conversa: agendar, informar preços ou passar para uma pessoa da equipe.", "whatsapp", tela_chatbot),
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
        botoes.append(f'<button type="button" class="demo-aba" role="tab" id="daba-{did}" aria-controls="dpainel-{did}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}"><span>{curto}</span></button>')
        paineis_.append(f"""          <div class="demo-painel" id="dpainel-{did}" role="tabpanel" aria-labelledby="daba-{did}"{"" if sel else " hidden"}>
            <div class="demo-info">
              <span class="selo-exemplo">Simulação demonstrativa</span>
              <h3>{titulo_aba}</h3>
              <p>{texto}</p>
              <a class="link-seta" href="{PAGINA_MOD[mod]}">Conhecer solução</a>
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
          {'<p class="demo-dica">Deslize para o lado para ver a próxima demonstração.</p>' if len(abas_) > 1 else ''}
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
SEG_FRASE = {'lanchonete': 'Do pedido no WhatsApp à entrega, sem anotação perdida.', 'barbearia': 'Agenda cheia, sem largar a máquina.', 'salao': 'Cada profissional com a sua agenda em ordem.', 'consultorio': 'Recepção mais leve e pacientes lembrados.', 'petshop': 'Banho, tosa e vacina sempre no dia certo.', 'empresa': 'Processos conectados para a empresa crescer.'}
# ------------------------------------------------------------------ metodologia, diferenciais e projetos
# Projetos reais entram aqui, com a autorização de cada cliente: (nome, segmento, o que foi feito, foto ou "")
PROJETOS = []
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
            f'<span class="sim-opcao-caixa"><span>{texto}</span><span class="sim-marca">{I["check"]}</span></span></label>')

SIM_NEGOCIOS = [(s[0], s[1], s[2]) for s in SEGMENTOS] + [("outro", "Outro tipo de negócio", "site")]
ORCAMENTO = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Monte o seu projeto.</h1>
          <p class="pagina-topo-apoio">Responda quatro perguntas rápidas e receba uma recomendação de solução. No fim, ela vai pronta para o nosso WhatsApp, sem compromisso.</p>
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
          <p>Atendemos Paulínia/SP e região. As soluções funcionam pela internet, então tudo começa por uma conversa no WhatsApp.</p>
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
    "gestao": ("Tenha mais controle sobre o que acontece no seu negócio.", "Pedidos, clientes e números organizados, com os seus sistemas conectados."),
    "site": ("Sua empresa merece uma presença digital à altura do seu negócio.", "Um site feito para o seu negócio, com o caminho direto para a conversa."),
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
        <div class="grade grade-3 pilares">
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
    ("API oficial", "WhatsApp pela API oficial da Meta", "Conexão aprovada pela Meta, sem atalhos que coloquem o número da sua empresa em risco."),
    ("Sob medida", "Feito para o seu negócio", "Cada automação é configurada com os seus produtos, preços, horários e jeito de atender."),
    ("Suporte", "Manutenção e suporte", "A nossa equipe acompanha cada solução depois de pronta, para a tecnologia seguir funcionando."),
    ("Mensalidade", "Sem contratar mais gente", "Você assina um serviço que trabalha junto com a sua equipe, em vez de aumentar a folha."),
]
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

SOLUCOES_SECAO = f"""    <section class="secao claro" id="solucoes" aria-labelledby="titulo-solucoes">
      <div class="container">
        <div class="cabeca-linha">
          <div class="cabeca">
            <h2 id="titulo-solucoes" data-revelar-texto>Soluções para cada parte do seu negócio.</h2>
            <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
          </div>
          <a class="link-seta" href="servicos.html">Ver os 19 serviços</a>
        </div>
        <ul class="solucoes carrossel" data-carrossel aria-label="Soluções da Kyzent">
          {"".join(cartao_solucao(mid, i == 0) for i, mid in enumerate(MOD))}
        </ul>
      </div>
    </section>"""

# ---------- experiência marcante do Início: do problema à tarefa feita (diagrama vivo, conduzido pela rolagem)
HISTORIA_PASSOS = [
    ("Mensagens chegam o dia todo.", "No WhatsApp, no Instagram, de madrugada. A IA da Kyzent responde na hora, com as informações do seu negócio."),
    ("Cada pedido é entendido.", "Agendamento, pedido, orçamento ou dúvida: a IA identifica o que o cliente quer e o que precisa ser feito."),
    ("Os sistemas conversam entre si.", "A agenda é atualizada, o estoque é conferido e o pedido entra no lugar certo, sem ninguém digitar duas vezes."),
    ("A equipe cuida do que importa.", "O que precisa de uma pessoa chega organizado, e os números do dia viram relatório."),
]
HISTORIA = f"""    <section class="secao historia historia-3d" id="como-funciona" aria-labelledby="titulo-historia">
      <div class="container historia-grade">
        <div class="historia-texto">
          <div class="cabeca">
            <h2 id="titulo-historia" data-revelar-texto>Uma mensagem entra. O trabalho sai feito.</h2>
            <p>O que acontece por trás de cada conversa quando o seu negócio tem automação. Toque em cada passo para ver o caminho.</p>
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
SEG_ALT = {
    "lanchonete": "Garçom servindo hambúrguer, batata frita e suco numa bandeja de madeira",
    "barbearia": "Barbeiros cortando o cabelo de clientes numa barbearia",
    "salao": "Cabeleireira atendendo uma cliente num salão de beleza",
    "consultorio": "Dentista examinando um paciente no consultório",
    "petshop": "Cachorro corgi sentado dentro de um pet shop",
    "empresa": "Equipe de uma empresa conversando em volta de um computador",
}
def segmentos_secao(classe="claro"):
    chips, paineis_ = [], []
    for i, (sid, nome, ic, arq, (w, h), artigo, desafios, solucoes, beneficios) in enumerate(SEGMENTOS):
        chips.append(f'<button type="button" class="seg-chip" role="tab" id="aba-seg-{sid}" data-seg="{sid}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" aria-controls="seg-{sid}">{nome}</button>')
        col = lambda titulo, itens, cls: f'<div class="seg-col {cls}"><h4>{titulo}</h4><ul>' + "".join(f"<li>{x}</li>" for x in itens) + "</ul></div>"
        paineis_.append(f"""          <article class="seg-painel{" ativo" if i == 0 else ""}" id="seg-{sid}" role="tabpanel" tabindex="0" aria-labelledby="aba-seg-{sid}">
            <div class="seg-foto">{foto(arq, w, h, alt=SEG_ALT[sid], sizes="(max-width: 760px) 100vw, 40vw")}
              <div class="seg-foto-texto"><h3 id="seg-{sid}-titulo">{nome}</h3><p>{SEG_FRASE[sid]}</p></div>
            </div>
            <div class="seg-texto">
              <div class="seg-colunas seg-colunas-2">
                {col("Como a Kyzent ajuda", solucoes, "seg-solucoes")}
                {col("O que melhora", beneficios, "seg-beneficios")}
              </div>
            </div>
          </article>""")
    return f"""    <section class="secao {classe}" id="segmentos" aria-labelledby="titulo-segmentos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-segmentos" data-revelar-texto>Tecnologia para o seu tipo de negócio.</h2>
          <p>Escolha o seu segmento e veja como a automação entra no seu dia a dia.</p>
        </div>
        <div class="seg-chips" role="tablist" aria-label="Segmentos" data-segmentos>{"".join(chips)}</div>
        <div class="seg-paineis">
          <div class="seg-palco" data-seg-palco data-seg-ativo="{SEGMENTOS[0][0]}" aria-hidden="true">
            {"".join(f'<span class="seg-palco-ic" data-ic="{sid}">{I[ic]}</span>' for sid, _n, ic, *_ in SEGMENTOS)}
          </div>
{chr(10).join(paineis_)}
        </div>
        <div class="seg-rodape">
          <p class="nota">{AVISO_RESULTADOS}</p>
          <a class="botao" href="orcamento.html">Simular meu orçamento</a>
        </div>
      </div>
    </section>"""

# ---------- apresentação curta (no Início, no lugar dos diferenciais repetidos)
SOBRE_CURTO = """    <section class="secao secao-faixa sobre-curto" aria-labelledby="titulo-sobre">
      <div class="container sobre-grade">
        <h2 id="titulo-sobre" data-revelar-texto>Uma empresa de tecnologia de Paulínia, perto de você.</h2>
        <div>
          <p>A Kyzent desenvolve soluções inteligentes para comércios e empresas, com WhatsApp pela API oficial, configuração feita para cada negócio e suporte da nossa equipe depois de tudo pronto.</p>
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
          <p class="hero-apoio">Inteligência artificial, automação e tecnologia para transformar a maneira como sua empresa trabalha, vende e cresce.</p>
          <div class="hero-acoes">
            <a class="botao botao-grande" href="#solucoes" data-magnetico>Conhecer nossas soluções</a>
            <a class="botao botao-grande botao-vidro" href="{link_whats(MSG_CONVERSA)}" target="_blank" rel="noopener" data-contato data-msg="{MSG_CONVERSA}" data-magnetico>Conversar no WhatsApp</a>
          </div>
        </div>
      </div>
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


TAREFAS = [("Responder \"qual o horário de sábado?\" pela 15ª vez", "A IA responde na hora, com o horário certo"),
           ("Anotar o pedido no papel no meio do movimento", "O pedido chega organizado e soma o total"),
           ("Ligar para confirmar o horário de amanhã", "A confirmação sai sozinha pelo WhatsApp"),
           ("Procurar o cliente que não volta há um mês", "O lembrete de retorno é enviado no dia certo")]
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
            <p class="depoimento-autor"><strong>[NOME]</strong><span>[NEGÓCIO], [CIDADE]</span></p>
          </li>
        </ul>
      </div>
    </section>
-->
"""

INICIO = f"""{HERO}

{comparar()}

{HISTORIA}

{SOLUCOES_SECAO}

{central_demos()}

{segmentos_secao()}

{como_trabalhamos(faixa=False)}

{SOBRE_CURTO}

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

VISUAL_MOD = {"whatsapp": (visual_atendimento, "Cada mensagem no lugar certo.", "A IA responde o que é rotina e passa para a equipe só o que precisa de uma pessoa."),
              "agenda": (visual_funil, "Nenhuma oportunidade parada.", "Contatos qualificados, horários marcados e clientes chamados de volta no momento certo."),
              "gestao": (visual_gestao, "Os números do negócio, sem planilha.", "Pedidos, clientes e faturamento reunidos e atualizados sozinhos."),
              "site": (visual_site, "Um site que trabalha por você.", "Feito para o seu negócio, rápido no celular e com o caminho direto para a conversa."),
              "ia": (visual_ia, "Uma IA que conhece a sua empresa.", "Pergunte em português e receba a resposta com base nos seus próprios sistemas.")}

def pagina_solucao(mid):
    nome, curto, ic, resumo, servs = MOD[mid]
    titulo, chamada_txt, benef, problemas = SOLUCOES[mid]
    itens = "\n".join(f'              <li class="item brilho"><h4>{a}</h4><p>{CATALOGO[a][0]}</p></li>' for a in servs)
    fn, vt, vd = VISUAL_MOD[mid]
    probs = "".join(f"<li>{p}</li>" for p in problemas)
    bens = "".join(f"<li>{I['check']}{b}</li>" for b in benef)
    return f"""    <section class="pagina-topo solucao-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <a class="voltar-link" href="servicos.html">{I["voltar"]}Todas as soluções</a>
          {ilustra(mid, "ilu ilu-grande")}
          <h1 id="titulo-pagina" data-revelar-texto>{titulo}</h1>
          <p class="pagina-topo-apoio">{chamada_txt}</p>
        </div>
        <div class="pagina-topo-texto">
          <a class="botao botao-grande" href="orcamento.html" data-magnetico>Pedir orçamento</a>
          <a class="link-seta" href="{link_whats(msg_modulo(mid))}" target="_blank" rel="noopener" data-contato data-msg="{msg_modulo(mid)}">Conversar no WhatsApp</a>
        </div>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-visual">
      <div class="container vis-grade">
        <div class="vis-texto">
          <h2 id="titulo-visual" data-revelar-texto>{vt}</h2>
          <p>{vd}</p>
        </div>
        {fn()}
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
          <p class="nota">{AVISO_RESULTADOS}</p>
        </div>
      </div>
    </section>

    <section class="secao claro secao-faixa" aria-labelledby="titulo-incluido">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-incluido" data-revelar-texto>O que está incluído.</h2>
        </div>
        <ul class="painel-itens itens-solucao">
{itens}
        </ul>
      </div>
    </section>

{chamada(mid)}"""

# ---------- Quem somos: a empresa apresentada uma vez; propósito, missão e proposta com papéis diferentes
QUEM = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Quem somos</h1>
          <p class="pagina-topo-apoio">Somos a Kyzent, uma empresa de Tecnologia e Inovação de Paulínia, dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio.</p>
          <p class="topo-alternativa">Trabalhamos com Inteligência Artificial para melhorar o atendimento, apoiar as vendas e organizar a gestão do dia a dia, e também criamos soluções sob medida quando o seu negócio pede algo diferente.</p>
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

{diferenciais("")}

    <section class="secao claro" aria-labelledby="titulo-proposta">
      <div class="container">
        <div class="proposta revelar-bloco">
          <p class="pilar-rotulo">Nossa proposta</p>
          <h2 id="titulo-proposta" data-revelar-texto>Mais eficiência, menos tarefas manuais e processos mais inteligentes.</h2>
          <p>Transformamos tecnologia em resultados para o seu negócio.</p>
        </div>
      </div>
    </section>"""

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
        <p>A Kyzent Technology Solutions, de Paulínia/SP, é a responsável (controladora) pelos dados pessoais tratados por este site e pelos nossos canais de atendimento. Para qualquer assunto sobre privacidade, fale com a gente pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

        <h2>2. Quais dados recebemos</h2>
        <ul>
          <li><strong>Simulador de orçamento:</strong> as respostas que você marca e, se quiser, o seu nome, o nome da empresa, a cidade e uma observação. O simulador funciona só no seu navegador: nada é enviado ao nosso servidor nem guardado no site. Esses dados só chegam até nós se você enviar a mensagem pronta pelo WhatsApp.</li>
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

# ---------- Soluções: central de navegação (5 cartões, os 19 serviços em lista, um único acesso ao simulador)
def lista_servicos():
    grupos = []
    for mid in MOD:
        nome, curto, ic, resumo, servs = MOD[mid]
        lis = "".join(f'<li><strong>{a}</strong><span>{CATALOGO[a][0]}</span></li>' for a in servs)
        grupos.append(f'<div class="cat-grupo"><h3><a href="{PAGINA_MOD[mid]}">{nome}</a></h3><ul>{lis}</ul></div>')
    return "".join(grupos)


def ecossistema():
    import math
    rx, ry = 250, 120
    nos = []
    for k, mid in enumerate(MOD):
        a = math.radians(-90 + k * 72)
        x, y = 320 + rx * math.cos(a), 190 + ry * math.sin(a)
        nome = MOD[mid][1]
        nos.append(f'<a class="eco-no" href="{PAGINA_MOD[mid]}" style="--x:{x / 640 * 100:.2f}%;--y:{y / 380 * 100:.2f}%;--i:{k}">'
                   f'<span class="eco-bola"></span><span class="eco-nome">{nome}</span></a>')
    return f"""<div class="ecossistema" data-ecossistema>
          <svg viewBox="0 0 640 380" aria-hidden="true" focusable="false">
            <ellipse class="eco-orbita" cx="320" cy="190" rx="{rx}" ry="{ry}"/>
            <ellipse class="eco-orbita eco-orbita-2" cx="320" cy="190" rx="{rx * .62:.0f}" ry="{ry * .62:.0f}"/>
            <path id="eco-trilho" d="M{320 - rx} 190a{rx} {ry} 0 1 0 {2 * rx} 0a{rx} {ry} 0 1 0 {-2 * rx} 0" fill="none"/>
            <circle class="eco-luz" r="5"><animateMotion dur="14s" repeatCount="indefinite"><mpath href="#eco-trilho"/></animateMotion></circle>
            {"".join(f'<line class="eco-raio" x1="320" y1="190" x2="{320 + rx * math.cos(math.radians(-90 + k * 72)):.1f}" y2="{190 + ry * math.sin(math.radians(-90 + k * 72)):.1f}"/>' for k in range(5))}
          </svg>
          {k3d("eco-k3d")}
          <nav class="eco-nos" aria-label="Soluções">{"".join(nos)}</nav>
        </div>"""

SERVICOS_PAG = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="pagina-topo-fundo" aria-hidden="true"></div>
      <div class="container pagina-topo-grade eco-grade">
        <div>
          <h1 id="titulo-pagina" data-revelar-texto>Soluções</h1>
          <p class="pagina-topo-apoio">Cinco soluções e {N_SERVICOS} serviços para automatizar o atendimento, as vendas e a gestão. Escolha por onde começar.</p>
        </div>
        {ecossistema()}
      </div>
    </section>

    <section class="secao claro" aria-labelledby="titulo-cinco">
      <div class="container">
        <h2 id="titulo-cinco" class="visualmente-oculto">As cinco soluções</h2>
        <ul class="solucoes carrossel" data-carrossel aria-label="Soluções da Kyzent">
          {"".join(cartao_solucao(mid, i == 0) for i, mid in enumerate(MOD))}
        </ul>
      </div>
    </section>

    <section class="secao claro secao-faixa" id="catalogo" aria-labelledby="titulo-catalogo">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-catalogo" data-revelar-texto>Todos os {N_SERVICOS} serviços.</h2>
          <p>Organizados por solução. Toque no nome da solução para ver a página completa.</p>
        </div>
        <div class="catalogo">{lista_servicos()}</div>
      </div>
    </section>

{chamada("servicos.html")}
"""
FILTRO_JANELA = ""

DESC = "A Kyzent é uma empresa de Tecnologia e Inovação de Paulínia/SP que automatiza processos, conecta sistemas e leva Inteligência Artificial ao atendimento, às vendas e à gestão de pequenas empresas."

saidas = [
    ("index.html", "Kyzent | Inteligência artificial e automação para o seu negócio", DESC, INICIO, "", None),
    ("servicos.html", "Soluções e serviços | Kyzent", "Catálogo de soluções da Kyzent: atendimento com IA no WhatsApp, agendamento e vendas, gestão, site e IA sob medida. Simule o seu orçamento.", SERVICOS_PAG, FILTRO_JANELA, None),
    ("quem-somos.html", "Quem somos | Kyzent", "A Kyzent é uma empresa de Tecnologia e Inovação de Paulínia/SP. Conheça o nosso propósito, a missão, a visão, os valores e os diferenciais.", QUEM, "", None),
    ("privacidade.html", "Política de Privacidade | Kyzent", "Como a Kyzent trata os seus dados pessoais, de acordo com a LGPD: quais dados recebemos, para que usamos, com quem compartilhamos e como exercer os seus direitos.", PRIVACIDADE, "", None),
    ("aurora.html", "Aurora, a IA de atendimento | Kyzent", "Conheça a Aurora, a IA de atendimento da Kyzent: atende os clientes do seu negócio no WhatsApp e no Instagram, 24 horas, e chama a sua equipe quando precisa.", aurora_pagina(), "", None),
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
