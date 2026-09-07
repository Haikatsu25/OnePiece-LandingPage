# 🏴‍☠️ Grand Line — One Piece Landing Page

Página fan interactiva de One Piece hecha con **Next.js + React**.

## ✨ Características

- 🌌 Fondo aurora animado con partículas doradas (canvas)
- 👒 Sombrero de paja de Luffy dibujado en SVG
- 🃏 Carteles **WANTED** de los 10 Mugiwara con inclinación 3D que sigue el cursor
- 🍈 Cartas de Frutas del Diablo que se voltean en 3D
- 🗺️ Línea de tiempo de las 11 sagas con animaciones al hacer scroll
- 📺 Historia del anime en carrusel horizontal deslizable
- 💰 Ranking de recompensas con contadores animados
- ⚖️ Calculadora de "tu recompensa" con cartel personalizado
- 🧭 Quiz interactivo con lluvia de confeti
- 🤖 **Chat Nakama con IA**: habla con Luffy, Chopper o Zoro (backend en Python + API de Claude)

## 🚀 Cómo ejecutar

### 1. Frontend (Next.js)

```bash
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000).

> En Windows PowerShell, si `npm` da error de política de ejecución usa `npm.cmd`.

### 2. Backend con IA (Python) — opcional

El chat flotante usa un backend en **FastAPI** que llama a la **API de Claude**.
La página funciona sin él; solo el chat lo necesita.

```bash
cd backend
pip install -r requirements.txt
```

Configura tu clave de [console.anthropic.com](https://console.anthropic.com) (la clave vive
solo en el servidor, nunca en el navegador):

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "tu-clave"

# Linux / macOS
export ANTHROPIC_API_KEY="tu-clave"
```

Y arranca el servidor:

```bash
uvicorn main:app --port 8000
```

Endpoints: `POST /api/chat` (conversación con personaje), `GET /api/personajes`, `GET /api/salud`.

## 🛠️ Stack

- [Next.js 15](https://nextjs.org) (App Router) + React 19
- CSS puro (sin frameworks) — todas las animaciones son hechas a mano
- [FastAPI](https://fastapi.tiangolo.com) + [SDK de Anthropic](https://docs.claude.com) para el chat con IA

---

Página fan sin ánimo de lucro · One Piece © Eiichiro Oda / Shueisha
