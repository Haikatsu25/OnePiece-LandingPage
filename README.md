# 🏴‍☠️ Grand Line — One Piece Landing Page

Página fan interactiva de One Piece hecha con **Next.js + React** y un backend en **Python (FastAPI)** con IA.

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
- 🤖 **Chat Nakama con IA**: habla con Luffy, Chopper o Zoro

## 🧠 La IA

El chat usa un backend en Python ([api/index.py](api/index.py)) que funciona con
**el primer proveedor cuya clave encuentre**:

| Variable de entorno | Proveedor | Modelo | Costo |
|---|---|---|---|
| `GEMINI_API_KEY` | Google Gemini | `gemini-2.5-flash` | Capa gratuita ([aistudio.google.com](https://aistudio.google.com/apikey)) |
| `ANTHROPIC_API_KEY` | API de Claude | `claude-opus-5` | De pago ([console.anthropic.com](https://console.anthropic.com)) |

La clave vive **solo en el servidor**, nunca llega al navegador.

## 🚀 Ejecutar en local

**Frontend** (terminal 1):

```bash
npm install
npm run dev
```

**Backend con IA** (terminal 2, desde la raíz del proyecto):

```bash
pip install -r requirements.txt
$env:GEMINI_API_KEY = "tu-clave"        # PowerShell (Linux/macOS: export GEMINI_API_KEY=...)
uvicorn api.index:app --port 8000
```

Abre [http://localhost:3000](http://localhost:3000). En desarrollo, Next.js redirige
`/api/py/*` al FastAPI local (ver [next.config.mjs](next.config.mjs)).

> En Windows PowerShell, si `npm` da error de política de ejecución usa `npm.cmd`.

## ☁️ Desplegar en Vercel (gratis)

1. Sube el repo a GitHub.
2. Entra a [vercel.com](https://vercel.com), inicia sesión con GitHub y pulsa **Add New → Project**.
3. Importa el repositorio `OnePiece-LandingPage` (detecta Next.js solo; no cambies nada).
4. En **Environment Variables** agrega `GEMINI_API_KEY` con tu clave de [aistudio.google.com](https://aistudio.google.com/apikey).
5. Pulsa **Deploy**. En un minuto tendrás una URL pública para compartir. 🎉

Vercel construye el frontend Next.js **y** convierte `api/index.py` en una función
serverless de Python automáticamente — un solo deploy para todo.

## 🛠️ Stack

- [Next.js 15](https://nextjs.org) (App Router) + React 19
- CSS puro (sin frameworks) — todas las animaciones son hechas a mano
- [FastAPI](https://fastapi.tiangolo.com) + Gemini / Claude para el chat con IA

---

Página fan sin ánimo de lucro · One Piece © Eiichiro Oda / Shueisha
