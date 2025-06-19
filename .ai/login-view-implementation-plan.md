# Plan implementacji widoku logowania i rejestracji

## 1. Przegląd
Ekran logowania i rejestracji służy uwierzytelnieniu użytkownika. Pozwala nowym użytkownikom założyć konto (rejestracja) oraz istniejącym użytkownikom zalogować się do aplikacji.

## 2. Routing widoku
- `/login` – ścieżka logowania
- `/register` – ścieżka rejestracji

## 3. Struktura komponentów
```
AuthPage
├── AuthLayout
│   ├── ToggleSwitch
│   └── {LoginForm | RegisterForm}
├── LoginForm
└── RegisterForm
``` 

## 4. Szczegóły komponentów

### AuthLayout
- Opis: kontener ustalający wspólny układ (nagłówek, karta formularza)
- Główne elementy: `<Paper>`, `<Typography>`, `<Box>`
- Obsługiwane zdarzenia: brak (layout statyczny)
- Warunki walidacji: brak
- Typy: żadne
- Propsy:
  - `mode: 'login' | 'register'`
  - `onToggle: () => void`

### ToggleSwitch
- Opis: link lub przycisk do przełączania między trybami logowania i rejestracji
- Główne elementy: `<Link>`
- Obsługiwane zdarzenia: `onClick` wywołuje `onToggle`
- Warunki walidacji: brak
- Typy: żadne
- Propsy:
  - `mode: 'login' | 'register'`
  - `onToggle: () => void`

### LoginForm
- Opis: formularz logowania
- Główne elementy:
  - `<TextField>` email
  - `<TextField type="password">` hasło
  - `<Button>` submit
- Obsługiwane zdarzenia:
  - `onChange` pola email, hasło
  - `onSubmit` formularza
- Warunki walidacji:
  - email: non-empty, poprawny format (`/^[^\s@]+@[^\s@]+\.[^\s@]+$/`)
  - password: non-empty
- Typy:
  - `LoginFormValues { email: string; password: string }`
- Propsy:
  - `onSubmit: (values: LoginFormValues) => void`
  - `isLoading: boolean`
  - `errorMessage?: string`

### RegisterForm
- Opis: formularz rejestracji
- Główne elementy:
  - `<TextField>` email
  - `<TextField type="password">` hasło
  - `<Button>` submit
- Obsługiwane zdarzenia:
  - `onChange` pola email, hasło
  - `onSubmit` formularza
- Warunki walidacji:
  - email: non-empty, poprawny format
  - password: min długość 8, przynajmniej litera i cyfra
- Typy:
  - `RegisterFormValues { email: string; password: string }`
- Propsy:
  - `onSubmit: (values: RegisterFormValues) => void`
  - `isLoading: boolean`
  - `errorMessage?: string`

## 5. Typy
```ts
// DTO żądania
interface RegisterRequest { email: string; password: string }
interface LoginRequest    { email: string; password: string }
// DTO odpowiedzi
interface AuthResponse { id: string; email: string; token: string }
// Typy formularza
interface LoginFormValues    { email: string; password: string }
interface RegisterFormValues { email: string; password: string }
```

## 6. Zarządzanie stanem
- Użycie React Query `useMutation` dla operacji `login` i `register`.
- Custom hook `useAuth`:
  - Metody: `login(values)`, `register(values)`
  - Wewnątrz: wywołania mutacji, zapisywanie tokena w lokalnym magazynie (localStorage)
  - Udostępnia `isLoading`, `error`, `onSuccess` callback (redirect)

## 7. Integracja API
- Endpointy:
  - POST `/auth/register` z payloadem `RegisterRequest` → `AuthResponse` (201)
  - POST `/auth/login` z payloadem `LoginRequest` → `AuthResponse` (200)
- W React Query:
  ```ts
  const registerMutation = useMutation<AuthResponse, ApiError, RegisterRequest>(
    data => api.post('/auth/register', data)
  );
  const loginMutation = useMutation<AuthResponse, ApiError, LoginRequest>(
    data => api.post('/auth/login', data)
  );
  ```
- Po sukcesie zapis tokena i redirect do dashboardu (`useNavigate`).

## 8. Interakcje użytkownika
1. Użytkownik wchodzi na `/login` lub `/register`.
2. Wypełnia pola (`email`, `password`).
3. Formularz waliduje dane w czasie rzeczywistym.
4. Kliknięcie „Zaloguj”/„Zarejestruj” wywołuje API.
5. Pokaż spinner w przycisku.
6. Po sukcesie redirect do `/dashboard`; po błędzie wyświetl komunikat.
7. Klik „Przełącz tryb” zmienia formularz.

## 9. Warunki i walidacja
- Wyłączony submit, gdy pola są niepoprawne lub puste.
- Email – validacja regex.
- Hasło – sprawdzenie długości i złożoności (litera+cyfra) przy rejestracji.
- Wyświetlanie błędów Pydantic: 400 (invalid), 401/409 (auth) z odpowiednim komunikatem.

## 10. Obsługa błędów
- Błędy walidacji front-end pod polami.
- Błędy serwera/API (400, 401, 409) w bannerze nad formularzem.
- Timeout/Network error: ogólne „Spróbuj ponownie później”.

## 11. Kroki implementacji
1. Utworzyć folder `src/features/auth/`.
2. Stworzyć komponenty: `AuthPage.tsx`, `AuthLayout.tsx`, `LoginForm.tsx`, `RegisterForm.tsx`.
3. Napisać typy w `auth.types.ts`.
4. Skonfigurować React Query i hook `useAuth` w `useAuth.ts`.
5. Dodać trasy w routerze (React Router): lazy load `AuthPage`.
6. Dodać obsługę redirect i zapisu tokena w kontekście/authie.
7. Stylizować komponenty za pomocą Material UI zgodnie ze stylem systemowym.
8. Przetestować formularze manualnie i dodać testy jednostkowe dla hooka.
9. Przeprowadzić code review i dopracować UX (focus, accessibility).
10. Zintegrować z resztą aplikacji i wdrożyć.
