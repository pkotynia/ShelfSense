# Plan Wdrożenia Endpointu „Login” (POST /auth/login)

## 1. Przegląd endpointu

**Metoda:** POST  
**Ścieżka:** `/auth/login`  
**Cel:** Uwierzytelnienie istniejącego użytkownika i wydanie tokenu JWT  
**Odpowiedź sukcesu:** 200 OK  
**Odpowiedź błędu:** 401 Unauthorized (nieprawidłowe dane uwierzytelniające)

---

## 2. Szczegóły żądania

### Nagłówki
- `Content-Type: application/json`

### Ciało żądania (JSON)
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

#### Parametry
- `email` (wymagane): poprawny adres e-mail (weryfikacja przez Pydantic `EmailStr`)
- `password` (wymagane): niepusty ciąg znaków (Pydantic `str`)

---

## 3. Modele danych

### Pydantic
- **LoginRequest** (używany do walidacji żądania)
  - `email: EmailStr`
  - `password: str`

- **AuthResponse** (używany do odpowiedzi)
  - `id: UUID`
  - `email: EmailStr`
  - `token: str`

### SQLAlchemy
- **User** (model odpowiadający tabeli `shelfsense.users`)
  - `id`, `email`, `password_hash`, `created_at`, `updated_at`

---

## 4. Szczegóły odpowiedzi

### Sukces (200 OK)
```json
{
  "id": "uuid-użytkownika",
  "email": "user@example.com",
  "token": "jwt-token"
}
```

### Błędy
- 401 Unauthorized: `{ "error": "Invalid credentials" }`
- 422 Unprocessable Entity: błąd walidacji Pydantic (np. niepoprawny e-mail)
- 500 Internal Server Error: `{ "error": "Internal server error" }`

---

## 5. Przepływ danych

1. **Odbiór żądania**: FastAPI parsuje JSON do `LoginRequest`.  
2. **Walidacja**: Pydantic sprawdza format e-mail i obecność hasła.  
3. **Logika uwierzytelniania** (w serwisie):
   - Pobranie użytkownika po adresie e-mail (ASGI DB session + SQLAlchemy).
   - Jeśli brak użytkownika lub weryfikacja hasła (bcrypt) zakończy się niepowodzeniem → `HTTPException(401)`.
   - Wygenerowanie tokenu JWT (użycie `jwt.encode` z tajnym kluczem i datą wygaśnięcia).
4. **Formatowanie odpowiedzi**: Zwrot obiektu `AuthResponse`.

---

## 6. Zależności FastAPI

- **Dependency Injection**:
  - sesja DB: `Depends(get_db_session)` z `dependencies.py`
  - serwis uwierzytelniania: `Depends(AuthService)` (lub bezpośrednie wywołanie statyczne)

- **Router**: w pliku `app/routers/auth.py`, dodanie ścieżki
  ```python
  @router.post("/login", response_model=AuthResponse)
  async def login(
      request: LoginRequest,
      db: Session = Depends(get_db_session),
  ):
      return await AuthService.authenticate(request, db)
  ```

---

## 7. Względy bezpieczeństwa

- **SQL Injection**: zapytania przez SQLAlchemy ORM.
- **Bezpieczne hashowanie**: porównanie `password_hash` za pomocą `bcrypt.checkpw` (stały czas).
- **JWT**:
  - użycie silnego sekretu (`settings.SECRET_KEY` z env).
  - ustawienie daty wygaśnięcia (np. 1h).
- **Logowanie**: tylko informacja o nieudanym logowaniu (bez szczegółów), brak zapisywania haseł.
- **RLS**: nie dotyczy etapu logowania.

---

## 8. Obsługa błędów

| Scenariusz                      | Kod HTTP | Wyjątek FastAPI                                         |
|---------------------------------|----------|---------------------------------------------------------|
| Walidacja Pydantic              | 422      | automatyczne przez FastAPI/Pydantic                     |
| Brak użytkownika / złe hasło    | 401      | `HTTPException(status_code=401, detail="Invalid credentials")`
| Błąd serwera (np. DB)           | 500      | `HTTPException(status_code=500, detail="Internal server error")` |

---

## 9. Rozważania wydajnościowe

- **Asynchroniczność**: użycie async/await przy I/O (DB).
- **Connection Pooling**: DB session z SQLAlchemy z poolingiem (ustawienia w `engine`).
- **Indeks**: indeks na kolumnie `email` w tabeli `shelfsense.users` przyśpieszy wyszukiwanie.
- **Brute force**: rozważ middleware rate limiting (poza MVP).

---

## 10. Kroki implementacji

1. **Serwis uwierzytelniania** (`app/services/auth_service.py`):
   - `async def authenticate(request: LoginRequest, db: Session) -> AuthResponse`
   - logika: pobranie user, weryfikacja hasła, generacja JWT.
2. **Dekoratory i zależności**:
   - Dodanie `get_db_session` w `app/dependencies.py`.
3. **Router** (`app/routers/auth.py`):
   - Import `LoginRequest`, `AuthResponse`, `AuthService`, `get_db_session`.
   - Dodanie endpointu `/login`.
4. **Konfiguracja**:
   - Uzupełnienie tajnego klucza i ustawień JWT w `app/settings.py` (lub env).
5. **Testy**:
   - Dodanie testów w `app/routers/test_auth.py` dla scenariuszy: poprawne dane, złe hasło, nieistniejący user.
6. **Dokumentacja**:
   - Sprawdzenie generowanej specyfikacji OpenAPI.

---

## 11. Przykładowy kod implementacji (fragment)

```python
# app/services/auth_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from bcrypt import checkpw
from jose import jwt
from datetime import datetime, timedelta
from app.schemas import LoginRequest, AuthResponse
from app.models import User
from app.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    @staticmethod
    async def authenticate(request: LoginRequest, db: Session) -> AuthResponse:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not checkpw(request.password.encode(), user.password_hash.encode()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid credentials")
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": str(user.id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        return AuthResponse(id=user.id, email=user.email, token=token)
```

*Powyższy plan dostarcza szczegółowe wskazówki dla zespołu deweloperskiego, zapewniając spójność z architekturą FastAPI, SQLAlchemy, PostgreSQL oraz polityką bezpieczeństwa i walidacji.*
