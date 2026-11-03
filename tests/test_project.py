from src.common.config import settings
from src.discovery.run import score
def test_daily_target():assert settings()["target_videos_per_day"]==3
def test_score_bounds():assert 0<=score("Amazing hidden ocean discovery","beautiful unusual place in the world")<=100
