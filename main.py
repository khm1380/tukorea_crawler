from src.util.env_config import load_config
from src.util.logger import get_logger
from src.tukorea.portal_login import PortalLogin
from src.tukorea.dream_redirect import DreamRedirect

logger = get_logger(__name__)


user_id, password, environment, headless = load_config()
logger.info(f"애플리케이션 환경: {environment}, headless: {headless}")
logger.info("🔍 크롤러 시작")

# TODO
"""
별도 크롤링 기능들 추가 예정
"""
with PortalLogin(user_id, password, headless=headless) as portal:
    portal.login()
    DreamRedirect(portal.driver).redirect()

