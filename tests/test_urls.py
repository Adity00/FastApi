from fastapi.testclient import TestClient

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


def test_clicks_counting():
    response = client.post(
        "/shorten",
        json={
            'url':'https://example.com',
            'expires_in':300
        }
    )
    assert response.status_code == 201

    data = response.json()
    shortcode = data['shortcode']

    response = client.get(
        f'/{shortcode}',
        follow_redirects=False
    )

    assert response.status_code == 302

    response = client.get(
        f'/{shortcode}',
        follow_redirects=False
    )

    assert response.status_code == 302

    response = client.get(f'/stats/{shortcode}')

    assert response.status_code == 200

    data = response.json()

    assert data['shortcode'] == shortcode
    assert data['clicks'] == 2


def test_url_stats():
    response = client.post(
        '/shorten',
        json={
            "url":"https://example.com",
            'expires_in':300
        }
    )
    assert response.status_code == 201

    data = response.json()
    shortcode = data['shortcode']

    response = client.get(f'/stats/{shortcode}')

    assert response.status_code == 200

    data = response.json()

    assert data['shortcode'] == shortcode
    assert data['original_url'] == "https://example.com/"
    assert data['clicks'] == 0
    assert data['expires_at'] is not None


def test_expired_url():
    response = client.post(
        '/shorten',
        json={
            'url':"https://example.com",
            'expires_in': 0
        }
    )

    assert response.status_code == 201

    data = response.json()
    shortcode = data['shortcode']

    response = client.get(
        f'/{shortcode}',
        follow_redirects=False
    )

    assert response.status_code == 410
    assert response.json()['detail'] == 'URL_Expired'


def test_nonexistent_short_code():

    response = client.get(
        '/doesnotexist',
        follow_redirects=False
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Short code not found'

def test_invalid_url():
    reponse = client.post(
        '/shorten',
        json={
            'url':'not-a-valid-url',
            'expires_in':300
        }
    )
    assert reponse.status_code == 422

def test_missing_url():
    response = client.post(
        '/shorten',
        json={
            'expires_in':300
        }
    )    

    assert response.status_code == 422

def test_invalid_expires_in():
    response = client.post(
        '/shorten',
        json={
            'url':'https://example.com',
            'expires_in':'invalid expires_in input'
        }
    )    

    assert response.status_code == 422
