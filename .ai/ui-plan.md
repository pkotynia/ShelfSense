# Architektura UI dla ShelfSense

## 1. Przegląd struktury UI
Całość opiera się o React + TypeScript z Material UI i React Router. Aplikacja podzielona jest na moduły widoków:
- Ekran uwierzytelniania
- Ekran główny (biblioteka)
- Ekran szczegółów książki
- Ekran preferencji
- Ekran generowania recenzji AI
- Ekran rekomendacji

Globalny Layout zawiera nagłówek z logotypem i przyciskiem wylogowania, oraz główny slot na aktualny widok. Wszystkie widoki chronione są HOC `withAuth`, poza `/login` i `/register`.

## 2. Lista widoków

### 2.1. Ekran logowania / rejestracji
- Ścieżka: `/login`, `/register`
- Cel: uwierzytelnienie użytkownika
- Wyświetlane informacje: pola `email`, `password`, przycisk submit, link do przełączenia trybu
- Kluczowe komponenty: `TextField`, `Button`
- UX: przycisk disabled gdy pola puste; inline error pod polami
- Bezpieczeństwo: brak chronionych danych, walidacja front-end

### 2.2. Ekran biblioteki użytkownika
- Ścieżka: `/library`
- Cel: przegląd listy przeczytanych książek
- Kluczowe informacje: karta książki (tytuł, autor), stronnicowanie (`page`, `limit`), pole wyszukiwania
- Komponenty: `Card`, `Grid`, `PaginationControls`, `TextField` (search)
- UX: responsywne siatki, filtro-/sortField, `aria-label` na przyciskach nawigacji
- Bezpieczeństwo: pobranie z `/users/me/library`, dołączenie JWT

### 2.3. Ekran szczegółów książki
- Ścieżka: `/books/:id`
- Cel: pokazanie pełnych danych książki + recenzji
- Kluczowe informacje: tytuł, autor, opis, data, page_count; istniejąca recenzja lub przyciski „Dodaj recenzję”/„Generuj AI”
- Komponenty: `Typography`, `Button`, `Card`, `ErrorMessage`
- UX: spinner lub disabled przycisku do ładowania; inline error; aria-label
- Bezpieczeństwo: fetch w `useEffect`, obsługa 404

### 2.4. Ekran preferencji
- Ścieżka: `/preferences`
- Cel: wprowadzenie/edycja tekstu preferencji
- Kluczowe informacje: pole `preferences_text`, przycisk zapisu
- Komponenty: `TextField` multiline, `Button`
- UX: walidacja obecności tekstu, disabled Submit gdy puste, inline error
- Bezpieczeństwo: PUT `/users/me/preferences`, obsługa 400/401

### 2.5. Ekran generowania recenzji AI
- Ścieżka: `/ai/review-template`
- Cel: uzyskanie szablonu recenzji od OpenAI
- Kluczowe informacje: pole notatek opcjonalnych `notes`, przycisk „Generuj”, podgląd wygenerowanego szablonu, przycisk „Zapisz recenzję”
- Komponenty: `TextField`, `Button`, `Card`
- UX: disabled przycisk gdy pola puste, inline error, aria-label
- Bezpieczeństwo: POST `/ai/review-template`, limit requestów

### 2.6. Ekran rekomendacji książek
- Ścieżka: `/recommendations`
- Cel: przegląd i ocenianie rekomendacji
- Kluczowe informacje: lista kart z książkami, pole rating (1.0–5.0, krok 0.5), przycisk odśwież
- Komponenty: `Rating`, `Card`, `Button`, `PaginationControls`
- UX: inline feedback po dodaniu ratingu, disabled jeśli już oceniono, obsługa braku danych (banner CTA do /preferences)
- Bezpieczeństwo: GET `/users/me/recommendations`, POST/PUT/DELETE rating, obsługa 401/409

## 3. Mapa podróży użytkownika
1. Użytkownik otwiera `/login` → loguje się → przekierowanie do `/library`.
2. Na `/library` przegląda listę, może wyszukać lub przejść do `/books/:id`.
3. Na `/books/:id` wybiera „Dodaj recenzję” → manualny formularz lub „Generuj AI” → `/ai/review-template`.
4. Po zapisaniu recenzji powraca do `/library`.
5. Nowa książka w bibliotece powoduje odświeżenie `/recommendations`.
6. Na `/recommendations` ocenia trafność lub w razie braku danych idzie do `/preferences`.
7. Na `/preferences` uzupełnia tekst → powrót do `/recommendations`.

## 4. Układ i struktura nawigacji
- Górny AppBar z logo, przyciskiem wylogowania i tytułem aktualnego widoku.
- Po zalogowaniu dolne menu/tab bar (mobile) lub boczne `Drawer` (desktop) z linkami: Biblioteka, Rekomendacje, Preferencje.
- Każdy route zawinięty w HOC `withAuth` chroniący `/library`, `/books/*`, `/recommendations`, `/preferences`, `/ai/*`.

## 5. Kluczowe komponenty
- Layout (AppBar + Content Slot + Footer/Menu)
- ProtectedRoute HOC (withAuth)
- FormField (TextField + ErrorMessage)
- SubmitButton (zwalidowany + disabled + aria-label)
- CardList + CardItem (książki, rekomendacje)
- PaginationControls (stronicowanie)
- RatingControl (MUI Rating z half-step)
- ErrorMessage (inline `<p className="error">`)
- LoadingSkeleton (MUI Skeleton)
- Navbar/Drawer/Menu (nawigacja główna)
- ReviewEditor (textarea + save)
- AIReviewPreview (podgląd + save)
- SearchBar (wyszukiwanie książek)
