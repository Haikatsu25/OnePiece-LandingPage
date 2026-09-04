"use client";

import { useEffect, useRef, useState, useCallback } from "react";

/* ================= SVG: sombrero de paja de Luffy ================= */
function StrawHat({ width = 120, uid = "a" }) {
  return (
    <svg width={width} viewBox="0 0 120 66" xmlns="http://www.w3.org/2000/svg" style={{ overflow: "visible", verticalAlign: "middle" }}>
      <defs>
        <linearGradient id={`straw${uid}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#fce9a6" /><stop offset="1" stopColor="#e0b04a" />
        </linearGradient>
        <linearGradient id={`brim${uid}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#f7d87f" /><stop offset="1" stopColor="#c98f2e" />
        </linearGradient>
      </defs>
      <ellipse cx="60" cy="50" rx="57" ry="13" fill={`url(#brim${uid})`} stroke="#8a5a12" strokeWidth="2.5" />
      <path d="M30 50 Q30 10 60 10 Q90 10 90 50 Z" fill={`url(#straw${uid})`} stroke="#8a5a12" strokeWidth="2.5" />
      <path d="M30 50 Q60 42 90 50 L90 41 Q60 33 30 41 Z" fill="#d0342c" stroke="#8a2019" strokeWidth="1.5" />
      <path d="M38 24 Q60 18 82 24" fill="none" stroke="#c49435" strokeWidth="1.5" opacity=".7" />
      <path d="M34 33 Q60 26 86 33" fill="none" stroke="#c49435" strokeWidth="1.5" opacity=".7" />
    </svg>
  );
}

/* ================= partículas doradas flotantes ================= */
function Particles() {
  const ref = useRef(null);
  useEffect(() => {
    const canvas = ref.current;
    const ctx = canvas.getContext("2d");
    let w, h, raf;
    const dots = [];
    const resize = () => { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; };
    resize();
    window.addEventListener("resize", resize);
    for (let i = 0; i < 70; i++) {
      dots.push({
        x: Math.random() * window.innerWidth, y: Math.random() * window.innerHeight,
        r: Math.random() * 2 + 0.6, s: Math.random() * 0.45 + 0.08,
        o: Math.random() * 0.55 + 0.15, gold: Math.random() < 0.72, ph: Math.random() * Math.PI * 2,
      });
    }
    const tick = (t) => {
      ctx.clearRect(0, 0, w, h);
      for (const p of dots) {
        p.y -= p.s;
        p.x += Math.sin(t * 0.0006 + p.ph) * 0.35;
        if (p.y < -12) { p.y = h + 12; p.x = Math.random() * w; }
        const glow = 0.5 + 0.5 * Math.sin(t * 0.002 + p.ph);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, 7);
        ctx.fillStyle = p.gold
          ? `rgba(245, 197, 66, ${p.o * glow})`
          : `rgba(159, 198, 239, ${p.o * glow * 0.8})`;
        ctx.shadowBlur = 8; ctx.shadowColor = p.gold ? "#f5c542" : "#9fc6ef";
        ctx.fill();
        ctx.shadowBlur = 0;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", resize); };
  }, []);
  return <canvas ref={ref} className="particles" />;
}

/* ================= barra de progreso + navbar ================= */
function NavBar() {
  const barRef = useRef(null);
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      if (barRef.current) barRef.current.style.width = `${(window.scrollY / Math.max(max, 1)) * 100}%`;
      setScrolled(window.scrollY > 40);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <>
      <div className="progress" ref={barRef} />
      <nav className={`nav ${scrolled ? "scrolled" : ""}`}>
        <a className="nav-brand" href="#top"><StrawHat width={38} uid="nav" /> Grand Line</a>
        <ul className="nav-links">
          <li><a href="#tripulacion">Tripulación</a></li>
          <li><a href="#frutas">Frutas</a></li>
          <li><a href="#sagas">Sagas</a></li>
          <li><a href="#anime">Anime</a></li>
          <li><a href="#recompensas">Recompensas</a></li>
          <li><a href="#quiz">Quiz</a></li>
        </ul>
      </nav>
    </>
  );
}

/* ================= reveal on scroll ================= */
function useReveal() {
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
      { threshold: 0.12 }
    );
    document.querySelectorAll(".reveal").forEach((el) => obs.observe(el));
    return () => obs.disconnect();
  }, []);
}

/* ================= tilt 3D para carteles ================= */
function Tilt({ children, className = "", style }) {
  const ref = useRef(null);
  const onMove = useCallback((e) => {
    const el = ref.current; if (!el) return;
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    el.style.transform = `perspective(800px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg) translateY(-8px) scale(1.03)`;
    el.style.setProperty("--mx", `${(x + 0.5) * 100}%`);
    el.style.setProperty("--my", `${(y + 0.5) * 100}%`);
  }, []);
  const onLeave = useCallback(() => {
    const el = ref.current; if (!el) return;
    el.style.transform = "";
  }, []);
  return (
    <div ref={ref} className={className} style={style} onMouseMove={onMove} onMouseLeave={onLeave}>
      {children}
    </div>
  );
}

/* ================= contador animado ================= */
function CountUp({ value, duration = 1600 }) {
  const ref = useRef(null);
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    let raf, started = false;
    const obs = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !started) {
        started = true;
        const t0 = performance.now();
        const step = (t) => {
          const p = Math.min((t - t0) / duration, 1);
          const ease = 1 - Math.pow(1 - p, 3);
          setDisplay(Math.round(value * ease));
          if (p < 1) raf = requestAnimationFrame(step);
        };
        raf = requestAnimationFrame(step);
        obs.disconnect();
      }
    }, { threshold: 0.4 });
    obs.observe(el);
    return () => { cancelAnimationFrame(raf); obs.disconnect(); };
  }, [value, duration]);
  return <span ref={ref}>{display.toLocaleString("es-MX")}</span>;
}

/* ================= barra de recompensa (se llena al verse) ================= */
function BountyBar({ name, value, max }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        el.style.width = `${(value / max) * 100}%`;
        obs.disconnect();
      }
    }, { threshold: 0.5 });
    obs.observe(el);
    return () => obs.disconnect();
  }, [value, max]);
  return (
    <div className="bounty-row">
      <div className="blabel"><span>{name}</span><b>฿ <CountUp value={value} /></b></div>
      <div className="btrack"><div className="bfill" ref={ref} /></div>
    </div>
  );
}

/* ================= confeti ================= */
function fireConfetti() {
  const canvas = document.createElement("canvas");
  canvas.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:100;";
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  const colors = ["#f5c542", "#e07b39", "#d0342c", "#9fc6ef", "#fff3c4"];
  const parts = Array.from({ length: 160 }, () => ({
    x: canvas.width / 2 + (Math.random() - 0.5) * 260,
    y: canvas.height * 0.35,
    vx: (Math.random() - 0.5) * 13,
    vy: -Math.random() * 13 - 4,
    s: Math.random() * 7 + 4,
    c: colors[(Math.random() * colors.length) | 0],
    a: Math.random() * Math.PI,
    va: (Math.random() - 0.5) * 0.3,
  }));
  let frames = 0;
  const tick = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const p of parts) {
      p.x += p.vx; p.y += p.vy; p.vy += 0.32; p.a += p.va;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
      ctx.fillStyle = p.c; ctx.fillRect(-p.s / 2, -p.s / 2, p.s, p.s * 0.6);
      ctx.restore();
    }
    if (++frames < 150) requestAnimationFrame(tick);
    else canvas.remove();
  };
  tick();
}

/* ================= datos ================= */
const CREW = [
  { face: "hat", name: "Monkey D. Luffy", role: "Capitán · Futuro Rey de los Piratas", bounty: "3.000.000.000", fruit: "Gomu Gomu no Mi (Nika)" },
  { face: "⚔️", name: "Roronoa Zoro", role: "Espadachín · Estilo de tres espadas", bounty: "1.111.000.000", fruit: null },
  { face: "🍊", name: "Nami", role: "Navegante · Ladrona de mapas", bounty: "366.000.000", fruit: null },
  { face: "🎯", name: "Usopp", role: "Tirador · 'Dios' Usopp", bounty: "500.000.000", fruit: null },
  { face: "🍳", name: "Sanji", role: "Cocinero · Pierna Negra", bounty: "1.032.000.000", fruit: null },
  { face: "🦌", name: "Tony Tony Chopper", role: "Médico · Renito mascota(?)", bounty: "1.000", fruit: "Hito Hito no Mi" },
  { face: "🌸", name: "Nico Robin", role: "Arqueóloga · Niña demonio", bounty: "930.000.000", fruit: "Hana Hana no Mi" },
  { face: "🤖", name: "Franky", role: "Carpintero · ¡SUPER! Cyborg", bounty: "394.000.000", fruit: null },
  { face: "🎻", name: "Brook", role: "Músico · Rey del Soul", bounty: "383.000.000", fruit: "Yomi Yomi no Mi" },
  { face: "🐳", name: "Jinbe", role: "Timonel · Caballero del Mar", bounty: "1.100.000.000", fruit: null },
];

const FRUITS = [
  {
    emoji: "✨", type: "Tipo I", name: "Paramecia",
    front: "Poderes sobrehumanos que alteran el cuerpo o el entorno. Las más comunes… y las más impredecibles.",
    back: <>Cuerpos de goma, ondas de choque, hilos, gravedad… La <b>Ope Ope no Mi</b> llegó a valer 5.000 millones de berries: puede otorgar la juventud eterna a cambio de la vida del usuario.</>,
  },
  {
    emoji: "🐉", type: "Tipo II", name: "Zoan",
    front: "Transformación animal, humana o híbrida. Las míticas —fénix, dragones, dioses— son las más raras de todas.",
    back: <>Las Zoan tienen voluntad propia y hasta las armas pueden comerlas. La <b>Hito Hito no Mi: modelo Nika</b> pasó 800 años oculta bajo otro nombre por el Gobierno Mundial.</>,
  },
  {
    emoji: "🔥", type: "Tipo III", name: "Logia",
    front: "El usuario se convierte en un elemento natural: fuego, hielo, luz, oscuridad, magma…",
    back: <>Intangibles ante ataques normales: solo el <b>Haki</b> (o su debilidad natural) puede tocarlos. La <b>Yami Yami no Mi</b> es la única que anula los poderes ajenos con el tacto.</>,
  },
];

const SAGAS = [
  ["East Blue", "El comienzo · Cap. 1", "Un chico de goma con un sombrero de paja recluta a un espadachín, una ladrona, un mentiroso y un cocinero. Nace la leyenda."],
  ["Alabasta", "El reino de arena", "La tripulación cruza la Grand Line para salvar un reino de la guerra civil orquestada por Crocodile y Baroque Works."],
  ["Skypiea", "La isla del cielo", "Una isla en el cielo, un 'dios' con poder del rayo y una campana que suena tras 400 años."],
  ["Water 7 / Enies Lobby", "La declaración de guerra", "«¡Quiero vivir!» — Robin. Los Sombrero de Paja le declaran la guerra al Gobierno Mundial y queman su bandera."],
  ["Thriller Bark", "La isla fantasma", "Sombras robadas, un esqueleto caballeroso y la promesa de reencontrarse con una ballena en Cabo Gemelos."],
  ["Guerra de Marineford", "La cima de la guerra", "La guerra que cambió el mundo. La era de Barbablanca termina y Luffy pierde lo que más quería proteger."],
  ["Isla Gyojin", "Dos años después", "La tripulación se reúne más fuerte que nunca y desciende 10.000 metros bajo el mar hacia el Nuevo Mundo."],
  ["Dressrosa", "El coliseo de juguetes", "Un país de cuentos con un rey de hilos. La alianza pirata derriba a un Shichibukai y nace la Gran Flota."],
  ["Whole Cake Island", "El rescate de Sanji", "Té, bodas falsas y una Emperatriz del Mar. Luffy contra Katakuri: el duelo que despertó su Haki de Observación."],
  ["Wano", "El país de los samuráis", "Veinte años de espera, nueve fundas rojas y el despertar de Nika. Luffy se convierte en Emperador del Mar."],
  ["Egghead", "La isla del futuro", "El laboratorio del Dr. Vegapunk, secretos del Siglo Vacío y el inicio de la guerra final. El One Piece está cerca."],
];

const ANIME = [
  ["1997", "✒️", "Nace el manga", "Eiichiro Oda publica «Romance Dawn» en la Weekly Shōnen Jump. Nadie imaginaba que sería el manga más vendido de la historia."],
  ["1999", "📺", "¡Zarpa el anime!", "El 20 de octubre, Toei Animation estrena One Piece en Fuji TV. El opening «We Are!» se vuelve el himno de toda una generación."],
  ["2000", "🎬", "Primera película", "One Piece llega a los cines japoneses. Sería la primera de más de 15 películas de la franquicia."],
  ["2011", "⏳", "El salto temporal", "Tras Marineford, el anime da el salto de 2 años: nuevos diseños, nuevos poderes y el reencuentro más esperado."],
  ["2019", "🎆", "20.º aniversario", "Se estrena Stampede y arranca Wano, con una dirección de arte que revoluciona el estilo visual del anime."],
  ["2021", "💯", "Episodio 1000", "«¡Soy Monkey D. Luffy! ¡El hombre que se convertirá en el Rey de los Piratas!». Celebración mundial."],
  ["2022", "🎤", "Film: Red", "La película de Uta arrasa en taquilla y sus canciones dominan las listas musicales de Japón."],
  ["2023", "🔥", "Gear 5 y Netflix", "El episodio 1071 anima el despertar de Nika y colapsa el streaming. El live-action es n.º 1 en más de 80 países."],
  ["2025", "🌅", "THE ONE PIECE", "WIT Studio prepara el remake desde East Blue, mientras la serie original navega hacia su saga final."],
];

const BOUNTIES = [
  ["Gol D. Roger 👑", 5564800000],
  ["Edward Newgate 'Barbablanca' 🌊", 5046000000],
  ["Kaido de las Bestias 🐉", 4611100000],
  ["Big Mom 🍰", 4388000000],
  ["Shanks el Pelirrojo 🍶", 4048900000],
  ["Barbanegra ⚫", 3996000000],
  ["Monkey D. Luffy ☀️", 3000000000],
  ["Trafalgar Law 🩺", 3000000000],
  ["Eustass Kid ⚙️", 3000000000],
];

const QUIZ = [
  ["¿Cuál es el verdadero nombre de la fruta de Luffy?", ["Gomu Gomu no Mi", "Hito Hito no Mi: modelo Nika", "Nika Nika no Mi", "Sun Sun no Mi"], 1],
  ["¿Cuántas espadas usa Zoro en su estilo característico?", ["Una", "Dos", "Tres", "Cuatro"], 2],
  ["¿Quién fue el primer miembro en unirse a Luffy?", ["Nami", "Usopp", "Sanji", "Zoro"], 3],
  ["¿Cómo se llama la isla final donde espera el One Piece?", ["Raftel", "Laugh Tale", "Elbaf", "Mary Geoise"], 1],
  ["¿Qué promesa une a Shanks y Luffy?", ["Repartirse el tesoro", "Devolverle el sombrero de paja al convertirse en un gran pirata", "Hundir la Marina", "Encontrar a Roger"], 1],
];

/* ================= página ================= */
export default function Page() {
  useReveal();

  /* tu recompensa */
  const [danger, setDanger] = useState(42);
  const myBounty = Math.round(Math.pow(danger / 100, 2.2) * 5600000000);
  const rank =
    danger < 15 ? ["Grumete de East Blue", "🐣"] :
    danger < 40 ? ["Novato de la Grand Line", "⛵"] :
    danger < 65 ? ["Supernova de la Peor Generación", "💥"] :
    danger < 85 ? ["Comandante Yonko", "⚡"] : ["¡EMPERADOR DEL MAR!", "👑"];

  /* quiz */
  const [answers, setAnswers] = useState(Array(QUIZ.length).fill(null));
  const [result, setResult] = useState(null);
  const submitQuiz = () => {
    const score = QUIZ.reduce((acc, [, , correct], i) => acc + (answers[i] === correct ? 1 : 0), 0);
    const r =
      score === 5 ? ["¡REY DE LOS PIRATAS!", "👑", "Gol D. Roger estaría orgulloso. El One Piece es prácticamente tuyo."] :
      score >= 4 ? ["Yonko en ascenso", "⚡", "Los periódicos del mundo ya hablan de ti, Emperador."] :
      score >= 3 ? ["Supernova prometedor", "💥", "La Peor Generación te espera. ¡Sigue navegando!"] :
      score >= 1 ? ["Grumete con futuro", "⛵", "Todo pirata legendario empezó en un bote de remos."] :
      ["¿Marine infiltrado?", "🚨", "Ni Buggy lo haría peor… ¡pero Buggy llegó a Emperador!"];
    setResult({ score, title: r[0], icon: r[1], msg: r[2] });
    if (score >= 4) fireConfetti();
  };

  const maxBounty = BOUNTIES[0][1];

  return (
    <main id="top">
      <div className="aurora" />
      <Particles />
      <NavBar />

      {/* ===== HÉROE ===== */}
      <header className="hero">
        <div className="hero-stars">
          {[["10%", "8%", 0], ["20%", "18%", 0.7], ["8%", "38%", 1.4], ["16%", "62%", 0.3], ["7%", "82%", 1], ["28%", "91%", 1.8], ["34%", "4%", 2.2], ["40%", "73%", 0.9], ["48%", "12%", 1.6], ["52%", "88%", 2.4]].map(([t, l, d], i) => (
            <span key={i} style={{ top: t, left: l, animationDelay: `${d}s` }}>✦</span>
          ))}
        </div>
        <div className="hero-hat"><StrawHat width={150} uid="hero" /></div>
        <h1 className="hero-title">GRAND LINE</h1>
        <div className="hero-sub">· Un homenaje a One Piece ·</div>
        <p className="hero-quote">
          «¿Mi tesoro? Si lo queréis, es vuestro… ¡Buscadlo! ¡Lo dejé todo en <b>ese lugar</b>!»<br />
          — Gol D. Roger, el Rey de los Piratas
        </p>
        <div className="hero-pills">
          <span className="pill">🏴‍☠️ Sombrero de Paja</span>
          <span className="pill">🍈 Frutas del Diablo</span>
          <span className="pill">🗺️ 11 Sagas</span>
          <span className="pill">📺 Desde 1999</span>
        </div>
        <div className="hero-ship"><span>⛵</span></div>
        <a className="hero-scroll" href="#tripulacion" aria-label="Bajar">⌄</a>
        <div className="waves back">
          <svg viewBox="0 0 1200 110" preserveAspectRatio="none">
            <path d="M0,55 C150,95 300,15 450,55 C600,95 750,15 900,55 C1050,95 1200,15 1350,55 C1500,95 1650,15 1800,55 C1950,95 2100,15 2250,55 L2400,55 L2400,110 L0,110 Z" fill="#0d3358" />
          </svg>
        </div>
        <div className="waves">
          <svg viewBox="0 0 1200 110" preserveAspectRatio="none">
            <path d="M0,65 C160,105 320,25 480,65 C640,105 800,25 960,65 C1120,105 1280,25 1440,65 C1600,105 1760,25 1920,65 C2080,105 2240,25 2400,65 L2400,110 L0,110 Z" fill="#0a2440" />
          </svg>
        </div>
      </header>

      {/* ===== TRIPULACIÓN ===== */}
      <section className="block" id="tripulacion">
        <div className="reveal">
          <div className="divider"><span className="dtitle">Los Sombrero de Paja</span></div>
          <span className="dsub">Mugiwara no Ichimi</span>
          <p className="intro">Diez sueños, un solo barco. Mueve el cursor sobre cada cartel… si te atreves. 🏴‍☠️</p>
        </div>
        <div className="crew-grid">
          {CREW.map((c, i) => (
            <div className="reveal" style={{ transitionDelay: `${(i % 5) * 0.08}s` }} key={c.name}>
              <Tilt className="wanted">
                <div className="wtop">WANTED</div>
                <div className="wface">{c.face === "hat" ? <StrawHat width={66} uid={`c${i}`} /> : c.face}</div>
                <div className="wdead">DEAD OR ALIVE</div>
                <div className="wname">{c.name}</div>
                <div className="wrole">{c.role}</div>
                <div className="wbounty"><small>RECOMPENSA</small>฿ {c.bounty}</div>
                <div className="wfruit" style={c.fruit ? undefined : { opacity: 0.55 }}>
                  {c.fruit ? `🍈 ${c.fruit}` : "Sin fruta"}
                </div>
              </Tilt>
            </div>
          ))}
        </div>
      </section>

      {/* ===== FRUTAS ===== */}
      <section className="block" id="frutas">
        <div className="reveal">
          <div className="divider"><span className="dtitle">Frutas del Diablo</span></div>
          <span className="dsub">Akuma no Mi · El poder del mar tiene un precio</span>
          <p className="intro">Pasa el cursor sobre cada carta para voltearla y descubrir sus secretos. 🍈</p>
        </div>
        <div className="fruit-grid">
          {FRUITS.map((f, i) => (
            <div className="reveal" style={{ transitionDelay: `${i * 0.12}s` }} key={f.name}>
              <div className="flip">
                <div className="flip-inner">
                  <div className="flip-face front">
                    <div className="flip-emoji">{f.emoji}</div>
                    <div className="ftype">{f.type}</div>
                    <div className="fname">{f.name}</div>
                    <p>{f.front}</p>
                    <div className="fhint">— PASA EL CURSOR PARA GIRAR —</div>
                  </div>
                  <div className="flip-face back">
                    <div className="fname">{f.name}</div>
                    <p>{f.back}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="reveal" style={{ marginTop: "1.4rem" }}>
          <div className="panel" style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem" }}>🌊</span>
            <h4>La maldición del mar</h4>
            <p style={{ maxWidth: 720, margin: "0.4rem auto 0" }}>
              Quien muerde una Fruta del Diablo obtiene un poder extraordinario… pero el océano lo rechaza para siempre:
              los usuarios se hunden como martillos y el <b style={{ color: "var(--gold-soft)" }}>kairoseki</b> anula
              por completo sus habilidades.
            </p>
          </div>
        </div>
      </section>

      {/* ===== SAGAS ===== */}
      <section className="block" id="sagas">
        <div className="reveal">
          <div className="divider"><span className="dtitle">La Gran Travesía</span></div>
          <span className="dsub">De East Blue a la última isla</span>
        </div>
        <div className="sagas-wrap">
          <div className="timeline">
            {SAGAS.map(([name, meta, desc], i) => (
              <div className="tl-item reveal" style={{ transitionDelay: `${(i % 4) * 0.07}s` }} key={name}>
                <div className="tlmeta">{meta}</div>
                <h5>{i + 1}. {name}</h5>
                <p>{desc}</p>
              </div>
            ))}
          </div>
          <div className="side-stack">
            <div className="panel reveal">
              <span className="logpose">🧭</span>
              <h4>Log Pose</h4>
              <p>En la Grand Line las brújulas normales enloquecen. Solo un Log Pose puede guiarte de isla en isla…
                y solo el <b style={{ color: "var(--gold-soft)" }}>Road Poneglyph</b> ×4 revela Laugh Tale.</p>
            </div>
            <div className="panel reveal">
              <h4>📜 Cifras de leyenda</h4>
              <p>
                <span className="bignum"><CountUp value={1100} /></span>+ capítulos del manga<br />
                <span className="bignum"><CountUp value={1100} /></span>+ episodios del anime<br />
                <span className="bignum"><CountUp value={500} /></span>M+ copias vendidas<br />
                <span style={{ fontSize: "0.85rem", color: "var(--blue)" }}>El manga más vendido de la historia ✒️ Eiichiro Oda, desde 1997</span>
              </p>
            </div>
            <div className="panel reveal">
              <span style={{ fontSize: "2rem" }}>🔔</span>
              <h4>¿Sabías que…?</h4>
              <p>Oda prometió que el final de One Piece haría que la Guerra de Marineford «pareciera un juego de niños».</p>
            </div>
          </div>
        </div>
      </section>

      {/* ===== ANIME ===== */}
      <section className="block" id="anime">
        <div className="reveal">
          <div className="divider"><span className="dtitle">Historia del Anime</span></div>
          <span className="dsub">Más de 25 años navegando en la televisión</span>
        </div>
        <div className="anime-stats reveal">
          {[["📺", "1999", "Año de estreno"], ["🎞️", "1.100+", "Episodios emitidos"], ["🎬", "15", "Películas en cines"], ["🎵", "26", "Openings icónicos"]].map(([e, n, l]) => (
            <div className="astat" key={l}>
              <span className="semoji">{e}</span>
              <div className="snum">{n}</div>
              <div className="slab">{l}</div>
            </div>
          ))}
        </div>
        <div className="rail-hint reveal">← Desliza para navegar la historia →</div>
        <div className="anime-rail reveal">
          {ANIME.map(([year, icon, title, desc]) => (
            <article className="acard" key={year}>
              <div className="ayear">{year}</div>
              <div className="abadge">{icon}</div>
              <div className="ayearlab">{year}</div>
              <h6>{title}</h6>
              <p>{desc}</p>
            </article>
          ))}
        </div>
        <div className="reveal" style={{ marginTop: "0.6rem" }}>
          <div className="panel" style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem" }}>🎶</span>
            <h4>«¡Arittake no yume o kakiatsume!»</h4>
            <p style={{ maxWidth: 700, margin: "0.4rem auto 0" }}>
              Del «We Are!» original al «UUUUUS!» de la saga final, cada opening marca una era.
              Millones de fans no pueden escuchar los primeros acordes sin que se les ponga la piel de gallina.
            </p>
          </div>
        </div>
      </section>

      {/* ===== RECOMPENSAS ===== */}
      <section className="block" id="recompensas">
        <div className="reveal">
          <div className="divider"><span className="dtitle">Las Mayores Recompensas</span></div>
          <span className="dsub">Los monstruos que gobiernan los mares</span>
        </div>
        <div className="panel bounty-panel reveal">
          {BOUNTIES.map(([name, value]) => (
            <BountyBar key={name} name={name} value={value} max={maxBounty} />
          ))}
          <div className="bnote">฿ = Berries · Recompensas conocidas hasta la saga de Egghead</div>
        </div>

        <div className="yourb reveal">
          <h3>⚖️ ¿CUÁNTO VALDRÍA TU CABEZA?</h3>
          <input
            type="range" min="0" max="100" value={danger} className="gold-slider"
            style={{ "--fill": `${danger}%` }}
            onChange={(e) => setDanger(Number(e.target.value))}
          />
          <Tilt className="wanted mini">
            <div className="wtop">WANTED</div>
            <div className="wface">{rank[1]}</div>
            <div className="wdead">DEAD OR ALIVE</div>
            <div className="wname">Tú, nakama</div>
            <div className="wrole">{rank[0]}</div>
            <div className="wbounty"><small>RECOMPENSA</small>฿ {myBounty.toLocaleString("es-MX")}</div>
          </Tilt>
        </div>
      </section>

      {/* ===== QUIZ ===== */}
      <section className="block" id="quiz">
        <div className="reveal">
          <div className="divider"><span className="dtitle">Pon a prueba tu Haki</span></div>
          <span className="dsub">5 preguntas · Solo un verdadero nakama las supera</span>
        </div>
        <div className="quiz-wrap">
          {QUIZ.map(([q, opts], qi) => (
            <div className="qq reveal" key={qi}>
              <h5>{qi + 1}. {q}</h5>
              <div className="opts">
                {opts.map((opt, oi) => (
                  <button
                    key={oi}
                    className={`opt ${answers[qi] === oi ? "sel" : ""}`}
                    onClick={() => {
                      setAnswers((prev) => {
                        const next = [...prev]; next[qi] = oi; return next;
                      });
                      setResult(null);
                    }}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>
          ))}
          <button className="btn-gold reveal" onClick={submitQuiz}>⚓ ¡ZARPAR CON MIS RESPUESTAS!</button>
          {result && (
            <div className="panel quiz-result">
              <div className="qr-icon">{result.icon}</div>
              <div className="qr-title">{result.title}</div>
              <div className="qr-score">{result.score} / 5 ACIERTOS</div>
              <p>{result.msg}</p>
              <button
                className="btn-gold"
                style={{ maxWidth: 320, margin: "1.1rem auto 0" }}
                onClick={() => { setAnswers(Array(QUIZ.length).fill(null)); setResult(null); }}
              >
                🔄 INTENTAR DE NUEVO
              </button>
            </div>
          )}
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="footer">
        <div style={{ fontSize: "2.2rem", marginBottom: "0.4rem" }}>🏴‍☠️</div>
        <div className="fquote">«El One Piece… ¡existe!»</div>
        <div className="fsub">— Edward Newgate, Barbablanca. Sus últimas palabras encendieron la Gran Era Pirata.</div>
        <div className="fnote">Página fan sin ánimo de lucro · One Piece © Eiichiro Oda / Shueisha · Hecha con ❤️ y Next.js</div>
      </footer>
    </main>
  );
}
