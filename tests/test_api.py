import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv('API_KEY')
URL = "https://www.goldapi.io/api/XAU/USD"

def test_api_status():
    headers = {
        "x-access-token": API_KEY
    }

    response = requests.get(URL, headers=headers, timeout=10)

    assert response.status_code == 200, f"Status code failed: {response.status_code}"

    data = response.json()

    # Vérification des champs essentiels
    assert "price" in data, "Missing 'price'"
    assert "timestamp" in data, "Missing 'timestamp'"
    assert "metal" in data, "Missing 'metal'"
    assert "currency" in data, "Missing 'currency'"

    # Vérification des valeurs
    assert data["price"] > 0, "Price must be > 0"
    assert data["metal"] == "XAU", "Metal should be XAU"
    assert data["currency"] == "USD", "Currency should be USD"

    print(" ==> API test passed")

if __name__ == "__main__":
    test_api_status()