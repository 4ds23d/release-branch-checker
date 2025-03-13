# Release Branch Checker

Release Branch Checker to narzędzie do sprawdzania, czy gałęzie release zostały zmergowane do gałęzi finalnej (np. `develop` lub `master`). Narzędzie to działa w nie w pełni sklonowanych repozytoriach, gdzie czasami następuje checkout na konkretnym commicie.

## Funkcje

- Wyszukiwanie wszystkich gałęzi release nie starszych niż określona liczba dni.
- Automatyczne sprawdzanie, czy wszystkie te gałęzie zostały zmergowane do gałęzi finalnej.
- Konfiguracja zapisywana w pliku `.git/config`, aby nie przeszkadzać w działaniu Git-a.

## Instalacja

1. Sklonuj repozytorium:
    ```sh
    git clone <URL_REPOZYTORIUM>
    cd release-branch-checker
    ```

2. Zainstaluj wymagane zależności (jeśli są jakieś dodatkowe):
    ```sh
    pip install -r requirements.txt
    ```

## Użycie

1. Uruchom skrypt [main.py](http://_vscodecontentref_/1):
    ```sh
    python src/main.py
    ```

2. Przy pierwszym uruchomieniu zostaniesz poproszony o podanie konfiguracji:
    - Nazwa gałęzi finalnej (np. `develop` lub `master`)
    - Wzór dla gałęzi release (np. `release/`)
    - Maksymalna liczba dni, jaką może mieć gałąź release

3. Skrypt automatycznie sprawdzi, czy wszystkie gałęzie release nie starsze niż określona liczba dni zostały zmergowane do gałęzi finalnej.

## Testowanie

Aby uruchomić testy, użyj `unittest`:

```sh
python -m unittest discover -s tests