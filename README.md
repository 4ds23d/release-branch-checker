# Release Branch Checker

Release Branch Checker to narzędzie napisane w Pythonie, które sprawdza, czy gałąź release została scalona z określoną gałęzią końcową (develop lub master). Projekt ten jest przydatny w procesie zarządzania wersjami w projektach opartych na systemie kontroli wersji Git.

## Spis treści

- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [Testowanie](#testowanie)
- [Licencja](#licencja)

## Wymagania

- Python 3.x
- Biblioteki do operacji na Git (np. GitPython)

## Instalacja

1. Sklonuj repozytorium:
   ```
   git clone <URL_REPOZYTORIUM>
   cd release-branch-checker
   ```

2. Zainstaluj wymagane biblioteki:
   ```
   pip install -r requirements.txt
   ```

## Użycie

Aby sprawdzić, czy gałąź release została scalona z gałęzią końcową, uruchom skrypt `main.py`:

```
python src/main.py
```

Upewnij się, że odpowiednie gałęzie są dostępne w lokalnym repozytorium.

## Testowanie

Aby uruchomić testy jednostkowe, użyj polecenia:

```
pytest tests/test_main.py
```

## Licencja

Ten projekt jest objęty licencją MIT. Zobacz plik LICENSE, aby uzyskać więcej informacji.