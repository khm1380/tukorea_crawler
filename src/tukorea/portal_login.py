from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.tukorea.base_crawler import BaseCrawler, handle_errors
from src.util.webdriver_init import configure_driver
from src.util.logger import get_logger

logger = get_logger(__name__)

"""
tukorea 크롤링시 진입지점

------
한번 로그인 한 것을 user 세션으로 저장하고 처리할수도 있지만, 일단 무조건 적으로 portal_login 후에 작동되도록 만들 예정
------
"""

"""
PortalLogin

포털(Single Sign-On) 로그인 처리 클래스
- WebDriver 초기화 및 설정
- 로그인 수행 후 지정된 포털 메인 페이지 로딩까지 대기
"""


class PortalLogin(BaseCrawler):
    LOGIN_URL = 'https://ksc.tukorea.ac.kr/sso/login_stand.jsp'

    SELECTORS = {
        'tab_login': (By.ID, 'interLogin'),
        'input_id': (By.ID, 'internalId'),
        'input_pw': (By.ID, 'internalPw'),
        'btn_login': (By.ID, 'internalLogin'),
    }

    def __init__(
            self,
            user_id: str,
            password: str,
            headless: bool = True
    ):
        """
        생성자: WebDriver 설정 및 사용자 정보 저장

       :param user_id: 포털 로그인에 사용할 사용자 ID
       :param password: 포털 로그인 비밀번호
       :param headless: 기본 headless True
       """

        driver = configure_driver(headless)
        super().__init__(driver)
        self.user_id = user_id
        self.password = password

    # 일시적 오류가 발생할 수 있어 1회 재시도 하기
    @handle_errors(retry=1, retry_exceptions=(Exception,))
    def login(self):

        #TODO
        # 로그랑 로직 무조건 수정 예정

        logger.info("[PortalLogin] 로그인 시작")

        self.driver.get(self.LOGIN_URL)
        wait = WebDriverWait(self.driver, self.timeout)

        logger.debug("내부 로그인 탭 클릭 대기 중...")
        wait.until(EC.element_to_be_clickable(self.SELECTORS["tab_login"])).click()

        logger.debug("사용자 ID 입력 대기 중...")
        wait.until(EC.presence_of_element_located(self.SELECTORS["input_id"]))
        self.driver.find_element(*self.SELECTORS["input_id"]).send_keys(self.user_id)

        logger.debug("비밀번호 입력 및 로그인 버튼 클릭")
        self.driver.find_element(*self.SELECTORS["input_pw"]).send_keys(self.password)
        self.driver.find_element(*self.SELECTORS["btn_login"]).click()

        logger.debug("로그인 성공 페이지 대기 중...")
        wait.until(EC.url_contains("/portal/default/stu"))
        logger.info('Portal login success (%s)', self.driver.current_url)
