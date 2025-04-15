# Dokument wymagań produktu (PRD) - ShelfSense

## 1. Przegląd produktu

ShelfSense to aplikacja mobilna zaprojektowana, aby pomóc użytkownikom zarządzać swoją historią przeczytanych książek oraz otrzymywać spersonalizowane rekomendacje na podstawie ich preferencji czytelniczych. Aplikacja skupia się na dwóch głównych funkcjonalnościach:

1. Tworzenie i zarządzanie osobistą biblioteką książek wraz z recenzjami
2. Generowanie spersonalizowanych rekomendacji książek w oparciu o dane wprowadzone przez użytkownika

ShelfSense wykorzystuje sztuczną inteligencję do pomagania użytkownikom w tworzeniu recenzji książek oraz generowania trafnych rekomendacji, które odpowiadają ich preferencjom czytelniczym.

## 2. Problem użytkownika

Użytkownicy, którzy dużo czytają, napotykają dwa główne problemy:

1. Trudności z przypomnieniem sobie kluczowych aspektów przeczytanych książek po upływie czasu
2. Trudności z odnalezieniem trafnych rekomendacji kolejnych lektur, które odpowiadałyby ich preferencjom

ShelfSense rozwiązuje te problemy, pozwalając użytkownikom:
- Tworzyć i zarządzać historią przeczytanych książek wraz z recenzjami
- Otrzymywać spersonalizowane rekomendacje na podstawie ich historii czytelniczej i preferencji

## 3. Wymagania funkcjonalne

### 3.1 Podstawowe funkcjonalności (MVP)

1. **Historia przeczytanych książek**
   - Możliwość dodawania książek do osobistej biblioteki
   - Możliwość dodawania recenzji do każdej książki (manualnie lub przy użyciu AI)
   - Przeglądanie historii przeczytanych książek

2. **Rekomendacje książek**
   - Generowanie rekomendacji na podstawie preferencji użytkownika
   - Generowanie rekomendacji na podstawie historii przeczytanych książek
   - System oceny trafności rekomendacji (skala 1-5 z dokładnością do 0,5)

3. **Preferencje użytkownika**
   - Rejestracja preferencji użytkownika w formie wolnego tekstu
   - Przechowywanie preferencji w profilu użytkownika

4. **Wsparcie AI**
   - Generowanie szablonów recenzji książek na podstawie informacji wprowadzonych przez użytkownika
   - Analiza preferencji użytkownika na potrzeby rekomendacji

## 4. Granice produktu

### 4.1 Ograniczenia funkcjonalne

1. MVP nie będzie zawierał:
   - Zaawansowanych mechanizmów uczenia maszynowego
   - Integracji głosowej (poza funkcjami systemowymi)
   - Dodatkowych źródeł danych o książkach (np. zewnętrzne bazy danych, recenzje innych użytkowników)
   - Funkcji społecznościowych (dzielenie się recenzjami, polecanie książek znajomym)
   - Automatycznej kategoryzacji książek według gatunków

2. Rekomendacje będą oparte wyłącznie na:
   - Preferencjach wprowadzonych przez użytkownika
   - Historii przeczytanych książek i ich recenzjach

3. Funkcje wprowadzania danych:
   - Do wprowadzania preferencji i danych o książkach będą wykorzystane standardowe funkcje systemowe
   - Nie przewiduje się dedykowanych rozwiązań głosowych w MVP

## 5. Historyjki użytkowników

### Rejestracja i ustawienia

#### US-001: Rejestracja użytkownika
**Tytuł**: Jako nowy użytkownik, chcę założyć konto w aplikacji
**Opis**: Użytkownik powinien mieć możliwość założenia konta w aplikacji, aby korzystać z jej funkcjonalności
**Kryteria akceptacji**:
- Użytkownik może utworzyć konto podając adres email i hasło
- System weryfikuje poprawność wprowadzonych danych
- Użytkownik otrzymuje potwierdzenie utworzenia konta
- Użytkownik może zalogować się do aplikacji po utworzeniu konta

#### US-002: Logowanie użytkownika
**Tytuł**: Jako zarejestrowany użytkownik, chcę zalogować się do aplikacji
**Opis**: Użytkownik powinien mieć możliwość zalogowania się do aplikacji, aby korzystać z jej funkcjonalności
**Kryteria akceptacji**:
- Użytkownik może zalogować się podając adres email i hasło
- System weryfikuje poprawność wprowadzonych danych
- W przypadku niepoprawnych danych, system wyświetla odpowiedni komunikat
- Po poprawnym zalogowaniu, użytkownik ma dostęp do swoich danych

#### US-003: Wprowadzanie preferencji czytelniczych
**Tytuł**: Jako użytkownik, chcę wprowadzić moje preferencje czytelnicze
**Opis**: Użytkownik powinien mieć możliwość wprowadzenia swoich preferencji czytelniczych, które będą wykorzystywane do generowania rekomendacji
**Kryteria akceptacji**:
- Użytkownik może wprowadzić swoje preferencje w formie wolnego tekstu
- System zapisuje wprowadzone preferencje w profilu użytkownika
- Użytkownik może edytować swoje preferencje w dowolnym momencie
- System wykorzystuje wprowadzone preferencje do generowania rekomendacji

### Biblioteka książek

#### US-004: Dodawanie książki do biblioteki
**Tytuł**: Jako użytkownik, chcę dodać książkę do mojej biblioteki
**Opis**: Użytkownik powinien mieć możliwość dodania przeczytanej książki do swojej biblioteki
**Kryteria akceptacji**:
- Użytkownik może dodać nową książkę podając jej tytuł, autora i opcjonalnie inne metadane
- System zapisuje informacje o książce w bibliotece użytkownika
- Dodana książka pojawia się w historii przeczytanych książek użytkownika
- Użytkownik może edytować lub usunąć dodaną książkę

#### US-005: Ręczne dodawanie recenzji
**Tytuł**: Jako użytkownik, chcę ręcznie dodać recenzję do książki
**Opis**: Użytkownik powinien mieć możliwość ręcznego dodania recenzji do książki w swojej bibliotece
**Kryteria akceptacji**:
- Użytkownik może dodać recenzję do wybranej książki
- Recenzja zawiera tekst opisujący opinię użytkownika o książce
- System zapisuje recenzję i powiązuje ją z odpowiednią książką
- Użytkownik może edytować lub usunąć dodaną recenzję

#### US-006: Generowanie recenzji przez AI
**Tytuł**: Jako użytkownik, chcę wygenerować szablon recenzji przy użyciu AI
**Opis**: Użytkownik powinien mieć możliwość wygenerowania szablonu recenzji przy użyciu AI, na podstawie wprowadzonych przez niego informacji o książce
**Kryteria akceptacji**:
- Użytkownik może wybrać opcję generowania recenzji przez AI
- Użytkownik wprowadza podstawowe informacje o książce
- System generuje szablon recenzji na podstawie wprowadzonych informacji
- Użytkownik może edytować wygenerowany szablon recenzji przed zapisaniem
- System zapisuje finalną wersję recenzji i powiązuje ją z odpowiednią książką

#### US-007: Przeglądanie biblioteki
**Tytuł**: Jako użytkownik, chcę przeglądać moją bibliotekę książek
**Opis**: Użytkownik powinien mieć możliwość przeglądania swojej biblioteki książek wraz z recenzjami
**Kryteria akceptacji**:
- Użytkownik może przeglądać listę wszystkich dodanych książek
- Dla każdej książki wyświetlane są podstawowe informacje (tytuł, autor)
- Użytkownik może wybrać książkę, aby zobaczyć jej szczegóły i recenzję
- Użytkownik może sortować i filtrować książki w bibliotece

### Rekomendacje

#### US-008: Otrzymywanie rekomendacji
**Tytuł**: Jako użytkownik, chcę otrzymywać rekomendacje książek
**Opis**: Użytkownik powinien mieć możliwość otrzymywania rekomendacji książek na podstawie swoich preferencji i historii czytelniczej
**Kryteria akceptacji**:
- System generuje rekomendacje na podstawie preferencji użytkownika i jego historii czytelniczej
- Rekomendacje są prezentowane użytkownikowi w czytelnej formie
- Dla każdej rekomendacji wyświetlane są podstawowe informacje o książce
- Użytkownik może odświeżyć listę rekomendacji

#### US-009: Ocenianie trafności rekomendacji
**Tytuł**: Jako użytkownik, chcę ocenić trafność otrzymanej rekomendacji
**Opis**: Użytkownik powinien mieć możliwość oceny trafności otrzymanej rekomendacji, aby pomóc systemowi w generowaniu lepszych rekomendacji w przyszłości
**Kryteria akceptacji**:
- Użytkownik może ocenić trafność rekomendacji w skali od 1 do 5 (z dokładnością do 0,5)
- System zapisuje ocenę i wykorzystuje ją do poprawy przyszłych rekomendacji
- Użytkownik może zmienić swoją ocenę w dowolnym momencie

#### US-010: Brak danych do rekomendacji
**Tytuł**: Jako użytkownik, chcę otrzymać informację o braku wystarczających danych do wygenerowania rekomendacji
**Opis**: System powinien informować użytkownika o braku wystarczających danych do wygenerowania rekomendacji i sugerować uzupełnienie preferencji
**Kryteria akceptacji**:
- System wykrywa brak wystarczających danych do wygenerowania rekomendacji
- System wyświetla użytkownikowi komunikat z informacją o braku danych
- Komunikat zawiera sugestię uzupełnienia preferencji czytelniczych
- Użytkownik może przejść bezpośrednio do edycji swoich preferencji z poziomu komunikatu

#### US-011: Automatyczna aktualizacja rekomendacji
**Tytuł**: Jako użytkownik, chcę aby rekomendacje aktualizowały się po dodaniu nowej książki
**Opis**: System powinien automatycznie aktualizować rekomendacje po dodaniu nowej książki do biblioteki użytkownika
**Kryteria akceptacji**:
- System wykrywa dodanie nowej książki do biblioteki
- System aktualizuje listę rekomendacji uwzględniając nowe dane
- Użytkownik otrzymuje powiadomienie o aktualizacji rekomendacji
- Użytkownik może przeglądać zaktualizowaną listę rekomendacji

## 6. Metryki sukcesu

### 6.1 Metryki użytkownika

1. **Zaangażowanie użytkowników**
   - Częstotliwość korzystania z aplikacji (sesje na tydzień)
   - Czas spędzony w aplikacji
   - Liczba dodanych książek do biblioteki

2. **Satysfakcja użytkowników**
   - Średnia ocena trafności rekomendacji (w skali 1-5)
   - Odsetek użytkowników, którzy oceniają rekomendacje
   - Odsetek użytkowników, którzy dodają do biblioteki książki z rekomendacji

### 6.2 Metryki techniczne

1. **Dokładność rekomendacji**
   - Średnia ocena trafności rekomendacji (w skali 1-5 z dokładnością do 0,5)
   - Odsetek rekomendacji ocenionych powyżej 4
   - Odsetek rekomendacji ocenionych poniżej 2

2. **Skuteczność AI**
   - Odsetek użytkowników korzystających z generowania recenzji przez AI
   - Odsetek wygenerowanych recenzji, które zostały edytowane przez użytkownika
   - Średni czas spędzony na edycji wygenerowanych recenzji

### 6.3 Metryki biznesowe

1. **Wzrost bazy użytkowników**
   - Miesięczny przyrost nowych użytkowników
   - Odsetek użytkowników powracających do aplikacji
   - Odsetek użytkowników, którzy porzucają aplikację po pierwszym użyciu

2. **Użycie funkcjonalności**
   - Odsetek użytkowników korzystających z biblioteki książek
   - Odsetek użytkowników korzystających z rekomendacji
   - Odsetek użytkowników korzystających z generowania recenzji przez AI
