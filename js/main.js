// KYZENT — tema, menu, janelas, abas, orçamento (carrinho), escolha de número e animações.
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

  /* ------------------------------------------------------------ tema */
  var botoesTema = $$("[data-trocar-tema]");
  function rotuloTema() {
    var escuro = raiz.getAttribute("data-theme") === "dark";
    botoesTema.forEach(function (b) {
      if (b.classList.contains("icone-botao")) b.setAttribute("aria-label", escuro ? "Usar tema claro" : "Usar tema escuro");
    });
  }
  rotuloTema();
  botoesTema.forEach(function (botao) {
    botao.addEventListener("click", function () {
      var novo = raiz.getAttribute("data-theme") === "dark" ? "light" : "dark";
      function aplicar() {
        raiz.setAttribute("data-theme", novo);
        try { localStorage.setItem("kyzent-tema", novo); } catch (e) {}
        rotuloTema();
      }
      // troca em círculo, saindo do botão
      if (!document.startViewTransition || semMovimento) { aplicar(); return; }
      var r = botao.getBoundingClientRect();
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      var raio = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      raiz.classList.add("trocando-tema");
      var t = document.startViewTransition(aplicar);
      t.ready.then(function () {
        raiz.animate(
          { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + raio + "px at " + x + "px " + y + "px)"] },
          { duration: 520, easing: "cubic-bezier(.2,.8,.2,1)", pseudoElement: "::view-transition-new(root)" }
        );
      });
      t.finished.then(function () { raiz.classList.remove("trocando-tema"); });
    });
  });

  /* ------------------------------------------------------------ menu do celular */
  var botaoMenu = $("[data-abrir-menu]");
  var menu = document.getElementById("menu-celular");
  function menuAberto(aberto) {
    menu.classList.toggle("aberto", aberto);
    raiz.classList.toggle("menu-aberto", aberto);
    botaoMenu.setAttribute("aria-expanded", aberto ? "true" : "false");
    botaoMenu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
  }
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () { menuAberto(!menu.classList.contains("aberto")); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menuAberto(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("aberto")) { menuAberto(false); botaoMenu.focus(); }
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
    if (dados.nome) linhas.push("Nome: " + dados.nome.trim());
    if (dados.negocio) linhas.push("Negócio: " + dados.negocio.trim());
    linhas.push("", "Serviços:");
    itens.forEach(function (i) { linhas.push("- " + i.nome + (i.area ? " (" + i.area + ")" : "")); });
    if (dados.obs) linhas.push("", "Observação: " + dados.obs.trim());
    return linhas.join("\n");
  }

  /* ------------------------------------------------------------ escolher o número */
  var janelaContato = document.getElementById("janela-contato");
  var mensagemAtual = MSG_PADRAO;

  function abrirContato(msg, comOrcamento) {
    if (!janelaContato) return false;
    mensagemAtual = msg;
    var leva = $("[data-contato-leva]", janelaContato);
    if (comOrcamento && itens.length) {
      leva.textContent = "Vai junto na mensagem: " + itens.length + " " + palavra(itens.length) + " do seu orçamento.";
      leva.hidden = false;
    } else {
      leva.hidden = true;
    }
    $$("[data-numero]", janelaContato).forEach(function (a) {
      var num = a.getAttribute("data-numero");
      if (num !== "sorteio") a.href = "https://wa.me/" + num + "?text=" + encodeURIComponent(msg);
    });
    return abrirJanela(janelaContato);
  }

  if (janelaContato) {
    var numeros = $$("[data-numero]", janelaContato)
      .map(function (a) { return a.getAttribute("data-numero"); })
      .filter(function (n) { return n !== "sorteio"; });
    $$("[data-numero]", janelaContato).forEach(function (a) {
      a.addEventListener("click", function () {
        if (a.getAttribute("data-numero") === "sorteio") {
          var num = numeros[Math.floor(Math.random() * numeros.length)];
          a.href = "https://wa.me/" + num + "?text=" + encodeURIComponent(mensagemAtual);
        }
        setTimeout(function () { fecharJanela(janelaContato); }, 150);
      });
    });
  }

  $$("[data-contato]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      var msg = b.getAttribute("data-msg");
      var comOrcamento = !msg && itens.length > 0;
      if (!msg) msg = comOrcamento ? mensagemOrcamento() : (/orçamento/i.test(b.textContent) ? "Olá, vim pelo site da Kyzent e quero um orçamento." : MSG_PADRAO);
      var origem = b.closest("dialog");
      e.preventDefault();
      if (origem && origem !== janelaContato) fecharJanela(origem, function () { abrirContato(msg, comOrcamento); });
      else abrirContato(msg, comOrcamento);
    });
  });

  var enviar = $("[data-carrinho-enviar]");
  if (enviar) enviar.addEventListener("click", function () {
    fecharJanela(gaveta, function () { abrirContato(mensagemOrcamento(), true); });
  });

  desenharCarrinho();
  atualizarBotoesServico();

  /* ------------------------------------------------------------ abas da página de serviços */
  var abas = $$('[role="tab"]');
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
        var ativa = $('[role="tab"][aria-selected="true"]');
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
    addEventListener("resize", function () { moverIndicador($('[role="tab"][aria-selected="true"]'), true); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { moverIndicador($('[role="tab"][aria-selected="true"]'), true); });
    if (inicial !== abas[0]) {
      setTimeout(function () {
        var secao = $(".secao-servicos");
        if (secao) scrollTo({ top: secao.getBoundingClientRect().top + scrollY - 72, behavior: "instant" });
      }, 0);
    }
  }

  /* ------------------------------------------------------------ aparecer ao rolar (leve, uma vez só) */
  if (!semMovimento && "IntersectionObserver" in window) {
    var grupos = ".grade, .ramos, .etapas, .painel-itens";
    var soltos = ".cabeca, .dupla-foto, .dupla-texto, .inicio-foto, .chamada-caixa, .pilar";
    var alvos = [];
    $$(grupos).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (filho, i) {
        filho.style.setProperty("--atraso", Math.min(i, 6) * 70 + "ms");
        alvos.push(filho);
      });
    });
    $$(soltos).forEach(function (el) { if (alvos.indexOf(el) === -1) alvos.push(el); });
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visivel"); observador.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    alvos.forEach(function (el) {
      // o que já está na tela ao abrir aparece sem esperar
      var r = el.getBoundingClientRect();
      el.classList.add("revelar");
      if (r.top < innerHeight && r.bottom > 0) requestAnimationFrame(function () { el.classList.add("visivel"); });
      else observador.observe(el);
    });
  }

  /* ------------------------------------------------------------ ano do rodapé */
  var ano = $("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
