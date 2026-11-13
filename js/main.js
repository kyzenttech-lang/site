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

  /* ------------------------------------------------------------ história do Início: o diagrama acompanha a leitura dos passos */
  var palcoH = $("[data-historia-palco]");
  if (palcoH) {
    var passosH = $$("[data-historia]");
    var marcarH = function (n) {
      palcoH.setAttribute("data-etapa", n);
      passosH.forEach(function (p) { p.classList.toggle("ativo", +p.getAttribute("data-historia") === n); });
    };
    marcarH(1);
    // o diagrama avança sozinho de passo em passo enquanto está na tela; passar o mouse ou tocar escolhe o passo
    var autoH = null, visivelH = false, pausaH = false;
    var proximoH = function () { if (!pausaH) marcarH(+palcoH.getAttribute("data-etapa") % passosH.length + 1); };
    if ("IntersectionObserver" in window && !semMovimento) {
      new IntersectionObserver(function (es) {
        visivelH = es[0].isIntersecting;
        clearInterval(autoH);
        if (visivelH) autoH = setInterval(proximoH, 3200);
      }, { threshold: .35 }).observe(palcoH);
    }
    var lista = $("[data-historia-lista]");
    if (lista) {
      lista.addEventListener("pointerenter", function () { pausaH = true; });
      lista.addEventListener("pointerleave", function () { pausaH = false; });
      passosH.forEach(function (p) { p.addEventListener("pointerenter", function () { marcarH(+p.getAttribute("data-historia")); }); });
    }
    passosH.forEach(function (p) { p.addEventListener("click", function () { marcarH(+p.getAttribute("data-historia")); }); });
    // as camadas do diagrama se movem com o cursor, cada uma numa profundidade
    if (ponteiroFino && !semMovimento) {
      var camadasH = $$(".camada", palcoH), alvoH = { x: 0, y: 0 }, atualH = { x: 0, y: 0 }, rodandoH = false;
      var passoH = function () {
        atualH.x += (alvoH.x - atualH.x) * .08; atualH.y += (alvoH.y - atualH.y) * .08;
        camadasH.forEach(function (c) {
          var f = parseFloat(c.getAttribute("data-prof"));
          c.setAttribute("transform", "translate(" + (atualH.x * 10 * f).toFixed(1) + " " + (atualH.y * 8 * f).toFixed(1) + ")");
        });
        if (Math.abs(alvoH.x - atualH.x) > .002 || Math.abs(alvoH.y - atualH.y) > .002) requestAnimationFrame(passoH); else rodandoH = false;
      };
      palcoH.addEventListener("pointermove", function (e) {
        var r = palcoH.getBoundingClientRect();
        alvoH.x = (e.clientX - r.left) / r.width - .5; alvoH.y = (e.clientY - r.top) / r.height - .5;
        if (!rodandoH) { rodandoH = true; requestAnimationFrame(passoH); }
      });
      palcoH.addEventListener("pointerleave", function () { alvoH.x = alvoH.y = 0; if (!rodandoH) { rodandoH = true; requestAnimationFrame(passoH); } });
    }
    if (semMovimento && palcoH.querySelector("svg").pauseAnimations) palcoH.querySelector("svg").pauseAnimations();
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

  /* ------------------------------------------------------------ registro de pedidos */
  $$("[data-pedidos]").forEach(function (pd) {
    var total = $("[data-pd-total]", pd), registrar = $("[data-pd-registrar]", pd), lista = $("[data-pd-lista]", pd);
    var numero = +pd.getAttribute("data-proximo") || 1044;
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
      voltar.hidden = false;
      voltar.textContent = n === 0 ? "Voltar à página anterior" : "Voltar";
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
    voltar.addEventListener("click", function () {
      if (atual > 0) { irPara(atual - 1); return; }
      var veioDoSite = document.referrer && document.referrer.indexOf(location.host) > -1;
      if (veioDoSite && history.length > 1) history.back(); else location.href = "index.html";
    });
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
      acoes.appendChild(bWhats);
      resultado.appendChild(acoes);
      resultado.appendChild(el("p", "sim-rec-nota", "A recomendação é um ponto de partida. O orçamento final é combinado pelo WhatsApp, conforme o seu negócio."));
      bWhats.addEventListener("click", function () {
        if (bWhats.disabled) return;
        if (NUMEROS.length) window.open(linkSorteado(mensagem), "_blank", "noopener");
        bWhats.disabled = true; bWhats.textContent = "Mensagem aberta no WhatsApp";
        setTimeout(function () { bWhats.disabled = false; bWhats.textContent = "Enviar pelo WhatsApp"; }, 4000);
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

  /* ------------------------------------------------------------ hero 3D do Início (js/hero-3d.js)
     O texto e o botão de WhatsApp já funcionam antes. O 3D só é baixado depois que a página
     abriu, e nunca com movimento reduzido ou economia de dados: aí fica a imagem do K. */
  var economia = navigator.connection && navigator.connection.saveData;
  if ($("[data-hero-palco]")) {
    if (semMovimento || economia) document.documentElement.classList.add("sem-3d");
    else {
      var carregarHero = function () { import("./hero-3d.js?v=" + (document.documentElement.getAttribute("data-v") || "1")).catch(function () { document.documentElement.classList.add("sem-3d"); }); };
      var depoisDeAbrir = function () { if ("requestIdleCallback" in window) requestIdleCallback(carregarHero, { timeout: 2000 }); else setTimeout(carregarHero, 300); };
      if (document.readyState === "complete") depoisDeAbrir(); else addEventListener("load", depoisDeAbrir);
    }
  }

  /* ------------------------------------------------------------ o K da marca em 3D: carrega o Three.js só onde precisa, depois que a página abriu */
  if ($("[data-k3d]")) {
    var carregarK = function () { import("./k3d.js").catch(function () {}); };
    if ("requestIdleCallback" in window) requestIdleCallback(carregarK, { timeout: 1500 }); else setTimeout(carregarK, 600);
  }

  /* ------------------------------------------------------------ ano do rodapé */
  var ano = $("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
