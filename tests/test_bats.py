import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_bats_existing():
    response = client.get("/bats/search")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  

    bat = data[0]
    assert "id" in bat
    assert "name" in bat
    assert "brand" in bat
    assert "price" in bat
    assert "is_wood" in bat


def test_create_bat():
    data = {
        "name": "Prime 919",
        "brand": "Louisville",
        "price": 199.99,
        "is_wood": False
    }
    response = client.post("/bats/", json=data)

    assert response.status_code == 201
    response_data = response.json()

    assert response_data["name"] == "Prime 919"
    assert response_data["brand"] == "Louisville"
    assert response_data["price"] == 199.99
    assert response_data["is_wood"] is False
    assert "id" in response_data

def test_get_bat_by_id():
    
    bat_data = {
        "name": "The Goods",
        "brand": "DeMarini",
        "price": 329.99,
        "is_wood": False
    }
    create_response = client.post("/bats/", json=bat_data)
    assert create_response.status_code == 201
    created_bat = create_response.json()
    bat_id = created_bat["id"]

    
    get_response = client.get(f"/bats/{bat_id}")
    assert get_response.status_code == 200
    bat = get_response.json()

    assert bat["id"] == bat_id
    assert bat["name"] == bat_data["name"]
    assert bat["brand"] == bat_data["brand"]
    assert bat["price"] == bat_data["price"]
    assert bat["is_wood"] == bat_data["is_wood"]


def test_get_bat_invalid_id():
    response = client.get("/bats/99999")  
    assert response.status_code == 404
    assert response.json() == {"detail": "Bat not found"}

def test_update_bat():
    
    bat_data = {
        "name": "Old Bat",
        "brand": "Rawlings",
        "price": 199.99,
        "is_wood": True
    }
    create_response = client.post("/bats/", json=bat_data)
    assert create_response.status_code == 201
    created_bat = create_response.json()
    bat_id = created_bat["id"]

  
    updated_data = {
        "name": "Updated Bat",
        "brand": "Rawlings",
        "price": 249.99,
        "is_wood": False
    }
    update_response = client.put(f"/bats/{bat_id}", json=updated_data)
    assert update_response.status_code == 200
    updated_bat = update_response.json()

    
    assert updated_bat["name"] == updated_data["name"]
    assert updated_bat["price"] == updated_data["price"]
    assert updated_bat["is_wood"] == updated_data["is_wood"]

def test_search_bats_by_is_wood():
    
    bat1 = {"name": "Wood Bat", "brand": "Marucci", "price": 100.0, "is_wood": True}
    bat2 = {"name": "Metal Bat", "brand": "Easton", "price": 120.0, "is_wood": False}

    client.post("/bats/", json=bat1)
    client.post("/bats/", json=bat2)

 
    response_wood = client.get("/bats/search?is_wood=true")
    assert response_wood.status_code == 200
    for bat in response_wood.json():
        assert bat["is_wood"] is True

   
    response_metal = client.get("/bats/search?is_wood=false")
    assert response_metal.status_code == 200
    for bat in response_metal.json():
        assert bat["is_wood"] is False


def test_create_bat_missing_fields():
    bad_data = {
        "brand": "DeMarini", 
    }
    response = client.post("/bats/", json=bad_data)
    assert response.status_code == 422  
