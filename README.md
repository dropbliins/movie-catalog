# Katalog kolekcji filmów (Movie Catalog)

Aplikacja webowa do zarządzania kolekcją filmów, napisana we wzorcu MVC.
Pozwala przeglądać i wyszukiwać filmy, oglądać ich szczegóły, a po zalogowaniu
dodawać je do ulubionych. Administrator zarządza całym katalogiem.

## Spis treści

- [Opis projektu](#opis-projektu)
- [Zrzuty ekranu](#zrzuty-ekranu)
- [Funkcjonalności](#funkcjonalności)
- [Wzorzec MVC w projekcie](#wzorzec-mvc-w-projekcie)
- [Struktura projektu](#struktura-projektu)
- [Wykorzystane technologie](#wykorzystane-technologie)
- [Wymagania](#wymagania)
- [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
- [Konto administratora](#konto-administratora)
- [Dane w aplikacji](#dane-w-aplikacji)

## Opis projektu

Każdy film ma tytuł, reżysera, rok, ocenę, plakat i opis. Dane trzymane są
w bazie PostgreSQL uruchamianej w Dockerze. Aplikacja rozróżnia gościa,
zalogowanego użytkownika i administratora, a każdy z nich ma inne uprawnienia.

## Zrzuty ekranu

### Strona główna — katalog filmów
![Strona główna](screenshots/home.png)

### Logowanie
![Logowanie](screenshots/login.png)

### Rejestracja
![Rejestracja](screenshots/register.png)

## Funkcjonalności

- Katalog filmów w formie siatki plakatów
- Strona pojedynczego filmu (plakat, reżyser, rok, ocena, opis)
- Wyszukiwanie po tytule lub reżyserze
- Sortowanie po ocenie, roku lub tytule
- Podział wyników na strony (paginacja)
- Dodawanie, edycja i usuwanie filmów (administrator)
- Walidacja danych po stronie serwera i klienta
- Rejestracja, logowanie i wylogowanie oparte na sesjach
- Role: administrator zarządza filmami, użytkownik tylko przegląda
- Ulubione filmy dla zalogowanych użytkowników (relacja wiele-do-wielu)
- Ciemny, responsywny interfejs z własnym motywem

## Wzorzec MVC w projekcie

| Element MVC | Lokalizacja | Odpowiedzialność |
|---|---|---|
| **Model** | `models.py` | Definicje danych: `Film`, `User`, relacja `favorites` |
| **View (Widok)** | `templates/` | Szablony HTML (Jinja2) prezentujące dane |
| **Controller (Kontroler)** | `controllers/` | Obsługa żądań HTTP, logika, łączenie modelu z widokiem |

## Struktura projektu

```
movie-catalog/
├── app.py              # punkt wejścia, uruchamia aplikację
├── extensions.py       # współdzielone obiekty (baza, logowanie)
├── models.py           # Model: Film, User, relacja favorites
├── validators.py       # walidacja formularza
├── decorators.py       # kontrola dostępu administratora
├── controllers/        # Kontrolery (trasy):
│   ├── films.py        #   katalog i zarządzanie filmami
│   ├── favorites.py    #   ulubione
│   └── auth.py         #   rejestracja, logowanie, wylogowanie
├── templates/          # Widoki (szablony HTML)
├── static/             # style CSS i czcionki
├── import_data.py      # skrypt wczytujący dane do bazy
├── docker-compose.yml  # baza PostgreSQL w Dockerze
├── requirements.txt    # lista bibliotek
└── .env                # konfiguracja (baza, klucz sesji)
```

## Wykorzystane technologie

- Python + Flask
- Flask-SQLAlchemy (ORM)
- Flask-Login (logowanie i sesje)
- PostgreSQL + psycopg
- Docker (baza danych)
- Jinja2 i Bootstrap 5 (widoki i styl)

## Wymagania

- Python 3.12+
- Docker

## Instalacja i uruchomienie

Utwórz plik `.env` w katalogu projektu:

```
DATABASE_URL=postgresql+psycopg://movieuser:moviepass@localhost:5432/moviedb
SECRET_KEY=dowolny-tajny-ciag
```

Następnie:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d
python app.py
```

Aplikacja działa pod adresem http://127.0.0.1:5000. Tabele i konto administratora
tworzone są automatycznie przy pierwszym uruchomieniu.

## Konto administratora

Domyślne konto:

- login: `admin`
- hasło: `admin123`

Administrator widzi przyciski dodawania, edycji i usuwania filmów. Zwykły
użytkownik z rejestracji przegląda katalog i dodaje filmy do ulubionych.

## Dane w aplikacji

Katalog wypełniono publicznym zbiorem TMDB za pomocą skryptu `import_data.py`.
Skrypt wczytuje pliki CSV i zapisuje filmy do bazy. Uruchamia się go raz,
sama aplikacja go nie używa.
