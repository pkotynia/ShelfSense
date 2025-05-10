# Plan wdrożenia endpointu POST /auth/register dla ShelfSense

## 1. Przegląd endpointu

- **Cel:** Rejestracja nowego użytkownika.
- **Metoda:** POST
- **Ścieżka:** `/auth/register`
- **Opis:** Tworzy nowego użytkownika na podstawie emaila i hasła, zwraca token JWT.

## 2. Szczegóły żądania

- **Nagłówki:**  
  - `Content-Type: application/json`
- **Ciało żądania (JSON):**
  - `email` (string, wymagany, poprawny email)
  - `password` (string, wymagany, min. 8 znaków, litery i cyfry)

## 3. Modele danych

### Pydantic

- **RegisterRequest**
  - email: EmailStr
  - password: str (min_length=8, walidator złożoności)

- **AuthResponse**
  - id: UUID
  - email: EmailStr
  - token: str

### SQLAlchemy

- **User** (`shelfsense.users`)
  - id: UUID (PK, default uuid_generate_v4())
  - email: VARCHAR(254), unique, not null
  - username: VARCHAR(255), not null (można ustawić na email lub pusty)
  - password_hash: VARCHAR(60), not null
  - created_at: TIMESTAMPTZ, default now()
  - updated_at: TIMESTAMPTZ, default now()

## 4. Szczegóły odpowiedzi

- **201 Created**  
  - JSON: `{ "id": uuid, "email": string, "token": string }`
- **400 Bad Request**  
  - JSON: `{ "error": "Opis błędu walidacji" }`
- **409 Conflict**  
  - JSON: `{ "error": "Email already exists" }`

## 5. Przepływ danych

1. FastAPI odbiera żądanie POST `/auth/register` z danymi JSON.
2. Walidacja danych przez Pydantic (`RegisterRequest`).
3. Sprawdzenie, czy email już istnieje w bazie (`User`).
4. Jeśli istnieje — zwróć 409 Conflict.
5. Hashowanie hasła (bcrypt).
6. Utworzenie nowego użytkownika w bazie.
7. Wygenerowanie tokena JWT (zawiera id/email).
8. Zwrócenie odpowiedzi (`AuthResponse`) z kodem 201.

## 6. Zależności FastAPI

- Sesja DB (`Depends(get_db)`)
- Generator JWT (np. serwis `auth_service`)
- Hashowanie haseł (bcrypt)
- Model Pydantic do walidacji wejścia/wyjścia

## 7. Względy bezpieczeństwa

- Hashowanie haseł przed zapisem (bcrypt)
- Sprawdzenie unikalności emaila (przed i na poziomie DB)
- Odpowiedzi nie zawierają hashów haseł
- JWT podpisany tajnym kluczem
- Ochrona przed SQL Injection (ORM)
- Ograniczenie liczby prób rejestracji (opcjonalnie: rate limiting)

## 8. Obsługa błędów

- 400: nieprawidłowe dane wejściowe (walidacja Pydantic)
- 409: email już istnieje (sprawdzenie w DB, przechwycenie IntegrityError)
- 500: nieoczekiwany błąd serwera (logowanie, generyczna odpowiedź)

## 9. Rozważania wydajnościowe

- Indeks na emailu (unikalność, szybkie wyszukiwanie)
- Użycie connection poola SQLAlchemy
- Szybkie hashowanie haseł (bcrypt z odpowiednim cost)
- Odpowiedzi asynchroniczne (jeśli I/O bound)

## 10. Kroki implementacji

1. **Modele:**  
   - Upewnij się, że model `User` w SQLAlchemy odpowiada schematowi bazy.
2. **Schematy Pydantic:**  
   - Użyj/rozszerz `RegisterRequest` i `AuthResponse`.
3. **Serwis rejestracji:**  
   - Utwórz funkcję serwisową `register_user(db, email, password)`:
     - Sprawdza, czy email istnieje.
     - Hashuje hasło.
     - Tworzy użytkownika.
     - Zwraca użytkownika.
4. **JWT:**  
   - Utwórz funkcję do generowania tokena JWT (np. `create_access_token(user)`).
5. **Router:**  
   - Dodaj endpoint POST `/auth/register` w nowym routerze `auth.py`.
   - Użyj walidacji Pydantic, obsłuż wyjątki.
6. **Obsługa błędów:**  
   - Zwracaj 400/409/500 z odpowiednimi komunikatami.
7. **Testy:**  
   - Testy jednostkowe i integracyjne: rejestracja, duplikat emaila, walidacja hasła.
8. **Logowanie:**  
   - Loguj błędy serwera i próby rejestracji z duplikatem emaila.

## 11. Przykładowy kod implementacji

```python
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import RegisterRequest, AuthResponse
from app.models import User
from app.dependencies import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    # Sprawdź, czy email już istnieje
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    # Hashuj hasło
    password_hash = auth_service.hash_password(data.password)
    # Utwórz użytkownika
    user = User(email=data.email, username=data.email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Wygeneruj JWT
    token = auth_service.create_access_token(user)
    return AuthResponse(id=user.id, email=user.email, token=token)
```

---

**Plik do zapisania:** `.ai/view-implementation-plan.md`
