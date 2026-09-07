from database.queries import create_url, get_url_and_increment_clicks, get_url_stats
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def test_get_url_and_increment_clicks():
    create_url(
        "abc123",
        "https://example.com"
    )

    get_url_and_increment_clicks("abc123")
    get_url_and_increment_clicks("abc123")
    get_url_and_increment_clicks("abc123")
    get_url_and_increment_clicks("abc123")

    stats = get_url_stats('abc123')

    assert stats['clicks'] == 4

def test_get_url_and_increment_clicks_not_found():

    result = get_url_and_increment_clicks('doesnotexist')
    assert result['status'] == 'not_found'

def test_get_url_and_increment_clicks_expired():

    expires_at = datetime.now() - timedelta(seconds=10)

    create_url(
        'exp001',
        'https://example.com',
        expires_at
    )

    result = get_url_and_increment_clicks('exp001')

    assert result['status'] == 'expired'

def test_expired_url_does_not_increment_clicks():

    expires_at = datetime.now() - timedelta(seconds=10)

    create_url(
        'exp002',
        'https://example.com',
        expires_at
    )

    result = get_url_and_increment_clicks('exp002')    

    assert result['status'] == 'expired'

    stats = get_url_stats('exp002')

    assert stats['clicks'] == 0

def test_concurrent_clicks():
    create_url(
        'con001',
        'https://example.com'
    )

    def make_request():
        return get_url_and_increment_clicks('con001')

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(
            executor.map(
                lambda _: make_request(),
                range(50)
            )
        )

    assert all(result['status'] == 'success' for result in results)    

    stats = get_url_stats('con001')

    assert stats['clicks'] == 50
