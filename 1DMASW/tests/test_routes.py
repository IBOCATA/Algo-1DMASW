def test_secure_endpoint():
    token_resp = client.post("/token", data={"username": "admin", "password": "pass"})
    token = token_resp.json()["access_token"]

    response = client.get("/secure-endpoint", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "message" in response.json()
