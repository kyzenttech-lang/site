# KYZENT

Site da **KYZENT Technology Solutions**, empresa de automação e IA para pequenos comércios de Paulínia (SP).

**Site:** https://otaviofelix-in.github.io/kyzent/
**Instagram:** [@kyzent.tech](https://www.instagram.com/kyzent.tech/)

## Arquivos

| Caminho | O que é |
|---|---|
| `index.html` | a página do site |
| `css/style.css` | cores, fontes e layout |
| `assets/` | logos, favicon e `og-image.png` (imagem que aparece ao compartilhar o link) |

O site é feito só com HTML e CSS. Não tem nada para instalar nem compilar.

## Como publicar

O site é publicado pelo GitHub Pages a partir da branch `main`.

1. No repositório, abra **Settings → Pages**.
2. Em **Build and deployment**, escolha **Deploy from a branch**, a branch `main` e a pasta `/ (root)`, e clique em **Save**.
3. Em 1 ou 2 minutos o site aparece no endereço acima.

Depois disso, todo `git push` na `main` atualiza o site.

## Como editar

- **Números de WhatsApp:** no `index.html`, entre os comentários `NÚMEROS DE WHATSAPP` e `fim dos números`. Em cada botão, troque o número no link (só dígitos, começando com `55`) e o número escrito.
- **Nome em cima de cada número:** no mesmo bloco, tire o comentário da linha `<span class="contato-nome">` e escreva o nome.
- **Ano do rodapé:** está fixo como `© 2026 KYZENT`. Troque na virada do ano.
- **Domínio próprio:** quando houver, configure em **Settings → Pages → Custom domain** e troque os endereços de `og:url` e `og:image` no topo do `index.html`.

O WhatsApp e o Instagram guardam a prévia do link em cache. Por isso, uma nova `og-image.png` pode demorar a aparecer em links que já foram enviados.
