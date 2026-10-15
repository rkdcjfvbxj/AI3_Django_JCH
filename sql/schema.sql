-- MySQL 8.0.11+ / UTF-8 (한글, 이모지 지원)
CREATE DATABASE IF NOT EXISTS todo_db
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE todo_db;

-- 제출용 Todo 테이블 DDL. 앱 실행 시에는 migrate로 생성하세요.
-- default=False는 db_default=False를 통해 DB 기본값에도 반영됩니다.
-- created_at은 Django auto_now_add가 UTC 값을 INSERT합니다.
CREATE TABLE todos_todo (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content LONGTEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- 선택 입력인 content는 NULL 대신 빈 문자열('')로 저장합니다.
-- admin/auth/session 등 Django 기본 테이블은 python manage.py migrate가 생성합니다.
