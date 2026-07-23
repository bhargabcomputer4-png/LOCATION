from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import qrcode
import io

app = FastAPI(
    title="NEXIVORA.QR API",
    description="Professional Enterprise-Grade QR Code Generation & Monetization Infrastructure",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanVerification(BaseModel):
    plan_id: str
    transaction_id: str
    user_email: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NEXIVORA.QR - Professional Enterprise Infrastructure</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-white flex items-center justify-center min-h-screen">
        <div class="text-center p-8 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl max-w-lg w-full">
            <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent mb-4">NEXIVORA.QR</h1>
            <p class="text-slate-400 mb-6">Enterprise-Grade QR Code Generation & Monetization Infrastructure is live and running successfully!</p>
            <div class="inline-block bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-4 py-2 rounded-full text-sm font-medium">
                ● System Status: Online
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/api/v1/generate")
def generate_qr(text: str, box_size: int = 10, border: int = 4):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text parameter cannot be empty.")
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return Response(content=buf.getvalue(), media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@app.post("/api/v1/verify-payment")
def verify_payment(data: PlanVerification):
    valid_plans = {
        "starter": {"name": "Starter Plan", "limit": 50, "price": 49},
        "growth": {"name": "Growth Plan", "limit": 150, "price": 149},
        "pro": {"name": "Professional Plan", "limit": 250, "price": 249}
    }
    
    if data.plan_id not in valid_plans:
        raise HTTPException(status_code=400, detail="Invalid plan selected.")
    
    if not data.transaction_id or len(data.transaction_id.strip()) < 6:
        raise HTTPException(status_code=400, detail="Invalid UPI Transaction Reference ID (UTR).")
        
    plan = valid_plans[data.plan_id]
    
    return {
        "success": True,
        "message": f"Payment submission received for {plan['name']}. Verification in progress by team.",
        "assigned_quota": plan["limit"],
        "support_email": "blinkxpro@gmail.com"
    }
    