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
  var GRUPOS = ".grade, .ramos, .etapas, .painel-itens, .solucoes, .hero-numeros, .aurora-faz, .perguntas, .diferenciais, .seg-cols";
  var SOLTOS = ".cabeca > p, .cabeca-linha > .link-seta, .dupla-foto, .dupla-texto, .demo-texto, .demo-tela, .pagina-topo-apoio, " +
               ".pagina-topo-texto, .revelar-bloco, .aurora-texto > p, .aurora-texto > .botao, .aurora-texto > .pilar-rotulo, .comparar, .chamada-caixa";
  var alvos = [];
  $$(GRUPOS).forEach(function (grupo) { Array.prototype.forEach.call(grupo.children, function (f) { alvos.push(f); }); });
  $$(SOLTOS).forEach(function (el) { if (alvos.indexOf(el) === -1) alvos.push(el); });
  alvos = alvos.filter(function (el) { return visivelNaPagina(el) && abaixoDaDobra(el) && !el.closest(".hero"); });
  if (alvos.length) {
    g.set(alvos, { autoAlpha: 0, y: 24 });
    ScrollTrigger.batch(alvos, {
      start: "top 90%", once: true,
      onEnter: function (lote) {
        g.to(lote, { autoAlpha: 1, y: 0, duration: 0.7, ease: EASE, stagger: 0.08, overwrite: true, clearProps: "transform,opacity,visibility" });
      },
    });
  }

  /* ------------------------------------------------------------ números: contagem ao entrar na tela */
  $$("[data-contar]").forEach(function (el) {
    var alvo = parseInt(el.getAttribute("data-contar"), 10);
    if (!alvo || !abaixoDaDobra(el)) return;
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

  // as abas das demos e o FAQ mudam a altura da página: recalcula os gatilhos
  document.addEventListener("click", function (e) {
    if (e.target.closest("[role=tab], summary")) setTimeout(function () { ScrollTrigger.refresh(); }, 350);
  });
})();
