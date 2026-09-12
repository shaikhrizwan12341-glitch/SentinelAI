from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.health import router as health_router
from backend.api.routes.url import router as url_router
from backend.api.routes.email import router as email_router
from backend.api.routes.sms import router as sms_router
from backend.api.routes.scans import router as scans_router
from backend.api.routes.auth import router as auth_router

app = FastAPI(
    title="SentinelAI API",
    description=(
        "AI-Powered Multilingual Phishing Detection API "
        "for URL, Email, and SMS analysis."
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(health_router)
app.include_router(url_router)
app.include_router(email_router)
app.include_router(sms_router)
app.include_router(scans_router)
app.include_router(auth_router)
# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to SentinelAI API",
        "status": "online",
        "version": "1.0.0"
    }