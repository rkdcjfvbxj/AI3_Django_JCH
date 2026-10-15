# MySQL 서버 없이 실행하는 보조 테스트 전용 설정입니다.
from .settings import *  # noqa: F403
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
