// KYZENT — menu, janelas, abas, WhatsApp com número sorteado, simulador de orçamento e animações.
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

  /* ------------------------------------------------------------ WhatsApp: número sorteado entre os dois, direto, sem janela de escolha */
  var NUMEROS = (document.body.getAttribute("data-whats") || "").split(" ").filter(Boolean);
  function linkSorteado(msg) {
    var num = NUMEROS[Math.floor(Math.random() * NUMEROS.length)];
    return "https://wa.me/" + num + "?text=" + encodeURIComponent(msg);
  }
  function mensagemDo(b) {
    var msg = b.getAttribute("data-msg");
    if (msg) return msg;
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

  /* ------------------------------------------------------------ animações
     Entradas, títulos e contadores ficam em js/animacoes.js (GSAP). Aqui: o que é interação. Desliga com prefers-reduced-motion. */
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

  // títulos, blocos que entram ao rolar e contadores: js/animacoes.js (GSAP)

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

  /* ------------------------------------------------------------ história do Início: o passo muda ao clicar (ou Enter/Espaço)
     O 3D (js/hero-3d.js) ouve "historia-etapa" e leva o ponto da órbita até a estação do passo. */
  var palcoH = $("[data-historia-palco]");
  if (palcoH) {
    var passosH = $$("[data-historia]"), rotuloH = $("[data-historia-rotulo]"), atualH = 0;
    var marcarH = function (n) {
      if (n === atualH) return;
      atualH = n;
      palcoH.setAttribute("data-etapa", n);
      passosH.forEach(function (p) {
        var ativo = +p.getAttribute("data-historia") === n;
        p.classList.toggle("ativo", ativo); p.setAttribute("aria-pressed", ativo ? "true" : "false");
      });
      if (rotuloH) rotuloH.textContent = n + " de " + passosH.length + " · " + $("h3", passosH[n - 1]).textContent;
      document.dispatchEvent(new CustomEvent("historia-etapa", { detail: n }));
    };
    passosH.forEach(function (p) {
      var n = +p.getAttribute("data-historia");
      p.addEventListener("click", function () { marcarH(n); });
      p.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); marcarH(n); } });
    });
    marcarH(1);
  }

  /* ------------------------------------------------------------ WhatsApp: no computador, um botão de cada vez
     (o do topo aparece no começo; depois do primeiro bloco, ele dá lugar ao botão flutuante) */
  var primeiroBloco = $("[data-hero]") || $(".pagina-topo");
  if (primeiroBloco && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { raiz.classList.toggle("passou-topo", !es[0].isIntersecting); }, { rootMargin: "-80px 0px 0px 0px" }).observe(primeiroBloco);
  }

  // gráfico da página de gestão se desenha quando aparece
  $$("[data-desenhar]").forEach(function (el) {
    if (semMovimento) { el.classList.add("crescer"); return; }
    quandoVisivel(el, function () { el.classList.add("crescer"); });
  });

  /* ------------------------------------------------------------ do jeito manual ao automático: divisória arrastável */
  $$("[data-comparar]").forEach(function (cmp) {
    var faixa = $("[data-comparar-faixa]", cmp);
    var aplicar = function () {
      cmp.style.setProperty("--corte", faixa.value + "%");
      var m = Math.round(+faixa.value);
      faixa.setAttribute("aria-valuetext", m >= 100 ? "Só o jeito manual" : m <= 0 ? "Só com a Kyzent" : m + "% manual, " + (100 - m) + "% com a Kyzent");
    };
    faixa.addEventListener("input", aplicar);
    var estreito = innerWidth < 640;
    if (estreito) faixa.value = 100;   // no celular começa no jeito manual inteiro
    aplicar();
    // uma dica de movimento na primeira vez que aparece: a divisória desliza e volta ao meio
    if (!semMovimento) quandoVisivel(cmp, function () {
      var ini = performance.now();
      (function passo(t) {
        var k = Math.min(1, (t - ini) / (estreito ? 2600 : 1800));
        if (document.activeElement === faixa) return;
        var suave = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        faixa.value = estreito ? 100 - suave * 100 : 50 + Math.sin(k * Math.PI * 2) * 22 * (1 - k);
        aplicar();
        if (k < 1) requestAnimationFrame(passo);
      })(ini);
    }, { threshold: .5 });
  });

  /* ------------------------------------------------------------ abas das demonstrações */
  $$("[data-demo-centro]").forEach(function (centro) {
    var abasD = $$('[role="tab"]', centro);
    function mostrar(aba, focar, sentido) {
      abasD.forEach(function (a) {
        var ativa = a === aba;
        a.setAttribute("aria-selected", ativa ? "true" : "false");
        a.tabIndex = ativa ? 0 : -1;
        var painel = document.getElementById(a.getAttribute("aria-controls"));
        painel.hidden = !ativa;
        if (ativa) {
          painel.removeAttribute("data-entra"); void painel.offsetWidth;
          if (sentido) painel.setAttribute("data-entra", sentido);
          $$(".revelar", painel).forEach(function (r) { r.classList.add("visivel"); });
          painel.dispatchEvent(new CustomEvent("demo-visivel"));
        }
      });
      if (focar) aba.focus();
      // a aba escolhida fica visível na faixa de abas, sem mexer na rolagem da página
      var faixa = aba.parentNode;
      faixa.scrollTo({ left: aba.offsetLeft - (faixa.clientWidth - aba.offsetWidth) / 2, behavior: semMovimento ? "auto" : "smooth" });
    }
    // celular: deslizar o dedo para o lado sobre a demonstração passa para a próxima ou volta à anterior
    var toque = null;
    centro.addEventListener("touchstart", function (e) {
      if (e.target.closest("input, textarea, .cl-lista, .demo-abas")) { toque = null; return; }
      toque = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }, { passive: true });
    centro.addEventListener("touchend", function (e) {
      if (!toque) return;
      var dx = e.changedTouches[0].clientX - toque.x, dy = e.changedTouches[0].clientY - toque.y;
      toque = null;
      if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
      var atual = abasD.filter(function (a) { return a.getAttribute("aria-selected") === "true"; })[0];
      var i = abasD.indexOf(atual), n = abasD.length;
      if (dx < 0) mostrar(abasD[(i + 1) % n], false, "dir");
      else mostrar(abasD[(i - 1 + n) % n], false, "esq");
    }, { passive: true });
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

  /* ------------------------------------------------------------ base das demos da Lanchonete Exemplo
     Um sistema só: uma venda registrada em Estoque ou em Pedidos vira o evento "demo-venda".
     Pedidos mostra o pedido, Estoque baixa a quantidade e o Painel conta mais um. */
  var demo = { numero: +(($("[data-pedidos]") || document.body).getAttribute("data-proximo")) || 1044 };
  function anunciarVenda(itens, quem, texto, origem) {
    // itens: [{ produto, qtd }]
    document.dispatchEvent(new CustomEvent("demo-venda", { detail: { numero: demo.numero++, itens: itens, quem: quem, texto: texto, origem: origem } }));
  }

  /* ------------------------------------------------------------ registro de pedidos */
  $$("[data-pedidos]").forEach(function (pd) {
    var total = $("[data-pd-total]", pd), registrar = $("[data-pd-registrar]", pd), lista = $("[data-pd-lista]", pd);
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
    // todo pedido novo (daqui ou do Estoque) entra na fila de Pedidos
    document.addEventListener("demo-venda", function (e) {
      var d = e.detail, li = el("li", "novo");
      li.innerHTML = '<span class="pd-num"></span><span><strong></strong><small></small></span><em class="estado estado-novo">Novo</em>';
      $(".pd-num", li).textContent = "#" + d.numero;
      $("strong", li).textContent = d.quem;
      $("small", li).textContent = d.texto;
      lista.insertBefore(li, lista.firstChild);
      setTimeout(function () { var em = $("em", li); em.className = "estado estado-preparo"; em.textContent = "Em preparo"; }, semMovimento ? 0 : 1800);
    });
    registrar.addEventListener("click", function () {
      var escolhidos = linhas.filter(function (l) { return +$("[data-qtd]", l).textContent > 0; });
      var itens = escolhidos.map(function (l) { return { produto: l.getAttribute("data-produto"), qtd: +$("[data-qtd]", l).textContent }; });
      var texto = itens.map(function (i) { return i.qtd + " " + i.produto; }).join(", ") + " · " + total.textContent;
      anunciarVenda(itens, "Você", texto, "pedidos");
      linhas.forEach(function (l) { $("[data-qtd]", l).textContent = "0"; });
      somar();
    });
  });

  /* ------------------------------------------------------------ estoque: baixa a cada venda e avisa quando passa do mínimo */
  $$("[data-estoque]").forEach(function (est) {
    var status = $("[data-est-status]", est);
    var itens = $$("[data-est-item]", est);
    function porNome(n) { return itens.filter(function (i) { return i.getAttribute("data-est-item") === n; })[0]; }
    function atualizar(item, qtd) {
      var saida = $("[data-est-qtd]", item), min = +item.getAttribute("data-min");
      saida.textContent = Math.max(0, qtd);
      saida.classList.remove("baixou"); void saida.offsetWidth; saida.classList.add("baixou");
      var acabando = qtd <= min;
      $("[data-est-aviso]", item).hidden = !acabando;
      $("[data-est-repor]", item).hidden = !acabando;
      item.classList.toggle("acabando", acabando);
      return acabando;
    }
    document.addEventListener("demo-venda", function (e) {
      var avisos = [];
      e.detail.itens.forEach(function (v) {
        var item = porNome(v.produto); if (!item) return;
        if (atualizar(item, +$("[data-est-qtd]", item).textContent - v.qtd)) avisos.push(v.produto);
      });
      status.textContent = "Venda #" + e.detail.numero + " registrada: o estoque baixou" +
        (avisos.length ? ". Acabando: " + avisos.join(", ") + "." : " e a venda entrou em Pedidos e no Painel.");
    });
    itens.forEach(function (item) {
      var nome = item.getAttribute("data-est-item");
      $("[data-est-vender]", item).addEventListener("click", function () {
        if (+$("[data-est-qtd]", item).textContent <= 0) { status.textContent = nome + " acabou. Faça o pedido ao fornecedor."; return; }
        anunciarVenda([{ produto: nome, qtd: 1 }], "Balcão", "1 " + nome, "estoque");
      });
      $("[data-est-repor]", item).addEventListener("click", function () {
        var b = this; b.disabled = true; b.textContent = "Pedido enviado ao fornecedor";
        status.textContent = "Pedido de " + nome + " enviado ao fornecedor (simulação).";
        setTimeout(function () { b.disabled = false; b.textContent = "Fazer pedido ao fornecedor"; }, 3000);
      });
    });
  });

  /* ------------------------------------------------------------ painel: conta cada venda e mostra o pedido no topo */
  $$("[data-gestao]").forEach(function (gd) {
    var kpi = $(".gd-kpis [data-contar]", gd), lista = $(".gd-pedidos", gd);
    document.addEventListener("demo-venda", function (e) {
      var d = e.detail;
      if (kpi) { var v = (+kpi.getAttribute("data-contar") || 0) + 1; kpi.setAttribute("data-contar", v); kpi.textContent = v.toLocaleString("pt-BR"); }
      if (lista) {
        var li = el("li", "novo");
        li.innerHTML = '<span class="pd-num"></span><span class="pd-quem"><strong></strong><small></small></span><span class="estado estado-novo">Novo</span>';
        $(".pd-num", li).textContent = "#" + d.numero; $("strong", li).textContent = d.quem; $("small", li).textContent = d.texto;
        lista.insertBefore(li, lista.firstChild);
        while (lista.children.length > 3) lista.removeChild(lista.lastElementChild);
      }
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
    // abas: setas esquerda/direita, Home e End trocam de segmento
    grupo.addEventListener("keydown", function (e) {
      var i = chips.indexOf(document.activeElement); if (i < 0) return;
      var n = e.key === "ArrowRight" ? (i + 1) % chips.length : e.key === "ArrowLeft" ? (i - 1 + chips.length) % chips.length
            : e.key === "Home" ? 0 : e.key === "End" ? chips.length - 1 : -1;
      if (n < 0) return;
      e.preventDefault(); chips[n].focus(); chips[n].click();
    });
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.setAttribute("aria-selected", x === c ? "true" : "false"); x.tabIndex = x === c ? 0 : -1; });
        $$(".seg-painel").forEach(function (p) { p.classList.toggle("ativo", p.id === "seg-" + c.getAttribute("data-seg")); });
        // o ícone do segmento (3D em js/hero-3d.js, ou o desenho em SVG sem 3D)
        var palcoS = $("[data-seg-palco]");
        if (palcoS) palcoS.setAttribute("data-seg-ativo", c.getAttribute("data-seg"));
        document.dispatchEvent(new CustomEvent("segmento-troca", { detail: c.getAttribute("data-seg") }));
        c.scrollIntoView({ block: "nearest", inline: "center", behavior: semMovimento ? "auto" : "smooth" });
      });
    });
  });

  /* ------------------------------------------------------------ simulador de orçamento
     Passos: o que precisa, tipo de negócio, tamanho, contato. No fim mostra a recomendação e
     deixa claro que falta enviar: pelo WhatsApp ou por e-mail, como a pessoa preferir. Nada vai para servidor. */
  $$("[data-simulador]").forEach(function (form) {
    var passos = $$("[data-passo]", form), atual = 0, aberto = Date.now();
    var mapa = JSON.parse(form.getAttribute("data-mapa")), servMod = JSON.parse(form.getAttribute("data-servmod"));
    var emailKyzent = form.getAttribute("data-email");
    var barra = $("[data-sim-barra]", form), num = $("[data-sim-num]", form), erro = $("[data-sim-erro]", form);
    var etapas = JSON.parse(num.getAttribute("data-etapas") || "[]");
    var voltar = $("[data-sim-voltar]", form), avancar = $("[data-sim-avancar]", form), enviar = $("[data-sim-enviar]", form);
    var resultado = $("[data-sim-resultado]");
    var limpo = function (v, max) { return String(v || "").replace(/[\u0000-\u0009\u000B-\u001F\u007F<>]/g, " ").replace(/\s{3,}/g, "  ").trim().slice(0, max); };
    var marcados = function (nome) { return $$('input[name="' + nome + '"]:checked', form).map(function (i) { return i.value; }); };
    var rotulo = function (input) { return input.closest(".sim-opcao").textContent.trim(); };

    // campos que só aparecem quando a pessoa escolhe "Outra coisa", "Outro tipo de negócio" ou e-mail
    function alternar(nomeGrupo, valor, caixa, campo, foco) {
      var sim = marcados(nomeGrupo).indexOf(valor) > -1;
      caixa.hidden = !sim;
      if (sim && foco) campo.focus();
    }
    var outraNec = $("[data-sim-outra-necessidade]", form), outraNecCampo = form.elements.necessidade_outra;
    var outroNeg = $("[data-sim-outro]", form), outroNegCampo = form.elements.negocio_outro;
    var caixaEmail = $("[data-sim-email]", form), campoEmail = form.elements.email;
    $$('input[name="necessidade"]', form).forEach(function (r) { r.addEventListener("change", function () { alternar("necessidade", "outro", outraNec, outraNecCampo, r.checked); }); });
    $$('input[name="negocio"]', form).forEach(function (r) { r.addEventListener("change", function () { alternar("negocio", "outro", outroNeg, outroNegCampo, true); }); });
    $$('input[name="canal_retorno"]', form).forEach(function (r) { r.addEventListener("change", function () { alternar("canal_retorno", "email", caixaEmail, campoEmail, true); }); });

    // ?ramo=barbearia já marca o tipo de negócio
    var pedido = /[?&]ramo=([a-z]+)/.exec(location.search);
    if (pedido) { var r0 = $('input[name="negocio"][value="' + pedido[1] + '"]', form); if (r0) r0.checked = true; }

    function mostrarErro(txt) { erro.textContent = txt; erro.hidden = !txt; }
    function irPara(n, inicial) {
      atual = n;
      passos.forEach(function (p, i) { p.hidden = i !== n; });
      barra.style.width = (n / passos.length * 100) + "%";   // conta só os passos já concluídos: vazia no passo 1
      num.textContent = "Passo " + (n + 1) + " de " + passos.length + (etapas[n] ? " · " + etapas[n] : "");
      voltar.hidden = n === 0;                                // no passo 1 não há botão que tire a pessoa da página
      avancar.hidden = n === passos.length - 1;
      enviar.hidden = n !== passos.length - 1;
      mostrarErro("");
      var primeiro = $("input, textarea", passos[n]);
      if (primeiro && document.activeElement && form.contains(document.activeElement)) primeiro.focus({ preventScroll: true });
      var topo = form.getBoundingClientRect().top;
      if (!inicial && topo < 80) scrollTo({ top: scrollY + topo - 100, behavior: semMovimento ? "auto" : "smooth" });
    }
    function exigir(campo, min, msg) {
      var ok = limpo(campo.value, 80).length >= min;
      campo.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok) { campo.focus(); return msg; }
      return "";
    }
    function valido(n) {
      if (n === 0) {
        if (!marcados("necessidade").length) return "Marque pelo menos uma opção para continuar.";
        if (marcados("necessidade").indexOf("outro") > -1) return exigir(outraNecCampo, 2, "Conte o que você precisa para continuar.");
      }
      if (n === 1) {
        if (!marcados("negocio").length) return "Escolha o seu tipo de negócio para continuar.";
        if (marcados("negocio")[0] === "outro") return exigir(outroNegCampo, 2, "Conte qual é o seu tipo de negócio para continuar.");
      }
      if (n === 2 && !marcados("equipe").length) return "Escolha quantas pessoas trabalham no negócio.";
      if (n === 3) {
        var e1 = exigir(form.elements.nome, 2, "Escreva o seu nome para a gente saber com quem fala.");
        if (e1) return e1;
        if (marcados("canal_retorno")[0] === "email") {
          var okEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(campoEmail.value.trim());
          campoEmail.setAttribute("aria-invalid", okEmail ? "false" : "true");
          if (!okEmail) { campoEmail.focus(); return "Escreva um e-mail válido para receber o retorno."; }
        }
        var aceite = form.elements.privacidade;
        if (aceite && !aceite.checked) { aceite.setAttribute("aria-invalid", "true"); aceite.focus(); return "Para enviar, marque que leu e concorda com a Política de Privacidade."; }
        if (aceite) aceite.setAttribute("aria-invalid", "false");
      }
      return "";
    }
    avancar.addEventListener("click", function () { var e = valido(atual); if (e) mostrarErro(e); else irPara(atual + 1); });
    voltar.addEventListener("click", function () { if (atual > 0) irPara(atual - 1); });
    form.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName === "INPUT" && atual < passos.length - 1) { e.preventDefault(); avancar.click(); }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var problema = valido(atual);
      if (problema) { mostrarErro(problema); return; }
      if (form.elements.site.value) return;   // campo-isca preenchido: robô
      if (Date.now() - aberto < 3000) { mostrarErro("Confira as respostas e tente de novo em alguns segundos."); return; }
      erro.hidden = true;

      var necessidades = $$('input[name="necessidade"]:checked', form);
      var servicos = [];
      necessidades.forEach(function (d) { (mapa[d.value] || []).forEach(function (s) { if (servicos.indexOf(s) === -1) servicos.push(s); }); });
      var grupos = {};
      servicos.forEach(function (s) { var m = servMod[s]; if (m) (grupos[m[0]] = grupos[m[0]] || { pagina: m[1], nome: m[2], itens: [] }).itens.push(s); });

      var negocioInput = $('input[name="negocio"]:checked', form);
      var canal = marcados("canal_retorno")[0] || "whatsapp";
      var dados = {
        nome: limpo(form.elements.nome.value, 60), empresa: limpo(form.elements.empresa.value, 80), obs: limpo(form.elements.obs.value, 400),
        negocio: negocioInput.value === "outro" ? "Outro: " + limpo(outroNegCampo.value, 60) : rotulo(negocioInput),
        equipe: marcados("equipe")[0] || "", quando: marcados("quando")[0] || "", email: limpo(campoEmail.value, 80)
      };
      var linhas = ["Olá, vim pelo site da Kyzent e fiz a simulação de orçamento.", "Nome: " + dados.nome];
      if (dados.empresa) linhas.push("Empresa: " + dados.empresa);
      linhas.push("Negócio: " + dados.negocio);
      if (dados.equipe) linhas.push("Pessoas no negócio: " + dados.equipe);
      if (dados.quando) linhas.push("Quando quer começar: " + dados.quando);
      if (canal === "email") linhas.push("Prefere retorno por e-mail: " + dados.email);
      linhas.push("", "O que preciso:");
      necessidades.forEach(function (d) { linhas.push("- " + (d.value === "outro" ? "Outra coisa: " + limpo(outraNecCampo.value, 80) : rotulo(d))); });
      linhas.push("", "Soluções recomendadas:");
      servicos.forEach(function (s) { linhas.push("- " + s); });
      if (dados.obs) linhas.push("", "Observação: " + dados.obs);
      if (!isNaN(fimPromo) && Date.now() < fimPromo) linhas.push("", "Quero aproveitar a implantação grátis da Black Friday.");
      var mensagem = linhas.join("\n");

      barra.style.width = "100%";
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

      // falta um passo: enviar (a recomendação sozinha não chega à Kyzent)
      var falta = el("div", "sim-falta");
      falta.appendChild(el("strong", null, "Falta só enviar."));
      falta.appendChild(el("p", null, "A Kyzent só recebe o seu pedido quando você envia a mensagem pronta. Responderemos com uma proposta para o seu negócio."));
      var acoes = el("div", "sim-rec-acoes");
      var bWhats = el("a", "botao", "Enviar pelo WhatsApp"), bEmail = el("a", "botao", "Enviar por e-mail");
      bWhats.href = NUMEROS.length ? linkSorteado(mensagem) : "#"; bWhats.target = "_blank"; bWhats.rel = "noopener";
      bEmail.href = "mailto:" + emailKyzent + "?subject=" + encodeURIComponent("Orçamento pelo site: " + dados.nome) + "&body=" + encodeURIComponent(mensagem);
      if (canal === "email") { bWhats.className = "botao botao-contorno"; acoes.appendChild(bEmail); acoes.appendChild(bWhats); }
      else { bEmail.className = "botao botao-contorno"; acoes.appendChild(bWhats); acoes.appendChild(bEmail); }
      falta.appendChild(acoes);
      resultado.appendChild(falta);
      resultado.appendChild(el("p", "sim-rec-nota", "A recomendação é um ponto de partida. O orçamento final é combinado com você, conforme o seu negócio."));
      [bWhats, bEmail].forEach(function (b) {
        b.addEventListener("click", function () { falta.classList.add("enviado"); $("strong", falta).textContent = "Mensagem aberta. É só enviar."; });
      });
      if (innerWidth < 1000) resultado.scrollIntoView({ behavior: semMovimento ? "auto" : "smooth", block: "start" });
      h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: innerWidth >= 1000 });
    });
    alternar("necessidade", "outro", outraNec, outraNecCampo, false);
    alternar("negocio", "outro", outroNeg, outroNegCampo, false);
    alternar("canal_retorno", "email", caixaEmail, campoEmail, false);
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

  /* ------------------------------------------------------------ Aurora: entrada uma vez e inclinação que segue o cursor (só com mouse) */
  $$("[data-aurora]").forEach(function (fig) {
    if (semMovimento || !("IntersectionObserver" in window)) return;
    if (fig.getBoundingClientRect().top < innerHeight) { fig.classList.add("aparece", "pronta"); }
    else fig.classList.add("vai-aparecer");
    var obs = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      fig.classList.add("aparece"); obs.disconnect();
      setTimeout(function () { fig.classList.add("pronta"); }, 1700);   // depois da entrada, a inclinação volta a responder rápido
    }, { threshold: .3 });
    obs.observe(fig);
    if (!ponteiroFino) return;   // no toque: só o flutuar lento do CSS
    var quadro = $("[data-aurora-quadro]", fig), secao = fig.closest("section") || fig, pedido = 0, rx = 0, ry = 0;
    secao.addEventListener("pointermove", function (e) {
      var r = fig.getBoundingClientRect();
      ry = ((e.clientX - r.left) / r.width - .5) * 10;   // até 5 graus para cada lado
      rx = -((e.clientY - r.top) / r.height - .5) * 8;
      if (!pedido) pedido = requestAnimationFrame(function () { pedido = 0; quadro.style.setProperty("--rx", rx.toFixed(2) + "deg"); quadro.style.setProperty("--ry", ry.toFixed(2) + "deg"); });
    });
    secao.addEventListener("pointerleave", function () { quadro.style.setProperty("--rx", "0deg"); quadro.style.setProperty("--ry", "0deg"); });
  });

  /* ------------------------------------------------------------ hero 3D do Início (js/hero-3d.js)
     O texto e o botão de WhatsApp já funcionam antes. O 3D só é baixado depois que a página
     abriu, e nunca com movimento reduzido ou economia de dados: aí fica a imagem do K. */
  var economia = navigator.connection && navigator.connection.saveData;
  if ($("[data-hero-palco]") || $("[data-k3d]")) {
    if (semMovimento || economia) document.documentElement.classList.add("sem-3d");
    else {
      var carregarHero = function () { import("./hero-3d.js?v=" + (document.documentElement.getAttribute("data-v") || "1")).catch(function () { document.documentElement.classList.add("sem-3d"); }); };
      var depoisDeAbrir = function () { if ("requestIdleCallback" in window) requestIdleCallback(carregarHero, { timeout: 2000 }); else setTimeout(carregarHero, 300); };
      if (document.readyState === "complete") depoisDeAbrir(); else addEventListener("load", depoisDeAbrir);
    }
  }

  /* ------------------------------------------------------------ perguntas: abas por assunto (sem JS, aparecem todas) */
  var perg = $("[data-perguntas]");
  if (perg) {
    var abasP = $$('[role="tab"]', perg), paineisP = $$('[role="tabpanel"]', perg);
    var mostrarP = function (aba, foco) {
      abasP.forEach(function (a) {
        var on = a === aba;
        a.setAttribute("aria-selected", on ? "true" : "false");
        a.tabIndex = on ? 0 : -1;
        document.getElementById(a.getAttribute("aria-controls")).hidden = !on;
      });
      if (foco) aba.focus();
    };
    mostrarP(abasP[0], false);
    abasP.forEach(function (aba, n) {
      aba.addEventListener("click", function () { mostrarP(aba, false); });
      aba.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        mostrarP(abasP[(n + d + abasP.length) % abasP.length], true);
      });
    });
  }

  /* ------------------------------------------------------------ "Todas as soluções": volta de verdade
     Se a pessoa veio de Soluções, volta pelo histórico (mesmo ponto da página, sem recarregar nem pular).
     Se entrou direto na página da solução, o link normal abre Soluções nos pilares. */
  $$(".voltar-link").forEach(function (l) {
    l.addEventListener("click", function (e) {
      var ref = document.referrer;
      if (!ref || history.length < 2) return;
      try {
        var u = new URL(ref);
        if (u.origin === location.origin && /servicos\.html$/.test(u.pathname)) { e.preventDefault(); history.back(); }
      } catch (_) {}
    });
  });

  /* ------------------------------------------------------------ BI: painel de exemplo (dados fictícios) */
  var bi = $("[data-bi3d]");
  if (bi) {
    var dadosBI = JSON.parse(bi.getAttribute("data-bi-dados"));
    var parado = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var fmt = {
      fat: function (v) { return v >= 100000 ? "R$ " + Math.round(v / 1000).toLocaleString("pt-BR") + " mil" : "R$ " + Math.round(v).toLocaleString("pt-BR"); },
      ticket: function (v) { return "R$ " + v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); },
      ped: function (v) { return Math.round(v).toLocaleString("pt-BR"); },
      novos: function (v) { return Math.round(v).toLocaleString("pt-BR"); },
    };
    var atual = { fat: 0, ticket: 0, ped: 0, novos: 0 };
    var caminho = function (vals, max) {
      var n = vals.length;
      return vals.map(function (v, i) { return (i ? "L" : "M") + (i * 300 / (n - 1)).toFixed(1) + " " + (125 - v / max * 110).toFixed(1); }).join(" ");
    };
    var desenhar = function (el) {
      if (parado) return;
      var len = 2400;   // o traço não escala com o SVG: um comprimento folgado, em pixels de tela
      el.style.transition = "none"; el.style.strokeDasharray = len; el.style.strokeDashoffset = len;
      el.getBoundingClientRect();
      el.style.transition = "stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1)"; el.style.strokeDashoffset = 0;
    };
    var mostrar = function (per) {
      var d = dadosBI[per];
      Object.keys(fmt).forEach(function (k) {
        var el = bi.querySelector('[data-bi-kpi="' + k + '"]'), de = atual[k], para = d.kpi[k], t0 = null;
        bi.querySelector('[data-bi-var="' + k + '"]').textContent = "+" + d.var[k] + "% que o período anterior";
        if (parado) { el.textContent = fmt[k](para); atual[k] = para; return; }
        var passo = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 800), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt[k](de + (para - de) * e);
          if (p < 1) requestAnimationFrame(passo); else atual[k] = para;
        };
        requestAnimationFrame(passo);
      });
      bi.querySelector("[data-bi-barras]").innerHTML = d.barras.map(function (h, i) {
        return '<span style="--h:' + h + '%;--i:' + i + '"><i></i><b>' + d.rot[i] + "</b></span>";
      }).join("");
      var max = Math.max.apply(null, d.atual.concat(d.ant)) * 1.05;
      var pa = bi.querySelector("[data-bi-atual]"), pb = bi.querySelector("[data-bi-ant]");
      pa.setAttribute("d", caminho(d.atual, max)); pb.setAttribute("d", caminho(d.ant, max));
      desenhar(pa);
      bi.querySelector("[data-bi-rank]").innerHTML = d.rank.map(function (r) { return "<li><span>" + r[0] + '</span><i style="--v:' + r[1] + '%"></i></li>'; }).join("");
      $$("[data-bi-per]", bi).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-bi-per") === per ? "true" : "false"); });
    };
    $$("[data-bi-per]", bi).forEach(function (b) {
      b.addEventListener("click", function () {
        // barras novas crescem do zero
        bi.classList.remove("entrou"); bi.getBoundingClientRect();
        mostrar(b.getAttribute("data-bi-per"));
        requestAnimationFrame(function () { bi.classList.add("entrou"); });
      });
    });
    if (!parado && "IntersectionObserver" in window) {
      bi.classList.add("pronto");
      var obs = new IntersectionObserver(function (ent) {
        if (!ent[0].isIntersecting) return;
        obs.disconnect();
        mostrar("semana");
        requestAnimationFrame(function () { bi.classList.add("entrou"); });
      }, { threshold: 0.3 });
      obs.observe(bi);
    } else { mostrar("semana"); bi.classList.add("entrou"); }
    // a cena inclina seguindo o mouse
    if (matchMedia("(pointer: fine)").matches && !parado) {
      var cenaBI = bi.querySelector("[data-bi-cena]");
      bi.addEventListener("pointermove", function (e) {
        if (!bi.classList.contains("entrou")) return;
        var r = bi.getBoundingClientRect();
        cenaBI.style.transform = "rotateX(" + (16 - ((e.clientY - r.top) / r.height - 0.5) * 8).toFixed(2) + "deg) rotateY(" + (-12 + ((e.clientX - r.left) / r.width - 0.5) * 12).toFixed(2) + "deg)";
      });
      bi.addEventListener("pointerleave", function () { cenaBI.style.transform = ""; });
    }
  }

  /* ------------------------------------------------------------ Vendas: os dois celulares contam a história (uma vez, ao aparecer) */
  var vd = $("[data-vd3d]");
  if (vd) {
    var vdParado = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var q = function (s) { return vd.querySelector(s); };
    var precos = [26, 22, 6];   // X-bacon, X-salada e refrigerante: 3 itens, R$ 54,00
    var reais = function (v) { return "R$ " + v.toFixed(2).replace(".", ","); };
    var final = function () {
      q("[data-vd-qtd]").textContent = "Pedido enviado"; q("[data-vd-total]").textContent = reais(54); q("[data-vd-carrinho]").classList.add("enviado");
      q("[data-vd-hora]").classList.add("on"); q("[data-vd-confirmar]").textContent = "Horário confirmado ✓"; q("[data-vd-confirmar]").classList.add("ok");
      q("[data-vd-nota-a]").classList.add("on"); q("[data-vd-nota-b]").classList.add("on");
    };
    var rodar = function () {
      var itens = vd.querySelectorAll("[data-vd-item]"), total = 0, passos = [];
      [0, 1, 2].forEach(function (k) {
        passos.push(function () {
          itens[k].classList.add("toque"); total += precos[k];
          q("[data-vd-qtd]").textContent = (k + 1) + (k ? " itens" : " item");
          q("[data-vd-total]").textContent = reais(total);
          setTimeout(function () { itens[k].classList.remove("toque"); }, 450);
        });
      });
      passos.push(function () { q("[data-vd-qtd]").textContent = "Pedido enviado"; q("[data-vd-carrinho]").classList.add("enviado"); q("[data-vd-nota-a]").classList.add("on"); });
      passos.push(function () { q("[data-vd-hora]").classList.add("on"); });
      passos.push(function () { q("[data-vd-confirmar]").textContent = "Horário confirmado ✓"; q("[data-vd-confirmar]").classList.add("ok"); q("[data-vd-nota-b]").classList.add("on"); });
      passos.forEach(function (f, n) { setTimeout(f, 900 + n * 750); });
    };
    if (vdParado || !("IntersectionObserver" in window)) { final(); }
    else {
      vd.classList.add("pronto");
      var obsVd = new IntersectionObserver(function (e) {
        if (!e[0].isIntersecting) return;
        obsVd.disconnect(); vd.classList.add("entrou"); rodar();
      }, { threshold: 0.35 });
      obsVd.observe(vd);
      if (matchMedia("(pointer: fine)").matches) {
        var cenaVd = q("[data-vd-cena]");
        vd.addEventListener("pointermove", function (ev) {
          if (!vd.classList.contains("entrou")) return;
          var r = vd.getBoundingClientRect();
          cenaVd.style.transform = "rotateX(" + (10 - ((ev.clientY - r.top) / r.height - 0.5) * 8).toFixed(2) + "deg) rotateY(" + (-14 + ((ev.clientX - r.left) / r.width - 0.5) * 14).toFixed(2) + "deg)";
        });
        vd.addEventListener("pointerleave", function () { cenaVd.style.transform = ""; });
      }
    }
  }

  /* ------------------------------------------------------------ ano do rodapé */
  var ano = $("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
