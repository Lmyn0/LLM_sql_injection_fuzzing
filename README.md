# LLM SQL Injection Fuzzing Reenactment

이 프로젝트는 LLM 기반의 자동화된 SQL 인젝션(Fuzzing) 루프를 재현하기 위한 테스트 베드 환경입니다.

## 환경 구성 (Prerequisites)
* XAMPP (Apache, MySQL)
* PHP 8.x
* MySQL (MariaDB)

## 실행 방법
1. XAMPP에서 Apache와 MySQL을 실행합니다.
2. `schema.sql` 파일을 복사하여 `http://localhost/phpmyadmin/` SQL 탭에서 실행 (Database & Table 생성).
3. `login.php` 파일을 로컬 서버 경로(`C:/xampp/htdocs/fuzzing_test/`)에 배치합니다.
4. `http://localhost/fuzzing_test/login.php`로 접속하여 정상 작동 여부를 확인합니다.
