import pytest
from database.connection import pool
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM urls")

    yield        

@pytest.fixture
def shortened_url():
    response = client.post(
        '/shorten',
        json={
            'url':'https://example.com',
            'expires_in':300
        }
    )
    assert response.status_code == 201

    return response.json()['shortcode']
    