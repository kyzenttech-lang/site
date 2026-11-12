// KYZENT — menu, janelas, abas, orçamento (carrinho), WhatsApp com número sorteado e animações.
(function () {
  "use strict";
  var raiz = document.documentElement;
  var semMovimento = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MSG_PADRAO = "Olá, vim pelo site da Kyzent.";

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function guardar(chave, valor) { try { localStorage.setItem(chave, JSON.stringify(valor)); } catch (e) {} }
  function ler(chave, padrao) {
    try { var v = JSON.parse(localStorage.getItem(chave)); return v == null ? padrao : v; } catch (e) { return padrao; }
  }

  /* ------------------------------------------------------------ menu do celular (painel lateral) */
  var botaoMenu = $("[data-abrir-menu]");
  var menu = document.getElementById("menu-celular");
  var barraTopo = $("[data-barra]");
  function menuAberto(aberto) {
    if (aberto && barraTopo) raiz.style.setProperty("--menu-topo", Math.max(0, barraTopo.getBoundingClientRect().bottom) + "px");
    menu.classList.toggle("aberto", aberto);
    raiz.classList.toggle("menu-aberto", aberto);
    botaoMenu.setAttribute("aria-expanded", aberto ? "true" : "false");
    botaoMenu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
    if (aberto) setTimeout(function () { var l = $("a", menu); if (l) l.focus({ preventScroll: true }); }, 120);
  }
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () { menuAberto(!menu.classList.contains("aberto")); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menuAberto(false); }); });
    $$("[data-fechar-menu]").forEach(function (f) { f.addEventListener("click", function () { menuAberto(false); }); });
    document.addEventListener("keydown", function (e) {
      if (!menu.classList.contains("aberto")) return;
      if (e.key === "Escape") { menuAberto(false); botaoMenu.focus(); return; }
      if (e.key === "Tab") {
        // o foco circula só entre o botão do menu e o painel
        var foco = [botaoMenu].concat($$("a, button", menu));
        var i = foco.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); foco[foco.length - 1].focus(); }
        else if (!e.shiftKey && i === foco.length - 1) { e.preventDefault(); foco[0].focus(); }
      }
    });
    addEventListener("resize", function () {
      if (innerWidth >= 1000 && menu.classList.contains("aberto")) menuAberto(false);
    });
  }

  /* ------------------------------------------------------------ janelas (abrir e fechar com animação) */
  function abrirJanela(j) {
    if (!j || typeof j.showModal !== "function") return false;
    if (menu && menu.classList.contains("aberto")) menuAberto(false);
    if (!j.open) j.showModal();
    j.classList.remove("fechando");
    raiz.classList.add("janela-aberta");
    return true;
  }
  function fecharJanela(j, depois) {
    if (!j || !j.open) { if (depois) depois(); return; }
    if (semMovimento) { j.close(); if (depois) depois(); return; }
    j.classList.add("fechando");
    setTimeout(function () {
      j.classList.remove("fechando");
      j.close();
      if (depois) depois();
    }, 200);
  }
  $$("dialog").forEach(function (j) {
    j.addEventListener("close", function () {
      if (!$("dialog[open]")) raiz.classList.remove("janela-aberta");
    });
    // Esc também fecha com animação
    j.addEventListener("cancel", function (e) { e.preventDefault(); fecharJanela(j); });
    // clique fora da caixa fecha
    j.addEventListener("click", function (e) { if (e.target === j) fecharJanela(j); });
    $$("[data-fechar-janela]", j).forEach(function (b) {
      b.addEventListener("click", function () { fecharJanela(j); });
    });
  });
  $$("[data-abrir-janela]").forEach(function (b) {
    b.addEventListener("click", function () { abrirJanela(document.getElementById(b.getAttribute("data-abrir-janela"))); });
  });

  /* ------------------------------------------------------------ orçamento (carrinho) */
  var CHAVE = "kyzent-orcamento";
  var itens = ler(CHAVE, []);
  if (!Array.isArray(itens)) itens = [];
  var dados = ler("kyzent-orcamento-dados", {});
  var gaveta = document.getElementById("carrinho");
  var lista = $("[data-carrinho-lista]");
  var form = $("[data-carrinho-form]");

  function tem(nome) { return itens.some(function (i) { return i.nome === nome; }); }
  function palavra(n) { return n === 1 ? "serviço" : "serviços"; }

  function atualizarBotoesServico() {
    $$("[data-servico]").forEach(function (b) {
      var ligado = tem(b.getAttribute("data-servico"));
      b.setAttribute("aria-pressed", ligado ? "true" : "false");
      var rot = $(".item-add-rotulo", b);
      if (rot) rot.textContent = ligado ? "No orçamento" : "Adicionar";
      var item = b.closest(".item");
      if (item) item.classList.toggle("escolhido", ligado);
    });
  }

  function desenharCarrinho() {
    var n = itens.length;
    $$("[data-contador]").forEach(function (c) { c.textContent = "(" + n + ")"; });
    $$(".orcamento-botao, .barra-fixa-orcamento").forEach(function (b) {
      b.hidden = n === 0;
      b.setAttribute("aria-label", "Ver orçamento, " + n + " " + palavra(n));
    });
    raiz.classList.toggle("tem-orcamento", n > 0);
    if (!gaveta) return;
    $("[data-carrinho-qtd]").textContent = n ? "(" + n + ")" : "";
    $("[data-carrinho-vazio]").hidden = n > 0;
    form.hidden = n === 0;
    $("[data-carrinho-base]").hidden = n === 0;
    var nota = $("[data-carrinho-nota]");
    if (nota) nota.hidden = n === 0;
    lista.innerHTML = "";
    itens.forEach(function (i) {
      var li = document.createElement("li");
      li.className = "gaveta-item";
      li.innerHTML = '<div><strong></strong><span></span></div>' +
        '<button type="button" class="gaveta-remover" aria-label="Tirar do orçamento">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>';
      $("strong", li).textContent = i.nome;
      $("span", li).textContent = i.area || "";
      $(".gaveta-remover", li).addEventListener("click", function () {
        li.classList.add("saindo");
        setTimeout(function () { remover(i.nome); }, semMovimento ? 0 : 180);
      });
      lista.appendChild(li);
    });
  }

  function salvar() { guardar(CHAVE, itens); desenharCarrinho(); atualizarBotoesServico(); }
  function remover(nome) { itens = itens.filter(function (i) { return i.nome !== nome; }); salvar(); }

  // outras abas do navegador com o site aberto ficam iguais
  addEventListener("storage", function (e) {
    if (e.key === CHAVE) { itens = ler(CHAVE, []); desenharCarrinho(); atualizarBotoesServico(); }
  });

  // bolinha que voa do botão até o ícone do orçamento
  function voar(origem) {
    if (semMovimento || !origem.animate) return;
    var alvo = $$(".orcamento-botao, .barra-fixa-orcamento").filter(function (el) {
      var r = el.getBoundingClientRect(); return r.width > 0 && r.top < innerHeight && r.bottom > 0;
    })[0];
    if (!alvo) return;
    var a = origem.getBoundingClientRect(), b = alvo.getBoundingClientRect();
    var bola = document.createElement("span");
    bola.className = "bolinha";
    bola.style.left = (a.left + 18) + "px";
    bola.style.top = (a.top + a.height / 2 - 6) + "px";
    document.body.appendChild(bola);
    var dx = b.left + b.width / 2 - (a.left + 24), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    bola.animate([
      { transform: "translate(0,0) scale(1)", opacity: 1 },
      { transform: "translate(" + dx * 0.5 + "px," + (dy * 0.5 - 60) + "px) scale(1.15)", opacity: 1, offset: 0.5 },
      { transform: "translate(" + dx + "px," + dy + "px) scale(.5)", opacity: .6 }
    ], { duration: 650, easing: "cubic-bezier(.5,0,.3,1)" }).onfinish = function () {
      bola.remove();
      $$("[data-contador]").forEach(function (c) { c.classList.remove("pulo"); void c.offsetWidth; c.classList.add("pulo"); });
    };
  }

  var aviso = $("[data-aviso]"), avisoTempo;
  function avisar(texto) {
    if (!aviso) return;
    $("[data-aviso-texto]", aviso).textContent = texto;
    aviso.hidden = false;
    aviso.classList.remove("saindo");
    clearTimeout(avisoTempo);
    avisoTempo = setTimeout(function () {
      aviso.classList.add("saindo");
      setTimeout(function () { aviso.hidden = true; aviso.classList.remove("saindo"); }, 220);
    }, 3200);
  }

  $$("[data-servico]").forEach(function (b) {
    b.addEventListener("click", function () {
      var nome = b.getAttribute("data-servico");
      if (tem(nome)) {
        remover(nome);
        avisar("Tirado do orçamento: " + nome);
      } else {
        itens.push({ nome: nome, area: b.getAttribute("data-area") || "" });
        salvar();
        voar(b);
        avisar("Adicionado ao orçamento: " + nome);
      }
    });
  });

  $$("[data-abrir-carrinho]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (aviso) aviso.hidden = true;
      abrirJanela(gaveta);
    });
  });

  if (form) {
    ["nome", "negocio", "obs"].forEach(function (campo) {
      var el = form.elements[campo];
      if (!el) return;
      if (dados[campo]) el.value = dados[campo];
      el.addEventListener("input", function () { dados[campo] = el.value; guardar("kyzent-orcamento-dados", dados); });
    });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
  }
  var limpar = $("[data-carrinho-limpar]");
  if (limpar) limpar.addEventListener("click", function () { itens = []; salvar(); });

  function mensagemOrcamento() {
    var linhas = ["Olá, vim pelo site da Kyzent e quero um orçamento."];
    if (!isNaN(fimPromo) && Date.now() < fimPromo) linhas.push("Quero aproveitar a implantação grátis da Black Friday.");
    if (dados.nome) linhas.push("Nome: " + dados.nome.trim());
    if (dados.negocio) linhas.push("Negócio: " + dados.negocio.trim());
    linhas.push("", "Serviços:");
    itens.forEach(function (i) { linhas.push("- " + i.nome + (i.area ? " (" + i.area + ")" : "")); });
    if (dados.obs) linhas.push("", "Observação: " + dados.obs.trim());
    return linhas.join("\n");
  }

  /* ------------------------------------------------------------ WhatsApp: número sorteado entre os dois, direto, sem janela de escolha */
  var NUMEROS = (document.body.getAttribute("data-whats") || "").split(" ").filter(Boolean);
  function linkSorteado(msg) {
    var num = NUMEROS[Math.floor(Math.random() * NUMEROS.length)];
    return "https://wa.me/" + num + "?text=" + encodeURIComponent(msg);
  }
  function mensagemDo(b) {
    var msg = b.getAttribute("data-msg");
    if (msg) return msg;
    if (itens.length) return mensagemOrcamento();
    return /orçamento/i.test(b.textContent) ? "Olá, vim pelo site da Kyzent e quero um orçamento." : MSG_PADRAO;
  }
  $$("[data-contato]").forEach(function (b) {
    // o link segue normal (abre em outra aba); só trocamos o endereço na hora do clique
    b.addEventListener("click", function () {
      if (!NUMEROS.length) return;
      b.href = linkSorteado(mensagemDo(b));
      var origem = b.closest("dialog");
      if (origem) setTimeout(function () { fecharJanela(origem); }, 150);
    });
  });

  var enviar = $("[data-carrinho-enviar]");
  if (enviar) enviar.addEventListener("click", function () {
    if (NUMEROS.length) window.open(linkSorteado(mensagemOrcamento()), "_blank", "noopener");
    fecharJanela(gaveta);
  });

  desenharCarrinho();
  atualizarBotoesServico();

  /* ------------------------------------------------------------ abas da página de serviços */
  var abas = $$('.abas [role="tab"]');
  var barraAbas = $(".abas");
  var indicador;
  if (barraAbas && abas.length) {
    indicador = document.createElement("span");
    indicador.className = "abas-indicador";
    barraAbas.appendChild(indicador);
    barraAbas.classList.add("com-indicador");
  }
  function moverIndicador(aba, instantaneo) {
    if (!indicador) return;
    if (instantaneo) indicador.style.transition = "none";
    indicador.style.width = (aba.offsetWidth - 16) + "px";
    indicador.style.transform = "translateX(" + (aba.offsetLeft + 8) + "px)";
    if (instantaneo) { void indicador.offsetWidth; indicador.style.transition = ""; }
  }
  function rolarParaServicos() {
    var secao = $(".secao-servicos");
    if (!secao) return;
    var topo = secao.getBoundingClientRect().top;
    if (topo < 72) scrollTo({ top: topo + scrollY - 72, behavior: semMovimento ? "auto" : "smooth" });
  }
  function mostrarAba(aba, focar, rolar) {
    abas.forEach(function (a) {
      var ativa = a === aba;
      a.setAttribute("aria-selected", ativa ? "true" : "false");
      a.tabIndex = ativa ? 0 : -1;
      var painel = document.getElementById(a.getAttribute("aria-controls"));
      if (!painel) return;
      painel.hidden = !ativa;
      if (ativa) {
        painel.removeAttribute("data-entrando");
        void painel.offsetWidth;
        painel.setAttribute("data-entrando", "");
        $$(".revelar", painel).forEach(function (el) { el.classList.add("visivel"); });
      }
    });
    moverIndicador(aba, !rolar && !focar);
    if (focar) aba.focus();
    if (rolar) rolarParaServicos();
  }
  if (abas.length) {
    abas.forEach(function (aba, i) {
      aba.addEventListener("click", function () {
        mostrarAba(aba, false, true);
        try { history.replaceState(null, "", location.pathname + location.search + "#" + aba.getAttribute("aria-controls")); } catch (e) {}
      });
      aba.addEventListener("keydown", function (e) {
        var alvo = null;
        var vis = abas.filter(function (a) { return !a.hidden; });
        var k = vis.indexOf(aba);
        if (e.key === "ArrowRight") alvo = vis[(k + 1) % vis.length];
        else if (e.key === "ArrowLeft") alvo = vis[(k - 1 + vis.length) % vis.length];
        else if (e.key === "Home") alvo = vis[0];
        else if (e.key === "End") alvo = vis[vis.length - 1];
        if (alvo) { e.preventDefault(); mostrarAba(alvo, true, false); }
      });
    });
    var inicial = abas[0];
    abas.forEach(function (a) { if ("#" + a.getAttribute("aria-controls") === location.hash) inicial = a; });
    mostrarAba(inicial, false, false);

    /* ---------------------------------------------------------- filtro por tipo de negócio */
    var filtro = $("[data-filtro]");
    if (filtro) {
      var chips = $$("[data-ramo]");
      var nomes = {};
      try { nomes = JSON.parse(filtro.getAttribute("data-nomes")) || {}; } catch (e) {}
      var atual = "todos";

      function aplicarFiltro(ramo) {
        atual = ramo;
        chips.forEach(function (c) { c.setAttribute("aria-pressed", c.getAttribute("data-ramo") === ramo ? "true" : "false"); });
        $$(".ex-var").forEach(function (v) { v.hidden = v.getAttribute("data-ex") !== ramo; });
        var rotulo = $("[data-filtro-atual]");
        if (rotulo) rotulo.textContent = ramo === "todos" ? "Todos" : (nomes[ramo] ? $("span", $('.filtro-chip[data-ramo="' + ramo + '"]')).textContent : ramo);
        var total = 0, primeira = null;
        abas.forEach(function (aba) {
          var painel = document.getElementById(aba.getAttribute("aria-controls"));
          var n = 0;
          $$(".item", painel).forEach(function (it) {
            var ramos = (it.getAttribute("data-ramos") || "").split(" ");
            var ok = ramo === "todos" || ramos.indexOf(ramo) > -1;
            it.hidden = !ok;
            if (ok) n++;
          });
          total += n;
          aba.hidden = n === 0;
          if (n && !primeira) primeira = aba;
          $("[data-qtd]", aba).textContent = n;
          $("[data-painel-num]", painel).textContent = n + " " + (n === 1 ? "serviço" : "serviços");
        });
        var ativa = $('.abas [role="tab"][aria-selected="true"]');
        if ((!ativa || ativa.hidden) && primeira) mostrarAba(primeira, false, false);
        else if (ativa) moverIndicador(ativa, true);
      }
      chips.forEach(function (c) {
        c.addEventListener("click", function () {
          aplicarFiltro(c.getAttribute("data-ramo"));
          var jan = c.closest("dialog");
          if (jan) fecharJanela(jan);
          try { history.replaceState(null, "", location.pathname + (atual === "todos" ? "" : "?ramo=" + atual) + location.hash); } catch (e) {}
        });
      });
      var pedido = /[?&]ramo=([a-z]+)/.exec(location.search);
      if (pedido && nomes[pedido[1]]) aplicarFiltro(pedido[1]);
    }
    addEventListener("resize", function () { moverIndicador($('.abas [role="tab"][aria-selected="true"]'), true); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { moverIndicador($('.abas [role="tab"][aria-selected="true"]'), true); });
    if (inicial !== abas[0]) {
      setTimeout(function () {
        var secao = $(".secao-servicos");
        if (secao) scrollTo({ top: secao.getBoundingClientRect().top + scrollY - 72, behavior: "instant" });
      }, 0);
    }
  }

  /* ------------------------------------------------------------ animações
     Tudo leve: sem biblioteca, pausa fora da tela e desliga com prefers-reduced-motion. */
  var ponteiroFino = window.matchMedia && matchMedia("(pointer: fine)").matches;
  function quandoVisivel(el, fn, opcoes) {
    if (!("IntersectionObserver" in window)) { fn(el); return; }
    var o = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { o.unobserve(en.target); fn(en.target); } });
    }, opcoes || { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
    o.observe(el);
  }
  function naTela(el) { var r = el.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }
  function duasVezes(fn) { requestAnimationFrame(function () { requestAnimationFrame(fn); }); }

  // títulos que surgem palavra por palavra
  $$("[data-revelar-texto]").forEach(function (t) {
    if (semMovimento || t.children.length) return;
    var texto = t.textContent.trim();
    t.setAttribute("aria-label", texto);
    t.innerHTML = texto.split(/\s+/).map(function (p, i) {
      return '<span class="palavra" aria-hidden="true"><span style="--i:' + i + '">' + p + "</span></span>";
    }).join(" ");
    if (naTela(t)) duasVezes(function () { t.classList.add("texto-visivel"); });
    else quandoVisivel(t, function () { t.classList.add("texto-visivel"); });
  });

  // blocos que aparecem ao rolar
  if (!semMovimento && "IntersectionObserver" in window) {
    var grupos = ".grade, .ramos, .etapas, .painel-itens";
    var soltos = ".cabeca > p, .cabeca-linha > .link-seta, .dupla-foto, .dupla-texto, .demo-texto, .demo-visual, .pagina-topo-apoio, .pagina-topo-texto";
    var alvos = [];
    $$(grupos).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (filho, i) {
        filho.style.setProperty("--atraso", Math.min(i, 6) * 80 + "ms");
        alvos.push(filho);
      });
    });
    $$(soltos).forEach(function (el) { if (alvos.indexOf(el) === -1) alvos.push(el); });
    [[".hero-apoio", 260], [".hero-acoes", 380], [".hero-numeros", 500], [".hero-palco", 180]].forEach(function (p) {
      var el = $(p[0]); if (el) { el.style.setProperty("--atraso", p[1] + "ms"); alvos.push(el); }
    });
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visivel"); observador.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    alvos.forEach(function (el) {
      el.classList.add("revelar");
      if (naTela(el)) duasVezes(function () { el.classList.add("visivel"); });
      else observador.observe(el);
    });
    $$(".revelar-bloco").forEach(function (el) { quandoVisivel(el, function () { el.classList.add("visivel"); }); });
  } else {
    $$(".revelar-bloco").forEach(function (el) { el.classList.add("visivel"); });
  }

  // contadores (os números do topo são reais; os dos desenhos são do exemplo)
  $$("[data-contar]").forEach(function (el) {
    if (semMovimento) return;
    var alvo = parseInt(el.getAttribute("data-contar"), 10);
    if (!alvo) return;
    el.textContent = "0";
    quandoVisivel(el, function () {
      var ini = performance.now(), dur = alvo > 50 ? 1600 : 1100;
      (function passo(agora) {
        var t = Math.min(1, Math.max(0, (agora - ini) / dur));
        el.textContent = Math.round(alvo * (1 - Math.pow(1 - t, 4))).toLocaleString("pt-BR");
        if (t < 1) requestAnimationFrame(passo);
      })(ini);
    });
  });

  // gráficos que crescem quando aparecem
  $$(".hero-painel, .gd").forEach(function (el) {
    if (semMovimento) { el.classList.add("crescer"); return; }
    quandoVisivel(el, function () { setTimeout(function () { el.classList.add("crescer"); }, 250); });
  });

  // botões magnéticos e brilho que segue o mouse
  if (ponteiroFino && !semMovimento) {
    $$("[data-magnetico]").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) / (r.width / 2);
        var y = (e.clientY - r.top - r.height / 2) / (r.height / 2);
        b.style.translate = (x * 6).toFixed(1) + "px " + (y * 5).toFixed(1) + "px";
      });
      b.addEventListener("pointerleave", function () { b.style.translate = ""; });
    });
    $$(".brilho").forEach(function (c) {
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty("--mx", (e.clientX - r.left) + "px");
        c.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  // topo do Início: rede de pontos, órbitas, painel com profundidade e lista que gira
  var hero = $(".hero");
  var heroVisivel = true;
  if (hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { heroVisivel = es[0].isIntersecting; }).observe(hero);
  }
  var orbitas = $(".hero-orbitas");
  if (orbitas && semMovimento && orbitas.pauseAnimations) orbitas.pauseAnimations();

  var tela = $("[data-rede]");
  if (tela && tela.getContext && !semMovimento) {
    var ctx = tela.getContext("2d"), pontos = [], W = 0, H = 0;
    var mouse = { x: -9999, y: -9999 };
    var medir = function () {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = tela.clientWidth; H = tela.clientHeight;
      tela.width = W * dpr; tela.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(W < 700 ? 18 : 64, (W * H) / 16000));
      pontos = [];
      for (var i = 0; i < n; i++) {
        pontos.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .22, vy: (Math.random() - .5) * .22, r: Math.random() * 1.4 + .6 });
      }
    };
    medir();
    var tempoRes, larguraAntes = innerWidth;
    addEventListener("resize", function () {
      if (innerWidth === larguraAntes) return;   // no celular, a barra do navegador some e muda só a altura
      larguraAntes = innerWidth;
      clearTimeout(tempoRes); tempoRes = setTimeout(medir, 200);
    });
    if (ponteiroFino) {
      hero.addEventListener("pointermove", function (e) { var r = tela.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
      hero.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    }
    var LIG = 130;
    (function desenhar() {
      requestAnimationFrame(desenhar);
      if (!heroVisivel || document.hidden) return;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < pontos.length; i++) {
        var p = pontos[i];
        var dxm = mouse.x - p.x, dym = mouse.y - p.y;
        if (dxm * dxm + dym * dym < 32400) { p.x += dxm * .004; p.y += dym * .004; }
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
        for (var j = i + 1; j < pontos.length; j++) {
          var q = pontos[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
          if (d < LIG * LIG) {
            ctx.strokeStyle = "rgba(63,180,255," + (0.16 * (1 - Math.sqrt(d) / LIG)).toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
          }
        }
        ctx.fillStyle = i % 5 === 0 ? "rgba(26,92,255,.85)" : "rgba(63,180,255,.6)";
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill();
      }
    })();
  }

  // demonstração: a IA passando pelas etapas
  $$("[data-fluxo]").forEach(function (fluxo) {
    if (semMovimento || !("IntersectionObserver" in window)) return;
    var passos = $$("[data-passo]", fluxo);
    var visivel = false, rodando = false;
    fluxo.classList.add("animando");
    function ciclo() {
      if (!visivel) { rodando = false; return; }
      rodando = true;
      passos.forEach(function (p) { p.classList.remove("ativo", "feito"); });
      passos.forEach(function (p, i) {
        setTimeout(function () { p.classList.add("ativo"); }, 500 + i * 1100);
        setTimeout(function () { p.classList.remove("ativo"); p.classList.add("feito"); }, 1350 + i * 1100);
      });
      setTimeout(ciclo, 500 + passos.length * 1100 + 2600);
    }
    new IntersectionObserver(function (es) {
      visivel = es[0].isIntersecting;
      if (visivel && !rodando) ciclo();
    }, { threshold: 0.35 }).observe(fluxo);
  });

  // linha do tempo que se preenche com a rolagem; topo que ganha borda ao rolar
  var barra = $("[data-barra]");
  var linhas = $$("[data-linha-tempo]");
  function aoRolar() {
    if (barra) barra.classList.toggle("rolou", scrollY > 8);
    linhas.forEach(function (l) {
      var r = l.getBoundingClientRect();
      var prog = semMovimento ? 1 : Math.max(0, Math.min(1, (innerHeight * .78 - r.top) / (r.height * .85)));
      l.style.setProperty("--progresso", prog.toFixed(3));
      var etapas = $$(".etapa", l), n = etapas.length;
      var ultima = -1;
      etapas.forEach(function (e, i) {
        var ativa = n < 2 || i / (n - 1) <= prog + .02;
        e.classList.toggle("ativa", ativa);
        if (ativa) ultima = i;
      });
      etapas.forEach(function (e, i) { e.classList.toggle("atual", !semMovimento && i === ultima && prog < 1); });
    });
  }
  var pedidoRolar = false;
  addEventListener("scroll", function () {
    if (pedidoRolar) return;
    pedidoRolar = true;
    requestAnimationFrame(function () { pedidoRolar = false; aoRolar(); });
  }, { passive: true });
  addEventListener("resize", aoRolar);
  aoRolar();

  /* ------------------------------------------------------------ carrosséis do celular: pontos que acompanham a rolagem */
  $$("[data-carrossel]").forEach(function (c) {
    var filhos = Array.prototype.slice.call(c.children);
    if (filhos.length < 2) return;
    var pontos = document.createElement("div");
    pontos.className = "carrossel-pontos";
    var botoes = filhos.map(function (f, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "carrossel-ponto";
      b.setAttribute("aria-label", "Mostrar o cartão " + (i + 1) + " de " + filhos.length);
      b.addEventListener("click", function () {
        c.scrollTo({ left: f.offsetLeft - filhos[0].offsetLeft, behavior: semMovimento ? "auto" : "smooth" });
      });
      pontos.appendChild(b);
      return b;
    });
    c.parentNode.insertBefore(pontos, c.nextSibling);
    function marcar() {
      var passo = filhos[1].offsetLeft - filhos[0].offsetLeft || 1;
      var atual = Math.min(filhos.length - 1, Math.round(c.scrollLeft / passo));
      if (c.scrollLeft + c.clientWidth >= c.scrollWidth - 4) atual = filhos.length - 1;
      botoes.forEach(function (b, i) { b.setAttribute("aria-current", i === atual ? "true" : "false"); });
    }
    var pedido = false;
    c.addEventListener("scroll", function () {
      if (pedido) return; pedido = true;
      requestAnimationFrame(function () { pedido = false; marcar(); });
    }, { passive: true });
    marcar();
  });

  /* ============================================================ KYZENT 2.0 */
  function el(tag, cls, texto) { var e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; }
  function espera(ms) { return new Promise(function (ok) { setTimeout(ok, semMovimento ? 0 : ms); }); }

  /* ------------------------------------------------------------ esfera neural do topo (canvas, sem biblioteca) */
  var esfera = $("[data-esfera]");
  if (esfera && esfera.getContext) {
    var ectx = esfera.getContext("2d");
    var celular = innerWidth < 760;
    var N = celular ? 170 : 340;
    var pts = [], arestas = [], pulsos = [];
    var ouro = Math.PI * (3 - Math.sqrt(5));
    for (var k = 0; k < N; k++) {
      var y = 1 - (k / (N - 1)) * 2, r = Math.sqrt(1 - y * y), t = ouro * k;
      pts.push([Math.cos(t) * r, y, Math.sin(t) * r]);
    }
    var limite = celular ? 0.3 : 0.22;
    for (var a = 0; a < N; a++) for (var b = a + 1; b < N; b++) {
      var dx = pts[a][0] - pts[b][0], dy = pts[a][1] - pts[b][1], dz = pts[a][2] - pts[b][2];
      if (dx * dx + dy * dy + dz * dz < limite * limite) arestas.push([a, b]);
    }
    var EW = 0, EH = 0, girar = 0, incl = { x: 0, y: 0 }, inclAlvo = { x: 0, y: 0 }, esferaVisivel = true;
    var medirEsfera = function () {
      var d = Math.min(window.devicePixelRatio || 1, 2);
      EW = esfera.clientWidth; EH = esfera.clientHeight;
      esfera.width = EW * d; esfera.height = EH * d;
      ectx.setTransform(d, 0, 0, d, 0, 0);
    };
    medirEsfera();
    addEventListener("resize", function () { if (Math.abs(esfera.clientWidth - EW) > 2) medirEsfera(); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { esferaVisivel = es[0].isIntersecting; }).observe(esfera);
    if (ponteiroFino && !semMovimento && hero) {
      hero.addEventListener("pointermove", function (e) { inclAlvo.x = (e.clientY / innerHeight - .5) * .5; inclAlvo.y = (e.clientX / innerWidth - .5) * .7; });
      hero.addEventListener("pointerleave", function () { inclAlvo.x = inclAlvo.y = 0; });
    }
    var desenharEsfera = function () {
      var R = Math.min(EW, EH) * 0.36, cx = EW / 2, cy = EH / 2;
      incl.x += (inclAlvo.x - incl.x) * .05; incl.y += (inclAlvo.y - incl.y) * .05;
      var ay = girar + incl.y, ax = -0.35 + incl.x;
      var cyy = Math.cos(ay), syy = Math.sin(ay), cxx = Math.cos(ax), sxx = Math.sin(ax);
      var proj = pts.map(function (p) {
        var x = p[0] * cyy - p[2] * syy, z = p[0] * syy + p[2] * cyy;
        var y2 = p[1] * cxx - z * sxx, z2 = p[1] * sxx + z * cxx;
        var esc = 2.6 / (2.6 + z2);
        return [cx + x * R * esc, cy + y2 * R * esc, z2];
      });
      ectx.clearRect(0, 0, EW, EH);
      ectx.lineWidth = 1;
      for (var i = 0; i < arestas.length; i++) {
        var p1 = proj[arestas[i][0]], p2 = proj[arestas[i][1]];
        var prof = (2 - (p1[2] + p2[2])) / 4;   // 0 (atrás) a 1 (frente)
        if (prof < 0.25) continue;
        ectx.strokeStyle = "rgba(63,180,255," + (prof * 0.32).toFixed(3) + ")";
        ectx.beginPath(); ectx.moveTo(p1[0], p1[1]); ectx.lineTo(p2[0], p2[1]); ectx.stroke();
      }
      for (var j = 0; j < proj.length; j++) {
        var p = proj[j], f = (1 - p[2]) / 2;
        ectx.fillStyle = j % 9 === 0 ? "rgba(255,255,255," + (0.35 + f * 0.65).toFixed(3) + ")" : "rgba(63,180,255," + (0.15 + f * 0.75).toFixed(3) + ")";
        ectx.beginPath(); ectx.arc(p[0], p[1], 0.6 + f * 1.6, 0, 6.283); ectx.fill();
      }
      // pulsos de luz correndo pelas ligações
      if (!semMovimento) {
        if (pulsos.length < (celular ? 5 : 10) && Math.random() < 0.08) pulsos.push({ a: arestas[Math.floor(Math.random() * arestas.length)], t: 0 });
        pulsos = pulsos.filter(function (u) {
          u.t += 0.025;
          var q1 = proj[u.a[0]], q2 = proj[u.a[1]];
          if ((q1[2] + q2[2]) / 2 > 0.2) return u.t < 1;
          var x = q1[0] + (q2[0] - q1[0]) * u.t, y = q1[1] + (q2[1] - q1[1]) * u.t;
          var g = ectx.createRadialGradient(x, y, 0, x, y, 7);
          g.addColorStop(0, "rgba(255,255,255,.95)"); g.addColorStop(1, "rgba(63,180,255,0)");
          ectx.fillStyle = g; ectx.beginPath(); ectx.arc(x, y, 7, 0, 6.283); ectx.fill();
          return u.t < 1;
        });
      }
    };
    if (semMovimento) desenharEsfera();
    else (function quadro() {
      requestAnimationFrame(quadro);
      if (!esferaVisivel || document.hidden) return;
      girar += celular ? 0.0022 : 0.0028;
      desenharEsfera();
    })();
  }

  /* ------------------------------------------------------------ abas das demonstrações */
  $$("[data-demo-centro]").forEach(function (centro) {
    var abasD = $$('[role="tab"]', centro);
    function mostrar(aba, focar) {
      abasD.forEach(function (a) {
        var ativa = a === aba;
        a.setAttribute("aria-selected", ativa ? "true" : "false");
        a.tabIndex = ativa ? 0 : -1;
        var painel = document.getElementById(a.getAttribute("aria-controls"));
        painel.hidden = !ativa;
        if (ativa) {
          $$(".revelar", painel).forEach(function (r) { r.classList.add("visivel"); });
          painel.dispatchEvent(new CustomEvent("demo-visivel"));
        }
      });
      if (focar) aba.focus();
      aba.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
    abasD.forEach(function (aba) {
      aba.addEventListener("click", function () { mostrar(aba, false); });
      aba.addEventListener("keydown", function (e) {
        var i = abasD.indexOf(aba), alvo = null;
        if (e.key === "ArrowRight") alvo = abasD[(i + 1) % abasD.length];
        else if (e.key === "ArrowLeft") alvo = abasD[(i - 1 + abasD.length) % abasD.length];
        else if (e.key === "Home") alvo = abasD[0];
        else if (e.key === "End") alvo = abasD[abasD.length - 1];
        if (alvo) { e.preventDefault(); mostrar(alvo, true); }
      });
    });
  });
  // começa a demonstração quando ela aparece (na tela ou ao trocar de aba)
  function aoAparecer(no, fn) {
    var feito = false, painel = no.closest(".demo-painel");
    function tentar() { if (!feito && !no.closest("[hidden]")) { feito = true; fn(); } }
    quandoVisivel(no, tentar, { threshold: 0.3 });
    if (painel) painel.addEventListener("demo-visivel", function () { setTimeout(tentar, 50); });
  }

  /* ------------------------------------------------------------ chatbot com opções */
  $$("[data-chatbot]").forEach(function (bot) {
    var roteiro = {};
    try { roteiro = JSON.parse(bot.getAttribute("data-roteiro")); } catch (e) { return; }
    var corpo = $("[data-chat-corpo]", bot), opcoes = $("[data-chat-opcoes]", bot), estado = $("[data-chat-estado]", bot);
    var digitando = el("div", "chat-digitando"); digitando.innerHTML = "<i></i><i></i><i></i>";
    var vez = 0;
    function rolarFim() { corpo.scrollTop = corpo.scrollHeight; }
    function bolha(quem, html) {
      var b = el("div", "chat-msg chat-" + quem + " entra");
      var p = el("p"); p.innerHTML = html;   // o texto vem do roteiro fixo do site
      b.appendChild(p); corpo.insertBefore(b, digitando); rolarFim();
    }
    function ir(chave) {
      var no = roteiro[chave]; if (!no) return;
      var minha = ++vez;
      opcoes.innerHTML = "";
      var fila = Promise.resolve();
      no.msg.forEach(function (m) {
        fila = fila.then(function () {
          if (minha !== vez) return;
          digitando.classList.add("mostra"); estado.textContent = "digitando"; rolarFim();
          return espera(750);
        }).then(function () {
          if (minha !== vez) return;
          digitando.classList.remove("mostra"); estado.textContent = "online";
          bolha("ia", m);
        });
      });
      fila.then(function () {
        if (minha !== vez) return;
        if (no.ok) {
          var r = el("div", "chat-resultado entra");
          r.innerHTML = '<span class="chat-resultado-icone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><span><strong></strong><small>Simulação demonstrativa</small></span>';
          $("strong", r).textContent = no.ok;
          corpo.insertBefore(r, digitando); rolarFim();
        }
        no.op.forEach(function (o) {
          var bt = el("button", "chat-opcao", o[0]); bt.type = "button";
          bt.addEventListener("click", function () {
            if (o[1] === "inicio") { corpo.querySelectorAll(".chat-msg, .chat-resultado").forEach(function (x) { x.remove(); }); }
            else bolha("cliente", o[0].replace(/</g, "&lt;"));
            ir(o[1]);
          });
          opcoes.appendChild(bt);
        });
      });
    }
    corpo.appendChild(digitando);
    aoAparecer(bot, function () { ir("inicio"); });
  });

  /* ------------------------------------------------------------ agendamento */
  $$("[data-agendamento]").forEach(function (ag) {
    var diasBox = $("[data-ag-dias]", ag), horasBox = $("[data-ag-horas]", ag), confirmar = $("[data-ag-confirmar]", ag);
    var aviso = $("[data-ag-aviso]", ag), lista = $("[data-ag-lista]", ag);
    var HORAS = ["09:00", "10:00", "11:00", "13:30", "14:30", "15:30", "16:30", "17:30"];
    var NOMES = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
    var escolha = { servico: "Escova", dia: null, hora: null }, marcados = {};
    function pressionar(grupo, alvo) { $$("button", grupo).forEach(function (b) { b.setAttribute("aria-pressed", b === alvo ? "true" : "false"); }); }
    $$("[data-ag-servico]", ag).forEach(function (b) {
      b.addEventListener("click", function () { escolha.servico = b.getAttribute("data-ag-servico"); pressionar(b.parentNode, b); });
    });
    function rotuloDia(i) {
      var d = new Date(); d.setDate(d.getDate() + i);
      return { curto: i === 0 ? "Hoje" : i === 1 ? "Amanhã" : NOMES[d.getDay()], num: d.getDate() + "/" + (d.getMonth() + 1) };
    }
    function desenharHoras() {
      horasBox.innerHTML = "";
      HORAS.forEach(function (h, j) {
        var b = el("button", "ag-hora", h); b.type = "button"; b.setAttribute("aria-pressed", "false");
        var ocupado = (escolha.dia * 5 + j * 3) % 4 === 0 || marcados[escolha.dia + h];
        if (ocupado) { b.disabled = true; b.setAttribute("aria-label", h + ", ocupado"); }
        b.addEventListener("click", function () { escolha.hora = h; pressionar(horasBox, b); confirmar.disabled = false; });
        horasBox.appendChild(b);
      });
      escolha.hora = null; confirmar.disabled = true;
    }
    for (var i = 0; i < 5; i++) (function (i) {
      var r = rotuloDia(i);
      var b = el("button", "ag-dia"); b.type = "button"; b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
      b.innerHTML = "<span></span><small></small>"; b.firstChild.textContent = r.curto; b.lastChild.textContent = r.num;
      b.addEventListener("click", function () { escolha.dia = i; pressionar(diasBox, b); desenharHoras(); });
      diasBox.appendChild(b);
    })(i);
    escolha.dia = 0; desenharHoras();
    confirmar.addEventListener("click", function () {
      if (escolha.hora == null) return;
      var r = rotuloDia(escolha.dia);
      marcados[escolha.dia + escolha.hora] = true;
      var li = el("li", "novo");
      li.innerHTML = '<time></time><span><strong>Você</strong><small></small></span><em class="estado estado-novo">Confirmado</em>';
      $("time", li).textContent = (escolha.dia === 0 ? "" : r.curto + " ") + escolha.hora;
      $("small", li).textContent = escolha.servico;
      lista.insertBefore(li, lista.firstChild);
      aviso.hidden = false;
      aviso.textContent = "Confirmado: " + escolha.servico.toLowerCase() + ", " + r.curto.toLowerCase() + " às " + escolha.hora + ". A confirmação foi pelo WhatsApp e o lembrete ficou programado para 1 hora antes.";
      desenharHoras();
    });
  });

  /* ------------------------------------------------------------ registro de pedidos */
  $$("[data-pedidos]").forEach(function (pd) {
    var total = $("[data-pd-total]", pd), registrar = $("[data-pd-registrar]", pd), lista = $("[data-pd-lista]", pd);
    var numero = 1043;
    var linhas = $$("[data-produto]", pd);
    function brl(v) { return "R$ " + v.toFixed(2).replace(".", ","); }
    function somar() {
      var s = 0, n = 0;
      linhas.forEach(function (l) { var q = +$("[data-qtd]", l).textContent; s += q * +l.getAttribute("data-preco"); n += q; });
      total.textContent = brl(s); registrar.disabled = n === 0;
    }
    linhas.forEach(function (l) {
      var q = $("[data-qtd]", l);
      $("[data-mais]", l).addEventListener("click", function () { q.textContent = Math.min(9, +q.textContent + 1); somar(); });
      $("[data-menos]", l).addEventListener("click", function () { q.textContent = Math.max(0, +q.textContent - 1); somar(); });
    });
    registrar.addEventListener("click", function () {
      var itensP = linhas.filter(function (l) { return +$("[data-qtd]", l).textContent > 0; })
        .map(function (l) { return $("[data-qtd]", l).textContent + " " + l.getAttribute("data-produto"); });
      var li = el("li", "novo");
      li.innerHTML = '<span class="pd-num"></span><span><strong>Você</strong><small></small></span><em class="estado estado-novo">Novo</em>';
      $(".pd-num", li).textContent = "#" + numero++;
      $("small", li).textContent = itensP.join(", ") + " · " + total.textContent;
      lista.insertBefore(li, lista.firstChild);
      linhas.forEach(function (l) { $("[data-qtd]", l).textContent = "0"; });
      somar();
      setTimeout(function () { var e = $("em", li); e.className = "estado estado-preparo"; e.textContent = "Em preparo"; }, semMovimento ? 0 : 1800);
    });
  });

  /* ------------------------------------------------------------ organização de clientes */
  $$("[data-clientes]").forEach(function (cl) {
    var busca = $("[data-cl-busca]", cl), conta = $("[data-cl-conta]", cl), filtro = "todos";
    var lis = $$("[data-cl-lista] li", cl);
    function aplicar() {
      var termo = busca.value.trim().toLowerCase(), n = 0;
      lis.forEach(function (li) {
        var ok = (filtro === "todos" || li.getAttribute("data-tipo") === filtro) && li.getAttribute("data-nome").indexOf(termo) > -1;
        li.hidden = !ok; if (ok) n++;
      });
      conta.textContent = n === 0 ? "Nenhum cliente com esse filtro." : n + (n === 1 ? " cliente" : " clientes");
    }
    busca.addEventListener("input", aplicar);
    $$("[data-cl-filtro]", cl).forEach(function (b) {
      b.addEventListener("click", function () {
        filtro = b.getAttribute("data-cl-filtro");
        $$("[data-cl-filtro]", cl).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        aplicar();
      });
    });
    $$("[data-lembrar]", cl).forEach(function (b) {
      b.addEventListener("click", function () { b.disabled = true; b.textContent = "Lembrete enviado pelo WhatsApp"; });
    });
  });

  /* ------------------------------------------------------------ segmentos */
  $$("[data-segmentos]").forEach(function (grupo) {
    var chips = $$("[data-seg]", grupo);
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        $$(".seg-painel").forEach(function (p) { p.classList.toggle("ativo", p.id === "seg-" + c.getAttribute("data-seg")); });
        c.scrollIntoView({ block: "nearest", inline: "center", behavior: semMovimento ? "auto" : "smooth" });
      });
    });
  });

  /* ------------------------------------------------------------ simulador de orçamento */
  $$("[data-simulador]").forEach(function (form) {
    var passos = $$("[data-passo]", form), atual = 0, aberto = Date.now();
    var mapa = JSON.parse(form.getAttribute("data-mapa")), servMod = JSON.parse(form.getAttribute("data-servmod"));
    var barra = $("[data-sim-barra]", form), num = $("[data-sim-num]", form), erro = $("[data-sim-erro]", form);
    var voltar = $("[data-sim-voltar]", form), avancar = $("[data-sim-avancar]", form), enviar = $("[data-sim-enviar]", form);
    var resultado = $("[data-sim-resultado]");
    var limpo = function (v, max) { return String(v || "").replace(/[\u0000-\u0009\u000B-\u001F\u007F<>]/g, " ").replace(/\s{3,}/g, "  ").trim().slice(0, max); };
    var marcados = function (nome) { return $$('input[name="' + nome + '"]:checked', form).map(function (i) { return i.value; }); };
    var rotulo = function (input) { return input.closest(".sim-opcao").textContent.trim(); };

    var pedido = /[?&]ramo=([a-z]+)/.exec(location.search);
    if (pedido) { var r = $('input[name="negocio"][value="' + pedido[1] + '"]', form); if (r) r.checked = true; }

    function mostrarErro(txt) { erro.textContent = txt; erro.hidden = !txt; }
    function irPara(n, inicial) {
      atual = n;
      passos.forEach(function (p, i) { p.hidden = i !== n; });
      barra.style.width = ((n + 1) / passos.length * 100) + "%";
      num.textContent = "Passo " + (n + 1) + " de " + passos.length;
      voltar.hidden = n === 0;
      avancar.hidden = n === passos.length - 1;
      enviar.hidden = n !== passos.length - 1;
      mostrarErro("");
      var primeiro = $("input, textarea", passos[n]);
      if (primeiro && document.activeElement && form.contains(document.activeElement)) primeiro.focus({ preventScroll: true });
      var topo = form.getBoundingClientRect().top;
      if (!inicial && topo < 80) scrollTo({ top: scrollY + topo - 100, behavior: semMovimento ? "auto" : "smooth" });
    }
    function valido(n) {
      if (n === 0 && !marcados("negocio").length) return "Escolha o seu tipo de negócio para continuar.";
      if (n === 1 && !marcados("desafio").length) return "Marque pelo menos uma opção para continuar.";
      if (n === 3) {
        var nome = form.elements.nome;
        var ok = limpo(nome.value, 60).length >= 2;
        nome.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) { nome.focus(); return "Escreva o seu nome para a gente saber com quem fala."; }
      }
      return "";
    }
    avancar.addEventListener("click", function () { var e = valido(atual); if (e) mostrarErro(e); else irPara(atual + 1); });
    voltar.addEventListener("click", function () { irPara(atual - 1); });
    form.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName === "INPUT" && atual < passos.length - 1) { e.preventDefault(); avancar.click(); }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var problema = valido(atual);
      if (problema) { mostrarErro(problema); return; }
      if (form.elements.site.value) return;   // campo-isca preenchido: robô
      if (Date.now() - aberto < 3000) { mostrarErro("Confira as respostas e tente de novo em alguns segundos."); return; }

      var negocioInput = $('input[name="negocio"]:checked', form);
      var desafios = $$('input[name="desafio"]:checked', form);
      var servicos = [];
      desafios.forEach(function (d) { (mapa[d.value] || []).forEach(function (s) { if (servicos.indexOf(s) === -1) servicos.push(s); }); });
      var grupos = {};
      servicos.forEach(function (s) { var m = servMod[s]; (grupos[m[0]] = grupos[m[0]] || { pagina: m[1], nome: m[2], itens: [] }).itens.push(s); });

      var dados = {
        nome: limpo(form.elements.nome.value, 60), empresa: limpo(form.elements.empresa.value, 80),
        cidade: limpo(form.elements.cidade.value, 60), obs: limpo(form.elements.obs.value, 400),
        negocio: rotulo(negocioInput), canais: marcados("canal").join(", "), volume: marcados("volume")[0] || ""
      };
      var linhas = ["Olá, vim pelo site da Kyzent e fiz a simulação de orçamento.", "Nome: " + dados.nome];
      if (dados.empresa) linhas.push("Empresa: " + dados.empresa);
      if (dados.cidade) linhas.push("Cidade: " + dados.cidade);
      linhas.push("Negócio: " + dados.negocio);
      if (dados.canais) linhas.push("Canais: " + dados.canais);
      if (dados.volume) linhas.push("Mensagens por dia: " + dados.volume);
      linhas.push("", "O que mais toma tempo:");
      desafios.forEach(function (d) { linhas.push("- " + rotulo(d)); });
      linhas.push("", "Soluções recomendadas:");
      servicos.forEach(function (s) { linhas.push("- " + s); });
      if (dados.obs) linhas.push("", "Observação: " + dados.obs);
      if (!isNaN(fimPromo) && Date.now() < fimPromo) linhas.push("", "Quero aproveitar a implantação grátis da Black Friday.");
      var mensagem = linhas.join("\n");

      resultado.innerHTML = "";
      var h = el("h3"); h.textContent = dados.nome.split(" ")[0] + ", estas são as soluções que mais combinam com o seu negócio.";
      resultado.appendChild(h);
      var rec = el("div", "sim-rec");
      Object.keys(grupos).forEach(function (k) {
        var g = grupos[k], caixa = el("div", "sim-rec-grupo");
        caixa.appendChild(el("h4", null, g.nome));
        var ul = el("ul"); g.itens.forEach(function (s) { ul.appendChild(el("li", null, s)); });
        caixa.appendChild(ul);
        var a = el("a", null, "Conhecer a solução"); a.href = g.pagina; caixa.appendChild(a);
        rec.appendChild(caixa);
      });
      resultado.appendChild(rec);
      var acoes = el("div", "sim-rec-acoes");
      var bWhats = el("button", "botao", "Enviar pelo WhatsApp"); bWhats.type = "button";
      var bOrc = el("button", "botao botao-contorno", "Guardar no meu orçamento"); bOrc.type = "button";
      acoes.appendChild(bWhats); acoes.appendChild(bOrc);
      resultado.appendChild(acoes);
      resultado.appendChild(el("p", "sim-rec-nota", "A recomendação é um ponto de partida. O orçamento final é combinado pelo WhatsApp, conforme o seu negócio."));
      bWhats.addEventListener("click", function () {
        if (bWhats.disabled) return;
        if (NUMEROS.length) window.open(linkSorteado(mensagem), "_blank", "noopener");
        bWhats.disabled = true; bWhats.textContent = "Mensagem aberta no WhatsApp";
        setTimeout(function () { bWhats.disabled = false; bWhats.textContent = "Enviar pelo WhatsApp"; }, 4000);
      });
      bOrc.addEventListener("click", function () {
        servicos.forEach(function (s) { if (!tem(s)) itens.push({ nome: s, area: servMod[s][2] }); });
        salvar(); avisar(servicos.length + " " + palavra(servicos.length) + " no seu orçamento");
      });
      if (innerWidth < 1000) resultado.scrollIntoView({ behavior: semMovimento ? "auto" : "smooth", block: "start" });
      h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: innerWidth >= 1000 });
    });
    irPara(0, true);
  });

  /* ------------------------------------------------------------ Black Friday: contador e fim da promoção */
  var fimPromo = Date.parse(document.body.getAttribute("data-promo-fim") || "");
  function encerrarPromo() {
    $$("[data-promo]").forEach(function (el) { el.hidden = true; });
    $$("[data-fora-texto]").forEach(function (b) {
      var t = $("[data-texto-botao]", b);
      if (t) t.textContent = b.getAttribute("data-fora-texto");
      b.removeAttribute("data-msg");
    });
    $$("[data-fora-msg]").forEach(function (b) { b.setAttribute("data-msg", b.getAttribute("data-fora-msg")); });
  }
  if (!isNaN(fimPromo)) {
    var relogios = $$("[data-relogio]");
    var antes = {};
    var doisDigitos = function (n) { return (n < 10 ? "0" : "") + n; };
    var tique = function () {
      var falta = fimPromo - Date.now();
      if (falta <= 0) { encerrarPromo(); clearInterval(intervalo); return; }
      var s = Math.floor(falta / 1000);
      var v = { dias: Math.floor(s / 86400), horas: Math.floor(s % 86400 / 3600), min: Math.floor(s % 3600 / 60), seg: s % 60 };
      relogios.forEach(function (r) {
        Object.keys(v).forEach(function (k) {
          var el = $("[data-" + k + "]", r);
          if (!el) return;
          var txt = doisDigitos(v[k]);
          if (el.textContent !== txt) {
            el.textContent = txt;
            if (!semMovimento && antes[k] !== undefined) { el.classList.remove("virou"); void el.offsetWidth; el.classList.add("virou"); }
          }
        });
        r.setAttribute("aria-label", "A promoção termina em " + v.dias + " dias e " + v.horas + " horas");
      });
      antes = v;
    };
    var intervalo = setInterval(tique, 1000);
    tique();
  }

  /* ------------------------------------------------------------ ano do rodapé */
  var ano = $("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
