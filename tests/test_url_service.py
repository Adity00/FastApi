from services.url_service import create_short_url
from database.queries import get_url_stats
from unittest.mock import patch
from datetime import datetime, timezone


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
    