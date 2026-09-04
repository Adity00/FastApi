from fastapi.testclient import TestClient
from fastapi import HTTPException

from main import app

client = TestClient(app)

def test_create_url():
    response = client.post(
        "/shorten",
        json={
            "url":"https://example.com",
            "expires_in":300
        }
    )

    assert response.status_code == 201

    data = response.json()
    shortcode = data["shortcode"]

    response=client.get(
        f"/{shortcode}",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers['location'] == 'https://example.com/'
