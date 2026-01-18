from fastapi import FastAPI
import requests

app = FastAPI()
OPA_URL = "http://localhost:8181/v1/data/portfolio/authz/allow"

def is_authorized(user_role, stock_info):
    payload = {
        "input": {
            "user": {"role": user_role},
            "stock": stock_info
        }
    }
    response = requests.post(OPA_URL, json=payload)
    return response.json().get("result", False)

@app.get("/stocks")
def get_my_stocks(role: str = "viewer"):
    # In a real app, this data comes from your database
    raw_stocks = [
        {"ticker": "AAPL", "restricted": False},
        {"ticker": "TSLA", "restricted": True}
    ]
    
    # Filter based on OPAL's real-time policy
    return [s for s in raw_stocks if is_authorized(role, s)]
