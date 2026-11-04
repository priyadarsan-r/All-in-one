from unittest.mock import patch
import requests
from src.common.config import settings
from src.discovery.run import score
from src.assets.fetch import commons, DEFAULT_HEADERS

def test_daily_target():assert settings()["target_videos_per_day"]==3
def test_score_bounds():assert 0<=score("Amazing hidden ocean discovery","beautiful unusual place in the world")<=100

def test_user_agent_present():
    assert "User-Agent" in DEFAULT_HEADERS
    assert "python-requests" not in DEFAULT_HEADERS["User-Agent"]

def test_commons_handles_http_error_gracefully():
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error: Forbidden")
        res = commons("test query")
        assert res is None

