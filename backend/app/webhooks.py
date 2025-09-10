from fastapi import APIRouter, Request, HTTPException
import stripe
import os

router = APIRouter()

# Defina a secret do webhook do Stripe (configure no Render também)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
stripe.api_key = STRIPE_API_KEY

@router.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    # 👇 Aqui você trata os eventos que vêm do Stripe
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Pagamento concluído: {session['id']}")

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        print(f"Assinatura atualizada: {subscription['id']}")

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        print(f"Assinatura cancelada: {subscription['id']}")

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        print(f"Falha no pagamento: {invoice['id']}")

    return {"status": "success"}
