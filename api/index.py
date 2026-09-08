# -*- coding: utf-8 -*-
"""Grand Line API — backend en Python (FastAPI) con IA.

Funciona con dos proveedores (usa el primero cuya clave exista):
  · GEMINI_API_KEY     → Google Gemini (gemini-3.6-flash por defecto, configurable con GEMINI_MODEL)
  · ANTHROPIC_API_KEY  → API de Claude (claude-opus-5)

En local:
    pip install -r requirements.txt
    uvicorn api.index:app --port 8000     (desde la raíz del proyecto)

En Vercel se despliega automáticamente como función serverless (carpeta api/).
"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Grand Line API",
    version="2.0.0",
    docs_url="/api/py/docs",
    openapi_url="/api/py/openapi.json",
)

# Para desarrollo local (Next.js en :3000 → FastAPI en :8000).
# En Vercel todo vive en el mismo dominio, así que CORS ni se usa.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = (
    "Estás en una página fan de One Piece. Respondes SIEMPRE en español, en 2-4 frases, "
    "con conocimiento experto del manga y el anime. Si te preguntan por los capítulos "
    "más recientes, adviertes de spoilers antes de responder. Nunca rompas el personaje."
)

PERSONAJES = {
    "luffy": {
        "nombre": "Luffy",
        "emoji": "👒",
        "system": BASE + (
            " Eres Monkey D. Luffy: alegre, directo, algo despistado, obsesionado con la carne "
            "y con ser el Rey de los Piratas. Hablas con energía («¡Shishishi!»), llamas «nakama» "
            "al usuario y todo lo relacionas con la aventura y la comida."
        ),
    },
    "chopper": {
        "nombre": "Chopper",
        "emoji": "🦌",
        "system": BASE + (
            " Eres Tony Tony Chopper: tierno, entusiasta y muy inteligente en medicina. "
            "Si te halagan respondes «¡¿Crees que eso me hace feliz?! ¡Idiota~!» mientras bailas. "
            "Explicas las cosas con dulzura y precisión de médico."
        ),
    },
    "zoro": {
        "nombre": "Zoro",
        "emoji": "⚔️",
        "system": BASE + (
            " Eres Roronoa Zoro: serio, lacónico, honorable, siempre dispuesto a entrenar. "
            "Respondes con frases cortas y contundentes, a veces refunfuñas, y de vez en cuando "
            "admites que estás perdido aunque el camino sea recto."
        ),
    },
}


class Mensaje(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=2000)


class ChatIn(BaseModel):
    personaje: str = "luffy"
    mensajes: list[Mensaje] = Field(min_length=1, max_length=40)


@app.get("/api/py/salud")
def salud():
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        ia = "gemini"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        ia = "claude"
    else:
        ia = None
    return {"ok": True, "ia": ia, "mensaje": "¡El Going Merry navega sin problemas!"}


@app.get("/api/py/personajes")
def personajes():
    return {k: {"nombre": v["nombre"], "emoji": v["emoji"]} for k, v in PERSONAJES.items()}


def _chat_gemini(system: str, historial: list[dict]) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client()  # lee GEMINI_API_KEY del entorno
    contents = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
        for m in historial
    ]
    resp = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-3.6-flash"),
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=1024,
        ),
    )
    return resp.text or "…"


def _chat_claude(system: str, historial: list[dict]) -> str:
    import anthropic

    client = anthropic.Anthropic()  # lee ANTHROPIC_API_KEY del entorno
    resp = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        system=system,
        messages=historial,
    )
    return "".join(b.text for b in resp.content if b.type == "text")


@app.post("/api/py/chat")
def chat(body: ChatIn):
    p = PERSONAJES.get(body.personaje)
    if p is None:
        raise HTTPException(400, f"Personaje desconocido: {body.personaje}")

    # Solo las últimas 20 vueltas para acotar costo y contexto
    historial = [m.model_dump() for m in body.mensajes][-20:]

    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        proveedor = "gemini"
        try:
            texto = _chat_gemini(p["system"], historial)
        except Exception as e:  # la API de Gemini lanza errores propios variados
            raise HTTPException(502, f"Error de Gemini: {str(e)[:180]}")
    elif os.environ.get("ANTHROPIC_API_KEY"):
        proveedor = "claude"
        import anthropic
        try:
            texto = _chat_claude(p["system"], historial)
        except anthropic.AuthenticationError:
            raise HTTPException(503, "La ANTHROPIC_API_KEY del servidor no es válida.")
        except anthropic.RateLimitError:
            raise HTTPException(429, "Demasiadas peticiones seguidas; espera un momento.")
        except anthropic.APIStatusError as e:
            raise HTTPException(502, f"Error de la API de Claude: {e.status_code}")
        except (anthropic.APIConnectionError, TypeError):
            raise HTTPException(502, "No se pudo conectar con la API de Claude.")
    else:
        raise HTTPException(
            503,
            "Configura GEMINI_API_KEY (gratis en aistudio.google.com) "
            "o ANTHROPIC_API_KEY en el servidor.",
        )

    return {"respuesta": texto, "personaje": body.personaje, "ia": proveedor}
