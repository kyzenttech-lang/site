# KYZENT

Site da **KYZENT Technology Solutions**, empresa de automação e IA para pequenos comércios de Paulínia (SP).

**Site:** https://kyzenttech-lang.github.io/site/
**Instagram:** [@kyzent.tech](https://www.instagram.com/kyzent.tech/)

## Arquivos

| Caminho | O que é |
|---|---|
| `index.html` | a página do site |
| `css/style.css` | cores, fontes e layout (tema escuro da marca, mobile first) |
| `assets/img/` | logos: `kyzent-horizontal-escuro.svg` (site), `kyzent-horizontal-claro.svg` (fundo branco) e `kyzent-k.svg` (o K grande do topo) |
| `assets/icons/` | favicon (`icon.svg`, `favicon-32.png`) e ícone do iPhone (`apple-touch-icon.png`) |
| `assets/og-image.png` | imagem que aparece ao compartilhar o link (1200 x 630) |
| `tools/` | o que gera os logos e a `og-image` (não aparece no site) |
| `.nojekyll` | avisa o GitHub Pages para publicar os arquivos como estão |

O site é feito só com HTML e CSS. Não tem nada para instalar nem compilar.

## Como publicar

O site é publicado pelo GitHub Pages a partir da branch `main`, pasta `/ (root)`. Para ligar (só uma vez, com a conta `kyzenttech-lang`):

1. No repositório, abra **Settings → Pages**.
2. Em **Build and deployment**, escolha **Deploy from a branch**, a branch `main` e a pasta `/ (root)`, e clique em **Save**.
3. Em 1 ou 2 minutos o site aparece no endereço acima.

Depois disso, todo `git push` na `main` atualiza o site.

## Como editar

- **Números de WhatsApp:** no `index.html`, entre os comentários `NÚMEROS DE WHATSAPP` e `fim dos números`. Em cada botão, troque o número no link (só dígitos, começando com `55`) e o número escrito.
- **Nome em cima de cada número:** no mesmo bloco, tire o comentário da linha `<span class="contato-nome">` e escreva o nome.
- **Ano do rodapé:** está fixo como `© 2026 KYZENT`. Troque na virada do ano.
- **Domínio próprio:** quando houver, configure em **Settings → Pages → Custom domain** e troque os endereços de `canonical`, `og:url` e `og:image` no topo do `index.html`.

## Logo

O logo do site é o K atual da marca (lâmina prata, braço azul, perna em fita e órbita), que fica em `empresa/logo-kyzent/camisas/svg/`, junto com o letreiro "KYZENT" e o slogan "AUTOMAÇÃO & IA". Se o K mudar, gere os logos de novo na raiz do site:

```
python tools/gera_assets.py "../empresa/logo-kyzent" tools/letreiro-kyzent.svg assets
```

Os PNGs (favicon, ícone do iPhone e `og-image`) são capturas do Chrome. A `og-image` sai de `tools/og-image.html`, aberto em 1200 x 630.

O WhatsApp e o Instagram guardam a prévia do link em cache. Por isso, uma nova `og-image.png` pode demorar a aparecer em links que já foram enviados.
