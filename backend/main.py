# -*- coding: utf-8 -*-
"""Grand Line API — backend en Python (FastAPI) con IA (API de Claude).

Ejecutar:
    pip install -r requirements.txt
    set ANTHROPIC_API_KEY=tu-clave   (o defínela en las variables de entorno)
    uvicorn main:app --port 8000
"""
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Grand Line API", version="1.0.0")

# El frontend Next.js corre en :3000 — sin esto el navegador bloquea las peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lee ANTHROPIC_API_KEY del entorno; la clave nunca toca el navegador
client = anthropic.Anthropic()

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


@app.get("/api/salud")
def salud():
    return {"ok": True, "mensaje": "¡El Going Merry navega sin problemas!"}


@app.get("/api/personajes")
def personajes():
    return {k: {"nombre": v["nombre"], "emoji": v["emoji"]} for k, v in PERSONAJES.items()}


@app.post("/api/chat")
def chat(body: ChatIn):
    p = PERSONAJES.get(body.personaje)
    if p is None:
        raise HTTPException(400, f"Personaje desconocido: {body.personaje}")

    # Solo las últimas 20 vueltas para acotar costo y contexto
    historial = [m.model_dump() for m in body.mensajes][-20:]

    try:
        resp = client.messages.create(
            model="claude-opus-5",
            max_tokens=1024,
            system=p["system"],
            messages=historial,
        )
    except TypeError:
        # El SDK lanza TypeError cuando no encuentra ninguna credencial configurada
        raise HTTPException(503, "El servidor no tiene configurada la ANTHROPIC_API_KEY.")
    except anthropic.AuthenticationError:
        raise HTTPException(503, "La ANTHROPIC_API_KEY del servidor no es válida.")
    except anthropic.RateLimitError:
        raise HTTPException(429, "Demasiadas peticiones seguidas; espera un momento.")
    except anthropic.APIStatusError as e:
        raise HTTPException(502, f"Error de la API de Claude: {e.status_code}")
    except anthropic.APIConnectionError:
        raise HTTPException(502, "No se pudo conectar con la API de Claude.")

    texto = "".join(b.text for b in resp.content if b.type == "text")
    return {"respuesta": texto, "personaje": body.personaje}
