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
import time
from collections import deque

from fastapi import FastAPI, HTTPException, Request
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


class PirataIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=40)
    rasgos: str = Field(min_length=1, max_length=200)
    sueno: str = Field(min_length=1, max_length=200)


PIRATA_SYSTEM = (
    "Eres el redactor del periódico del Gobierno Mundial en el universo de One Piece. "
    "A partir del nombre, los rasgos y el sueño de una persona, inventa su identidad pirata. "
    "Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional ni bloques de código, con exactamente estas claves: "
    "epiteto (apodo pirata corto, estilo «Sombrero de Paja» o «Cazador de Piratas»), "
    "fruta (nombre de una fruta del diablo inventada con el formato «Xxx Xxx no Mi» y, entre paréntesis, qué poder da), "
    "recompensa (número entero de berries entre 30000000 y 3000000000, sin separadores), "
    "rol (puesto en la tripulación), "
    "historia (2 o 3 frases épicas en español sobre su llegada a la Grand Line) y "
    "frase (una frase de batalla corta). Todo en español."
)


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


def _texto_de(resp) -> str:
    """Texto de una respuesta de Gemini; si viene vacía, lanza un error con el motivo (finish_reason)."""
    texto = getattr(resp, "text", None)
    if texto:
        return texto
    motivo = None
    try:
        motivo = getattr(resp.candidates[0], "finish_reason", None)
    except Exception:
        pass
    raise ValueError(f"respuesta vacia ({motivo})")


def _json_de_texto(texto: str) -> dict:
    """Extrae el primer objeto JSON del texto (tolera ```json ... ```)."""
    import json, re
    t = texto.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I | re.M).strip()
    i, j = t.find("{"), t.rfind("}")
    if i == -1 or j == -1:
        raise ValueError("sin JSON")
    return json.loads(t[i:j + 1])


def _pirata_gemini(prompt: str) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client()
    modelo = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    # 1) Salida estructurada nativa; 2) si el modelo/cuenta no la admite, texto libre + extracción del JSON
    try:
        resp = client.models.generate_content(
            model=modelo, contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=PIRATA_SYSTEM, response_mime_type="application/json", max_output_tokens=4096,
            ),
        )
        return _json_de_texto(_texto_de(resp))
    except Exception as e:
        print(f"[pirata/gemini json-mode] {type(e).__name__}: {e}")
        resp = client.models.generate_content(
            model=modelo, contents=contents,
            config=types.GenerateContentConfig(system_instruction=PIRATA_SYSTEM, max_output_tokens=4096),
        )
        return _json_de_texto(_texto_de(resp))


def _pirata_claude(prompt: str) -> dict:
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-opus-5",
        max_tokens=800,
        system=PIRATA_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return _json_de_texto("".join(b.text for b in resp.content if b.type == "text"))


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


# ---- Límite sencillo por IP (en memoria, por instancia): evita que alguien agote la cuota de la API
LIMITE_PETICIONES = 20      # peticiones…
VENTANA_SEGUNDOS = 300      # …cada 5 minutos
_llamadas: dict[str, deque] = {}


def _limitar_por_ip(ip: str) -> None:
    ahora = time.time()
    cola = _llamadas.setdefault(ip, deque())
    while cola and ahora - cola[0] > VENTANA_SEGUNDOS:
        cola.popleft()
    if len(cola) >= LIMITE_PETICIONES:
        raise HTTPException(429, "Demasiadas preguntas seguidas, nakama. Espera unos minutos.")
    cola.append(ahora)
    if len(_llamadas) > 5000:  # no crecer sin límite
        _llamadas.clear()


@app.post("/api/py/chat")
def chat(body: ChatIn, request: Request):
    ip = request.headers.get("x-forwarded-for", "") or (request.client.host if request.client else "?")
    _limitar_por_ip(ip.split(",")[0].strip())
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
            print(f"[gemini] {type(e).__name__}: {e}")  # queda en los logs del servidor, no en el cliente
            raise HTTPException(502, "La IA no pudo responder en este momento. Inténtalo de nuevo en unos segundos.")
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


@app.post("/api/py/pirata")
def pirata(body: PirataIn, request: Request):
    """Generador de identidad pirata: la IA devuelve JSON estructurado que el frontend pinta como cartel WANTED."""
    ip = request.headers.get("x-forwarded-for", "") or (request.client.host if request.client else "?")
    _limitar_por_ip(ip.split(",")[0].strip())

    prompt = (
        f"Nombre: {body.nombre.strip()}\n"
        f"Rasgos de personalidad: {body.rasgos.strip()}\n"
        f"Sueño: {body.sueno.strip()}"
    )
    try:
        if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
            proveedor, datos = "gemini", _pirata_gemini(prompt)
        elif os.environ.get("ANTHROPIC_API_KEY"):
            proveedor, datos = "claude", _pirata_claude(prompt)
        else:
            raise HTTPException(503, "Configura GEMINI_API_KEY (gratis en aistudio.google.com) o ANTHROPIC_API_KEY en el servidor.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[pirata/{type(e).__name__}] {e}")
        raise HTTPException(502, f"La IA no pudo generar tu identidad en este momento ({type(e).__name__}). Inténtalo de nuevo.")

    # Saneado: claves esperadas, tipos correctos y recompensa dentro de rango
    try:
        recompensa = int(str(datos.get("recompensa", "0")).replace(".", "").replace(",", "").strip() or 0)
    except ValueError:
        recompensa = 0
    recompensa = max(30_000_000, min(recompensa, 5_000_000_000))
    return {
        "ia": proveedor,
        "nombre": body.nombre.strip(),
        "epiteto": str(datos.get("epiteto", "El Desconocido"))[:60],
        "fruta": str(datos.get("fruta", "Sin fruta"))[:120],
        "recompensa": recompensa,
        "rol": str(datos.get("rol", "Grumete"))[:60],
        "historia": str(datos.get("historia", ""))[:600],
        "frase": str(datos.get("frase", ""))[:120],
    }
