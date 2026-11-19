// KYZENT — animações 2D com GSAP + ScrollTrigger (assets/vendor/gsap, versão 3.13).
// O CustomEase deixa o GSAP usar as mesmas curvas do CSS (--ease e --mola).
//
// Regras: 0,2 a 0,8 s; só transform e opacity; nada em loop perto de texto.
// O estado escondido é aplicado aqui, pelo JS: se o GSAP não carregar, tudo fica visível.
// Com movimento reduzido nada é animado. O que já está na tela ao abrir não é animado
// (evita piscar e não atrasa o LCP: o título do topo aparece na hora).
(function () {
  "use strict";
  var g = window.gsap;
  var semMovimento = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!g || !window.ScrollTrigger || semMovimento) return;
  g.registerPlugin(window.ScrollTrigger, window.CustomEase);
  var EASE = window.CustomEase ? CustomEase.create("kyzent", ".2,.8,.2,1") : "power3.out";
  var MOLA = window.CustomEase ? CustomEase.create("mola", ".34,1.4,.64,1") : "back.out(1.6)";
  var ponteiroFino = matchMedia("(pointer: fine)").matches;

  function $$(sel, raiz) { return Array.prototype.slice.call((raiz || document).querySelectorAll(sel)); }
  function abaixoDaDobra(el) { var r = el.getBoundingClientRect(); return r.top > innerHeight * 0.92 || (r.width === 0 && r.height === 0); }
  function visivelNaPagina(el) { return !el.closest("[hidden]"); }

  /* ------------------------------------------------------------ títulos: revelação por linha */
  // As palavras são medidas para descobrir as linhas reais (depois que a fonte carrega).
  // Cada linha sobe de dentro de uma máscara. No fim, o título volta a ser texto simples,
  // então girar o celular ou mudar a largura não quebra nada.
  function revelarTitulo(t) {
    var texto = t.textContent.trim();
    var palavras = texto.split(/\s+/);
    t.innerHTML = palavras.map(function (p) { return '<span class="tl-palavra">' + p + "</span>"; }).join(" ");
    var linhas = [], topo = null;
    $$(".tl-palavra", t).forEach(function (s) {
      if (topo === null || Math.abs(s.offsetTop - topo) > 4) { linhas.push([]); topo = s.offsetTop; }
      linhas[linhas.length - 1].push(s.textContent);
    });
    t.innerHTML = '<span class="visualmente-oculto">' + texto + "</span>" + linhas.map(function (l) {
      return '<span class="tl-linha" aria-hidden="true"><span class="tl-dentro">' + l.join(" ") + "</span></span>";
    }).join("");
    var dentro = $$(".tl-dentro", t);
    g.set(dentro, { yPercent: 105 });
    g.to(dentro, {
      yPercent: 0, duration: 0.8, ease: EASE, stagger: 0.09,
      scrollTrigger: { trigger: t, start: "top 88%", once: true },
      onComplete: function () { t.textContent = texto; },
    });
  }
  var titulos = $$("[data-revelar-texto]").filter(function (t) {
    return !t.children.length && !t.closest(".hero") && abaixoDaDobra(t);
  });
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () {
    titulos.forEach(revelarTitulo);
    ScrollTrigger.refresh();
  });

  /* ------------------------------------------------------------ blocos que entram ao rolar (fade + 24 px), cartões em sequência */
  var GRUPOS = ".grade, .ramos, .etapas, .painel-itens, .solucoes, .hero-numeros, .aurora-faz, .perguntas, .diferenciais, .seg-cols, .eg";
  var SOLTOS = ".cabeca > p, .cabeca-linha > .link-seta, .dupla-foto, .dupla-texto, .demo-texto, .demo-tela, .pagina-topo-apoio, " +
               ".pagina-topo-texto, .revelar-bloco, .aurora-texto > p, .aurora-texto > .botao, .aurora-texto > .pilar-rotulo, .comparar, .chamada-caixa";
  var alvos = [];
  $$(GRUPOS).forEach(function (grupo) { Array.prototype.forEach.call(grupo.children, function (f) { alvos.push(f); }); });
  $$(SOLTOS).forEach(function (el) { if (alvos.indexOf(el) === -1) alvos.push(el); });
  alvos = alvos.filter(function (el) { return visivelNaPagina(el) && abaixoDaDobra(el) && !el.closest(".hero"); });
  if (alvos.length) {
    g.set(alvos, { autoAlpha: 0, y: 24, transition: "none" });
    ScrollTrigger.batch(alvos, {
      start: "top 90%", once: true,
      onEnter: function (lote) {
        g.to(lote, { autoAlpha: 1, y: 0, duration: 0.7, ease: EASE, stagger: 0.08, overwrite: true, clearProps: "transform,opacity,visibility,transition" });
      },
    });
  }

  /* ------------------------------------------------------------ números: contagem ao entrar na tela */
  $$("[data-contar]").forEach(function (el) {
    var alvo = parseInt(el.getAttribute("data-contar"), 10);
    if (!alvo) return;
    var aba = el.closest("[role=tabpanel]");
    if (aba && aba.hidden) {
      aba.addEventListener("demo-visivel", function () {
        var m = { v: 0 };
        g.to(m, { v: alvo, duration: 0.8, ease: EASE, onUpdate: function () { el.textContent = Math.round(m.v).toLocaleString("pt-BR"); } });
      });
      return;
    }
    if (!abaixoDaDobra(el)) return;
    var n = { v: 0 };
    el.textContent = "0";
    g.to(n, {
      v: alvo, duration: 0.8, ease: EASE,
      scrollTrigger: { trigger: el, start: "top 92%", once: true },
      onUpdate: function () { el.textContent = Math.round(n.v).toLocaleString("pt-BR"); },
    });
  });

  /* ------------------------------------------------------------ cartões de soluções: inclinação 3D que segue o cursor (só com mouse) */
  if (ponteiroFino) {
    $$(".solucao").forEach(function (c) {
      c.classList.add("gsap-inclina");
      g.set(c, { transformPerspective: 900 });
      var rx = g.quickTo(c, "rotationX", { duration: 0.4, ease: EASE });
      var ry = g.quickTo(c, "rotationY", { duration: 0.4, ease: EASE });
      var y = g.quickTo(c, "y", { duration: 0.4, ease: EASE });
      c.addEventListener("pointerenter", function () { y(-6); });
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - 0.5) * 8);    // até 4 graus para cada lado
        rx(-((e.clientY - r.top) / r.height - 0.5) * 6);
      });
      c.addEventListener("pointerleave", function () { rx(0); ry(0); y(0); });
    });
  }

  /* ------------------------------------------------------------ antes e depois: as tarefas passam de "Pendente" para "Feito" em sequência */
  $$("[data-comparar]").forEach(function (cmp) {
    if (!abaixoDaDobra(cmp)) return;
    var estados = $$(".cmp-auto-item .cmp-estado", cmp);
    estados.forEach(function (e) { e.textContent = "Pendente"; e.classList.remove("cmp-feito"); });
    ScrollTrigger.create({
      trigger: cmp, start: "top 70%", once: true,
      onEnter: function () {
        estados.forEach(function (e, i) {
          g.delayedCall(0.3 + i * 0.45, function () {
            e.textContent = "Feito"; e.classList.add("cmp-feito");
            g.fromTo(e, { scale: 0.8 }, { scale: 1, duration: 0.4, ease: MOLA });
          });
        });
      },
    });
  });

  /* ------------------------------------------------------------ ERP: cena 3D (os blocos descem sobre a base) e caminho da venda */
  $$("[data-erp-3d]").forEach(function (cena) {
    cena.classList.add("pronto");
    ScrollTrigger.create({ trigger: cena, start: "top 75%", once: true, onEnter: function () { cena.classList.add("entrou"); } });
    if (!ponteiroFino) return;
    var plano = cena.querySelector("[data-erp-cena]");
    var base = { rx: 56, rz: -38 };
    var rx = g.quickTo(plano, "rotationX", { duration: 0.6, ease: EASE });
    var rz = g.quickTo(plano, "rotationZ", { duration: 0.6, ease: EASE });
    g.set(plano, { rotationX: base.rx, rotationZ: base.rz, transformPerspective: 1400 });
    cena.addEventListener("pointermove", function (e) {
      var r = cena.getBoundingClientRect();
      rz(base.rz + ((e.clientX - r.left) / r.width - 0.5) * 16);   // gira até 8 graus para cada lado
      rx(base.rx - ((e.clientY - r.top) / r.height - 0.5) * 10);
    });
    cena.addEventListener("pointerleave", function () { rx(base.rx); rz(base.rz); });
  });
  /* ERP, o que resolve: os papéis caem na mesa, a tela gira para a frente e os itens acendem; a cena segue o mouse */
  $$("[data-er]").forEach(function (sec) {
    sec.classList.add("pronto");
    ScrollTrigger.create({ trigger: sec, start: "top 70%", once: true, onEnter: function () { sec.classList.add("visto"); } });
    if (!ponteiroFino) return;
    $$("[data-er-cena] > *", sec).forEach(function (alvo) {
      var ry = g.quickTo(alvo, "rotationY", { duration: 0.7, ease: EASE });
      var rx = g.quickTo(alvo, "rotationX", { duration: 0.7, ease: EASE });
      var base = alvo.classList.contains("er-tela") ? { x: 8, y: -16 } : { x: 16, y: 12 };
      sec.addEventListener("pointermove", function (e) {
        if (!sec.classList.contains("visto")) return;
        var r = sec.getBoundingClientRect();
        ry(base.y + ((e.clientX - r.left) / r.width - 0.5) * 10);
        rx(base.x - ((e.clientY - r.top) / r.height - 0.5) * 8);
      });
      sec.addEventListener("pointerleave", function () { ry(base.y); rx(base.x); });
    });
  });
  $$("[data-erp-caminho]").forEach(function (cam) {
    var sem = $$(".ec-sem li", cam), com = $$(".ec-com li", cam);
    g.set(sem.concat(com), { autoAlpha: 0, y: 16 });
    ScrollTrigger.create({
      trigger: cam, start: "top 72%", once: true,
      onEnter: function () {
        // sem ERP: uma etapa depois da outra, devagar; com ERP: tudo de uma vez, e a luz atravessa a faixa
        g.to(sem, { autoAlpha: 1, y: 0, duration: 0.5, ease: EASE, stagger: 0.5 });
        g.to(com, { autoAlpha: 1, y: 0, duration: 0.45, ease: EASE, stagger: 0.05, delay: 0.1, onStart: function () { cam.classList.add("rodou"); } });
      },
    });
  });
  $$("[data-erp-ganho]").forEach(function (c) {
    ScrollTrigger.create({ trigger: c, start: "top 78%", once: true, onEnter: function () { c.classList.add("visto"); } });
  });
  if (ponteiroFino) {
    $$(".eg-item").forEach(function (c) {
      g.set(c, { transformPerspective: 900 });
      var rx = g.quickTo(c, "rotationX", { duration: 0.4, ease: EASE });
      var ry = g.quickTo(c, "rotationY", { duration: 0.4, ease: EASE });
      var y = g.quickTo(c, "y", { duration: 0.4, ease: EASE });
      c.addEventListener("pointerenter", function () { y(-6); });
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - 0.5) * 10);
        rx(-((e.clientY - r.top) / r.height - 0.5) * 8);
      });
      c.addEventListener("pointerleave", function () { rx(0); ry(0); y(0); });
    });
  }

  // as abas das demos e o FAQ mudam a altura da página: recalcula os gatilhos
  document.addEventListener("click", function (e) {
    if (e.target.closest("[role=tab], summary")) setTimeout(function () { ScrollTrigger.refresh(); }, 350);
  });
})();
