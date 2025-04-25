# API Endpoint Implementation Plan: User Preferences

## 1. Przegląd endpointu

Ten plan obejmuje implementację dwóch endpointów REST API służących do zarządzania preferencjami użytkownika w aplikacji ShelfSense:

1.  **`GET /users/me/preferences`**: Pobiera preferencje zalogowanego użytkownika.
2.  **`PUT /users/me/preferences`**: Ustawia lub aktualizuje preferencje zalogowanego użytkownika.

Oba endpointy wymagają uwierzytelnienia użytkownika za pomocą tokenu JWT.

## 2. Szczegóły żądania

### GET /users/me/preferences
-   **Metoda HTTP**: `GET`
-   **Ścieżka URL**: `/users/me/preferences`
-   **Parametry ścieżki**: Brak
-   **Parametry zapytania**: Brak
-   **Headers**:
    -   `Authorization: Bearer <token>` (Wymagany - JWT token dostępowy)
-   **Request Body**: Brak

### PUT /users/me/preferences
-   **Metoda HTTP**: `PUT`
-   **Ścieżka URL**: `/users/me/preferences`
-   **Parametry ścieżki**: Brak
-   **Parametry zapytania**: Brak
-   **Headers**:
    -   `Authorization: Bearer <token>` (Wymagany - JWT token dostępowy)
-   **Request Body**: Schemat Pydantic `schemas.PreferenceRequest`
    ```json
    {
      "preferences_text": "string" 
    }
    ```
    -   `preferences_text`: Musi być niepustym stringiem (`min_length=1`).

## 3. Modele danych

-   **Modele Pydantic (`app/schemas.py`)**:
    -   Request (`PUT`): `PreferenceRequest`
    -   Response (`GET`, `PUT`): `PreferenceResponse`
-   **Modele SQLAlchemy (`app/models.py`)**:
    -   `UserPreference`: Mapowanie tabeli `shelfsense.user_preferences`. Kluczowe pola: `id`, `user_id`, `preferences_text`, `created_at`, `updated_at`.
    -   `User`: Potrzebny do pobrania `user_id` z uwierzytelnionego użytkownika.

## 4. Szczegóły odpowiedzi

### GET /users/me/preferences
-   **Sukces (200 OK)**: Zwraca obiekt JSON zgodny ze schematem `schemas.PreferenceResponse`.
    ```json
    {
      "id": "uuid",
      "preferences_text": "string",
      "updated_at": "string (datetime)"
    }
    ```
-   **Błędy**:
    -   `401 Unauthorized`: Nieprawidłowy lub brakujący token JWT.
    -   `404 Not Found`: Użytkownik jest uwierzytelniony, ale nie ma jeszcze ustawionych preferencji.
    -   `500 Internal Server Error`: Błąd serwera (np. problem z bazą danych).

### PUT /users/me/preferences
-   **Sukces (200 OK)**: Zwraca obiekt JSON zgodny ze schematem `schemas.PreferenceResponse` z utworzonymi lub zaktualizowanymi danymi.
    ```json
    {
      "id": "uuid",
      "preferences_text": "string",
      "updated_at": "string (datetime)"
    }
    ```
-   **Błędy**:
    -   `400 Bad Request`: Nieprawidłowe ciało żądania (np. pusty `preferences_text`). Walidacja Pydantic.
    -   `401 Unauthorized`: Nieprawidłowy lub brakujący token JWT.
    -   `500 Internal Server Error`: Błąd serwera (np. problem z bazą danych podczas zapisu).

## 5. Przepływ danych

### GET /users/me/preferences
1.  Odebranie żądania `GET`.
2.  Weryfikacja tokenu JWT przez zależność `get_current_user`. Pobranie `user_id`.
3.  Wywołanie funkcji serwisowej `preferences_service.get_user_preferences(db, user_id)`.
4.  Serwis odpytuje bazę danych (SQLAlchemy) o rekord w `shelfsense.user_preferences` dla danego `user_id`.
5.  Jeśli rekord istnieje, jest zwracany do endpointu.
6.  Jeśli rekord nie istnieje, serwis zwraca `None`. Endpoint zwraca `404 Not Found`.
7.  Endpoint konwertuje model SQLAlchemy na model Pydantic `PreferenceResponse` i zwraca odpowiedź 200 OK.

### PUT /users/me/preferences
1.  Odebranie żądania `PUT`.
2.  Weryfikacja tokenu JWT przez zależność `get_current_user`. Pobranie `user_id`.
3.  Walidacja ciała żądania przez FastAPI względem modelu `schemas.PreferenceRequest`. W razie błędu zwracane jest 400.
4.  Wywołanie funkcji serwisowej `preferences_service.upsert_user_preferences(db, user_id, preference_data)`.
5.  Serwis sprawdza, czy preferencje dla `user_id` już istnieją w bazie danych.
6.  Jeśli istnieją: Aktualizuje istniejący rekord (`UPDATE`).
7.  Jeśli nie istnieją: Tworzy nowy rekord (`INSERT`).
8.  SQLAlchemy wykonuje operację `COMMIT`.
9.  Serwis zwraca utworzony/zaktualizowany model SQLAlchemy do endpointu.
10. Endpoint konwertuje model SQLAlchemy na model Pydantic `PreferenceResponse` i zwraca odpowiedź 200 OK.

## 6. Zależności FastAPI

-   `Depends(get_db)`: Wstrzykuje sesję SQLAlchemy (`db: Session`).
-   `Depends(get_current_user)`: Wstrzykuje uwierzytelniony model użytkownika (`current_user: models.User`). Ta zależność musi obsługiwać weryfikację tokenu JWT.

## 7. Względy bezpieczeństwa

-   **Uwierzytelnianie**: Wymagany ważny token JWT (przekazywany w nagłówku `Authorization: Bearer <token>`). Obsługiwane przez zależność `get_current_user`.
-   **Autoryzacja**: Użytkownik może modyfikować i odczytywać tylko *własne* preferencje. Jest to zapewnione przez:
    -   Użycie `user_id` z `current_user` w logice serwisowej.
    -   Politykę RLS `user_manage_own_preferences` w PostgreSQL, która dodatkowo zabezpiecza dostęp na poziomie bazy danych.
-   **Walidacja danych wejściowych**: Pydantic (`PreferenceRequest`) zapewnia, że `preferences_text` jest poprawnym, niepustym stringiem.
-   **Ochrona przed SQL Injection**: Użycie SQLAlchemy ORM minimalizuje ryzyko.

## 8. Obsługa błędów

-   **400 Bad Request**: Zwracany automatycznie przez FastAPI/Pydantic w przypadku nieprawidłowego formatu `PUT` request body.
-   **401 Unauthorized**: Zwracany przez zależność `get_current_user` w przypadku problemów z tokenem JWT. Należy użyć `HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})`.
-   **404 Not Found**: Zwracany przez endpoint `GET`, gdy preferencje dla użytkownika nie istnieją. Należy użyć `HTTPException(status_code=404, detail="User preferences not found")`.
-   **500 Internal Server Error**: Ogólne błędy serwera (np. błędy bazy danych podczas zapisu/odczytu). Należy logować szczegóły błędu po stronie serwera i zwracać generyczny komunikat `HTTPException(status_code=500, detail="Internal server error")`.

## 9. Rozważania wydajnościowe

-   Operacje na tabeli `user_preferences` są proste (odczyt/zapis pojedynczego wiersza po `user_id`).
-   Indeks `idx_user_preferences_user_id` na kolumnie `user_id` zapewnia szybkie wyszukiwanie.
-   Obciążenie tych endpointów powinno być niskie. Użycie `async def` dla endpointów jest zgodne z najlepszymi praktykami FastAPI, ale operacje DB z SQLAlchemy (w domyślnej konfiguracji) są synchroniczne. W razie potrzeby można rozważyć `databases` lub asynchroniczne sterowniki.

## 10. Kroki implementacji

1.  **Utworzenie modułu serwisowego**: Stworzyć plik `app/services/preferences_service.py`.
2.  **Implementacja logiki serwisowej**:
    -   Dodać funkcję `get_user_preferences(db: Session, user_id: UUID) -> models.UserPreference | None`.
    -   Dodać funkcję `upsert_user_preferences(db: Session, user_id: UUID, preferences_data: schemas.PreferenceRequest) -> models.UserPreference`.
3.  **Utworzenie modułu routera**: Stworzyć plik `app/routers/preferences.py` (lub dodać do istniejącego routera użytkownika, np. `users.py`).
4.  **Implementacja endpointu GET**:
    -   Dodać funkcję endpointu z dekoratorem `@router.get("/me/preferences", response_model=schemas.PreferenceResponse)`.
    -   Wstrzyknąć zależności `db` i `current_user`.
    -   Wywołać `preferences_service.get_user_preferences`.
    -   Obsłużyć przypadek `None` (404).
    -   Zwrócić wynik.
5.  **Implementacja endpointu PUT**:
    -   Dodać funkcję endpointu z dekoratorem `@router.put("/me/preferences", response_model=schemas.PreferenceResponse)`.
    -   Wstrzyknąć zależności `db`, `current_user` oraz ciało żądania `preferences: schemas.PreferenceRequest`.
    -   Wywołać `preferences_service.upsert_user_preferences`.
    -   Zwrócić wynik.
6.  **Rejestracja routera**: Dodać router preferencji do głównej aplikacji FastAPI w `app/main.py`.
7.  **Testy jednostkowe/integracyjne**: Napisać testy (pytest) dla funkcji serwisowych i endpointów, pokrywając przypadki sukcesu i błędów (w tym autoryzacji i walidacji).
8.  **Dokumentacja**: FastAPI automatycznie wygeneruje dokumentację OpenAPI (Swagger/ReDoc). Sprawdzić, czy opisy i schematy są poprawne.

## 11. Przykładowy kod implementacji (Ilustracja)

### `app/routers/preferences.py` (lub `users.py`)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated # Użycie Annotated dla lepszej czytelności zależności

from .. import schemas, models, dependencies, services # Załóżmy istnienie tych modułów

router = APIRouter(
    prefix="/users", # Lub inny odpowiedni prefix
    tags=["preferences"], # Tag dla dokumentacji OpenAPI
)

# Zależności wstrzykiwane do endpointów
DBSession = Annotated[Session, Depends(dependencies.get_db)]
CurrentUser = Annotated[models.User, Depends(dependencies.get_current_user)]

@router.get("/me/preferences", response_model=schemas.PreferenceResponse)
async def read_user_preferences(
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Retrieves the preferences for the currently authenticated user.
    """
    preferences = services.preferences_service.get_user_preferences(db, current_user.id)
    if preferences is None:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preferences

@router.put("/me/preferences", response_model=schemas.PreferenceResponse)
async def update_user_preferences(
    preferences_data: schemas.PreferenceRequest,
    db: DBSession,
    current_user: CurrentUser,
):
    """
    Sets or updates the preferences for the currently authenticated user.
    """
    # Walidacja Pydantic jest robiona automatycznie przez FastAPI
    try:
        updated_preferences = services.preferences_service.upsert_user_preferences(
            db=db, user_id=current_user.id, preferences_data=preferences_data
        )
        return updated_preferences
    except Exception as e:
        # Logowanie błędu po stronie serwera
        # logger.error(f"Error updating preferences for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating preferences")

```

### `app/services/preferences_service.py`
```python
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from uuid import UUID

from .. import models, schemas

def get_user_preferences(db: Session, user_id: UUID) -> models.UserPreference | None:
    """Fetches preferences for a specific user."""
    statement = select(models.UserPreference).where(models.UserPreference.user_id == user_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()

def upsert_user_preferences(db: Session, user_id: UUID, preferences_data: schemas.PreferenceRequest) -> models.UserPreference:
    """Creates or updates preferences for a specific user."""
    
    # Sprawdź, czy preferencje już istnieją
    existing_prefs = get_user_preferences(db, user_id)
    
    if existing_prefs:
        # Aktualizuj istniejące
        existing_prefs.preferences_text = preferences_data.preferences_text
        # SQLAlchemy automatycznie zaktualizuje updated_at dzięki triggerowi
        db.commit()
        db.refresh(existing_prefs)
        return existing_prefs
    else:
        # Utwórz nowe
        new_prefs = models.UserPreference(
            user_id=user_id,
            preferences_text=preferences_data.preferences_text
        )
        db.add(new_prefs)
        db.commit()
        db.refresh(new_prefs)
        return new_prefs

```
