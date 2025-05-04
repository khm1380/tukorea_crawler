import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_config(env_path: str = None) -> tuple:
    environment = os.environ.get('ENVIRONMENT', 'prod').lower()

    if env_path and os.path.isfile(env_path):
        chosen_env = env_path
    else:
        env_file_specific = f'.env.{environment}'
        if os.path.isfile(env_file_specific):
            chosen_env = env_file_specific
        elif os.path.isfile('.env'):
            chosen_env = '.env'
        else:
            chosen_env = None

    if chosen_env:
        logger.info(f"'{chosen_env}'에서 환경변수 로드")
        load_dotenv(chosen_env, override=False)
    else:
        logger.warning("설정 파일을 찾지 못했습니다.")

    user = os.getenv('TUKOREA_ID')
    pw = os.getenv('TUKOREA_PW')
    if not user or not pw:
        raise EnvironmentError(
            "TUKOREA_ID와 TUKOREA_PW를 환경변수 또는 .env 파일에 설정해주세요."
        )

    headless = False if environment == 'dev' else True

    return user, pw, environment, headless