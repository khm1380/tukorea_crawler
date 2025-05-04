import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.tukorea.base_crawler import BaseCrawler, handle_errors
from src.util.logger import get_logger

logger = get_logger(__name__)

SCRIPT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "util", "click_simulator.js"
)


class DormApplication(BaseCrawler):
    # 부속행정 ID
    FIRST_ID = "mainframe_VFrameSet_TopFrame_form_mb_topMenu_MPA0001"

    # 외박신청 그리드 셀 ID
    NAMESPACE = "mainframe_VFrameSet_HFrameSet_leftFrame_form_grd_leftMenu_body_gridrow_10_cell_10_0"

    # 조회 버튼 ID
    SEARCH_ID = (
        "mainframe_VFrameSet_HFrameSet_VFrameSet1_WorkFrame_Child_"
        "MPB0022_form_div_Work_div_search_btn_search"
    )

    def __init__(self, driver):
        """
        생성자: WebDriver 인스턴스 검증 및 script file
        :param driver: Selenium WebDriver
        """
        super().__init__(driver)

        if not os.path.isfile(SCRIPT_PATH):
            logger.error("스크립트 파일 없음 : %s", SCRIPT_PATH)
            raise FileNotFoundError(f"script file missing {SCRIPT_PATH}")

        # 스크립트 문자열로 저장
        with open(SCRIPT_PATH, encoding="utf-8") as f:
            self.click_js = f.read()

    @handle_errors()
    def search_applications(self):
        # 생활관 외박신청 조회 메서드

        wait = WebDriverWait(self.driver, self.timeout)

        def simulate_click(el, desc: str):
            """
            Nexacro UI에서 안정적인 클릭을 위해 JS로 마우스 이벤트 시뮬레이션 수행

            :param el: 클릭할 WebElement
            :param desc: 이 클릭이 의미하는 설명 문자열
            """
            self.driver.execute_script(self.click_js, el)
            time.sleep(0.5)
            logger.info(f"[Clicked] {desc}")

        # TODO
        # 생활관 외박신청 조회 부분 최적화 고민
        # 반복적으로 해결할지, 아니면 이렇게 절차적으로 할지

        temp_menu = ["부속행정", "생활관", "외박신청", "조회"]

        logger.info(f"{temp_menu[0]} 메뉴 클릭 대기")
        el1 = wait.until(EC.element_to_be_clickable((By.ID, self.FIRST_ID)))
        simulate_click(el1, f"{temp_menu[0]} 메뉴")

        logger.info(f"{temp_menu[1]} 메뉴 클릭 대기")
        el2 = wait.until(lambda d: next(
            (e for e in d.find_elements(By.CSS_SELECTOR, "div")
             if e.text.strip() == f"{temp_menu[1]}"),
            None
        ))
        if not el2:
            logger.error(f"{temp_menu[1]} 요소를 찾지 못함")
            raise RuntimeError(f"{temp_menu[1]} 요소를 찾지 못함")
        simulate_click(el2, f"{temp_menu[1]}생활관 메뉴")

        logger.info(f"{temp_menu[2]} 메뉴 클릭 대기")
        el3 = wait.until(EC.element_to_be_clickable((By.ID, self.NAMESPACE)))
        simulate_click(el3, f"{temp_menu[2]} 항목")

        logger.info(f"{temp_menu[3]}  클릭 대기 중…")
        el4 = wait.until(EC.element_to_be_clickable((By.ID, self.SEARCH_ID)))
        simulate_click(el4, f"{temp_menu[3]} 버튼")

        logger.info("조회 완료!!")
