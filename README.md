# CatFact

A minimal Python/FastAPI project that exposes a `GET /me` endpoint returning profile information and a dynamic cat fact fetched from the Cat Facts API (`https://catfact.ninja/fact`).

## Project structure

```txt
CatFact/
├─ README.md (this file)
├─ main.py
├─ requirements.txt
├─ Procfile
├─ runtime.txt
├─ .env.example
├─ .gitignore
└─ tests/
   └─ test_main.py
```

### `.env.example`

```env
# Copy to .env locally (this file should not be committed with secrets)
USER_EMAIL=user@example.com
USER_NAME=Your name
USER_STACK=Python/FastAPI
CATFACT_URL=https://catfact.ninja/fact
EXTERNAL_TIMEOUT=5.0
```

## How to run locally

1. Clone the repository by running `git clone https://github.com/triplee12/CatFacts.git`
2. Change working directory by running `cd CatFacts`
3. (Optional) Create a virtualenv: `python -m venv .venv && source .venv/bin/activate`
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file from `.env.example` and edit if you want to override the defaults.
6. Run the app locally:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Or
python -m main
```

7. Visit `http://localhost:8000/me` — you should get the JSON response described in the task.

8. Visit `http://localhost:8000/docs` or `http://0.0.0.0:8000/redoc` - you should get the API documentation

9. Run tests:

```bash
pytest -q
```

## Deployment to Railway (quick steps)

1. Create a new project on Railway and connect your GitHub repo (or `git push` to a Railway remote).
2. Set environment variables under the Railway project settings if you want to override `USER_EMAIL`, `USER_NAME`, or `USER_STACK`.
3. Railway automatically sets the `$PORT` env var — Procfile uses it.
4. Deploy and open the provided URL -> `/me`.

## Notes & Best practices implemented

* Uses `httpx.AsyncClient` with a configurable timeout (defaults to 5s) — prevents hanging.
* Graceful handling of network and HTTP errors from the external Cat Facts API — returns a fallback fact message if needed.
* Profile fields are configurable through environment variables (no secrets in repo).
* `Content-Type: application/json` is returned automatically by FastAPI's JSONResponse.
* CORS middleware is included (allowing all origins) — adjust for production.
* Basic logging is enabled.
* Tests included (pytest + pytest-asyncio).

## Authors

* Chukwuebuka Emmanuel Ejie
