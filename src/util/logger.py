import logging
import os
from logging.handlers import RotatingFileHandler

#TODO
# 로그설정 다시 할 예정

LOG_FILE = os.getenv('CRAWLER_LOG_FILE', 'logs/crawler.log')
LOG_LEVEL = os.getenv('CRAWLER_LOG_LEVEL', 'INFO').upper()
VALID_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def get_logger(name: str) -> logging.Logger:
    """
    모듈별로 일관된 로거 반환
    - 콘솔 + 파일(Rotating) 핸들러
    - 로그 디렉터리 자동 생성
    - 레벨 유효성 검증
    """
    # 로그 디렉터리 확인 및 생성
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    level = LOG_LEVEL if LOG_LEVEL in VALID_LEVELS else 'INFO'

    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(getattr(logging, level))
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s:%(funcName)s] %(message)s'
    )

    # 콘솔 핸들러
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # 파일 핸들러 (회전)
    fh = RotatingFileHandler(
        LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger