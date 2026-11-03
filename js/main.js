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
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () {
      var aberto = menu.classList.toggle("aberto");
      botaoMenu.setAttribute("aria-expanded", aberto ? "true" : "false");
      botaoMenu.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
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

  // ano do rodapé sempre atualizado
  var ano = document.querySelector("[data-ano]");
  if (ano) ano.textContent = new Date().getFullYear();
})();
