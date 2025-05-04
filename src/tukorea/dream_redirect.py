from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.tukorea.base_crawler import BaseCrawler, handle_errors
from src.tukorea.dorm_application import DormApplication
from src.util.logger import get_logger

logger = get_logger(__name__)


class DreamRedirect(BaseCrawler):
    """
    포털 로그인 후 통합정보시스템 탭으로 이동하고,
    해당 탭에서 생활관 외박신청 조회 기능을 호출하는 클래스
    """

    TARGET_PREFIX = "https://dream.tukorea.ac.kr/nx/"
    SELECTOR_MENU = (By.XPATH, "//a[@title=\"통합정보시스템\"]")

    @handle_errors()
    def redirect(self):
        """
        메인 포털에서 통합정보시스템 이동 -> 외박신청 조회 기능 메서드 호출
        """

        #TODO
        # 로그 및 코드 최적화 예정

        logger.info("[DreamRedirect] 시작")
        wait = WebDriverWait(self.driver, self.timeout)

        original_handles = set(self.driver.window_handles)

        logger.info("통합정보시스템 메뉴 클릭 대기 중...")
        wait.until(EC.element_to_be_clickable(self.SELECTOR_MENU)).click()

        wait.until(lambda d: len(d.window_handles) > len(original_handles))
        new_handle = (set(self.driver.window_handles) - original_handles).pop()
        self.driver.switch_to.window(new_handle)
        logger.info(f"새 탭으로 전환: {new_handle}")

        wait.until(EC.url_contains(self.TARGET_PREFIX))
        logger.info("Dream 시스템 로드 완료: %s", self.driver.current_url)

        logger.info("생활관 외박신청 조회 시작")
        DormApplication(self.driver).search_applications()
        logger.info("DreamRedirect 완료")