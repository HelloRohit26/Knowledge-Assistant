"""
Integration Tests for FastAPI API Endpoints (Phase 10-12)
"""


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["version"] == "2.0.0"


def test_registry_health(client):
    response = client.get("/api/registry/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_auth_register_and_login(client):
    # Register user
    reg_resp = client.post("/api/auth/register", json={
        "username": "apiuser",
        "email": "apiuser@test.com",
        "password": "mypassword123",
        "role": "user"
    })
    assert reg_resp.status_code == 200
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["username"] == "apiuser"

    # Login user
    login_resp = client.post("/api/auth/login", json={
        "username": "apiuser",
        "password": "mypassword123"
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data

    # Access protected route /api/auth/me
    token = login_data["access_token"]
    me_resp = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["username"] == "apiuser"


def test_analytics_endpoint(client):
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "by_department" in data
