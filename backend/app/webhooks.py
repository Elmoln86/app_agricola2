import os
import stripe
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe")
async def stripe_webhook(req: Request):
    payload = await req.body()
    sig = req.headers.get("stripe-signature")

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET nÃ£o configurado")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig, secret=WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Assinatura invÃ¡lida: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payload invÃ¡lido: {e}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("âœ… checkout.session.completed",
              session.get("metadata", {}).get("supabase_user_id"),
              session.get("subscription"))
    elif event["type"] == "customer.subscription.updated":
        print("â„¹ï¸ subscription.updated")
    elif event["type"] == "customer.subscription.deleted":
        print("â„¹ï¸ subscription.deleted")

    return {"received": True}
