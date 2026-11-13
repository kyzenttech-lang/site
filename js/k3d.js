// KYZENT — o K da marca em 3D (Three.js, carregado só nas páginas que mostram o K).
// As três peças vêm do SVG oficial (empresa/logo-kyzent/camisas/svg/k-cor-fundo-escuro.svg),
// extrudadas com borda arredondada, com os degradês da marca e a órbita como um anel de verdade.
import * as THREE from "../assets/vendor/three/three.module.min.js";
import { SVGLoader } from "../assets/vendor/three/SVGLoader.js";
import { RoomEnvironment } from "../assets/vendor/three/RoomEnvironment.js";

const PECAS = [
  { // perna: azul -> branco -> prata, da esquerda para a direita
    d: "M228 507 L338 352 C360 322 384 306 422 305 L585 305 C625 305 652 322 676 345 L870 515 L655 515 L530 403 C520 395 508 392 496 392 L455 392 C442 392 432 396 424 403 L312 507 Z",
    cor: (x) => grad((x - 228) / (870 - 228), [[0, "#0A3DFF"], [.3, "#1A5CFF"], [.55, "#F4F7FB"], [1, "#8E9AAE"]]),
    metal: .55, aspereza: .18,
  },
  { // braço: azul escuro embaixo -> azul claro em cima
    d: "M400 282 C470 232 560 150 620 100 C652 72 684 58 724 58 L866 58 L702 222 C690 232 668 238 640 238 L482 240 C452 242 426 258 400 282 Z",
    cor: (x, y) => grad(((x - 400) / 466 + (282 - y) / 224) / 2, [[0, "#0A3DFF"], [1, "#3FB4FF"]]),
    metal: .25, aspereza: .14,
  },
  { // lâmina: prata
    d: "M390 80 L388 225 L237 372 L237 235 Z",
    cor: (x, y) => grad(((x - 237) / 153 + (y - 80) / 292) / 2, [[0, "#F4F7FB"], [1, "#8E9AAE"]]),
    metal: .9, aspereza: .12,
  },
];
const CENTRO = { x: 549, y: 286 };
const FOLGA = 1.6;   // a tela de desenho tem 160% do tamanho da caixa do K

function grad(t, paradas) {
  t = Math.min(1, Math.max(0, t));
  for (let i = 1; i < paradas.length; i++) {
    if (t <= paradas[i][0]) {
      const [t0, c0] = paradas[i - 1], [t1, c1] = paradas[i];
      return new THREE.Color(c0).lerp(new THREE.Color(c1), (t - t0) / (t1 - t0 || 1));
    }
  }
  return new THREE.Color(paradas[paradas.length - 1][1]);
}

function brilhoTextura() {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const g = c.getContext("2d"), r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(.25, "rgba(143,211,255,.9)"); r.addColorStop(1, "rgba(26,92,255,0)");
  g.fillStyle = r; g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

function montar(caixa) {
  const semMovimento = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const celular = innerWidth < 760;
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, celular ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1.05;
  caixa.appendChild(renderer.domElement);

  const cena = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  cena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(28, 1, 10, 10000);
  camera.position.set(0, 0, 2300);

  // luzes: chave branca de cima, contraluz azul atrás e um preenchimento ciano
  const chave = new THREE.DirectionalLight(0xffffff, 2.2); chave.position.set(-600, 900, 1200); cena.add(chave);
  const contra = new THREE.PointLight(0x1a5cff, 6, 0, 0); contra.position.set(700, -200, -700); cena.add(contra);
  const fill = new THREE.PointLight(0x3fb4ff, 3, 0, 0); fill.position.set(-900, -400, 600); cena.add(fill);

  const k = new THREE.Group(); cena.add(k);
  const loader = new SVGLoader();
  const seg = celular ? 14 : 28;
  PECAS.forEach((p) => {
    const dados = loader.parse(`<svg xmlns="http://www.w3.org/2000/svg"><path d="${p.d}"/></svg>`);
    const formas = SVGLoader.createShapes(dados.paths[0]);
    const geo = new THREE.ExtrudeGeometry(formas, { depth: 90, bevelEnabled: true, bevelThickness: 14, bevelSize: 10, bevelSegments: celular ? 4 : 8, curveSegments: seg });
    // cor de cada vértice pelo degradê da marca (coordenadas originais do SVG)
    const pos = geo.attributes.position, cores = new Float32Array(pos.count * 3);
    for (let i = 0; i < pos.count; i++) {
      const c = p.cor(pos.getX(i), pos.getY(i)); cores.set([c.r, c.g, c.b], i * 3);
    }
    geo.setAttribute("color", new THREE.BufferAttribute(cores, 3));
    geo.translate(-CENTRO.x, -CENTRO.y, -45);
    geo.scale(1, -1, -1);          // o SVG tem o eixo y para baixo
    geo.computeVertexNormals();
    const mat = new THREE.MeshPhysicalMaterial({ vertexColors: true, metalness: p.metal, roughness: p.aspereza, clearcoat: 1, clearcoatRoughness: .06, envMapIntensity: .95 });
    k.add(new THREE.Mesh(geo, mat));
  });

  // a órbita do logo: um anel de verdade, inclinado como no símbolo, com o ponto de luz girando
  const orbita = new THREE.Group();
  orbita.rotation.z = THREE.MathUtils.degToRad(24);
  const inclinacao = new THREE.Group(); inclinacao.rotation.x = THREE.MathUtils.degToRad(73);
  orbita.add(inclinacao); k.add(orbita);
  const anel = new THREE.Mesh(
    new THREE.TorusGeometry(520, 10, 24, celular ? 160 : 260),
    new THREE.MeshPhysicalMaterial({ color: 0x2f8bff, emissive: 0x1a5cff, emissiveIntensity: .5, metalness: .5, roughness: .2, clearcoat: 1, envMapIntensity: .6 })
  );
  inclinacao.add(anel);
  const ponto = new THREE.Group();
  const bola = new THREE.Mesh(new THREE.SphereGeometry(26, 32, 32), new THREE.MeshPhysicalMaterial({ color: 0xbfe6ff, emissive: 0x3fb4ff, emissiveIntensity: 1.4, roughness: .1 }));
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: brilhoTextura(), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
  halo.scale.set(220, 220, 1);
  ponto.add(bola, halo); inclinacao.add(ponto);

  // tamanho
  const ajustar = () => {
    // a tela de desenho é maior que a caixa (veja o CSS), para o brilho e o anel nunca baterem na borda
    const tela = renderer.domElement, w = tela.clientWidth || caixa.clientWidth, h = tela.clientHeight || w;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const raio = 560 * FOLGA, dist = raio / Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) / Math.min(1, camera.aspect);
    camera.position.z = dist * .8;
  };
  ajustar();
  new ResizeObserver(ajustar).observe(caixa);

  // cursor: o K vira na direção dele
  const alvo = { x: 0, y: 0 }, atual = { x: 0, y: 0 };
  if (matchMedia("(pointer: fine)").matches && !semMovimento) {
    addEventListener("pointermove", (e) => { alvo.x = e.clientX / innerWidth - .5; alvo.y = e.clientY / innerHeight - .5; }, { passive: true });
  }

  let visivel = true, a = 1.1;
  new IntersectionObserver((es) => { visivel = es[0].isIntersecting; }).observe(caixa);
  const relogio = new THREE.Clock();
  const quadro = () => {
    const t = relogio.getElapsedTime();
    atual.x += (alvo.x - atual.x) * .05; atual.y += (alvo.y - atual.y) * .05;
    k.rotation.y = -0.2 + Math.sin(t * .45) * .2 + atual.x * .6;
    k.rotation.x = 0.08 + Math.sin(t * .32) * .06 + atual.y * .4;
    k.position.y = Math.sin(t * .8) * 14;
    a += .012;
    ponto.position.set(Math.cos(a) * 520, Math.sin(a) * 520, 0);
    renderer.render(cena, camera);
  };
  if (semMovimento) { k.rotation.y = -0.2; ponto.position.set(Math.cos(a) * 520, Math.sin(a) * 520, 0); renderer.render(cena, camera); }
  else renderer.setAnimationLoop(() => { if (visivel && !document.hidden) quadro(); });
  caixa.classList.add("k3d-pronto");
}

document.querySelectorAll("[data-k3d]").forEach((caixa) => {
  try { montar(caixa); } catch (e) { caixa.classList.add("k3d-sem-webgl"); }   // sem WebGL fica a imagem do logo
});
