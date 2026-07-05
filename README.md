# LLM SQL Injection Fuzzing Reenactment

## 프로젝트 개요

이 프로젝트는 **LLM(Large Language Model)** 을 이용한 SQL Injection Fuzzing 기법을 재현하기 위한 연구 프로젝트입니다.

논문의 전체 파이프라인(Fuzz Function → SQL Function → Mutator → Detector → DBMS)을 단계적으로 구현하는 것을 목표로 합니다.

현재 구현된 단계는 다음과 같습니다.

- Input Vector 생성
- Fuzz Function을 이용한 Trace 삽입
- SQL Function을 통한 Trace 기반 SQL 생성
- LLM(Mutator)을 이용한 Payload 생성
- Payload Parsing
- Final SQL 생성
---

## 프로젝트 구조

```
LLM_SQL
│
├── dataset/
├── prompts/
│   ├── mutator_prompt.txt
│   └── detector_prompt.txt
│
├── runner.py
├── fuzzer.py
├── mutator.py
├── detector.py
├── fuzz_loop.py
├── llm.py
│
├── test_fuzzer.py
├── test_login.py
└── test_mutator.py
```

---

## 개발 환경

- Python 3.14
- Ollama
- Llama 3.2
- XAMPP (Apache + MariaDB)
- PHP 8.x

---

## 웹 애플리케이션 환경

1. XAMPP에서 Apache와 MySQL을 실행합니다.

2. `schema.sql`을 phpMyAdmin에서 실행하여 데이터베이스와 테이블을 생성합니다.

3. `login.php`를 아래 경로에 배치합니다.

```
C:\xampp\htdocs\fuzzing_test\
```

4. 브라우저에서 정상 동작 여부를 확인합니다.

```
http://localhost/fuzzing_test/login.php
```

---

## 실행 방법

### 1. Fuzzer 테스트

```bash
python test_fuzzer.py
```

### 2. Mutator 테스트

```bash
python test_mutator.py
```

### 3. 전체 파이프라인 실행

```bash
python runner.py
```

---

## 현재 구현 상태

| 단계 | 구현 여부 |
|------|----------|
| Input Vector | ✅ |
| Fuzz Function | ✅ |
| SQL Function | ✅ |
| Mutator | ✅ |
| Payload Parsing | ✅ |
| Final SQL Generation | ✅ |
| Detector | 🚧 진행 중 |
| DBMS Execution | 🚧 진행 중 |
| Logging | 🚧 진행 중 |

---

## 참고

본 프로젝트는 **LLM 기반 SQL Injection Fuzzing 논문**을 기반으로 구현한 연구용 프로젝트입니다.
