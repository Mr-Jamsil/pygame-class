# pygame-class

## 셋팅

- Terminal -> New Terminal
- Command Prompt 열기 (+버튼 옆에)
- `python -m venv .venv`
- `.\.venv\Scripts\activate.bat`
- ---> (.venv) 가 보여야 함.

- 처음 패키지 설치
```shell
pip install pygame
pip install black isort 
pip freeze > requirements.txt
```

- 패키지 재설치 (reqirements.txt가 있을 경우)
```shell
pip install -r requirements.txt
```

## Troubleshooting

### `SyntaxError: invalid syntax`

해결방법 : 터미널 종료하고 다시 실행하기

터미널 종료는 휴지통 모양 클릭

```shell
>>> /Users/jwseo/GitHub/game-class/.venv/bin/python /Users/jwseo/GitHub/game-class/main0.py
  File "<stdin>", line 1
    /Users/jwseo/GitHub/game-class/.venv/bin/python /Users/jwseo/GitHub/game-class/main0.py
    ^
SyntaxError: invalid syntax
```

### `pygame.init() AttributeError: module 'pygame' has no attribute 'init'`

해결방법 : `.venv` 폴더 지우고, 가상환경 다시 만들기

