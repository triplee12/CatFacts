"""
The main module for the CatFacts API Platform.
"""
import os
import logging
from datetime import datetime, timezone
import httpx
import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

USER_EMAIL = os.getenv("USER_EMAIL", "tripleeoliver@gmail.com")
USER_NAME = os.getenv("USER_NAME", "Chukwuebuka Emmanuel Ejie")
USER_STACK = os.getenv("USER_STACK", "Python/FastAPI")
CATFACT_URL = os.getenv("CATFACT_URL", "https://catfact.ninja/fact")
EXTERNAL_TIMEOUT = float(os.getenv("EXTERNAL_TIMEOUT", "5.0"))
ENV = os.getenv("ENV", "local")

app = FastAPI(
    title="Profile + CatFact API",
    version="0.1.0",
    docs_url=(
        "/docs"
    ),
    openapi_url="/docs/openapi.json",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


@app.get("/me")
async def get_profile():
    """Return profile info and a dynamic cat fact fetched from the Cat Facts API.

    Response JSON shape (strict):
    {
      "status": "success",
      "user": { "email": "...", "name": "...", "stack": "..." },
      "timestamp": "<UTC ISO 8601>",
      "fact": "<cat fact or fallback message>"
    }
    """
    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    fallback_fact = "Could not fetch a cat fact at this time."
    fact_text = fallback_fact

    try:
        async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT) as client:
            resp = await client.get(CATFACT_URL)
            resp.raise_for_status()
            data = resp.json()
            fact_text = data.get("fact") or fallback_fact
    except httpx.RequestError as e:
        logger.warning("Network error fetching cat fact: %s", e)
    except httpx.HTTPStatusError as e:
        logger.warning("Bad status from cat fact service: %s", e)
    except Exception as e:
        logger.exception("Unexpected error fetching cat fact: %s", e)

    payload = {
        "status": "success",
        "user": {
            "email": USER_EMAIL,
            "name": USER_NAME,
            "stack": USER_STACK,
        },
        "timestamp": timestamp,
        "fact": fact_text,
    }

    return JSONResponse(content=payload, status_code=status.HTTP_200_OK)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handles StarletteHTTPExceptions raised within the application.

    Logs the exception at the ERROR level and returns a JSONResponse
    with the status code and detail from the exception.

    :param request: The current request context
    :param exc: The StarletteHTTPException being handled
    :return: A JSONResponse with the status code and detail from the exception
    """
    status_code, detail, url_path = exc.status_code, exc.detail, request.url.path
    logger.error(
        "status code: %s, detail: %s, url path: %s",
        status_code, detail, url_path
    )
    return JSONResponse(status_code=status_code, content=detail)


def main():
    """
    Starts the CatFacts API Platform using Uvicorn.

    This function is the entrypoint for the application, and is responsible
    for starting the Uvicorn server with the appropriate settings.

    It logs a message to indicate that the application is starting, and
    then starts the Uvicorn server with the following settings:
    - host: 0.0.0.0
    - port: 8000
    - reload: False if the environment is "deployment", True otherwise
    - workers: 1
    """
    logger.info("Starting CatFacts API Platform...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False if ENV.startswith("deployment") else True,
        workers=1
    )


if __name__ == "__main__":
    main()
