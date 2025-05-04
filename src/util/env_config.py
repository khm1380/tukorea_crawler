import os
import dotenv

def load_config() -> tuple:
    dotenv.load_dotenv()
    user = os.getenv("TUKOREA_ID")
    pw = os.getenv("TUKOREA_PW")
    if not user or not pw:
        raise EnvironmentError(".env 파일에 TUKOREA_ID/TUKOREA_PW 설정 필요")
    return user, pw
