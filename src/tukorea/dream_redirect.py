import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DreamRedirect:
    TARGET_PREFIX = "https://dream.tukorea.ac.kr/nx/"
    TIMEOUT = 20

    def __init__(self, driver):
        if driver is None:
            raise ValueError("WebDriver must be initialized before redirect")
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def redirect(self) -> None:
        self.logger.info("DreamRedirect 시도")

        existing = set(self.driver.window_handles)

        menu = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='통합정보시스템']"))
        )
        menu.click()
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.window_handles) > len(existing)
        )

        new_win = (set(self.driver.window_handles) - existing).pop()
        self.driver.switch_to.window(new_win)

        start = time.time()
        while time.time() - start < self.TIMEOUT:
            if self.driver.current_url.startswith(self.TARGET_PREFIX):
                self.logger.info(f"DreamRedirect 성공: {self.driver.current_url}")
                break
            time.sleep(1)
        else:
            raise RuntimeError("redirect timed out")

        self._click_nexacro_sequence()

    def _click_nexacro_sequence(self):

        def simulate_click(el):

            dir_here = os.path.dirname(os.path.realpath(__file__))
            js_file = os.path.normpath(os.path.join(dir_here, '..', 'util', 'click_simulator.js'))
            if not os.path.isfile(js_file):
                raise FileNotFoundError(f"click_simulator.js not found at {js_file}")
            with open(js_file, 'r', encoding='utf-8') as f:
                js = f.read()
            self.driver.execute_script(js, el)

        first_id = 'mainframe_VFrameSet_TopFrame_form_mb_topMenu_MPA0001'
        self.logger.info("1) 부속행정 대기 중…")
        first_el = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, first_id))
        )
        simulate_click(first_el)

        self.logger.info("2) 생활관 대기 중…")
        second_el = WebDriverWait(self.driver, self.TIMEOUT).until(lambda d:
            next((el for el in d.find_elements(By.CSS_SELECTOR, "div")
                  if el.text.strip() == "생활관"), None)
        )
        if not second_el:
            raise RuntimeError("생활관 요소를 찾지 못했습니다")
        simulate_click(second_el)

        third_id = 'mainframe_VFrameSet_HFrameSet_leftFrame_form_grd_leftMenu_body_gridrow_10_cell_10_0'
        self.logger.info("3) -외박신청 대기 중…")
        third_el = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, third_id))
        )
        simulate_click(third_el)

        search_id = (
            'mainframe_VFrameSet_HFrameSet_VFrameSet1_WorkFrame_Child_'
            'MPB0022_form_div_Work_div_search_btn_search'
        )
        self.logger.info("4) 조회 버튼 대기 중…")
        search_el = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, search_id))
        )
        simulate_click(search_el)

        self.logger.info("작업 완료")
