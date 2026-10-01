from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from .metrics import collect

app = FastAPI(title="Teamcenter Monitoring Adapter")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/metrics")
def metrics():
    collect()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
