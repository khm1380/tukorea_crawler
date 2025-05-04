import time
import logging
from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.util.webdriver_init import configure_driver
class PortalLogin:
    LOGIN_URL = "https://ksc.tukorea.ac.kr/sso/login_stand.jsp"
    TIMEOUT = 20

    def __init__(
        self,
        user_id: str,
        password: str,
        headless: bool = True,
        close_on_exit: bool = True,
    ):
        if not user_id or not password:
            raise ValueError("User ID and password must be provided")
        self.user_id = user_id
        self.password = password
        self.close_on_exit = close_on_exit
        self.driver = configure_driver(headless)
        self.logger = logging.getLogger(__name__)

    def login(self) -> None:
        self.logger.info("PortalLogin: 로그인 시작")
        self.driver.get(self.LOGIN_URL)

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "interLogin"))
        ).click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "internalId"))
        ).send_keys(self.user_id)
        self.driver.find_element(By.ID, "internalPw").send_keys(self.password)
        self.driver.find_element(By.ID, "internalLogin").click()

        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.url_contains("/portal/default/stu")
            )
            self.logger.info(f"로그인 성공: {self.driver.current_url}")
        except Exception:
            self.logger.exception("로그인 실패")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.close_on_exit:
            self.logger.info("브라우저 세션 종료 (quit)")
            self.driver.quit()
        else:
            self.logger.info("브라우저 세션 유지 (quit 건너뜀)")
