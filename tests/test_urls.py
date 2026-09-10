from fastapi.testclient import TestClient
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from database.queries import get_url_stats
from exceptions import URLCreationError
from unittest.mock import patch

import time
import uuid

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


def test_url_stats(shortened_url):

    response = client.get(f'/stats/{shortened_url}')

    assert response.status_code == 200

    data = response.json()

    assert data['shortcode'] == shortened_url
    assert data['original_url'] == "https://example.com/"
    assert data['clicks'] == 0
    assert data['expires_at'] is not None


def test_expired_url():
    response = client.post(
        '/shorten',
        json={
            'url':"https://example.com",
            'expires_in': 1
        }
    )

    assert response.status_code == 201

    data = response.json()
    shortcode = data['shortcode']

    time.sleep(1.1)

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


def test_invalid_expiration():
    response = client.post(
        '/shorten',
        json={
            'url':"https://example.com",
            'expires_in':0
        }
    )

    assert response.status_code == 422


def test_negative_expiration():
    response = client.post(
        '/shorten',
        json={
            'url':'https://example.com',
            'expires_in':-10
        }
    )

    assert response.status_code == 422


def test_shortcode_collison():
    response = client.post(
        '/shorten',
        json={
            "url": 'https://example.com',
            'expires_in': 300
        }
    )

    assert response.status_code == 201

    existing_shortcode = response.json()['shortcode']

    new_shortcode = uuid.uuid4().hex[:6]

    while get_url_stats(new_shortcode)is not None:
        new_shortcode = uuid.uuid4().hex[:6]

    #creates a fake API input which generates a already present shortcode which
    #returns false and then again give second input which is gurenteed unique using uuid
    with patch(
        "services.url_service.generate_short_code",
        side_effect=[existing_shortcode, new_shortcode]
    ):
        response = client.post(
            '/shorten',
            json={
                'url': 'https://google.com',
                'expires_in': 300
            }
        )

    assert response.status_code == 201
    assert response.json()['shortcode'] == new_shortcode


def test_connection_pool_concurrency():
    response = client.post(
        '/shorten',
        json={
            'url':'https://example.com',
            'expires_in': 300
        }
    )

    assert response.status_code == 201

    shortcode =response.json()['shortcode']

    def make_request():
        return client.get(f'/stats/{shortcode}')

    with ThreadPoolExecutor(max_workers=20) as executor:
        responses = list(
            executor.map(
                lambda _: make_request(),
                range(20)
            )
        )

    assert all(response.status_code == 200 for response in responses)


def test_concurrent_clicks():
    response = client.post(
        '/shorten',
        json={
            'url':'https://example.com',
            'expires_in':300
        }
    )

    assert response.status_code == 201

    shortcode = response.json()['shortcode']

    def make_request():
        return client.get(
            f'/{shortcode}',
            follow_redirects=False
        )

    with ThreadPoolExecutor(max_workers=20) as executor:
        responses = list(
            executor.map(
                lambda _: make_request(),
                range(50)
            )
        )

        assert all(response.status_code == 302 for response in responses)

        response = client.get(f'/stats/{shortcode}')

        assert response.status_code == 200
        assert response.json()['clicks'] == 50


def test_shorten_database_failure():
    with patch(
        "routes.urls.create_short_url",
        side_effect=URLCreationError("could not create short URL")
    ):
        response = client.post(
            "/shorten",
            json={
                "url": "https://example.com"
            }
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "could not create short URL"
