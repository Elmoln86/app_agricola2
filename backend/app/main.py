from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api_routes import router as weather_router  # sua rota jÃ¡ existente (clima)
from app.stripe_routes import router as billing_router
from app.webhooks import router as webhook_router

app = FastAPI(title='Modelo2 Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://SEU-APP-VERCEL.vercel.app",
        "https://app.terravivaia.com.br",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/health')
async def health():
    return {'status': 'ok'}

app.include_router(weather_router)  # se nÃ£o quiser pÃºblica, adicione Depends no arquivo api_routes.py
app.include_router(billing_router, prefix='/api/billing', tags=['billing'])
app.include_router(webhook_router, prefix='/api/webhooks', tags=['webhooks'])

