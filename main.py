import logging
from src.util.logger import configure_logging
from src.util.env_config import load_config
from src.tukorea.portal_login import PortalLogin
from src.tukorea.dream_redirect import DreamRedirect

configure_logging()
logger = logging.getLogger(__name__)

try:
    user_id, password = load_config()

    with PortalLogin(user_id, password, headless=False, close_on_exit=False) as portal:
        portal.login()
        DreamRedirect(portal.driver).redirect()

except Exception:
    logger.exception("error")
