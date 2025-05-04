from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def configure_driver(
        headless: bool = True,
        page_load_timeout: int = 60,
        implicit_wait: int = 10
) -> webdriver.Chrome:
    """
    Selenium Chrome WebDriver 초기화
    """
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if headless:
        opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver.set_window_size(1280, 800)
    driver.set_page_load_timeout(page_load_timeout)
    driver.implicitly_wait(implicit_wait)
    return driver
