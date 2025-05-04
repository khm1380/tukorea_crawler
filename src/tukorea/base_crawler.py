import os
import time
import functools
from src.util.logger import get_logger

logger = get_logger(__name__)


def handle_errors(retry: int = 0, retry_exceptions: tuple = ()):
    # 예외 발생 시 스택·스크린샷 기록, 필요 시 재시도
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            attempts = 0
            while True:
                try:

                    return func(self, *args, **kwargs)
                except Exception as e:
                    logger.exception(f"[{func.__name__}] 실행 중 오류: {e}")

                    # 스크린샷 저장
                    try:
                        os.makedirs('screenshots', exist_ok=True)
                        fname = f"screenshots/{func.__name__}_{int(time.time())}.png"
                        self.driver.save_screenshot(fname)

                        logger.info(f"[Screenshots] 저장 완료: {fname}")

                    except Exception as se:
                        logger.warning(f"[Screenshots] 실패: {se}")

                    if attempts < retry and isinstance(e, retry_exceptions):
                        attempts += 1
                        logger.info(f"[Retry] {func.__name__} ({attempts}/{retry})")

                        time.sleep(1)
                        continue

                    logger.critical(f"{func.__name__}")
                    raise

        return wrapper

    return decorator


class BaseCrawler:
    def __init__(self, driver):
        if not driver:
            raise ValueError("WebDriver 미입력")
        self.driver = driver
        self.timeout = getattr(self, 'TIMEOUT', 20)

    def __enter__(self):
        logger.debug("[Context] 세션 시작")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error(f"[Context] 얘외 발생 종료: {exc_val}")
        else:
            logger.debug("[Context] 정상 종료")
        self.driver.quit()
