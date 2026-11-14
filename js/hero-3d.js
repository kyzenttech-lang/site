// KYZENT — cena 3D do Início (a partir do protótipo kyzent-hero-3d.html): topo e fluxo em 4 passos.
// O K da logo extrudado dos paths do SVG oficial, a órbita como anel 3D com o ponto azul,
// três cartões de notificação e partículas. Um único renderer WebGL: ele fica no topo e,
// nas etapas seguintes, outras cenas (fluxo, segmentos) podem pedir o mesmo canvas.
//
// Carregado por js/main.js com import dinâmico, depois da página aberta.
// Enquanto isso (e se der errado) fica a imagem do K (.hero-poster) no mesmo lugar.
import * as THREE from "../assets/vendor/three/three.module.min.js";
import { SVGLoader } from "../assets/vendor/three/SVGLoader.js";
import { RoomEnvironment } from "../assets/vendor/three/RoomEnvironment.js";

// Dois palcos, um canvas: o topo (K, cartões e partículas) e a seção "Uma mensagem entra"
// (o ponto da órbita viaja pelas 4 estações, uma por passo). O canvas se muda para o palco
// que está na tela; com nenhum na tela, nada é desenhado.
const palcoHero = document.querySelector("[data-hero-palco]");
const hero = palcoHero && palcoHero.closest("[data-hero]");
const palcoFluxo = document.querySelector("[data-historia-palco]");
const palcoSeg = document.querySelector("[data-seg-palco]");   // ícone 3D do segmento escolhido
if (palcoHero && hero) iniciar();

function desistir(canvas, renderer) {
  // volta para a imagem parada (sem WebGL ou aparelho lento)
  document.documentElement.classList.add("sem-3d");
  hero?.classList.remove("hero-3d-pronto");
  palcoFluxo?.classList.remove("palco-3d-pronto");
  palcoSeg?.classList.remove("palco-3d-pronto");
  if (renderer) { renderer.setAnimationLoop(null); renderer.dispose(); renderer.forceContextLoss?.(); }
  canvas?.remove();
}

function iniciar() {
  const fraco = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory || 8) <= 4;
  const canvas = document.createElement("canvas");
  canvas.className = "hero-canvas";
  canvas.setAttribute("aria-hidden", "true");

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: !fraco, alpha: true, powerPreference: "high-performance" });
  } catch (e) { desistir(canvas); return; }
  let palco = palcoHero, modo = "hero";
  palco.appendChild(canvas);

  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(0, 0, 9);

  // reflexos suaves no metal
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();

  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  const sol = new THREE.DirectionalLight(0xffffff, 1.6); sol.position.set(3, 4, 6); scene.add(sol);
  const luzA = new THREE.PointLight(0x1A5CFF, 40); luzA.position.set(-4, -2, 3); scene.add(luzA);
  const luzB = new THREE.PointLight(0x3FB4FF, 25); luzB.position.set(4, 3, 2); scene.add(luzB);

  // ---------- K: os 3 paths do SVG oficial ----------
  const svgK = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 1080 520">
    <path id="perna" d="M228 507 L338 352 C360 322 384 306 422 305 L585 305 C625 305 652 322 676 345 L870 515 L655 515 L530 403 C520 395 508 392 496 392 L455 392 C442 392 432 396 424 403 L312 507 Z"/>
    <path id="braco" d="M400 282 C470 232 560 150 620 100 C652 72 684 58 724 58 L866 58 L702 222 C690 232 668 238 640 238 L482 240 C452 242 426 258 400 282 Z"/>
    <path id="haste" d="M390 80 L388 225 L237 372 L237 235 Z"/>
  </svg>`;

  const c = (h) => new THREE.Color(h);
  const rampa = (paradas) => (t) => {        // degradê com várias paradas
    t = Math.min(1, Math.max(0, t));
    for (let i = 1; i < paradas.length; i++) {
      const [t0, c0] = paradas[i - 1], [t1, c1] = paradas[i];
      if (t <= t1) return c0.clone().lerp(c1, (t - t0) / (t1 - t0 || 1));
    }
    return paradas[paradas.length - 1][1].clone();
  };
  // os mesmos degradês do SVG da marca
  const gradientes = {
    perna: { cor: rampa([[0, c("#0A3DFF")], [.3, c("#1A5CFF")], [.55, c("#F4F7FB")], [1, c("#8E9AAE")]]), t: (x) => (x - 228) / (870 - 228) },
    braco: { cor: rampa([[0, c("#0A3DFF")], [1, c("#3FB4FF")]]), t: (x, y) => ((x - 400) / 466 + (282 - y) / 224) / 2 },
    haste: { cor: rampa([[0, c("#F4F7FB")], [1, c("#8E9AAE")]]), t: (x, y) => ((x - 237) / 153 + (y - 80) / 292) / 2 },
  };

  const raiz = new THREE.Group();            // posição, escala e rotação interativas
  const espelho = new THREE.Group();         // o SVG tem o y para baixo
  espelho.scale.set(0.005, -0.005, 0.005);
  raiz.add(espelho); scene.add(raiz);

  const metal = new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 0.55, roughness: 0.26, envMapIntensity: 0.9 });
  for (const p of new SVGLoader().parse(svgK).paths) {
    const g = gradientes[p.userData.node.id];
    const geo = new THREE.ExtrudeGeometry(SVGLoader.createShapes(p), {
      depth: 90, bevelEnabled: true, bevelThickness: 12, bevelSize: 9, bevelSegments: fraco ? 2 : 4, curveSegments: fraco ? 8 : 16,
    });
    const pos = geo.attributes.position, cores = new Float32Array(pos.count * 3);
    for (let i = 0; i < pos.count; i++) {
      const cor = g.cor(g.t(pos.getX(i), pos.getY(i)));
      cores.set([cor.r, cor.g, cor.b], i * 3);
    }
    geo.setAttribute("color", new THREE.BufferAttribute(cores, 3));
    geo.translate(-530, -285, -45);
    espelho.add(new THREE.Mesh(geo, metal));
  }

  // ---------- órbita: o anel da logo em 3D ----------
  const R = 515;
  const orbita = new THREE.Group();
  orbita.rotation.order = "ZYX";
  orbita.rotation.set(1.27, 0, THREE.MathUtils.degToRad(-24));   // inclinação + os -24° do SVG
  espelho.add(orbita);

  const anelGeo = new THREE.TorusGeometry(R, 9, 10, fraco ? 96 : 200);
  {
    const pos = anelGeo.attributes.position, cores = new Float32Array(pos.count * 3);
    const meio = c("#1A5CFF"), ponta = c("#3FB4FF");
    for (let i = 0; i < pos.count; i++) {
      const cor = meio.clone().lerp(ponta, Math.abs(pos.getX(i)) / R);
      const frente = THREE.MathUtils.smoothstep(pos.getY(i), -120, 120);   // metade de trás mais apagada, como na logo
      cor.multiplyScalar(0.5 + 0.5 * frente);
      cores.set([cor.r, cor.g, cor.b], i * 3);
    }
    anelGeo.setAttribute("color", new THREE.BufferAttribute(cores, 3));
  }
  orbita.add(new THREE.Mesh(anelGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false })));

  const ponto = new THREE.Mesh(new THREE.SphereGeometry(24, 20, 20), new THREE.MeshBasicMaterial({ color: 0x8FD4FF, toneMapped: false }));
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaHalo(), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
  halo.scale.setScalar(260); ponto.add(halo); orbita.add(ponto);

  // ---------- estações dos 4 passos (só no modo "fluxo"): pontos fixos no anel ----------
  const ANGULOS = [0.4, 2.0, 3.6, 5.2];
  const corApagada = c("#1A5CFF"), corAcesa = c("#3FB4FF"), corAtual = c("#DDF1FF");
  const estacoes = ANGULOS.map((a) => {
    const m = new THREE.Mesh(new THREE.SphereGeometry(17, 16, 16), new THREE.MeshBasicMaterial({ color: corApagada, toneMapped: false }));
    m.position.set(Math.cos(a) * R, Math.sin(a) * R, 0); m.visible = false; orbita.add(m); return m;
  });
  let etapa = +(palcoFluxo?.getAttribute("data-etapa") || 1), impulso = 0;
  document.addEventListener("historia-etapa", (e) => { etapa = e.detail; impulso = 1; });

  // ---------- cartões flutuantes (o que a automação faz) ----------
  const cartoes = [
    { texto: "Agendamento confirmado", cor: "#4ADE9B", p: [-1.75, 1.5, 0.7], cel: [-1.15, 2.05, 0.7] },
    { texto: "Novo pedido recebido", cor: "#3FB4FF", p: [1.3, -1.55, 0.9], cel: [1.2, -1.4, 0.9] },
    { texto: "Cliente respondido", cor: "#F5C451", p: [1.35, 1.8, -0.6], cel: [1.55, 0.75, 0.4] },
  ].map((d, i) => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ transparent: true, depthWrite: false }));
    s.userData = { ...d, fase: i * 2.1 }; raiz.add(s); return s;
  });
  const pintar = () => cartoes.forEach((s) => {
    s.material.map?.dispose(); s.material.map = texturaCartao(s.userData.texto, s.userData.cor); s.material.needsUpdate = true;
  });
  pintar(); document.fonts?.ready.then(pintar);

  // ---------- partículas de fundo ----------
  const celular = innerWidth < 860;
  const N = fraco || celular ? 220 : 600;
  const pGeo = new THREE.BufferGeometry(), pPos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) pPos.set([(Math.random() - .5) * 22, (Math.random() - .5) * 14, -6 + Math.random() * 9], i * 3);
  pGeo.setAttribute("position", new THREE.BufferAttribute(pPos, 3));
  const particulas = new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0x3FB4FF, size: 0.035, transparent: true, opacity: 0.55, depthWrite: false }));
  scene.add(particulas);

  // ---------- ícones dos segmentos: formas simples, nas cores da marca ----------
  // Cada ícone cabe numa caixa de ~1,3 unidade. Só o do segmento escolhido aparece.
  const prata = new THREE.MeshStandardMaterial({ color: c("#C9D2DF"), metalness: 0.6, roughness: 0.28 });
  const azul = new THREE.MeshStandardMaterial({ color: c("#1A5CFF"), metalness: 0.3, roughness: 0.3 });
  const azulClaro = new THREE.MeshStandardMaterial({ color: c("#3FB4FF"), metalness: 0.2, roughness: 0.3 });
  const malha = (geo, mat, x = 0, y = 0, z = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); return m; };
  const FORMAS = {
    lanchonete() {   // hambúrguer
      const g = new THREE.Group();
      const topo = malha(new THREE.SphereGeometry(0.58, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), prata, 0, 0.16); topo.scale.y = 0.75;
      g.add(topo, malha(new THREE.CylinderGeometry(0.64, 0.64, 0.06, 40), azulClaro, 0, 0.12),
        malha(new THREE.CylinderGeometry(0.6, 0.6, 0.2, 40), azul, 0, -0.02), malha(new THREE.CylinderGeometry(0.56, 0.5, 0.2, 40), prata, 0, -0.24));
      return g;
    },
    barbearia() {    // tesoura
      const g = new THREE.Group();
      [0.42, -0.42].forEach((a, i) => {
        const lado = new THREE.Group(); lado.rotation.z = a;
        lado.add(malha(new THREE.BoxGeometry(0.95, 0.09, 0.06), prata, 0.32, 0), malha(new THREE.TorusGeometry(0.17, 0.05, 12, 32), azul, -0.32, 0));
        lado.position.z = i * 0.07; g.add(lado);
      });
      g.add(malha(new THREE.SphereGeometry(0.06, 16, 16), azulClaro, 0, 0, 0.1));
      return g;
    },
    salao() {        // secador
      const g = new THREE.Group();
      const corpo = malha(new THREE.CylinderGeometry(0.3, 0.3, 0.8, 32), azul, 0, 0.18); corpo.rotation.z = Math.PI / 2;
      const bico = malha(new THREE.CylinderGeometry(0.2, 0.28, 0.26, 32), prata, 0.52, 0.18); bico.rotation.z = Math.PI / 2;
      const tampa = malha(new THREE.CylinderGeometry(0.32, 0.32, 0.06, 32), prata, -0.42, 0.18); tampa.rotation.z = Math.PI / 2;
      const cabo = malha(new THREE.BoxGeometry(0.2, 0.62, 0.2), azul, -0.12, -0.36); cabo.rotation.z = 0.18;
      g.add(corpo, bico, tampa, cabo);
      return g;
    },
    consultorio() {  // cruz
      const g = new THREE.Group();
      g.add(malha(new THREE.BoxGeometry(0.36, 1.1, 0.28), azul), malha(new THREE.BoxGeometry(1.1, 0.36, 0.28), azul),
        malha(new THREE.BoxGeometry(0.2, 0.2, 0.3), azulClaro, 0, 0, 0.01));
      return g;
    },
    petshop() {      // pata
      const g = new THREE.Group();
      const almofada = malha(new THREE.SphereGeometry(0.34, 32, 16), prata, 0, -0.2); almofada.scale.set(1.25, 1, 0.55); g.add(almofada);
      [[-0.46, 0.18], [-0.17, 0.42], [0.17, 0.42], [0.46, 0.18]].forEach(([x, y]) => {
        const dedo = malha(new THREE.SphereGeometry(0.15, 24, 12), azul, x, y); dedo.scale.z = 0.6; g.add(dedo);
      });
      return g;
    },
    empresa() {      // prédio
      const g = new THREE.Group();
      g.add(malha(new THREE.BoxGeometry(0.66, 1.15, 0.5), prata), malha(new THREE.BoxGeometry(0.72, 0.07, 0.56), azul, 0, 0.6));
      for (let l = 0; l < 4; l++) for (let k = 0; k < 2; k++) g.add(malha(new THREE.BoxGeometry(0.16, 0.14, 0.04), azulClaro, -0.14 + k * 0.28, 0.36 - l * 0.26, 0.26));
      return g;
    },
  };
  const icones = new THREE.Group(); icones.visible = false; scene.add(icones);
  const icone = {};
  for (const id in FORMAS) { icone[id] = FORMAS[id](); icone[id].visible = false; icones.add(icone[id]); }
  let segAtivo = palcoSeg?.getAttribute("data-seg-ativo") || "lanchonete", giro = 0;
  if (icone[segAtivo]) icone[segAtivo].visible = true;
  document.addEventListener("segmento-troca", (e) => {
    if (!icone[e.detail]) return;
    icone[segAtivo].visible = false; segAtivo = e.detail; icone[segAtivo].visible = true;
    giro = Math.PI * 2;                                       // gira uma volta ao trocar de segmento
  });

  // ---------- layout: o K fica onde o CSS reservou (.hero-k) ----------
  // No computador, à direita do texto; no celular, em cima dele.
  const reservaHero = hero.querySelector(".hero-k") || palcoHero;
  let base = { x: 0, y: 0, s: 1 }, espalhar = 1, largoAgora = true;
  function ajustar() {
    const w = palco.clientWidth, h = palco.clientHeight;
    if (!w || !h) return;
    const largo = innerWidth >= 1000;
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, fraco || !largo ? 1.5 : 2));
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const visH = 2 * camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const porPx = visH / h;                                    // unidades do mundo por pixel (no plano z = 0)
    if (modo === "icone") {                                  // o ícone ocupa ~62% do palco pequeno
      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
      const visH2 = 2 * camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
      base = { x: 0, y: 0, s: (Math.min(w, h) * 0.62 * (visH2 / h)) / 1.3 };
      return;
    }
    const reserva = modo === "hero" ? reservaHero : palco;
    const caixa = reserva.getBoundingClientRect(), p = palco.getBoundingClientRect();
    const cx = caixa.left + caixa.width / 2 - p.left, cy = caixa.top + caixa.height / 2 - p.top;
    const larguraK = modo === "hero"                           // o K com a órbita mede ~5,2 unidades
      ? Math.min(caixa.width * (largo ? 0.95 : 0.9), caixa.height * 1.9)
      : Math.min(caixa.width * 0.8, caixa.height * 1.55);
    base = { x: (cx - w / 2) * porPx, y: (h / 2 - cy) * porPx, s: (larguraK * porPx) / 5.2 };
    espalhar = largo ? 1 : 0.8; largoAgora = largo;
    cartoes.forEach((s) => { const k = largo ? 1 : 1.35; s.scale.set(1.9 * k, 0.475 * k, 1); });   // no celular o K é menor: os cartões compensam para dar para ler
  }

  // ---------- entrada: mouse, toque e rolagem ----------
  const alvo = { x: 0, y: 0 }, atual = { x: 0, y: 0 };
  addEventListener("pointermove", (e) => { alvo.x = (e.clientX / innerWidth - .5) * 2; alvo.y = (e.clientY / innerHeight - .5) * 2; }, { passive: true });
  let rolagem = 0, rolagemSuave = 0;
  const medirRolagem = () => { rolagem = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight); };
  addEventListener("scroll", medirRolagem, { passive: true });
  addEventListener("resize", ajustar);
  if ("ResizeObserver" in window) { const ro = new ResizeObserver(() => ajustar()); [palcoHero, palcoFluxo, palcoSeg].forEach((p) => p && ro.observe(p)); }

  // ---------- quando e onde desenhar: no palco que está na tela, com a aba visível ----------
  let visivel = true, pronto = false;
  const naTela = new Map();
  function marcarPronto(sim) {
    if (palco === palcoHero) hero.classList.toggle("hero-3d-pronto", sim);
    else palco.classList.toggle("palco-3d-pronto", sim);
  }
  function escolher() {
    const alvoP = naTela.get(palcoFluxo) ? palcoFluxo : naTela.get(palcoSeg) ? palcoSeg : naTela.get(palcoHero) ? palcoHero : null;
    if (alvoP && alvoP !== palco) {
      marcarPronto(false);
      palco = alvoP; modo = alvoP === palcoHero ? "hero" : alvoP === palcoSeg ? "icone" : "fluxo";
      palco.appendChild(canvas);
      estacoes.forEach((m) => { m.visible = modo === "fluxo"; });
      cartoes.forEach((s) => { s.visible = modo === "hero"; });
      raiz.visible = particulas.visible = modo !== "icone";
      icones.visible = modo === "icone";
      ajustar();
      if (pronto) marcarPronto(true);
    }
    visivel = !!alvoP; ligar();
  }
  const io = new IntersectionObserver((es) => { es.forEach((e) => naTela.set(e.target, e.isIntersecting)); escolher(); });
  [palcoHero, palcoFluxo, palcoSeg].forEach((p) => p && io.observe(p));
  document.addEventListener("visibilitychange", ligar);
  function ligar() { renderer.setAnimationLoop(visivel && !document.hidden ? quadro : null); anterior = performance.now(); }

  // ---------- aparelho fraco: mede o FPS entre 0,6 s e 2,6 s depois do primeiro quadro ----------
  let quadros = 0, inicioMedida = 0, medindo = true, primeiro = 0;

  // ---------- animação ----------
  let angulo = -0.12, t = 0, anterior = performance.now();
  function quadro(agora) {
    const dt = Math.min(0.05, (agora - anterior) / 1000); anterior = agora;
    t += dt;

    if (!primeiro) { primeiro = agora; pronto = true; marcarPronto(true); }
    if (medindo && agora - primeiro > 600) {
      if (!inicioMedida) inicioMedida = agora;
      quadros++;
      const passou = agora - inicioMedida;
      if (passou > 2000) {
        medindo = false;
        if ((quadros * 1000) / passou < 30) { desistir(canvas, renderer); return; }
      }
    }

    const k = 1 - Math.pow(0.001, dt);                       // suavização independente do FPS
    atual.x += (alvo.x - atual.x) * k; atual.y += (alvo.y - atual.y) * k;
    rolagemSuave += (rolagem - rolagemSuave) * k;

    if (modo === "icone") {                                   // só o ícone do segmento: balança devagar e gira ao trocar
      giro *= Math.pow(0.02, dt);
      icones.scale.setScalar(base.s);
      icones.rotation.set(0.22 + atual.y * 0.12, Math.sin(t * 0.6) * 0.35 + atual.x * 0.2 + giro, 0);
      icones.position.y = Math.sin(t * 0.9) * 0.03;
      renderer.render(scene, camera);
      return;
    }

    raiz.position.set(base.x, base.y + Math.sin(t * 0.8) * 0.06, 0);
    raiz.scale.setScalar(base.s);
    if (modo === "hero") {
      raiz.rotation.y = atual.x * 0.45 + Math.sin(t * 0.5) * 0.12 + rolagemSuave * Math.PI * 2;   // uma volta na página inteira
      raiz.rotation.x = atual.y * 0.25 + Math.sin(t * 0.4) * 0.04;
      angulo += dt * 0.7;
    } else {
      // fluxo: o K fica de frente e o ponto viaja pelo caminho mais curto até a estação do passo atual
      raiz.rotation.y = atual.x * 0.3 + Math.sin(t * 0.5) * 0.1;
      raiz.rotation.x = atual.y * 0.2 + 0.08;
      const destino = ANGULOS[etapa - 1], d = Math.atan2(Math.sin(destino - angulo), Math.cos(destino - angulo));
      angulo += d * (1 - Math.pow(0.03, dt));
      estacoes.forEach((m, i) => {
        m.material.color.copy(i < etapa - 1 ? corAcesa : i === etapa - 1 ? corAtual : corApagada);
        m.scale.setScalar(i === etapa - 1 ? 1.35 : 1);
      });
    }
    impulso *= Math.pow(0.15, dt);
    halo.scale.setScalar(260 + impulso * 220);                // o brilho do ponto cresce quando um passo começa
    ponto.position.set(Math.cos(angulo) * R, Math.sin(angulo) * R, 0);

    const somem = THREE.MathUtils.clamp(1 - rolagemSuave * 8, 0, 1);   // os cartões somem ao rolar
    cartoes.forEach((s) => {
      const [x, y, z] = largoAgora ? s.userData.p : s.userData.cel, f = s.userData.fase;   // no celular, posições próprias para não se sobreporem
      s.position.set(x * (largoAgora ? espalhar : 1), y + Math.sin(t * 0.9 + f) * 0.09, z);
      s.material.opacity = somem;
    });
    particulas.rotation.y = t * 0.02 + atual.x * 0.05;

    renderer.render(scene, camera);
  }

  medirRolagem();
  ajustar();
  ligar();
}

// texturas desenhadas em canvas (sem baixar imagens)
function texturaHalo() {
  const cv = document.createElement("canvas"); cv.width = cv.height = 128;
  const g = cv.getContext("2d"), grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  grad.addColorStop(0, "rgba(63,180,255,.9)"); grad.addColorStop(.3, "rgba(26,92,255,.35)"); grad.addColorStop(1, "rgba(26,92,255,0)");
  g.fillStyle = grad; g.fillRect(0, 0, 128, 128);
  return new THREE.CanvasTexture(cv);
}
function texturaCartao(texto, cor) {
  const cv = document.createElement("canvas"); cv.width = 640; cv.height = 160;
  const g = cv.getContext("2d");
  g.beginPath(); g.roundRect ? g.roundRect(6, 6, 628, 148, 40) : g.rect(6, 6, 628, 148);
  g.fillStyle = "rgba(20,24,34,.88)"; g.fill();
  g.lineWidth = 3; g.strokeStyle = "rgba(63,180,255,.45)"; g.stroke();
  g.beginPath(); g.arc(70, 80, 16, 0, Math.PI * 2); g.fillStyle = cor; g.fill();
  g.font = '600 40px "Mona Sans","Segoe UI",system-ui,sans-serif'; g.fillStyle = "#ECEEF4"; g.textBaseline = "middle";
  g.fillText(texto, 108, 83);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  return tex;
}
