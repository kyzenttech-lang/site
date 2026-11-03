// KYZENT — tema claro/escuro, menu do celular e ano do rodapé.
(function () {
  var raiz = document.documentElement;

  // botão de tema: alterna e lembra a escolha neste aparelho
  var botaoTema = document.querySelector("[data-trocar-tema]");
  function rotuloTema() {
    if (!botaoTema) return;
    var escuro = raiz.getAttribute("data-theme") === "dark";
    botaoTema.setAttribute("aria-label", escuro ? "Usar tema claro" : "Usar tema escuro");
  }
  if (botaoTema) {
    rotuloTema();
    botaoTema.addEventListener("click", function () {
      var novo = raiz.getAttribute("data-theme") === "dark" ? "light" : "dark";
      raiz.setAttribute("data-theme", novo);
      try { localStorage.setItem("kyzent-tema", novo); } catch (e) {}
      rotuloTema();
    });
  }

  // menu do celular
  var botaoMenu = document.querySelector("[data-abrir-menu]");
  var menu = document.getElementById("menu-celular");
  function menuAberto(aberto) {
    menu.classList.toggle("aberto", aberto);
    raiz.classList.toggle("menu-aberto", aberto);
    botaoMenu.setAttribute("aria-expanded", aberto ? "true" : "false");
    botaoMenu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
  }
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () {
      menuAberto(!menu.classList.contains("aberto"));
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { menuAberto(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("aberto")) { menuAberto(false); botaoMenu.focus(); }
    });
    // se a tela crescer (girou o celular), o menu de celular fecha
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1000 && menu.classList.contains("aberto")) menuAberto(false);
    });
  }

  // janelas dos ramos (lanchonete, barbearia...)
  function fecharJanela(j) {
    if (j.open) j.close();
  }
  document.querySelectorAll("[data-abrir-janela]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      var j = document.getElementById(botao.getAttribute("data-abrir-janela"));
      if (!j || typeof j.showModal !== "function") return;
      j.showModal();
      raiz.classList.add("janela-aberta");
    });
  });
  document.querySelectorAll("dialog.janela").forEach(function (j) {
    j.addEventListener("close", function () { raiz.classList.remove("janela-aberta"); });
    // clique fora da caixa fecha
    j.addEventListener("click", function (e) { if (e.target === j) fecharJanela(j); });
    j.querySelectorAll("[data-fechar-janela]").forEach(function (b) {
      b.addEventListener("click", function () { fecharJanela(j); });
    });
  });

  // abas da página de serviços
  var abas = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
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
        void painel.offsetWidth; // reinicia a animação
        painel.setAttribute("data-entrando", "");
      }
    });
    if (focar) aba.focus();
    aba.scrollIntoView({ block: "nearest", inline: "nearest" });
    // se a pessoa já desceu a página, volta para o começo do painel novo
    if (rolar) rolarParaServicos(true);
  }
  function rolarParaServicos(suave) {
    var secao = document.querySelector(".secao-servicos");
    if (!secao) return;
    var topo = secao.getBoundingClientRect().top;
    var barraTopo = 72;
    if (topo < barraTopo) window.scrollTo({ top: topo + window.scrollY - barraTopo, behavior: suave ? "smooth" : "auto" });
  }
  if (abas.length) {
    abas.forEach(function (aba, i) {
      aba.addEventListener("click", function () {
        mostrarAba(aba, false, true);
        try { history.replaceState(null, "", "#" + aba.getAttribute("aria-controls")); } catch (e) {}
      });
      aba.addEventListener("keydown", function (e) {
        var alvo = null;
        if (e.key === "ArrowRight") alvo = abas[(i + 1) % abas.length];
        else if (e.key === "ArrowLeft") alvo = abas[(i - 1 + abas.length) % abas.length];
        else if (e.key === "Home") alvo = abas[0];
        else if (e.key === "End") alvo = abas[abas.length - 1];
        if (alvo) { e.preventDefault(); mostrarAba(alvo, true, false); }
      });
    });
    // abre a aba que veio no link (ex.: servicos.html#servico-02)
    var inicial = abas[0];
    abas.forEach(function (a) { if ("#" + a.getAttribute("aria-controls") === location.hash) inicial = a; });
    mostrarAba(inicial, false, false);
    if (inicial !== abas[0]) {
      setTimeout(function () {
        var secao = document.querySelector(".secao-servicos");
        if (secao) window.scrollTo(0, secao.getBoundingClientRect().top + window.scrollY - 72);
      }, 0);
    }
  }

  // monte o seu orçamento
  var barra = document.querySelector("[data-selecao]");
  if (barra) {
    var escolhidos = [];
    var enviar = barra.querySelector("[data-selecao-enviar]");
    var numero = enviar.getAttribute("data-numero");
    function atualizar() {
      var n = escolhidos.length;
      barra.hidden = n === 0;
      document.body.classList.toggle("com-selecao", n > 0);
      barra.querySelector("[data-selecao-total]").textContent = n;
      barra.querySelector("[data-selecao-palavra]").textContent = n === 1 ? "serviço" : "serviços";
      barra.querySelector("[data-selecao-lista]").textContent = escolhidos.join(" · ");
      var msg = "Olá, vim pelo site da KYZENT e quero um orçamento para:\n" +
        escolhidos.map(function (s) { return "- " + s; }).join("\n");
      enviar.href = "https://wa.me/" + numero + "?text=" + encodeURIComponent(msg);
    }
    document.querySelectorAll("[data-servico]").forEach(function (b) {
      b.addEventListener("click", function () {
        var nome = b.getAttribute("data-servico");
        var i = escolhidos.indexOf(nome);
        if (i === -1) escolhidos.push(nome); else escolhidos.splice(i, 1);
        var ligado = i === -1;
        b.setAttribute("aria-pressed", ligado ? "true" : "false");
        b.querySelector(".item-add-rotulo").textContent = ligado ? "Adicionado" : "Adicionar ao orçamento";
        b.closest(".item").classList.toggle("escolhido", ligado);
        atualizar();
      });
    });
    barra.querySelector("[data-selecao-limpar]").addEventListener("click", function () {
      escolhidos = [];
      document.querySelectorAll('[data-servico][aria-pressed="true"]').forEach(function (b) {
        b.setAttribute("aria-pressed", "false");
        b.querySelector(".item-add-rotulo").textContent = "Adicionar ao orçamento";
        b.closest(".item").classList.remove("escolhido");
      });
      atualizar();
    });
  }

  // ano do rodapé sempre atualizado
  var ano = document.querySelector("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
