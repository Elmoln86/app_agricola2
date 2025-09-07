import os
import stripe
from fastapi import APIRouter, HTTPException, Depends
from app.deps import get_current_user

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
FRONTEND_URL = os.getenv("FRONTEND_PUBLIC_URL", "http://localhost:5173")

@router.post("/checkout")
async def create_checkout_session(user=Depends(get_current_user)):
    if not stripe.api_key or not PRICE_ID:
        raise HTTPException(status_code=500, detail="Stripe nÃ£o configurado.")
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            success_url=f"{FRONTEND_URL}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/billing/cancel",
            metadata={"supabase_user_id": user.get("sub", "")},
            automatic_tax={"enabled": False},
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
