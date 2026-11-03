"""Monta as páginas do site com o mesmo topo, rodapé e janelas.
Uso (na raiz do site): python tools/monta_paginas.py .
Atenção: sobrescreve index.html, quem-somos.html e servicos.html.
Edite o texto aqui e rode de novo, para as páginas não ficarem diferentes entre si."""
import json, os, sys
from urllib.parse import quote

SITE = sys.argv[1]
BASE = "https://kyzenttech-lang.github.io/site/"
VERSAO = "29"   # aumente a cada mudança no CSS/JS, para o navegador baixar o arquivo novo

WHATS = [("5519988728894", "(19) 98872-8894"), ("5519971246077", "(19) 97124-6077")]
MSG = quote("Olá, vim pelo site da Kyzent")
BOTAO = "Chamar no WhatsApp"   # o mesmo nome em todo botão de contato

def link_whats(msg=None, n=0):
    return f"https://wa.me/{WHATS[n][0]}?text={quote(msg) if msg else MSG}"

def brl(v):
    return "R$ " + f"{v:,}".replace(",", ".")

def svg(d, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

I = {
    "lua": svg('<path d="M20.5 13.2A8.5 8.5 0 1 1 10.8 3.5a6.6 6.6 0 0 0 9.7 9.7z"/>', "icone-lua"),
    "sol": svg('<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>', "icone-sol"),
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
    "voltar": svg('<path d="M15 5l-7 7 7 7"/>'),
    "mic": svg('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>'),
}
TIQUES = ('<svg class="zap-tiques" viewBox="0 0 18 11" aria-hidden="true"><path d="M1 6.2l3 3L11 1.5M7 9.2l.8.8L15 1.5" '
          'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

PAGINAS = [("index.html", "Início"), ("quem-somos.html", "Quem somos"), ("servicos.html", "Serviços")]

# ------------------------------------------------------------------ catálogo de serviços (sem preço: o valor é combinado com cada cliente)
# ramos: para quais tipos de negócio o serviço é indicado (filtro da página Serviços)
TODOS = ["lanchonete", "barbearia", "salao", "consultorio"]
CATALOGO = {
    "Chatbots inteligentes": ("Atendimento automatizado pelo WhatsApp e Instagram, disponível 24 horas.", TODOS),
    "Respostas inteligentes": ("Resolução automática de dúvidas e perguntas frequentes.", TODOS),
    "Triagem de atendimento": ("Identificação das necessidades dos clientes e encaminhamento para atendentes humanos.", ["salao", "consultorio"]),
    "Centrais inteligentes de atendimento": ("Múltiplos agentes de IA trabalhando em diferentes funções.", []),
    "Agendamentos automáticos": ("Organização de reuniões, consultas e serviços.", ["barbearia", "salao", "consultorio"]),
    "Captação e qualificação de leads": ("Identificação e classificação de potenciais clientes.", ["salao", "consultorio"]),
    "Follow-up inteligente": ("Acompanhamento automático de clientes e recuperação de oportunidades.", TODOS),
    "Orçamentos automatizados": ("Geração e envio de propostas comerciais.", ["salao"]),
    "Automação de processos comerciais": ("Integração e otimização de etapas do processo de vendas.", []),
    "Gestão de cadastros e pedidos": ("Organização automatizada de informações e solicitações.", ["lanchonete"]),
    "Integração com CRM": ("Centralização e gerenciamento do relacionamento com clientes.", ["barbearia", "salao", "consultorio"]),
    "Relatórios automatizados": ("Geração de relatórios para acompanhamento empresarial.", ["lanchonete", "barbearia"]),
    "Automação de documentos": ("Organização e envio automático de documentos.", ["consultorio"]),
    "Integração de sistemas": ("Conexão entre diferentes plataformas e ferramentas empresariais.", []),
    "Integração com estoque e ERP": ("Automatização e conexão de sistemas de gestão empresarial.", ["lanchonete"]),
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

# as 4 frentes oficiais da empresa (Início): (n, título, ícone, curto, resumo, módulo que abre, serviços)
AREAS = [
    ("01", "Atendimento e relacionamento", "conversa", "Atendimento", "", "whatsapp",
     ["Chatbots inteligentes", "Respostas inteligentes", "Triagem de atendimento"]),
    ("02", "Vendas e captação de clientes", "vendas", "Vendas", "", "agenda",
     ["Captação e qualificação de leads", "Agendamentos automáticos", "Follow-up inteligente", "Orçamentos automatizados"]),
    ("03", "Administração e gestão empresarial", "gestao", "Gestão", "", "gestao",
     ["Gestão de cadastros e pedidos", "Integração com CRM", "Relatórios automatizados", "Automação de documentos",
      "Assistentes internos de IA", "Integração de sistemas"]),
    ("04", "Soluções avançadas e personalizadas", "avancado", "Avançadas", "", "ia",
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
    ("consultorio", "Consultórios odontológicos", "dente", "um consultório odontológico", "Consulta confirmada sem a recepção ligar.",
     "Recepção mais leve, agenda confirmada e pacientes acompanhados.", [
        ("Agendamentos automáticos", "Marcação e confirmação de consultas pelo WhatsApp."),
        ("Triagem de atendimento", "Identifica se é avaliação, retorno ou urgência e encaminha para a recepção."),
        ("Respostas inteligentes", "Convênios, endereço, horários e tipos de tratamento respondidos na hora."),
        ("Follow-up inteligente", "Lembrete de consulta e de retorno para revisão e limpeza."),
        ("Automação de documentos", "Envio automático de orientações e documentos ao paciente."),
        ("Cadastro de pacientes e CRM", "Informações de cada paciente organizadas, com cuidado com os dados (LGPD)."),
    ]),
]

# fotos de banco (Unsplash, licença livre; origem em assets/fotos/CREDITOS.md): arquivo, largura, altura
FOTO_RAMO = {
    "lanchonete": ("lanchonete.jpg", 1200, 675),
    "barbearia": ("barbearia.jpg", 880, 1100),
    "salao": ("salao.jpg", 734, 1100),
    "consultorio": ("consultorio.jpg", 1200, 800),
}

def ramos_cartoes():
    cartoes = []
    for rid, nome, *_ in RAMOS:
        foto, w, h = FOTO_RAMO[rid]
        cartoes.append(
            f'<button class="ramo" type="button" data-abrir-janela="janela-{rid}" aria-haspopup="dialog">'
            f'<img src="assets/fotos/{foto}" alt="" width="{w}" height="{h}" loading="lazy">'
            f'<span class="ramo-texto"><span class="ramo-nome">{nome}</span>'
            f'<span class="ramo-ver">Ver mais {I["mais"]}</span></span></button>')
    return '<div class="ramos">\n          ' + "\n          ".join(cartoes) + "\n        </div>"

def ramos_janelas():
    janelas = []
    for rid, nome, ic, artigo, _, resumo, itens in RAMOS:
        lis = "".join(f"<li><strong>{t}</strong> {d}</li>" for t, d in itens)
        msg = f"Olá, vim pelo site da Kyzent. Tenho {artigo} e quero saber o que vocês podem automatizar."
        janelas.append(f"""  <dialog class="janela" id="janela-{rid}" aria-labelledby="janela-{rid}-titulo">
    <div class="janela-foto"><img src="assets/fotos/{FOTO_RAMO[rid][0]}" alt="" width="{FOTO_RAMO[rid][1]}" height="{FOTO_RAMO[rid][2]}" loading="lazy"></div>
    <button class="janela-fechar" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    <div class="janela-corpo">
      <p class="janela-sobre">O que a Kyzent faz para</p>
      <h2 id="janela-{rid}-titulo" tabindex="-1" autofocus>{nome}</h2>
      <p class="janela-resumo">{resumo}</p>
      <ul class="lista-check">{lis}</ul>
      <div class="janela-acoes">
        <a class="botao" href="{link_whats(msg)}" target="_blank" rel="noopener" data-contato data-msg="{msg}">{BOTAO}</a>
        <a class="link-seta" href="servicos.html?ramo={rid}">Ver serviços para {nome.lower()}</a>
      </div>
    </div>
  </dialog>""")
    return "\n".join(janelas)

# ------------------------------------------------------------------ partes comuns
def menu(atual, classe):
    itens = []
    for arq, nome in PAGINAS:
        cur = ' aria-current="page"' if arq == atual else ""
        itens.append(f'<li><a href="{arq}"{cur}>{nome}</a></li>')
    return f'<ul class="{classe}">' + "".join(itens) + "</ul>"

def logos():
    return ('<img class="logo-claro" src="assets/img/kyzent-horizontal-claro.svg" alt="Kyzent, automação e IA" width="590" height="140">'
            '<img class="logo-escuro" src="assets/img/kyzent-horizontal-escuro.svg" alt="Kyzent, automação e IA" width="590" height="140">')

def numero_opcao(n):
    return (f'<a class="numero" href="{link_whats(None, n)}" target="_blank" rel="noopener" data-numero="{WHATS[n][0]}">'
            f'<span class="numero-icone">{I["conversa"]}</span>'
            f'<span class="numero-texto"><span class="numero-tipo">WhatsApp</span><span class="numero-valor">{WHATS[n][1]}</span></span></a>')

RAMOS_NOMES = ["Lanchonete", "Barbearia", "Salão de beleza", "Consultório odontológico", "Restaurante", "Loja", "Clínica"]

JANELAS_GERAIS = f"""  <dialog class="janela janela-pequena" id="janela-contato" aria-labelledby="contato-titulo">
    <button class="janela-fechar" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    <div class="janela-corpo">
      <h2 id="contato-titulo" tabindex="-1" autofocus>{BOTAO}</h2>
      <p class="janela-resumo">Escolha um número. A conversa abre com a mensagem pronta; é só enviar.</p>
      <p class="contato-leva" data-contato-leva hidden></p>
      <div class="numeros">
        {numero_opcao(0)}
        {numero_opcao(1)}
        <a class="numero numero-qualquer" href="{link_whats(None, 0)}" target="_blank" rel="noopener" data-numero="sorteio"><span class="numero-icone">{I["sorteio"]}</span><span class="numero-texto"><span class="numero-tipo">Tanto faz</span><span class="numero-valor">Qualquer um dos dois</span></span></a>
      </div>
    </div>
  </dialog>

  <dialog class="gaveta" id="carrinho" aria-labelledby="carrinho-titulo">
    <div class="gaveta-topo">
      <h2 id="carrinho-titulo" tabindex="-1" autofocus>Seu orçamento <span class="gaveta-qtd" data-carrinho-qtd></span></h2>
      <button class="icone-botao" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    </div>
    <div class="gaveta-corpo">
      <div class="gaveta-vazia" data-carrinho-vazio>
        <span class="gaveta-vazia-icone">{I["orcamento"]}</span>
        <p><strong>Nenhum serviço no orçamento ainda.</strong></p>
        <p>Na página de serviços, toque em "Adicionar ao orçamento" no que interessar. Tudo fica guardado aqui.</p>
        <a class="botao botao-contorno" href="servicos.html">Ver serviços</a>
      </div>
      <ul class="gaveta-lista" data-carrinho-lista></ul>
      <p class="gaveta-nota" data-carrinho-nota hidden>Valores combinados pelo WhatsApp, conforme a necessidade do seu negócio.</p>
      <form class="gaveta-form" data-carrinho-form>
        <p class="gaveta-form-titulo">Para a gente já chegar preparado <span>(opcional)</span></p>
        <label>Seu nome<input name="nome" autocomplete="name"></label>
        <label>Tipo de negócio<input name="negocio" list="lista-negocios" placeholder="Ex.: barbearia"></label>
        <datalist id="lista-negocios">{"".join(f'<option value="{r}">' for r in RAMOS_NOMES)}</datalist>
        <label>Observação<textarea name="obs" rows="3" placeholder="Ex.: atendo 40 clientes por dia no WhatsApp"></textarea></label>
      </form>
    </div>
    <div class="gaveta-base" data-carrinho-base>
      <button class="botao" type="button" data-carrinho-enviar>Enviar orçamento pelo WhatsApp</button>
      <button class="link-botao" type="button" data-carrinho-limpar>Limpar orçamento</button>
    </div>
  </dialog>

  <div class="aviso" role="status" aria-live="polite" data-aviso hidden>
    <span class="aviso-icone">{I["check"]}</span>
    <span class="aviso-texto" data-aviso-texto></span>
    <button class="aviso-botao" type="button" data-abrir-carrinho>Ver orçamento</button>
  </div>
"""


def pagina(arq, titulo, descricao, corpo, janelas=""):
    url = BASE + ("" if arq == "index.html" else arq)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{descricao}">
  <meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0B0B0F" media="(prefers-color-scheme: dark)">
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

  <link rel="icon" href="assets/icons/icon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/icons/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">

  <!-- aplica o tema antes de desenhar a página (evita piscar) -->
  <script>(function(){{var t;try{{t=localStorage.getItem("kyzent-tema")}}catch(e){{}}if(t!=="light"&&t!=="dark")t=window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";document.documentElement.setAttribute("data-theme",t);document.documentElement.classList.add("js")}})();</script>

  <link rel="preload" href="assets/fonts/mona-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css?v={VERSAO}">
  <script src="js/main.js?v={VERSAO}" defer></script>
</head>
<body>
  <a class="pular" href="#conteudo">Pular para o conteúdo</a>

  <header class="barra">
    <div class="container barra-conteudo">
      <a class="barra-logo" href="index.html" aria-label="Kyzent, página inicial">{logos()}</a>
      <nav aria-label="Principal">{menu(arq, "menu")}</nav>
      <div class="barra-acoes">
        <button class="orcamento-botao" type="button" data-abrir-carrinho hidden>Orçamento <span data-contador>(0)</span></button>
        <button class="icone-botao tema-botao" type="button" data-trocar-tema aria-label="Trocar tema">{I["lua"]}{I["sol"]}</button>
        <button class="icone-botao botao-menu" type="button" data-abrir-menu aria-expanded="false" aria-controls="menu-celular" aria-label="Abrir menu">{svg('<path d="M4 7h16M4 12h16M4 17h16"/>', "icone-abrir")}{svg('<path d="M6 6l12 12M18 6L6 18"/>', "icone-fechar")}</button>
        <a class="botao" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a>
      </div>
    </div>
    <nav class="menu-celular" id="menu-celular" aria-label="Menu">
      {menu(arq, "")}
      <button class="menu-tema" type="button" data-trocar-tema>{I["lua"]}{I["sol"]}<span class="menu-tema-escuro">Usar tema escuro</span><span class="menu-tema-claro">Usar tema claro</span></button>
      <a class="botao" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a>
    </nav>
  </header>

  <main id="conteudo">
{corpo}
  </main>

  <footer class="rodape">
    <div class="container">
      <div class="rodape-grade">
        <div class="rodape-marca">
          <a href="index.html" aria-label="Kyzent, página inicial">{logos()}</a>
          <p>Automação inteligente e IA para comércios de Paulínia e região.</p>
        </div>
        <div>
          <h2>Navegação</h2>
          {menu(None, "")}
        </div>
        <div>
          <h2>WhatsApp</h2>
          <ul>
            <li><a href="{link_whats(None, 0)}" target="_blank" rel="noopener">{WHATS[0][1]}</a></li>
            <li><a href="{link_whats(None, 1)}" target="_blank" rel="noopener">{WHATS[1][1]}</a></li>
          </ul>
        </div>
        <div>
          <h2>Redes</h2>
          <ul>
            <li><a href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">Instagram @kyzent.tech</a></li>
          </ul>
        </div>
      </div>
      <div class="rodape-base">
        <p>© <span data-ano>2026</span> Kyzent Technology Solutions</p>
        <p>Paulínia/SP</p>
      </div>
    </div>
  </footer>
  <div class="barra-fixa">
    <button class="barra-fixa-orcamento" type="button" data-abrir-carrinho hidden>Orçamento <span data-contador>(0)</span></button>
    <a class="whats-fixo" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}<span class="whats-longo">{BOTAO}</span><span class="whats-curto">WhatsApp</span></a>
  </div>

{JANELAS_GERAIS}
{janelas}
</body>
</html>
"""

CHAMADA = f"""    <section class="chamada" aria-labelledby="titulo-chamada">
      <div class="container">
        <div class="chamada-caixa">
          <div>
            <h2 id="titulo-chamada">Quer ver funcionando no seu comércio?</h2>
            <p>Conte como é o seu dia a dia. A gente responde no WhatsApp e monta um orçamento personalizado.</p>
          </div>
          <a class="botao" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{BOTAO}</a>
        </div>
      </div>
    </section>"""

PARA_QUEM = f"""    <section class="secao secao-faixa" id="para-quem" aria-labelledby="titulo-ramos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-ramos">Feito para o seu tipo de comércio.</h2>
          <p>Toque no seu ramo e veja o que a Kyzent faz no seu dia a dia.</p>
        </div>
        {ramos_cartoes()}
      </div>
    </section>"""

ETAPAS = [
    ("Você chama no WhatsApp", "Conta como funciona o seu comércio e o que mais toma o seu tempo."),
    ("A gente configura", "A IA aprende o seu cardápio, os preços, os horários e o jeito de atender do seu comércio."),
    ("A IA começa a atender", "E a gente acompanha, ajusta e dá suporte todo mês."),
]
COMO_FUNCIONA = f"""    <section class="secao" aria-labelledby="titulo-etapas">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-etapas">Como funciona.</h2>
        </div>
        <ol class="etapas">
{chr(10).join(f'          <li class="etapa"><span class="etapa-num">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(ETAPAS))}
        </ol>
      </div>
    </section>"""

PILARES = """    <section class="secao secao-faixa" aria-labelledby="titulo-pilares">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-pilares">Missão, visão e valores.</h2>
        </div>
        <div class="grade grade-3 grade-pilares">
          <article class="pilar">
            <h3>Nossa missão</h3>
            <p>Oferecer soluções tecnológicas que promovam produtividade, automação e crescimento, otimizando processos e potencializando os resultados dos nossos clientes.</p>
          </article>
          <article class="pilar">
            <h3>Nossa visão</h3>
            <p>Ser referência em Tecnologia e Inovação, reconhecida por transformar negócios e contribuir para a evolução do mercado.</p>
          </article>
          <article class="pilar">
            <h3>Nossos valores</h3>
            <p>Atuar com respeito, ética e compromisso com nossos clientes e colaboradores, construindo relações sólidas e duradouras, pautadas na lealdade, transparência e dignidade.</p>
          </article>
        </div>
      </div>
    </section>"""

# ------------------------------------------------------------------ Início
# Textos oficiais: empresa/KYZENT.md (Quem somos, missão, visão, valores) e a lista de serviços.
# foto de cada frente: arquivo, largura, altura e posição do recorte
FOTO_FRENTE = {
    "01": ("celular-mensagem.jpg", 733, 1100, "50% 45%"),
    "02": ("comercio-balcao.jpg", 1600, 900, "50% 50%"),
    "03": ("equipe-reuniao.jpg", 1600, 900, "50% 50%"),
    "04": ("cafeteria.jpg", 733, 1100, "50% 62%"),
}

def frente(n, titulo, modulo, itens):
    foto, w, h, pos = FOTO_FRENTE[n]
    lista = "".join(f"<li>{a}</li>" for a in itens)
    return (f'          <li><article class="cartao cartao-link">'
            f'<div class="cartao-foto"><img src="assets/fotos/{foto}" alt="" width="{w}" height="{h}" loading="lazy" style="object-position:{pos}"></div>'
            f'<div class="cartao-corpo"><h3>{titulo}</h3><ul class="cartao-itens">{lista}</ul>'
            f'<a class="cartao-ver" href="servicos.html#modulo-{modulo}">Ver serviços</a></div></article></li>')

FRENTES = "\n".join(frente(n, t, mod, itens) for n, t, ic, curto, resumo, mod, itens in AREAS)

INICIO = f"""    <section class="inicio" aria-labelledby="titulo-inicio">
      <div class="container inicio-grade">
        <div class="inicio-texto">
          <h1 id="titulo-inicio">Tecnologia e inovação para o seu comércio.</h1>
          <p class="inicio-apoio">Automatizamos o atendimento, as vendas e a gestão de pequenas empresas de Paulínia e região.</p>
          <div class="inicio-acoes">
            <a class="botao botao-grande" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}{BOTAO}</a>
          </div>
        </div>
        <div class="inicio-marca" aria-hidden="true">
          <img class="logo-claro" src="assets/img/kyzent-k-claro.svg" alt="" width="1080" height="520">
          <img class="logo-escuro" src="assets/img/kyzent-k-escuro.svg" alt="" width="1080" height="520">
        </div>
      </div>
    </section>

    <section class="secao secao-faixa" aria-labelledby="titulo-frentes">
      <div class="container">
        <div class="cabeca-linha">
          <div class="cabeca">
            <h2 id="titulo-frentes">Automação inteligente para empresas.</h2>
            <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
          </div>
          <a class="link-seta" href="servicos.html">Ver serviços</a>
        </div>
        <ol class="grade grade-4">
{FRENTES}
        </ol>
      </div>
    </section>

{PARA_QUEM.replace('class="secao secao-faixa"', 'class="secao"', 1)}

{CHAMADA}"""

# ------------------------------------------------------------------ Quem somos
QUEM = f"""    <section class="pagina-topo pagina-topo-larga" aria-labelledby="titulo-pagina">
      <div class="container">
        <h1 id="titulo-pagina">Quem somos</h1>
        <p>Somos a Kyzent, uma empresa de Tecnologia e Inovação de Paulínia, dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio. Trabalhamos com Inteligência Artificial para melhorar o atendimento, apoiar as vendas e organizar a gestão do dia a dia, e também criamos soluções sob medida quando o seu negócio pede algo diferente.</p>
        <p>Cada solução é pensada para a realidade do seu comércio e vem com manutenção e suporte da nossa equipe, para você ter a tecnologia funcionando sem se preocupar com a parte técnica.</p>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-proposito">
      <div class="container dupla">
        <div class="dupla-foto">
          <img src="assets/fotos/equipe-reuniao.jpg" alt="Equipe conversando em uma reunião num escritório" width="1600" height="900">
        </div>
        <div class="dupla-texto">
          <h2 id="titulo-proposito">Transformar processos por meio da tecnologia.</h2>
          <p>Nosso propósito é transformar processos por meio da tecnologia, oferecendo mais produtividade, automação e eficiência para impulsionar os resultados dos nossos clientes.</p>
          <p>A Kyzent é uma empresa de tecnologia de Paulínia que automatiza o trabalho repetitivo do seu comércio. Em vez de contratar mais gente, você assina um serviço que trabalha junto com a sua equipe.</p>
        </div>
      </div>
    </section>

{PILARES}"""

# ------------------------------------------------------------------ Serviços
def balao(quem, texto, hora):
    tiques = TIQUES if quem == "ia" else ""
    return f'<div class="zap-msg zap-{quem}"><p>{texto}</p><span class="zap-hora">{hora}{tiques}</span></div>'

CONVERSA = f"""<figure class="zap-figura">
          <div class="zap" role="img" aria-label="Exemplo de conversa no WhatsApp: um cliente pede um lanche às 21h47 e a IA anota o pedido, soma o total e combina o pagamento.">
            <div class="zap-topo" aria-hidden="true">
              <span class="zap-voltar">{I["voltar"]}</span>
              <span class="zap-avatar">SL</span>
              <span class="zap-nome"><strong>Sua lanchonete</strong><small>online</small></span>
            </div>
            <div class="zap-corpo" aria-hidden="true">
              <p class="zap-dia">Hoje</p>
              {balao("cliente", "Boa noite! Ainda dá pra pedir?", "21:47")}
              {balao("ia", "Boa noite! Dá sim, a cozinha vai até as 23h. O que vai ser?", "21:47")}
              {balao("cliente", "1 X-salada e 1 refri lata. Entrega na Rua das Flores, 120", "21:48")}
              {balao("ia", "Anotado:<br>1 X-salada: R$ 22,00<br>1 refri lata: R$ 6,00<br>Entrega: R$ 5,00<br><strong>Total: R$ 33,00</strong><br>Vai pagar no Pix ou na entrega?", "21:48")}
              {balao("cliente", "Pix", "21:49")}
              {balao("ia", "Perfeito! Mandei a chave Pix aqui embaixo. Seu pedido chega em uns 40 minutos.", "21:49")}
            </div>
            <div class="zap-base" aria-hidden="true"><span class="zap-campo">Mensagem</span><span class="zap-mic">{I["mic"]}</span></div>
          </div>
          <figcaption>Exemplo de conversa. A IA responde com o cardápio, os preços e o horário do seu comércio.</figcaption>
        </figure>"""

# ilustrações de cada módulo (no lugar das fotos de banco): exemplos desenhados em HTML/CSS
def mock_agenda():
    linhas = [("09:00", "Carlos", "Corte", "ok", "Confirmado"),
              ("10:30", "Marina", "Retorno", "ok", "Confirmado"),
              ("11:15", "", "", "livre", "Horário livre"),
              ("14:00", "João", "Avaliação", "lembrete", "Lembrete enviado")]
    lis = ""
    for hora, nome, serv, cls, estado in linhas:
        quem = f"<strong>{nome}</strong><small>{serv}</small>" if nome else "<small>Pode ser preenchido pela IA</small>"
        lis += f'<li class="mock-linha mock-{cls}"><time>{hora}</time><span class="mock-quem">{quem}</span><span class="mock-chip">{estado}</span></li>'
    return f"""<figure class="mock-figura">
          <div class="mock mock-agenda" role="img" aria-label="Exemplo de agenda do dia, com horários confirmados e lembretes enviados automaticamente.">
            <div class="mock-topo" aria-hidden="true"><strong>Agenda de hoje</strong><span>4 horários</span></div>
            <ul class="mock-corpo" aria-hidden="true">{lis}</ul>
          </div>
          <figcaption>Exemplo ilustrativo. A IA marca, confirma e lembra o cliente, sem você parar o que está fazendo.</figcaption>
        </figure>"""

def mock_gestao():
    barras = "".join(f'<i style="--h:{h}%"></i>' for h in (38, 52, 44, 70, 58, 86, 64))
    return f"""<figure class="mock-figura">
          <div class="mock mock-gestao" role="img" aria-label="Exemplo de painel com pedidos do dia, clientes cadastrados e um gráfico da semana.">
            <div class="mock-topo" aria-hidden="true"><strong>Resumo da semana</strong><span>Atualizado agora</span></div>
            <div class="mock-numeros" aria-hidden="true">
              <div><small>Pedidos</small><strong>128</strong></div>
              <div><small>Clientes</small><strong>214</strong></div>
              <div><small>Retornos</small><strong>37</strong></div>
            </div>
            <div class="mock-barras" aria-hidden="true">{barras}</div>
          </div>
          <figcaption>Exemplo ilustrativo. Cadastros, pedidos e relatórios organizados sem planilha na mão.</figcaption>
        </figure>"""

def mock_site():
    return f"""<figure class="mock-figura">
          <div class="mock mock-site" role="img" aria-label="Exemplo de site de um comércio, com título, botão de WhatsApp e três blocos de serviços.">
            <div class="mock-topo mock-navegador" aria-hidden="true"><span class="mock-pontos"><i></i><i></i><i></i></span><span class="mock-url">seunegocio.com.br</span></div>
            <div class="mock-pagina" aria-hidden="true">
              <p class="mock-titulo">O seu negócio, do seu jeito.</p>
              <p class="mock-sub">Serviços, horários e contato num lugar só.</p>
              <span class="mock-botao">{BOTAO}</span>
              <div class="mock-blocos"><i></i><i></i><i></i></div>
            </div>
          </div>
          <figcaption>Exemplo ilustrativo. O site é feito sob medida, com o seu jeito e o que você quer mostrar.</figcaption>
        </figure>"""

def mock_ia():
    def fila(nomes, cls):
        return f'<ul class="mock-fila {cls}">' + "".join(f"<li>{n}</li>" for n in nomes) + "</ul>"
    return f"""<figure class="mock-figura">
          <div class="mock mock-ia" role="img" aria-label="Exemplo de como uma IA sob medida recebe mensagens do WhatsApp, Instagram e site e conversa com agenda, estoque e cadastro de clientes.">
            <div class="mock-fluxo" aria-hidden="true">
              {fila(["WhatsApp", "Instagram", "Site"], "mock-entrada")}
              <div class="mock-seta"></div>
              <div class="mock-ia-centro">{I["avancado"]}<strong>IA sob medida</strong><small>Do jeito da sua empresa</small></div>
              <div class="mock-seta"></div>
              {fila(["Agenda", "Estoque", "Clientes"], "mock-saida")}
            </div>
          </div>
          <figcaption>Exemplo ilustrativo. A IA conversa com os canais e com os sistemas que a sua empresa já usa.</figcaption>
        </figure>"""

EXEMPLOS = {"whatsapp": CONVERSA, "agenda": mock_agenda(), "gestao": mock_gestao(), "site": mock_site(), "ia": mock_ia()}

# nome do ramo (filtro): id -> (texto do botão, ícone)
FILTRO_RAMOS = {"lanchonete": ("Lanchonete", "lanche"), "barbearia": ("Barbearia", "tesoura"),
                "salao": ("Salão de beleza", "pente"), "consultorio": ("Consultório", "dente")}

abas = []
paineis = []
for i, (mid, t, curto, ic, resumo, nomes) in enumerate(MODULOS):
    sel = "true" if i == 0 else "false"
    abas.append(
        f'<button class="aba" type="button" role="tab" id="aba-{mid}" aria-controls="modulo-{mid}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="aba-icone">{I[ic]}</span><span class="aba-texto"><span class="aba-longo">{t}</span><span class="aba-curto">{curto}</span></span>'
        f'<span class="aba-qtd" data-qtd>{len(nomes)}</span></button>')
    cards = "\n".join(
        f'''              <li class="item" data-ramos="{" ".join(CATALOGO[a][1])}">
                <h4>{a}</h4>
                <p>{CATALOGO[a][0]}</p>
                <button class="item-add" type="button" data-servico="{a}" data-area="{t}" aria-pressed="false">
                  <span class="item-add-mais">{I["mais"]}</span><span class="item-add-feito">{I["check"]}</span><span class="item-add-rotulo">Adicionar</span>
                </button>
              </li>''' for a in nomes)
    paineis.append(f"""        <section class="painel tem-exemplo" id="modulo-{mid}" role="tabpanel" aria-labelledby="aba-{mid}" tabindex="-1">
          <div class="painel-lado">
            <span class="painel-icone">{I[ic]}</span>
            <span class="painel-num" data-painel-num>{len(nomes)} {"serviço" if len(nomes) == 1 else "serviços"}</span>
            <h2>{t}</h2>
            <p>{resumo}</p>
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

SERVICOS_PAG = f"""    <section class="pagina-topo pagina-topo-servicos" aria-labelledby="titulo-pagina">
      <div class="container topo-servicos">
        <div>
          <h1 id="titulo-pagina">Automação inteligente para empresas.</h1>
          <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
        </div>
      </div>
    </section>

{COMO_FUNCIONA.replace('class="secao"', 'class="secao secao-faixa"', 1)}

    <section class="secao secao-servicos" id="catalogo" aria-label="Serviços por módulo">
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
        <p class="precos-nota">Valores combinados conforme a necessidade de cada negócio.</p>
      </div>
    </section>
"""

DESC = "A Kyzent é uma empresa de Tecnologia e Inovação dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio. Paulínia e região."

saidas = [
    ("index.html", "Kyzent | Tecnologia e Inovação para o seu comércio", DESC, INICIO, ramos_janelas()),
    ("quem-somos.html", "Quem somos | Kyzent", "A Kyzent é uma empresa de Tecnologia e Inovação de Paulínia. Conheça os sócios, a missão, a visão e os valores.", QUEM, ""),
    ("servicos.html", "Serviços | Kyzent", "WhatsApp, agendamento, gestão, site e IA sob medida para o seu comércio. Escolha o seu tipo de negócio e monte o seu orçamento.", SERVICOS_PAG, FILTRO_JANELA),
]
for arq, titulo, desc, corpo, janelas in saidas:
    with open(os.path.join(SITE, arq), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina(arq, titulo, desc, corpo, janelas))
    print("ok", arq)
