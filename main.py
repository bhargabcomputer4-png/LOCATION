from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="India PIN Code API",
    description="Free PIN Code Lookup API for Developers & Businesses",
    version="1.0.0"
)

# Enable CORS so anyone can access your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample PIN Code Database (Aap isme aur bhi data add kar sakte hain)
PINCODE_DATABASE = {
    "110001": {
        "pincode": "110001",
        "office_name": "Connaught Place G.P.O.",
        "district": "Central Delhi",
        "state": "Delhi",
        "country": "India",
        "latitude": 28.6280,
        "longitude": 77.2090
    },
    "400001": {
        "pincode": "400001",
        "office_name": "Mumbai Fort",
        "district": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 18.9388,
        "longitude": 72.8353
    },
    "560001": {
        "pincode": "560001",
        "office_name": "Bangalore G.P.O.",
        "district": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "latitude": 12.9716,
        "longitude": 77.5946
    }
}

@app.get("/")
def home():
    return {
        "status": "online", 
        "message": "Welcome to PIN Code API! Use /api/v1/pincode/{code} to lookup."
    }

@app.get("/api/v1/pincode/{pincode}")
def get_pincode_details(pincode: str):
    # Validate length
    if len(pincode) != 6 or not pincode.isdigit():
        raise HTTPException(status_code=400, detail="Invalid PIN code format. Must be a 6-digit number.")
    
    # Search in database
    result = PINCODE_DATABASE.get(pincode)
    if not result:
        raise HTTPException(status_code=404, detail="PIN code not found in the database.")
    
    return {"success": True, "data": result}
    