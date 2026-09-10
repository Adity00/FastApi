from services.url_service import create_short_url,get_url_for_redirect
from database.queries import get_url_stats
from unittest.mock import patch
from datetime import datetime, timezone
import time
from psycopg import OperationalError
from exceptions import URLCreationError
import pytest


def test_create_short_url():

    shortcode, expires_at = create_short_url(
        'https://example.com',
        300
    )

    assert shortcode is not None
    assert len(shortcode) == 6
    assert expires_at is not None

    record = get_url_stats(shortcode)

    assert record is not None
    assert record['url'] == 'https://example.com'
    assert record['clicks'] == 0


def test_create_short_url_collision_retry():

    first_code = "ABC123"
    second_code = "XYZ789"

    with patch(
        'services.url_service.generate_short_code',
        side_effect=[first_code, second_code]
    ):
        create_short_url(
            'https://example.com',
            300
        )

        shortcode, expires_at = create_short_url(
            'https://google.com',
            300
        )

    assert shortcode == second_code

    record = get_url_stats(second_code)

    assert record is not None
    assert record['url'] == 'https://google.com'

def test_create_short_url_expiration():
    before = datetime.now(timezone.utc)

    shortcode, expires_at = create_short_url(
        'https://example.com',
        300
    )

    after = datetime.now(timezone.utc)

    assert expires_at is not None
    assert before.timestamp() + 300 <= expires_at.timestamp()
    assert expires_at.timestamp() <= after.timestamp()+300

def test_create_short_url_retries_database_failure():

    first_code = "ABC123"
    second_code = "XYZ789"

    with patch(
        "services.url_service.generate_short_code",
        side_effect=[first_code, second_code]
    ), patch(
        "services.url_service.create_url",
        side_effect=[False, True]
    ):
        shortcode, expires_at = create_short_url(
            "https://example.com",
            300
        )

    assert shortcode == second_code

def test_get_url_for_redirect():
    shortcode, expires_at = create_short_url(
        'https://example.com',
        300
    )    

    result = get_url_for_redirect(shortcode)

    assert result['status'] == 'success'
    assert result['url'] == 'https://example.com'

def test_get_url_redirect_not_found():
    result = get_url_for_redirect("blabla")

    assert result['status']== 'not_found'    

def test_get_url_for_redirect_expired():
    shortcode, expires_at = create_short_url(
        'https://example.com',
        1
    )

    time.sleep(1.1)

    result = get_url_for_redirect(shortcode)

    assert result['status'] == 'expired'

def test_create_short_url_database_failure():
    with patch(
        "services.url_service.create_url",
        side_effect = OperationalError('database unavailable')
        ) as mock_create_url:
        with pytest.raises(URLCreationError):
            create_short_url(
                'https://example.com',
                300
            )
    assert mock_create_url.call_count  == 3

def test_create_short_url_database_retry_success():

    with patch(
        "services.url_service.create_url",
        side_effect=[
            OperationalError("database unavailable"),
            OperationalError("database unavailable"),
            True
        ]
    ) as mock_create_url:
        shortcode, expires_at = create_short_url(
            'https://example.com',
            300
        )

    assert shortcode is not None
    assert len(shortcode) == 6
    assert expires_at is not None
    assert mock_create_url.call_count == 3
    