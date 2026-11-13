// KYZENT — hero 3D do Início (a partir do protótipo kyzent-hero-3d.html).
// O K da logo extrudado dos paths do SVG oficial, a órbita como anel 3D com o ponto azul,
// três cartões de notificação e partículas. Um único renderer WebGL: ele fica no topo e,
// nas etapas seguintes, outras cenas (fluxo, segmentos) podem pedir o mesmo canvas.
//
// Carregado por js/main.js com import dinâmico, depois da página aberta.
// Enquanto isso (e se der errado) fica a imagem do K (.hero-poster) no mesmo lugar.
import * as THREE from "../assets/vendor/three/three.module.min.js";
import { SVGLoader } from "../assets/vendor/three/SVGLoader.js";
import { RoomEnvironment } from "../assets/vendor/three/RoomEnvironment.js";

const palco = document.querySelector("[data-hero-palco]");
const hero = palco && palco.closest("[data-hero]");
if (palco && hero) iniciar();

function desistir(canvas, renderer) {
  // volta para a imagem parada (sem WebGL ou aparelho lento)
  document.documentElement.classList.add("sem-3d");
  hero?.classList.remove("hero-3d-pronto");
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

  // ---------- layout: o K fica onde o CSS reservou (.hero-k) ----------
  // No computador, à direita do texto; no celular, em cima dele.
  const reserva = hero.querySelector(".hero-k") || palco;
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
    const caixa = reserva.getBoundingClientRect(), p = palco.getBoundingClientRect();
    const cx = caixa.left + caixa.width / 2 - p.left, cy = caixa.top + caixa.height / 2 - p.top;
    const larguraK = Math.min(caixa.width * (largo ? 0.95 : 0.9), caixa.height * 1.9);   // o K com a órbita mede ~5,2 unidades
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
  if ("ResizeObserver" in window) new ResizeObserver(ajustar).observe(palco);

  // ---------- quando desenhar: só com o topo na tela e a aba visível ----------
  let visivel = true;
  new IntersectionObserver((es) => { visivel = es[0].isIntersecting; ligar(); }).observe(palco);
  document.addEventListener("visibilitychange", ligar);
  function ligar() { renderer.setAnimationLoop(visivel && !document.hidden ? quadro : null); anterior = performance.now(); }

  // ---------- aparelho fraco: mede o FPS entre 0,6 s e 2,6 s depois do primeiro quadro ----------
  let quadros = 0, inicioMedida = 0, medindo = true, primeiro = 0;

  // ---------- animação ----------
  let angulo = -0.12, t = 0, anterior = performance.now();
  function quadro(agora) {
    const dt = Math.min(0.05, (agora - anterior) / 1000); anterior = agora;
    t += dt;

    if (!primeiro) { primeiro = agora; hero.classList.add("hero-3d-pronto"); }
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

    raiz.position.set(base.x, base.y + Math.sin(t * 0.8) * 0.06, 0);
    raiz.scale.setScalar(base.s);
    raiz.rotation.y = atual.x * 0.45 + Math.sin(t * 0.5) * 0.12 + rolagemSuave * Math.PI * 2;   // uma volta na página inteira
    raiz.rotation.x = atual.y * 0.25 + Math.sin(t * 0.4) * 0.04;

    angulo += dt * 0.7;
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
