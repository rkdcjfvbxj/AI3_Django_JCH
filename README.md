# Django Todo List

Django 5.2 / MySQL 기반 할 일 관리 과제입니다. Python 3.10 이상과 MySQL 8.0.11 이상이 필요합니다.

제출 저장소: https://github.com/rkdcjfvbxj/AI3_Django_JCH

## 구현 기능

- 제목(필수, 최대 200자), 세부 내용(선택), 완료 여부(기본 False), 생성 일시(자동 입력)
- 할 일 등록 / 목록 / 수정 / 삭제 확인
- 목록 체크박스로 완료·미완료 전환, 완료 항목 취소선 및 배경색
- 등록·수정 서버 유효성 검사: 빈 제목, 공백 제목, 200자 초과 제목 오류 표시 및 입력값 유지
- Django 템플릿 `{% for %}` 반복, `{% empty %}` 빈 목록 안내
- 모든 변경 요청에 CSRF 적용, 완료 전환 POST 전용, 출력 HTML 자동 이스케이프
- 관리자 Todo 목록 / 검색 / 필터 / 완료 상태 편집
- 반응형 한국어 UI

## Windows PowerShell 실행

```powershell
git clone https://github.com/rkdcjfvbxj/AI3_Django_JCH.git
cd AI3_Django_JCH
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`의 DB 계정·비밀번호를 실제 MySQL 값으로 수정하세요. `DJANGO_SECRET_KEY`도 임의의 긴 문자열로 변경합니다. `.env`는 Git에 포함되지 않습니다.

MySQL 관리자 계정으로 다음을 실행하세요. 비밀번호는 `.env`와 동일하게 설정합니다.

```sql
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'change-this-password';
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
```

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

- 서비스: http://127.0.0.1:8000/
- 관리자: http://127.0.0.1:8000/admin/ (위에서 만든 관리자 계정)

Linux/macOS에서는 `python3 -m venv .venv` 후 `.venv/bin/python`을 사용하세요. Ubuntu에서 mysqlclient 빌드에 필요한 패키지는 `python3-dev default-libmysqlclient-dev build-essential pkg-config`입니다.

## MySQL 설정

`config/settings.py`의 기본 DB는 `django.db.backends.mysql`입니다. `.env`의 `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`를 읽고 `utf8mb4`와 `STRICT_TRANS_TABLES`를 설정합니다. 시간은 UTC 저장, Asia/Seoul 표시입니다.

## 테이블 생성 DDL

제출용 코드는 [sql/schema.sql](sql/schema.sql)에 있습니다. 앱의 실제 테이블 생성은 `migrate`를 사용하세요. DDL을 먼저 실행한 뒤 일반 migrate를 실행하면 테이블 중복 오류가 발생하므로 두 방식을 함께 실행하지 마세요. Django 관리자·인증·세션 테이블도 migrate가 생성합니다.

`content` 선택 입력은 `blank=True`로 처리하며 NULL 대신 빈 문자열을 저장합니다. `created_at`은 Django `auto_now_add`가 자동 입력합니다. 완료 기본값은 모델과 DB 모두 False입니다.

## 검증

```powershell
# 실제 MySQL 연결 및 시스템 검사
.\.venv\Scripts\python.exe manage.py check --database default
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
# MySQL 통합 테스트 (테스트 DB 생성 권한이 있는 계정 필요)
.\.venv\Scripts\python.exe manage.py test
# MySQL 서버 없이 기능을 검증하는 보조 테스트
.\.venv\Scripts\python.exe manage.py test --settings=config.test_settings
```

기본 실행 설정은 항상 MySQL이며 `config.test_settings`는 명시적으로 지정할 때만 SQLite 메모리 DB를 사용하는 테스트 설정입니다.

## 파일 구조

- `config/settings.py`: MySQL 및 Django 설정
- `todos/models.py`, `migrations/`: Todo 모델과 DB 마이그레이션
- `todos/forms.py`: 등록·수정 유효성 검사
- `todos/views.py`, `urls.py`: CRUD 및 완료 처리
- `todos/templates/todos/`, `static/todos/`: 화면 및 스타일
- `todos/admin.py`: 관리자 등록
- `todos/tests.py`: 기능·보안 테스트
- `sql/schema.sql`: 제출용 MySQL DDL

이 앱은 과제용 공용 Todo 목록입니다. 사용자별 목록 분리는 포함하지 않습니다. 공개 서비스 운영 시에는 로그인 및 접근 권한을 추가해야 합니다.

참고: [Django 공식 MySQL 문서](https://docs.djangoproject.com/en/5.2/ref/databases/#mysql-notes)
