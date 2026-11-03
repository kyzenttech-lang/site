"""Monta as páginas do site com o mesmo topo, rodapé e janelas dos ramos.
Uso (na raiz do site): python tools/monta_paginas.py .
Atenção: sobrescreve index.html, quem-somos.html, servicos.html e contato.html.
Edite o texto aqui e rode de novo, para as páginas não ficarem diferentes entre si."""
import os, sys
from urllib.parse import quote

SITE = sys.argv[1]
BASE = "https://kyzenttech-lang.github.io/site/"
VERSAO = "6"   # aumente a cada mudança no CSS/JS, para o navegador baixar o arquivo novo

WHATS = [("5519988728894", "(19) 98872-8894"), ("5519971246077", "(19) 97124-6077")]
MSG = quote("Olá, vim pelo site da KYZENT")

def link_whats(msg=None, n=0):
    return f"https://wa.me/{WHATS[n][0]}?text={quote(msg) if msg else MSG}"

def svg(d, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

I = {
    "lua": svg('<path d="M20.5 13.2A8.5 8.5 0 1 1 10.8 3.5a6.6 6.6 0 0 0 9.7 9.7z"/>', "icone-lua"),
    "sol": svg('<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>', "icone-sol"),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "fechar": svg('<path d="M6 6l12 12M18 6L6 18"/>'),
    "mais": svg('<path d="M12 5v14M5 12h14"/>'),
    "conversa": svg('<path d="M20.5 11.5a8.5 8.5 0 0 1-12.4 7.6L3.5 20.5l1.4-4.4A8.5 8.5 0 1 1 20.5 11.5z"/>'),
    "vendas": svg('<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'),
    "gestao": svg('<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M8 13h3M8 16h6"/>'),
    "orcamento": svg('<path d="M9 3.5h6v3H9z"/><path d="M9 5H6.5A1.5 1.5 0 0 0 5 6.5v13A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5v-13A1.5 1.5 0 0 0 17.5 5H15"/><path d="M9 11.5h6M9 15.5h4"/>'),
    "sorteio": svg('<path d="M16 3.5h4.5V8M4 20 20.5 3.5M20.5 16v4.5H16M14.5 14.5l6 6M4 4l5 5"/>'),
    "check": svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    "avancado": svg('<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>'),
}

PAGINAS = [("index.html", "Início"), ("quem-somos.html", "Quem somos"), ("servicos.html", "Serviços"), ("contato.html", "Contato")]

# ------------------------------------------------------------------ serviços
SERVICOS = [
    ("01", "Atendimento e relacionamento", "conversa",
     "Chatbots no WhatsApp e no Instagram, respostas automáticas e triagem para atendentes.", [
        ("Chatbots inteligentes", "Atendimento automatizado pelo WhatsApp e Instagram, disponível 24 horas."),
        ("Respostas inteligentes", "Resolução automática de dúvidas e perguntas frequentes."),
        ("Triagem de atendimento", "Identificação das necessidades dos clientes e encaminhamento para atendentes humanos."),
    ]),
    ("02", "Vendas e captação de clientes", "vendas",
     "Leads qualificados, agendamentos, follow-up e orçamentos no automático.", [
        ("Captação e qualificação de leads", "Identificação e classificação de potenciais clientes."),
        ("Agendamentos automáticos", "Organização de reuniões, consultas e serviços."),
        ("Follow-up inteligente", "Acompanhamento automático de clientes e recuperação de oportunidades."),
        ("Orçamentos automatizados", "Geração e envio de propostas comerciais."),
    ]),
    ("03", "Administração e gestão empresarial", "gestao",
     "Cadastros, pedidos, CRM, relatórios, documentos e sistemas conectados.", [
        ("Gestão de cadastros e pedidos", "Organização automatizada de informações e solicitações."),
        ("Integração com CRM", "Centralização e gerenciamento do relacionamento com clientes."),
        ("Relatórios automatizados", "Geração de relatórios para acompanhamento empresarial."),
        ("Automação de documentos", "Organização e envio automático de documentos."),
        ("Assistentes internos de IA", "Ferramentas inteligentes para auxiliar funcionários."),
        ("Integração de sistemas", "Conexão entre diferentes plataformas e ferramentas empresariais."),
    ]),
    ("04", "Soluções avançadas e personalizadas", "avancado",
     "Agentes de IA, integração com ERP e sistemas sob medida para a sua empresa.", [
        ("Agentes de IA personalizados", "Inteligência artificial desenvolvida conforme as necessidades da empresa."),
        ("Integração com estoque e ERP", "Automatização e conexão de sistemas de gestão empresarial."),
        ("Centrais inteligentes de atendimento", "Múltiplos agentes de IA trabalhando em diferentes funções."),
        ("Automação de processos comerciais", "Integração e otimização de etapas do processo de vendas."),
        ("Sistemas personalizados", "Desenvolvimento de soluções de atendimento e automação sob medida."),
    ]),
]

# ------------------------------------------------------------------ ramos (cartões com janela)
RAMOS = [
    ("lanchonete", "Lanchonetes", "lanchonete.jpg", 1200, 675, "uma lanchonete",
     "Pedidos, dúvidas e clientes atendidos sem parar o caixa.", [
        ("Chatbot no WhatsApp e no Instagram", "Recebe os pedidos e apresenta o cardápio a qualquer hora, inclusive no horário de pico."),
        ("Respostas inteligentes", "Horário de funcionamento, endereço, entrega e formas de pagamento respondidos na hora."),
        ("Gestão de pedidos", "Cada pedido chega organizado, sem anotação perdida em papel."),
        ("Follow-up inteligente", "Chama de volta o cliente que não pede há algum tempo."),
        ("Relatórios automatizados", "Pedidos e vendas do período reunidos para você acompanhar."),
        ("Integração com estoque", "Os pedidos conversando com o controle do que tem na cozinha."),
    ]),
    ("barbearia", "Barbearias", "barbearia.jpg", 880, 1100, "uma barbearia",
     "Agenda cheia e organizada, sem responder mensagem entre um corte e outro.", [
        ("Agendamentos automáticos", "O cliente escolhe o serviço e o horário direto na conversa."),
        ("Chatbot no WhatsApp e no Instagram", "Atende quem chama de noite, no domingo ou enquanto você está cortando."),
        ("Respostas inteligentes", "Preços, serviços e horários livres respondidos na hora."),
        ("Follow-up inteligente", "Lembra o cliente do horário e chama de volta quem já está na hora do próximo corte."),
        ("Cadastro de clientes e CRM", "Histórico de cada cliente guardado em um só lugar."),
        ("Relatórios automatizados", "Atendimentos e faturamento do período para acompanhar o negócio."),
    ]),
    ("salao", "Salões de beleza", "salao.jpg", 734, 1100, "um salão de beleza",
     "Agenda de cada profissional organizada e cliente bem atendida do primeiro contato ao retorno.", [
        ("Agendamentos automáticos", "Marcação por serviço e por profissional, sem conflito de horário."),
        ("Respostas inteligentes", "Serviços, preços e duração de cada procedimento respondidos na hora."),
        ("Triagem de atendimento", "Pedidos que precisam de avaliação vão direto para a pessoa certa da equipe."),
        ("Orçamentos automatizados", "Propostas para pacotes, eventos e noivas montadas e enviadas."),
        ("Follow-up inteligente", "Lembretes de horário e convite de retorno para manutenção."),
        ("Cadastro de clientes e CRM", "Preferências e histórico de cada cliente sempre à mão."),
    ]),
    ("consultorio", "Consultórios odontológicos", "consultorio.jpg", 1200, 800, "um consultório odontológico",
     "Recepção mais leve, agenda confirmada e pacientes acompanhados.", [
        ("Agendamentos automáticos", "Marcação e confirmação de consultas pelo WhatsApp."),
        ("Triagem de atendimento", "Identifica se é avaliação, retorno ou urgência e encaminha para a recepção."),
        ("Respostas inteligentes", "Convênios, endereço, horários e tipos de tratamento respondidos na hora."),
        ("Follow-up inteligente", "Lembrete de consulta e de retorno para revisão e limpeza."),
        ("Automação de documentos", "Envio automático de orientações e documentos ao paciente."),
        ("Cadastro de pacientes e CRM", "Informações de cada paciente organizadas, com cuidado com os dados (LGPD)."),
    ]),
]

def ramos_cartoes():
    cartoes = []
    for rid, nome, foto, w, h, *_ in RAMOS:
        cartoes.append(
            f'<button class="ramo" type="button" data-abrir-janela="janela-{rid}" aria-haspopup="dialog">'
            f'<img src="assets/fotos/{foto}" alt="" width="{w}" height="{h}" loading="lazy">'
            f'<span class="ramo-texto"><span class="ramo-nome">{nome}</span>'
            f'<span class="ramo-ver">Ver o que fazemos {I["mais"]}</span></span></button>')
    return '<div class="ramos">\n          ' + "\n          ".join(cartoes) + "\n        </div>"

def ramos_janelas():
    janelas = []
    for rid, nome, foto, w, h, artigo, resumo, itens in RAMOS:
        lis = "".join(f"<li><strong>{t}</strong> {d}</li>" for t, d in itens)
        msg = f"Olá, vim pelo site da KYZENT. Tenho {artigo} e quero saber o que vocês podem automatizar."
        janelas.append(f"""  <dialog class="janela" id="janela-{rid}" aria-labelledby="janela-{rid}-titulo">
    <div class="janela-foto"><img src="assets/fotos/{foto}" alt="" width="{w}" height="{h}" loading="lazy"></div>
    <button class="janela-fechar" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    <div class="janela-corpo">
      <p class="janela-sobre">O que a KYZENT faz para</p>
      <h2 id="janela-{rid}-titulo" tabindex="-1" autofocus>{nome}</h2>
      <p class="janela-resumo">{resumo}</p>
      <ul class="lista-check">{lis}</ul>
      <div class="janela-acoes">
        <a class="botao" href="{link_whats(msg)}" target="_blank" rel="noopener" data-contato data-msg="{msg}">Quero isso no meu comércio</a>
        <a class="link-seta" href="servicos.html">Ver todos os serviços</a>
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
    return ('<img class="logo-claro" src="assets/img/kyzent-horizontal-claro.svg" alt="KYZENT, automação e IA" width="590" height="140">'
            '<img class="logo-escuro" src="assets/img/kyzent-horizontal-escuro.svg" alt="KYZENT, automação e IA" width="590" height="140">')

def numero_opcao(n):
    return (f'<a class="numero" href="{link_whats(None, n)}" target="_blank" rel="noopener" data-numero="{WHATS[n][0]}">'
            f'<span class="numero-icone">{I["conversa"]}</span>'
            f'<span class="numero-texto"><span class="numero-tipo">WhatsApp</span><span class="numero-valor">{WHATS[n][1]}</span></span></a>')

RAMOS_NOMES = ["Lanchonete", "Barbearia", "Salão de beleza", "Consultório odontológico", "Restaurante", "Loja", "Clínica"]

JANELAS_GERAIS = f"""  <dialog class="janela janela-pequena" id="janela-contato" aria-labelledby="contato-titulo">
    <button class="janela-fechar" type="button" data-fechar-janela aria-label="Fechar">{I["fechar"]}</button>
    <div class="janela-corpo">
      <h2 id="contato-titulo" tabindex="-1" autofocus>Falar com a KYZENT</h2>
      <p class="janela-resumo">Escolha um número. A conversa abre no WhatsApp com a mensagem pronta; é só enviar.</p>
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
      <form class="gaveta-form" data-carrinho-form>
        <p class="gaveta-form-titulo">Para a gente já chegar preparado <span>(opcional)</span></p>
        <label>Seu nome<input name="nome" autocomplete="name"></label>
        <label>Tipo de negócio<input name="negocio" list="lista-negocios" placeholder="Ex.: barbearia"></label>
        <datalist id="lista-negocios">{"".join(f'<option value="{r}">' for r in RAMOS_NOMES)}</datalist>
        <label>Observação<textarea name="obs" rows="3" placeholder="Ex.: atendo 40 clientes por dia no WhatsApp"></textarea></label>
      </form>
    </div>
    <div class="gaveta-base" data-carrinho-base>
      <button class="botao" type="button" data-carrinho-enviar>Enviar pedido pelo WhatsApp</button>
      <button class="link-botao" type="button" data-carrinho-limpar>Limpar orçamento</button>
    </div>
  </dialog>

  <div class="aviso" role="status" aria-live="polite" data-aviso hidden>
    <span class="aviso-icone">{I["check"]}</span>
    <span class="aviso-texto" data-aviso-texto></span>
    <button class="aviso-botao" type="button" data-abrir-carrinho>Ver orçamento</button>
  </div>"""


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
  <meta property="og:site_name" content="KYZENT">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descricao}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Logo da KYZENT com o texto: automação e IA para empresas">
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
      <a class="barra-logo" href="index.html" aria-label="KYZENT, página inicial">{logos()}</a>
      <nav aria-label="Principal">{menu(arq, "menu")}</nav>
      <div class="barra-acoes">
        <button class="icone-botao carrinho-botao" type="button" data-abrir-carrinho aria-label="Ver orçamento">{I["orcamento"]}<span class="contador" data-contador hidden>0</span></button>
        <button class="icone-botao" type="button" data-trocar-tema aria-label="Trocar tema">{I["lua"]}{I["sol"]}</button>
        <button class="icone-botao botao-menu" type="button" data-abrir-menu aria-expanded="false" aria-controls="menu-celular" aria-label="Abrir menu">{svg('<path d="M4 7h16M4 12h16M4 17h16"/>', "icone-abrir")}{svg('<path d="M6 6l12 12M18 6L6 18"/>', "icone-fechar")}</button>
        <a class="botao" href="contato.html" data-contato>Fale conosco</a>
      </div>
    </div>
    <nav class="menu-celular" id="menu-celular" aria-label="Menu">
      {menu(arq, "")}
      <a class="botao" href="contato.html" data-contato>Fale conosco</a>
    </nav>
  </header>

  <main id="conteudo">
{corpo}
  </main>

  <footer class="rodape">
    <div class="container">
      <div class="rodape-grade">
        <div class="rodape-marca">
          <a href="index.html" aria-label="KYZENT, página inicial">{logos()}</a>
          <p>Automação inteligente e IA para empresas de Paulínia e região.</p>
        </div>
        <div>
          <h2>Navegação</h2>
          {menu(None, "")}
        </div>
        <div>
          <h2>Contato</h2>
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
        <p>© <span data-ano>2026</span> KYZENT Technology Solutions</p>
        <p>Paulínia/SP</p>
      </div>
    </div>
  </footer>
  <div class="barra-fixa">
    <button class="barra-fixa-orcamento" type="button" data-abrir-carrinho hidden>{I["orcamento"]}<span>Orçamento</span><span class="contador" data-contador>0</span></button>
    <a class="whats-fixo" href="{link_whats()}" target="_blank" rel="noopener" data-contato>{I["conversa"]}<span class="whats-longo">Chamar no WhatsApp</span><span class="whats-curto">WhatsApp</span></a>
  </div>

{JANELAS_GERAIS}
{janelas}
</body>
</html>
"""

CHAMADA = """    <section class="chamada" aria-labelledby="titulo-chamada">
      <div class="container">
        <div class="chamada-caixa">
          <div>
            <h2 id="titulo-chamada">Mais eficiência, menos tarefas manuais e processos mais inteligentes.</h2>
            <p>Entre em contato e solicite um orçamento personalizado.</p>
          </div>
          <a class="botao" href="contato.html" data-contato>Solicitar orçamento</a>
        </div>
      </div>
    </section>"""

PARA_QUEM = f"""    <section class="secao secao-faixa" id="para-quem" aria-labelledby="titulo-ramos">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-ramos">Soluções para cada tipo de comércio.</h2>
          <p>Toque no seu ramo e veja o que a KYZENT pode automatizar no seu dia a dia.</p>
        </div>
        {ramos_cartoes()}
        <p class="ramos-nota">Tem outro tipo de negócio? <a class="link-seta" href="contato.html" data-contato>Fale com a gente</a></p>
      </div>
    </section>"""

# ------------------------------------------------------------------ Início
cartoes_servicos = "\n".join(
    f'          <li><a class="cartao cartao-link" href="servicos.html#servico-{n}"><span class="cartao-icone">{I[ic]}</span>'
    f'<h3>{t}</h3><p>{resumo}</p><span class="cartao-ver">Ver serviços</span></a></li>'
    for n, t, ic, resumo, _ in SERVICOS)

INICIO = f"""    <section class="inicio" aria-labelledby="titulo-inicio">
      <div class="container inicio-grade">
        <div>
          <h1 id="titulo-inicio">Seu comércio atendendo no WhatsApp 24h, sem precisar contratar.</h1>
          <p class="inicio-apoio">A KYZENT coloca uma IA no WhatsApp do seu comércio, que responde seus clientes a qualquer hora. Você paga uma mensalidade, mais barata que um funcionário, e a gente cuida de tudo.</p>
          <div class="inicio-acoes">
            <a class="botao" href="contato.html" data-contato>Fale conosco</a>
            <a class="botao botao-contorno" href="servicos.html">Conheça os serviços</a>
          </div>
          <ul class="inicio-selos">
            <li>Funciona 24 horas</li>
            <li>API oficial da Meta</li>
            <li>Manutenção e suporte inclusos</li>
          </ul>
        </div>

        <div class="inicio-foto">
          <img src="assets/fotos/comercio-balcao.jpg" alt="Dona de comércio sorrindo atrás do balcão" width="1600" height="900" fetchpriority="high">
          <div class="conversa" aria-label="Exemplo de conversa com a IA no WhatsApp">
            <p class="conversa-topo">Exemplo de conversa no WhatsApp</p>
            <p class="balao balao-cliente">Boa noite! Vocês abrem amanhã?</p>
            <p class="balao balao-ia">Boa noite! Abrimos sim, das 9h às 18h. Quer que eu já agende um horário?</p>
          </div>
        </div>
      </div>
    </section>

    <section class="secao" aria-labelledby="titulo-servicos">
      <div class="container">
        <div class="cabeca-linha">
          <div class="cabeca">
            <h2 id="titulo-servicos">Automação inteligente para empresas.</h2>
            <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
          </div>
          <a class="link-seta" href="servicos.html">Ver todos os serviços</a>
        </div>
        <ol class="grade grade-4">
{cartoes_servicos}
        </ol>
      </div>
    </section>

{PARA_QUEM}

    <section class="secao" aria-labelledby="titulo-quem">
      <div class="container dupla">
        <div class="dupla-foto">
          <img src="assets/fotos/equipe-computador.jpg" alt="Pessoas trabalhando juntas em frente a um computador" width="1600" height="900" loading="lazy">
        </div>
        <div class="dupla-texto">
          <h2 id="titulo-quem">Tecnologia e inovação para o seu comércio.</h2>
          <p>Somos a KYZENT, uma empresa de Tecnologia e Inovação dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio.</p>
          <p>Nosso propósito é transformar processos por meio da tecnologia, oferecendo mais produtividade, automação e eficiência para impulsionar os resultados dos nossos clientes.</p>
          <a class="link-seta" href="quem-somos.html">Conheça a KYZENT</a>
        </div>
      </div>
    </section>

{CHAMADA}"""

# ------------------------------------------------------------------ Quem somos
QUEM = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="container">
        <h1 id="titulo-pagina">Tecnologia e inovação para o seu comércio.</h1>
        <p>Somos a KYZENT, uma empresa de Tecnologia e Inovação dedicada a desenvolver soluções inteligentes para atender às necessidades do seu comércio.</p>
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
          <p>A KYZENT é uma empresa de tecnologia de Paulínia que automatiza o trabalho repetitivo do seu comércio. Em vez de contratar mais gente, você assina um serviço que trabalha junto com a sua equipe.</p>
        </div>
      </div>
    </section>

    <section class="secao secao-faixa" aria-labelledby="titulo-pilares">
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
    </section>

{CHAMADA}"""

# ------------------------------------------------------------------ Serviços
FOTO_SERV = {
    "01": ("celular-mensagem.jpg", 733, 1100, "Pessoa usando o celular ao lado de uma xícara de café"),
    "02": ("comercio-balcao.jpg", 1600, 900, "Dona de comércio atendendo uma cliente no balcão"),
    "03": ("equipe-computador.jpg", 1600, 900, "Pessoas trabalhando juntas em frente a um computador"),
    "04": ("equipe-reuniao.jpg", 1600, 900, "Equipe conversando em uma reunião num escritório"),
}

ETAPAS = [
    ("Conversa", "Entendemos como funciona o seu negócio e onde está o trabalho repetitivo."),
    ("Proposta", "Indicamos as automações certas e enviamos um orçamento personalizado."),
    ("Implantação", "Configuramos tudo com as informações do seu negócio, pela API oficial da Meta."),
    ("Acompanhamento", "Manutenção e suporte contínuos, com ajustes conforme o seu negócio cresce."),
]

CURTO = {'01': 'Atendimento', '02': 'Vendas', '03': 'Gestão', '04': 'Avançadas'}
abas = []
paineis = []
for i, (n, t, ic, resumo, itens) in enumerate(SERVICOS):
    sel = "true" if i == 0 else "false"
    abas.append(
        f'<button class="aba" type="button" role="tab" id="aba-{n}" aria-controls="servico-{n}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="aba-icone">{I[ic]}</span><span class="aba-texto"><span class="aba-longo">{t}</span><span class="aba-curto">{CURTO[n]}</span></span></button>')
    foto, fw, fh, falt = FOTO_SERV[n]
    cards = "\n".join(
        f'''              <li class="item">
                <h4>{a}</h4>
                <p>{d}</p>
                <button class="item-add" type="button" data-servico="{a}" data-area="{t}" aria-pressed="false">
                  <span class="item-add-mais">{I["mais"]}</span><span class="item-add-feito">{I["check"]}</span><span class="item-add-rotulo">Adicionar ao orçamento</span>
                </button>
              </li>''' for a, d in itens)
    paineis.append(f"""        <section class="painel" id="servico-{n}" role="tabpanel" aria-labelledby="aba-{n}" tabindex="-1">
          <div class="painel-lado">
            <div class="painel-foto"><img src="assets/fotos/{foto}" alt="{falt}" width="{fw}" height="{fh}" loading="lazy"></div>
            <span class="painel-num">{len(itens)} serviços</span>
            <h2>{t}</h2>
            <p>{resumo}</p>
          </div>
          <ul class="painel-itens">
{cards}
          </ul>
        </section>""")

etapas = "\n".join(
    f'          <li class="etapa"><span class="etapa-num">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>'
    for i, (t, d) in enumerate(ETAPAS))

SERVICOS_PAG = f"""    <section class="pagina-topo pagina-topo-servicos" aria-labelledby="titulo-pagina">
      <div class="container topo-servicos">
        <div>
          <h1 id="titulo-pagina">Automação inteligente para empresas.</h1>
          <p>Desenvolvemos soluções com Inteligência Artificial para automatizar processos, otimizar operações, melhorar o atendimento e aumentar a produtividade da sua empresa.</p>
        </div>
        <div class="topo-servicos-dica">
          <span class="cartao-icone">{I["orcamento"]}</span>
          <p><strong>Monte o seu orçamento.</strong> Adicione os serviços que interessam, como num carrinho, e envie tudo de uma vez pelo WhatsApp.</p>
        </div>
      </div>
    </section>

    <section class="secao secao-servicos" aria-label="Serviços por área">
      <div class="abas-faixa">
        <div class="container">
          <div class="abas" role="tablist" aria-label="Áreas de serviço">
            {"".join(abas)}
          </div>
        </div>
      </div>
      <div class="container paineis">
{chr(10).join(paineis)}
      </div>
    </section>

    <section class="secao secao-faixa" aria-labelledby="titulo-etapas">
      <div class="container">
        <div class="cabeca">
          <h2 id="titulo-etapas">Do primeiro contato à automação funcionando.</h2>
        </div>
        <ol class="etapas">
{etapas}
        </ol>
      </div>
    </section>

{PARA_QUEM.replace('class="secao secao-faixa"', 'class="secao"', 1)}

{CHAMADA}"""

# ------------------------------------------------------------------ Contato
def botao_whats(n):
    return f"""            <a class="contato" href="{link_whats(None, n)}" target="_blank" rel="noopener">
              <span class="contato-icone">{I["conversa"]}</span>
              <span class="contato-texto">
                <!-- <span class="contato-nome">NOME AQUI</span> -->
                <span class="contato-tipo">WhatsApp</span>
                <span class="contato-numero">{WHATS[n][1]}</span>
              </span>
              <span class="contato-seta" aria-hidden="true">→</span>
            </a>"""

CONTATO = f"""    <section class="pagina-topo" aria-labelledby="titulo-pagina">
      <div class="container">
        <h1 id="titulo-pagina">Solicite um orçamento personalizado.</h1>
        <p>Chame a gente no WhatsApp. Toque em um dos números: a conversa abre com uma mensagem pronta, é só enviar.</p>
      </div>
    </section>

    <section class="secao" aria-label="Formas de contato">
      <div class="container dupla">
        <div>
          <div class="contatos">
{botao_whats(0)}
{botao_whats(1)}
          </div>

          <dl class="info">
            <div><dt>Instagram</dt><dd><a href="https://www.instagram.com/kyzent.tech/" target="_blank" rel="noopener">@kyzent.tech</a></dd></div>
            <div><dt>Onde estamos</dt><dd>Paulínia/SP</dd></div>
            <div><dt>Atendemos</dt><dd>Paulínia e região</dd></div>
          </dl>
        </div>
        <div class="dupla-foto dupla-foto-alta">
          <img src="assets/fotos/cafeteria.jpg" alt="Mulher usando o celular em uma cafeteria" width="733" height="1100">
        </div>
      </div>
    </section>"""

DESC = "A KYZENT desenvolve automação inteligente com IA para empresas: atendimento no WhatsApp e Instagram, vendas, agendamentos, gestão e sistemas sob medida. Paulínia e região."

saidas = [
    ("index.html", "KYZENT | Automação inteligente e IA para empresas em Paulínia", DESC, INICIO, ramos_janelas()),
    ("quem-somos.html", "Quem somos | KYZENT", "A KYZENT é uma empresa de Tecnologia e Inovação de Paulínia que desenvolve soluções inteligentes para o seu comércio. Conheça nossa missão, visão e valores.", QUEM, ""),
    ("servicos.html", "Serviços | KYZENT", "Atendimento, vendas, gestão e soluções personalizadas com Inteligência Artificial. Conheça os serviços da KYZENT.", SERVICOS_PAG, ramos_janelas()),
    ("contato.html", "Contato | KYZENT", "Fale com a KYZENT pelo WhatsApp e solicite um orçamento personalizado. Paulínia e região.", CONTATO, ""),
]
for arq, titulo, desc, corpo, janelas in saidas:
    with open(os.path.join(SITE, arq), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina(arq, titulo, desc, corpo, janelas))
    print("ok", arq)
